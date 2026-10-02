"""Cover / divider / certificate pages in the ultra-realistic western style (AI-generated art plates,
extended to full pages by compose_art.py; all lettering is live text so the brand spelling is exact)."""
from lib import BRAND, esc

PLATES = ["el1", "el2", "el3"]           # desert dusk · vineyard sunrise · Bible, candle and chain

CSS = r"""
@font-face{font-family:'Rye';font-style:normal;font-weight:400;src:url('books-src/fonts/Rye.ttf') format('truetype');}
.artp{page:cover;width:8.5in;height:11in;break-after:page;break-before:page;position:relative;overflow:hidden;background-size:100% 100%;background-repeat:no-repeat;color:#1f3b63}
.artp .tx{position:absolute;left:1.95in;right:.5in;text-align:center}
.artp .kick{font:400 15pt 'Rye';letter-spacing:.14em;color:#a06f1c;text-transform:uppercase}
.artp h1{font:400 50pt/1.06 'Rye';color:#1f3b63;margin:.1in 0 .06in;border:0;padding:0;text-shadow:0 1px 0 rgba(255,255,255,.5)}
.artp h1.sm{font-size:38pt}
.artp .orn{margin:.12in auto;width:4.4in;height:.3in}
.artp .sub{font:italic 600 12.5pt/1.5 'Libre Franklin';color:#2a3b5a;margin:.08in .2in}
.artp .brand{font:400 27pt 'Rye';color:#a06f1c;letter-spacing:.06em}
.artp .tag{font:700 22pt 'Caveat';color:#7a2c4a;margin-top:.04in}
.artp .foot{position:absolute;left:1.95in;right:.5in;bottom:.7in;text-align:center}
.artp .small{font:800 8.5pt 'Libre Franklin';letter-spacing:.3em;text-transform:uppercase;color:#5b6b86;margin-top:.1in}
.artp .mk{font-size:2px;line-height:0;color:rgba(255,255,255,.01)}
.cert2 .tx{left:1.15in;right:1.15in}
.cert2 .frame{position:absolute;left:1.05in;right:1.05in;top:.5in;bottom:.5in;border:3px double #b58a2e}
.cert2 .line{border-bottom:2px solid #8a7a5a;height:.5in;margin:0 .5in}
.cert2 h1{font-size:34pt}
.cert2 .lbl{font:800 8pt 'Libre Franklin';letter-spacing:.14em;text-transform:uppercase;color:#5b6b86;margin-top:.04in}
.cert2 p{margin:.18in .3in 0;font:600 11pt/1.5 'Libre Franklin';color:#2a3b5a}
"""

ORN = """<svg class="orn" viewBox="0 0 440 30" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="#a06f1c" stroke-width="2" stroke-linecap="round">
<path d="M4 15H178"/><path d="M262 15H436"/><path d="M178 15c10-12 22-12 30 0 8-12 20-12 30 0"/><path d="M178 15c10 12 22 12 30 0 8 12 20 12 30 0"/></g><circle cx="220" cy="15" r="4" fill="#a06f1c"/></svg>"""

def _bg(plate):
    return f"background-image:url('books-src/art/{plate}_page.jpg')"

def cover(plate, kicker, title_lines, sub_lines, mk=""):
    t = "<br>".join(esc(x) for x in title_lines)
    s = "<br>".join(esc(x) for x in sub_lines)
    return f"""<section class="artp" style="{_bg(plate)}"><div class="tx" style="top:4.15in">
<div class="kick">{esc(kicker)}</div><h1>{t}{mk}</h1>{ORN}<div class="sub">{s}</div></div>
<div class="foot"><div class="brand">{BRAND}</div><div class="tag">You survived. Now we rebuild.</div></div></section>"""

def divider(plate, kicker, title, sub, bottom, mk=""):
    cls = "sm" if len(title) > 24 else ""
    return f"""<section class="artp" style="{_bg(plate)}"><div class="tx" style="top:4.45in">
<div class="kick">{esc(kicker)}</div><h1 class="{cls}">{esc(title)}{mk}</h1>{ORN}<div class="sub">{esc(sub)}</div></div>
<div class="foot"><div class="brand" style="font-size:20pt">{BRAND}</div><div class="small">{esc(bottom)}</div></div></section>"""

def certificate(title, mk=""):
    return f"""<section class="artp cert2" style="background-image:url('books-src/art/cert_page.jpg')"><div class="frame"></div>
<div class="tx" style="top:.95in"><div class="kick" style="font-size:13pt">{BRAND}</div>
<h1>Certificate<br>of Completion{mk}</h1>{ORN}
<p style="margin-top:.1in">This certifies that</p><div class="line"></div><div class="lbl">Participant’s name</div>
<p>has completed</p><h1 class="sm" style="color:#a06f1c;font-size:26pt;margin:.06in 0">{esc(title)}</h1>
<p>with honesty, courage, and grace for the days that were hard. Brokenness is not the destination. Keep going, one next step at a time.</p>
<div style="display:flex;gap:.6in;margin:.55in .4in 0"><div style="flex:1"><div class="line" style="margin:0"></div><div class="lbl">Signature</div></div>
<div style="flex:1"><div class="line" style="margin:0"></div><div class="lbl">Date</div></div></div></div>
<div class="foot" style="left:1.15in;right:1.15in;bottom:.85in"><div class="tag" style="font-size:26pt">You survived. Now we rebuild.</div><div class="small">{BRAND} &amp; CO.</div></div></section>"""
