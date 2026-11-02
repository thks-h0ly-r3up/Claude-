# -*- coding: utf-8 -*-
import html, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from days import DAYS, ARCS

HERE = os.path.dirname(os.path.abspath(__file__))
E = html.escape

# ---- crop the sticker sheet into 3x3 art pieces -------------------------------------------
st = Image.open(os.path.join(HERE, "img", "stickers.jpg")).convert("RGB")
W, H = st.size
cw, ch = W / 3, H / 3
for r in range(3):
    for c in range(3):
        box = (int(c * cw + 18), int(r * ch + 18), int((c + 1) * cw - 18), int((r + 1) * ch - 18))
        st.crop(box).save(os.path.join(HERE, "img", f"stk_{r}{c}.jpg"), quality=86)

ARC_ART = {1: "stk_00", 2: "stk_01", 3: "stk_12", 4: "stk_20" if False else "stk_21", 5: "stk_22"}
ARC_BY_DAY = {}
for a in ARCS:
    for d in range(a[2], a[3] + 1):
        ARC_BY_DAY[d] = a

FAST = {4, 6, 11, 13, 18, 20, 25, 27}
JAR = {1, 8, 15, 22, 29}
SPECIAL = {10: "Hidar 1", 21: "Hidar 12 · St. Michael", 26: "Thanksgiving (US)", 30: "Hidar 21 · Tsion Mariam"}

CSS = open(os.path.join(HERE, "fonts.css")).read() + """
:root{--turq:#19A7A3;--turqd:#0E7C7A;--gold:#D9A441;--peach:#F6C9A0;--pink:#E6559A;--purple:#8A5BC0;
--denim:#4A74A8;--ivory:#FBF4E4;--ivory2:#F3E7CB;--leather:#5B3A22;--navy:#1D2C57;--ink:#2A2118;}
@page{size:8.5in 11in;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:var(--ivory);-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Lora',serif;color:var(--ink);font-size:10.5pt;line-height:1.38;counter-reset:pg}
.page{width:8.5in;height:11in;position:relative;overflow:hidden;page-break-after:always;padding:.42in .5in .55in;
  background:var(--ivory);counter-increment:pg}
.page:before{content:"";position:absolute;inset:.18in;border:2px dashed #b98b57;border-radius:10px;pointer-events:none;opacity:.8}
.page:after{content:"7HE H0LY R3UP  ·  THE R3NEW  ·  NOVEMBER 2026  ·  " counter(pg);position:absolute;bottom:.26in;left:0;right:0;
  text-align:center;font-family:'Rye',serif;font-size:7pt;letter-spacing:.08em;color:var(--leather)}
.cover:after,.cover:before{display:none}
.brand{font-family:'Rye',serif;letter-spacing:.04em}
.z{position:relative;display:inline-block}.z:after{content:"";position:absolute;left:12%;right:12%;top:50%;height:.09em;background:currentColor;transform:rotate(-62deg)}
.anton{font-family:'Anton',sans-serif;text-transform:uppercase;letter-spacing:.02em}
.play{font-family:'Playfair Display',serif}
.script{font-family:'Kaushan Script',cursive}
.grk{font-family:'Noto Serif','Playfair Display',serif}.heb{font-family:'Noto Sans Hebrew',sans-serif}
.eth{font-family:'Noto Sans Ethiopic',sans-serif}.ara{font-family:'Noto Naskh Arabic',serif}
.dev{font-family:'Noto Sans Devanagari',sans-serif}.jp{font-family:'Noto Sans JP',sans-serif}
.sc{font-family:'Noto Sans SC',sans-serif}.kr{font-family:'Noto Sans KR',sans-serif}
h1.title{font-family:'Anton',sans-serif;font-size:68pt;line-height:.95;text-transform:uppercase;
  background:linear-gradient(90deg,var(--turq),var(--pink) 60%,var(--purple));-webkit-background-clip:text;color:transparent}
h2{font-family:'Anton',sans-serif;font-size:25pt;text-transform:uppercase;color:var(--navy);letter-spacing:.02em;line-height:1}
h3{font-family:'Playfair Display',serif;font-size:12.5pt;color:var(--navy)}
.band{height:10px;border-radius:5px;background:linear-gradient(90deg,var(--turq),var(--peach),var(--pink),var(--purple));margin:6px 0 10px}
.stitch{border:1.6px dashed #b98b57;border-radius:10px;background:#fffaf0}
.tag{display:inline-block;font-family:'Anton',sans-serif;font-size:7.5pt;letter-spacing:.07em;text-transform:uppercase;color:#fff;
  padding:2px 7px;border-radius:3px}
.small{font-size:7.6pt}.mut{color:#6d5a46}
.cover{padding:.5in .5in;background:radial-gradient(circle at 50% 8%,#FFE3BC 0,var(--ivory) 52%)}
.cover .emb{width:6.4in;height:6.4in;object-fit:cover;border-radius:16px;margin:10px auto 0;display:block;border:3px solid var(--leather);
  box-shadow:0 8px 26px rgba(91,58,34,.35)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
ul.tight{margin-left:14px}ul.tight li{margin:2px 0}
/* calendar */
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin-top:8px}
.dow{font-family:'Anton',sans-serif;text-align:center;background:var(--navy);color:#fff;font-size:8.5pt;padding:3px 0;border-radius:3px;letter-spacing:.1em}
.cell{height:1.43in;border:1.4px dashed #b98b57;border-radius:6px;padding:4px 5px;background:#fffaf0;position:relative;overflow:hidden}
.cell.blank{background:transparent;border:none}
.cell .dn{font-family:'Anton',sans-serif;font-size:17pt;line-height:1;color:var(--navy)}
.cell .lg{font-family:'Playfair Display',serif;font-weight:700;font-size:8.4pt;line-height:1.1;margin-top:2px}
.cell .nt{white-space:nowrap;font-size:12.5pt;line-height:1.15;margin-top:2px;color:var(--leather)}
.cell .mk{position:absolute;left:4px;bottom:3px;right:4px;font-size:6.5pt;line-height:1.15;color:#6d5a46}
.cell .bar{position:absolute;left:0;top:0;bottom:0;width:5px}
/* day cards */
.arcbar{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.arcbar img{width:.55in;height:.55in;object-fit:cover;border-radius:8px;border:1.5px solid var(--leather)}
.arcname{font-family:'Anton',sans-serif;font-size:15pt;text-transform:uppercase;letter-spacing:.04em}
.card{height:4.6in;margin-bottom:.12in;border:1.8px dashed #b98b57;border-radius:12px;background:#fffaf0;overflow:hidden;position:relative}
.card .hd{display:flex;align-items:center;gap:10px;padding:6px 12px;color:#fff;font-family:'Anton',sans-serif;letter-spacing:.06em;text-transform:uppercase;font-size:11pt}
.card .hd .r{margin-left:auto;font-size:8.6pt}
.card .body{display:grid;grid-template-columns:2.3in 1fr;gap:12px;padding:9px 12px 0}
.word{border-radius:10px;padding:10px 9px 9px;text-align:center;background:var(--ivory2);border:1.4px solid #d8bd8f}
.word .nat{line-height:1.2;color:var(--navy);font-weight:700;word-break:keep-all;overflow-wrap:anywhere}
.word .lng{font-family:'Rye',serif;font-size:12.5pt;color:var(--leather);margin-bottom:2px}
.word .tr{font-family:'Playfair Display',serif;font-style:italic;font-size:11.5pt;color:var(--purple);margin-top:2px}
.word .pr{font-size:8.6pt;color:#6d5a46}
.word .mn{font-size:9.6pt;margin-top:7px;line-height:1.32}
.lbl{font-family:'Anton',sans-serif;font-size:8.4pt;letter-spacing:.09em;text-transform:uppercase;color:var(--turqd);margin-bottom:1px}
.txt p{margin-bottom:5px;font-size:9.6pt;line-height:1.38}
.hook{font-family:'Kaushan Script',cursive;font-size:13.5pt;line-height:1.2;color:var(--pink);margin:2px 0 6px}
.trio{display:grid;grid-template-columns:1fr 1fr;gap:7px;padding:7px 12px 0}
.box{border:1.2px dashed #c9a56d;border-radius:8px;padding:4px 8px;background:#fff;font-size:9.2pt;line-height:1.32}
.verify{margin:5px 12px 0;font-size:7.2pt;color:#7a6650;text-align:center;border-top:1px dotted #cdb48a;padding-top:2px}
.tr2{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.brick{display:inline-block;width:.62in;height:.34in;border:1.4px solid var(--leather);margin:2px;border-radius:3px;text-align:center;
  font-family:'Anton',sans-serif;font-size:10pt;line-height:.3in;color:var(--navy);background:linear-gradient(180deg,#f9e6cf,#e9c9a0)}
"""

def nsize(t, big=28, mid=20, small=15, tiny=12):
    n = len(t)
    return big if n <= 8 else mid if n <= 11 else small if n <= 14 else tiny

def card(d):
    a = ARC_BY_DAY[d["n"]]
    col = a[4]
    mark = []
    if d["n"] in FAST: mark.append("Wed/Fri fast day*")
    if d["n"] in JAR: mark.append("Jar Reveal")
    if d["n"] in SPECIAL: mark.append(SPECIAL[d["n"]])
    mk = " · ".join(mark)
    nat_cls = d["cls"]
    lang_attr = {"jp": "ja", "sc": "zh", "kr": "ko"}.get(nat_cls, "")
    la = f' lang="{lang_attr}"' if lang_attr else ""
    nat_dir = ' dir="rtl"' if nat_cls == "ara" else ""
    return f"""
<div class="card">
 <div class="hd" style="background:linear-gradient(90deg,{col},{col}cc)"><span>DAY {d['n']:02d}</span><span>{d['dow']} · NOV {d['n']}</span><span class="r">{E(mk)}</span></div>
 <div class="body">
  <div class="word">
   <div class="lng">{E(d['lang'])}</div>
   <div class="nat {nat_cls}"{la}{nat_dir} style="font-size:{nsize(d['native'])}pt">{E(d['native'])}</div>
   <div class="tr">{E(d['translit'])}</div>
   <div class="pr">{E(d['pron'])}</div>
   <div class="mn"><b>Means:</b> {E(d['meaning'])}</div>
  </div>
  <div class="txt">
   <div class="hook">“{E(d['hook'])}”</div>
   <div class="lbl">What it means</div><p>{E(d['explain'])}</p>
   <div class="lbl">Fun fact</div><p>{E(d['fact'])}</p>
   <div class="lbl">Word of God</div><p><b>{E(d['ref'])}</b></p>
  </div>
 </div>
 <div class="trio">
  <div class="box"><div class="lbl">Mini recap · builds on yesterday</div>{E(d['builds'])}</div>
  <div class="box"><div class="lbl">R3NEW interactive post</div>{E(d['interact'])}</div>
 </div>
 <div class="trio" style="grid-template-columns:1fr">
  <div class="box"><div class="lbl">10-minute step (low-energy option included)</div>{E(d['step'])}</div>
 </div>
 <div class="verify">Don't take my word for it: search the word + “etymology,” compare two sources, ask a native speaker.</div>
</div>"""

def day_pages():
    out = []
    for i in range(0, 30, 2):
        pair = DAYS[i:i + 2]
        a = ARC_BY_DAY[pair[0]["n"]]
        a2 = ARC_BY_DAY[pair[-1]["n"]]
        arcs_here = [a] if a == a2 else [a, a2]
        bar = ""
        for ar in arcs_here:
            bar += f"""<div style="display:flex;align-items:center;gap:8px"><img src="img/{ARC_ART[ar[0]]}.jpg" style="width:.5in;height:.5in;object-fit:cover;border-radius:8px;border:1.5px solid #5B3A22">
            <div><div class="arcname" style="color:{ar[4]}">Arc {ar[0]} · {E(ar[1])} <span class="mut small" style="font-family:Lora">Nov {ar[2]}–{ar[3]}</span></div><div class="small mut">{E(ar[5])}</div></div></div>"""
        out.append(f'<section class="page"><div class="arcbar" style="gap:24px">{bar}</div>' + "".join(card(d) for d in pair) + "</section>")
    return "\n".join(out)

def calendar():
    cells = []
    for _ in range(0):  # Nov 1, 2026 is a Sunday: no leading blanks
        cells.append('<div class="cell blank"></div>')
    for d in DAYS:
        a = ARC_BY_DAY[d["n"]]
        mark = []
        if d["n"] in FAST: mark.append("◆ fast day*")
        if d["n"] in JAR: mark.append("🫙 Jar Reveal")
        if d["n"] in SPECIAL: mark.append(SPECIAL[d["n"]])
        lang_attr = {"jp": "ja", "sc": "zh", "kr": "ko"}.get(d["cls"], "")
        la = f' lang="{lang_attr}"' if lang_attr else ""
        nat = "" if d["n"] == 30 else f'<div class="nt {d["cls"]}"{la} style="font-size:{nsize(d["native"],13,10.5,8.5,7.5)}pt">{E(d["native"])}</div>'
        cells.append(f"""<div class="cell"><div class="bar" style="background:{a[4]}"></div><div style="padding-left:4px"><div class="dn">{d['n']}</div>
        <div class="lg" style="color:{a[4]}">{E(d['lang'])}</div>{nat}</div><div class="mk" style="padding-left:4px">{E('<br>'.join(mark)) if False else '<br>'.join(E(m) for m in mark)}</div></div>""")
    heads = "".join(f'<div class="dow">{x}</div>' for x in ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"])
    return f'<div class="cal">{heads}{"".join(cells)}</div>'

def arcs_page():
    rows = ""
    for a in ARCS:
        langs = ", ".join(d["lang"] for d in DAYS if a[2] <= d["n"] <= a[3])
        rows += f"""<div class="stitch" style="padding:7px 10px;margin-bottom:7px;display:flex;gap:10px;align-items:center">
        <img src="img/{ARC_ART[a[0]]}.jpg" style="width:.85in;height:.85in;object-fit:cover;border-radius:10px;border:1.5px solid #5B3A22">
        <div><div class="arcname" style="color:{a[4]}">Arc {a[0]} · {E(a[1])} · Nov {a[2]}–{a[3]}</div>
        <div style="font-size:9.8pt"><i>{E(a[5])}</i></div><div class="small mut" style="font-size:8.6pt"><b>Languages:</b> {E(langs)}</div></div></div>"""
    return rows

PAGES = []

# 1 COVER
PAGES.append(f"""<section class="page cover" style="text-align:center">
<div class="brand" style="font-size:15pt;color:var(--leather)">7HE H0LY R3UP</div>
<div class="small mut" style="letter-spacing:.2em">YOU SURVIVED. NOW WE REBUILD.</div>
<h1 class="title" style="margin-top:6px">THE R3NEW</h1>
<div class="play" style="font-size:15pt;color:var(--navy);margin-top:2px;font-style:italic">30 days · 30 languages · one word: <b>again</b></div>
<img class="emb" src="img/emblem.jpg">
<div class="band" style="margin:14px 0 8px"></div>
<div class="anton" style="font-size:16pt;color:var(--turqd)">November 2026 Content Calendar + Outline</div>
<div class="small mut" style="margin-top:4px">A daily interactive series for the family: Morning drop + R3NEW post, each day building on the last, every day able to stand alone.</div>
<div class="script" style="font-size:13pt;color:var(--pink);margin-top:10px">Big Boy approved. God Almighty gets the glory.</div>
</section>""")

# 2 WELCOME
PAGES.append(f"""<section class="page">
<h2>Welcome to the R3NEW</h2><div class="band"></div>
<div style="display:grid;grid-template-columns:2.4in 1fr;gap:16px">
<img src="img/heart.jpg" style="width:2.4in;border-radius:12px;border:2px solid #5B3A22">
<div>
<p class="script" style="font-size:19pt;color:var(--pink);line-height:1.2;margin-bottom:8px">“Renew ain't 'new.' Renew is 'again,' on purpose, scars and all.”</p>
<p>November is the R3NEW. Every day for 30 days, one language gives us its word for <b>renew</b>, a different meaning, a different definition, and a fun fact you didn't see coming. Then we drop one real, low-energy step you can do in 10 minutes or less.</p>
<p style="margin-top:6px">I'm not here to be above anybody. I'm beside you. Same rebuild, different rooms. The family does this together, in the comments, one brick at a time.</p>
</div></div>
<h3 style="margin-top:16px;font-size:15pt">What makes this different</h3>
<ul class="tight" style="margin-top:4px">
<li><b>Each day builds on the one before.</b> Every post starts with a mini recap (“Yesterday: ___. Today builds: ___.”) so new people can hop in and old people feel the climb.</li>
<li><b>Every day also stands alone.</b> Each post carries a one-line “Start here” catch-up. Nobody's ever behind. You are being positioned, not behind.</li>
<li><b>Two posts a day, two jobs.</b> The <i>Daily R3UP · Morning</i> drop teaches the word. The separate <i>R3NEW</i> post is the interactive one: comment, vote, say it back, tag your crew.</li>
<li><b>The Jar.</b> Every day the family drops a Jar word. Every Sunday is a Jar Reveal: I read yours out loud, raw, with thanks.</li>
<li><b>The Wall.</b> Each day adds one brick to the R3NEW Wall graphic. By Nov 30 the wall is built, with 30 words in 30 tongues.</li>
<li><b>Thanksgiving voice.</b> Gratitude for mercy already completed, not “almost there.” Gratitude and grief can sit at the same table.</li>
</ul>
<div class="stitch" style="padding:10px 14px;margin-top:14px;font-size:9.4pt">
<b>Honest disclaimer.</b> This series is faith-based education, personal testimony and encouragement. It is not medical, mental-health or legal advice and it doesn't diagnose or treat anything. Struggling isn't weak faith. If you're in crisis or thinking about hurting yourself, call or text 988 (US) or your local emergency number. Scripture references are listed by book, chapter and verse; before posting, quote from your Ethiopian Orthodox Tewahedo edition and name the edition and translator on the graphic. Psalm numbers follow the Ge'ez/Septuagint tradition and can run one number behind Hebrew-numbered Bibles. Language pronunciations are friendly approximations. Ask a native speaker, a deacon or a priest to confirm. Copyright © 2026 7HE H0LY R3UP. All rights reserved.
</div>
</section>""")

# 3 HOW A DAY WORKS
PAGES.append(f"""<section class="page">
<h2>How Each Day Works</h2><div class="band"></div>
<div style="display:grid;grid-template-columns:2.9in 1fr;gap:16px">
<div><img src="img/goodmorning.jpg" style="width:2.9in;border-radius:10px;border:2px solid #5B3A22"><div class="small mut" style="text-align:center;margin-top:3px">Morning graphic: swap in the day's word + date</div></div>
<div>
<h3>1 · Daily R3UP · Morning (teach)</h3>
<ul class="tight" style="font-size:9.6pt">
<li><b>Mini recap (2 lines):</b> “Yesterday: ___ (language) meant ___. Today builds: ___.”</li>
<li><b>Start-here line:</b> “Joining late? Renew = making new again. That's all you need.”</li>
<li><b>Hook</b> in my voice (real struggle, short punchy sentences).</li>
<li><b>The word:</b> script, sound, meaning, explanation, fun fact.</li>
<li><b>Word of God:</b> exact book, chapter and verse. Church teaching, Scripture, history, testimony and metaphor kept separate.</li>
<li><b>Verify it:</b> search the word, compare two sources, ask a native speaker or clergy.</li>
</ul>
<h3 style="margin-top:8px">2 · R3NEW post (interact)</h3>
<ul class="tight" style="font-size:9.6pt">
<li>One simple action: comment a word, vote, fill in a blank, say it back, tag a crew member.</li>
<li>A 10-minute step, plus a low-energy option and a no-cost, private option.</li>
<li>Reply to as many comments as possible in the first hour. Pin the best Jar word.</li>
</ul></div></div>
<h3 style="margin-top:12px">The caption blueprint (every post)</h3>
<div class="stitch" style="padding:9px 13px;font-size:9.6pt;line-height:1.5">
<b>1.</b> Hook (specific, real) → <b>2.</b> Mini recap + start-here line → <b>3.</b> Teaching + evidence-backed context → <b>4.</b> Interactive ask → <b>5.</b> 10-minute step (and low-energy option) → <b>6.</b> Verification invite: <i>“Check both sides, including mine. Read the sources. Truth can withstand honest questions.”</i> → <b>7.</b> Invitation → <b>8.</b> Signature closing.
</div>
<div class="grid2" style="margin-top:10px">
<div class="stitch" style="padding:9px 13px;font-size:9.4pt"><b>Standard Bio</b><br>“I'm Nikki, founder of 7HE H0LY R3UP, a survivor rebuilding through faith, with Big Boy, my American Bully service dog, beside me. I share lived experience, carefully sourced teaching, and practical steps for the next stretch of rebuilding.”</div>
<div class="stitch" style="padding:9px 13px;font-size:9.4pt"><b>Standard Invitation</b><br>“If this meets you where you are, reach out through this page. Share only what feels safe. What step are you working on?”<br><br><b>Signature Closing</b><br>“We survived. Now let's go back, with truth and a hand out. Souls are attached to my obedience. God Almighty gets the glory.”</div>
</div>
<h3 style="margin-top:10px">Grounding invitation (optional, top of Morning post)</h3>
<p style="font-size:9.6pt">“If it's okay for you: feet on the floor, one slow breath in, one out. Eyes open or closed, your call. Skip this if it doesn't feel good today. You're still welcome here.”</p>
<h3 style="margin-top:8px">Hashtag set</h3><p class="small">#7HEH0LYR3UP · #THER3NEW · #YouSurvivedNowWeRebuild · #BigBoy</p>
</section>""")

# 4 CALENDAR
PAGES.append(f"""<section class="page">
<div style="display:flex;align-items:flex-end;justify-content:space-between"><h2>November 2026 · 30 Languages</h2><div class="brand" style="color:var(--leather);font-size:10pt">THE R3NEW</div></div>
<div class="band"></div>
{calendar()}
<div class="small mut" style="margin-top:9px;line-height:1.45;font-size:8.6pt">
<b>Color bar = arc.</b> <span style="color:#19A7A3">■ Roots</span> · <span style="color:#E6559A">■ Rise</span> · <span style="color:#D9A441">■ Repair</span> · <span style="color:#8A5BC0">■ Return + Thanks</span> · <span style="color:#4A74A8">■ Every Tongue</span>.
<b>🫙 Jar Reveal</b> = Sunday read-aloud of the week's Jar words.
<b>* ◆ Wed/Fri</b> are traditional fast days in the Ethiopian Orthodox Tewahedo Church. Food fasting isn't for everyone (health, history with food, pregnancy). Ask your priest. Low-energy option: fast from scrolling for one hour.
Ethiopian-calendar notes (Hidar 1 = Nov 10, Hidar 12 = Nov 21, Hidar 21 = Nov 30) follow the standard conversion for 2026. Confirm feast days with your church calendar.
</div>
</section>""")

# 5 ARC ROADMAP
PAGES.append(f"""<section class="page">
<h2>The Roadmap: What's To Come</h2><div class="band"></div>
<img src="img/corkboard.jpg" style="width:100%;height:2.7in;object-fit:cover;border-radius:12px;border:2px solid #5B3A22">
<div class="small mut" style="text-align:center;margin:3px 0 8px">The Wall starts as a corkboard. By Nov 30 it's a wall of 30 bricks.</div>
{arcs_page()}
<div class="stitch" style="padding:9px 13px;margin-top:6px;font-size:9.4pt"><b>Weekly rhythm.</b> Sundays: Jar Reveal + arc recap. Mon–Sat: one word, one fact, one step. Wed + Fri: lighter posts (fast days; fewer words, more prayer). Day 20 plants a sprout jar. Day 25 is the check-in. Day 26 is Thanksgiving. Day 29 opens the Q+A. Day 30 reveals the whole Wall.</div>
</section>""")

# 6.. DAY CARDS
PAGES.append(day_pages())

# INTERACTION MENU
PAGES.append(f"""<section class="page">
<h2>The Interaction Playbook</h2><div class="band"></div>
<p style="font-size:10.5pt">Followers become family when they get to <i>do</i> something. Rotate these. Keep each ask small enough for a tired nervous system.</p>
<div class="grid2" style="margin-top:8px">
<div class="stitch" style="padding:10px 13px;font-size:10pt"><h3>🫙 Drop your Jar word</h3>One word in the comments. Read out every Sunday. Builds a Jar graphic that grows all month.</div>
<div class="stitch" style="padding:10px 13px;font-size:10pt"><h3>🗳 This or That</h3>Story poll. Two clear choices. Reply to every “why.”</div>
<div class="stitch" style="padding:10px 13px;font-size:10pt"><h3>🎙 Say it back</h3>10-second voice or video of the day's word. Duet or stitch. Feature the family.</div>
<div class="stitch" style="padding:10px 13px;font-size:10pt"><h3>✍ Fill in the blank</h3>“God is growing a new ___ in me.” Easy, low-stakes, honest.</div>
<div class="stitch" style="padding:10px 13px;font-size:10pt"><h3>👥 Tag your crew</h3>Thank one person. Everyone tagged gets a reply. Builds community.</div>
<div class="stitch" style="padding:10px 13px;font-size:10pt"><h3>🌱 Sprout check-in</h3>Day 20 plant, Day 25 compare. A real thing growing across days, a living recap.</div>
<div class="stitch" style="padding:10px 13px;font-size:10pt"><h3>❓ Raw Q+A</h3>Day 29 opens it. Day 30 answers. Faith or rebuild questions. Honest “I don't know” counts as an answer.</div>
<div class="stitch" style="padding:10px 13px;font-size:10pt"><h3>🧱 Wall vote</h3>Day 30: vote your favorite word. The Wall graphic gets everybody's pick.</div>
</div>
<h3 style="margin-top:12px">Targeted critique + both sides (use when it fits)</h3>
<div class="stitch" style="padding:10px 14px;font-size:9.8pt;line-height:1.5">
Name a <b>specific quote or pattern</b>, never a whole group or denomination. Show: <b>what was claimed</b> → <b>what the source says in context</b> → <b>the other view</b> → <b>the practical difference</b> → <b>your action step</b>. Example for Day 4 (chalaf): some English verses read “renew” where Hebrew says “exchange.” Check a Hebrew interlinear and ask your priest which sense the Church teaches.
</div>
<h3 style="margin-top:12px">Boundaries for the whole series</h3>
<ul class="tight" style="font-size:9.8pt">
<li>No tarot or divination, no syncretic spirituality, no generational-curse mechanics for medical or trauma conditions.</li>
<li>Distinguish spiritual language from behavioral recovery. Faith walks beside therapy and medical care. It doesn't replace them.</li>
<li>Other languages and cultures are honored for their words. We borrow no one's religion and make no claims about their beliefs.</li>
<li>Never promise outcomes. Never use fake urgency or FOMO. “You are not behind” means it.</li>
<li>Big Boy is presented respectfully: he's my service dog and my companion. No invented tasks, no spiritual authority.</li>
</ul>
<h3 style="margin-top:12px">How to measure it (keep it simple)</h3>
<p style="font-size:9.8pt">Weekly: comments per post · saves · shares · new followers · replies sent. Keep the top 3 interaction types and drop the lowest. Ask the family what they want more of.</p>
</section>""")

# TRACKER WALL
bricks = "".join(f'<span class="brick">{i}</span>' for i in range(1, 31))
PAGES.append(f"""<section class="page" style="text-align:center">
<h2>My R3NEW Wall</h2><div class="band"></div>
<p style="font-size:9pt">Color in one brick a day. Missed a day? Skip it and keep going. You are not behind.</p>
<div style="margin:12px auto;width:7in;padding:10px;border:2px dashed #b98b57;border-radius:12px;background:#fffaf0">{bricks}</div>
<div class="grid2" style="text-align:left;margin-top:12px">
<div class="stitch" style="padding:9px 12px;font-size:8.6pt"><h3>My Jar words</h3><br>_______________________<br><br>_______________________<br><br>_______________________<br><br>_______________________</div>
<div class="stitch" style="padding:9px 12px;font-size:8.6pt"><h3>Words I'm carrying into December</h3><br>_______________________<br><br>_______________________<br><br>_______________________<br><br>_______________________</div>
</div>
<div class="stitch" style="margin:14px auto 0;width:6.6in;padding:16px 20px;border-width:3px">
<div class="brand" style="font-size:12pt;color:var(--leather)">7HE H0LY R3UP</div>
<div class="anton" style="font-size:24pt;color:var(--navy);margin-top:2px">Certificate of Completion</div>
<div class="play" style="font-style:italic;margin-top:4px">This certifies that</div>
<div style="border-bottom:1.5px solid var(--leather);width:4in;margin:10px auto 2px;height:22px"></div>
<div class="play" style="font-style:italic">rebuilt, renewed and showed up for the R3NEW, November 2026: 30 days, 30 languages.</div>
<div class="script" style="font-size:13pt;color:var(--pink);margin-top:8px">You survived. Now we rebuild.</div>
<div class="small" style="margin-top:6px">We survived. Now let's go back, with truth and a hand out. Souls are attached to my obedience. God Almighty gets the glory.</div>
</div>
</section>""")

import re
def zslash(h):
    # slash the zero in H0LY only inside .brand elements
    return re.sub(r'(<[^>]*class="brand"[^>]*>)([^<]*)',lambda m:m.group(1)+m.group(2).replace("H0LY",'H<span class="z">0</span>LY'),h)

HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>THE R3NEW · November 2026 · 7HE H0LY R3UP</title>
<style>{CSS}</style></head><body>{''.join(PAGES)}</body></html>"""
HTML = zslash(HTML)
open(os.path.join(HERE, "r3new-november-2026.html"), "w", encoding="utf-8").write(HTML)
print("html written", len(HTML))
