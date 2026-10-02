#!/usr/bin/env python3
"""Binder covers (card stock), spine strips, and a print/binding guide for The 90-Day Rebuild."""
import os
import lib
import art_pages as A
from lib import BRAND, esc

PDF = os.path.join(lib.OUT, "the-90-day-rebuild.pdf")
f, N = lib.find_marker_pages(PDF, ["101", "104", "105", "54", "70"])
# Volume breaks (all start on a front-of-sheet = odd page):
#   Vol 1: front matter + Arcs 1-4 (ends with day 45); Vol 2: Arc 4 review + Arcs 5-9 + extras; Vol 3: Reference Library
v1_end = int(f["105"]) - 2                    # last page of arc 4 days (arc 5 divider is f["105"], review is f["105"]-1)
v2_start, v2_end = v1_end + 1, int(f["70"]) - 1
v3_start, v3_end = int(f["70"]), N
for a in (v2_start, v3_start):
    assert a % 2 == 1, a
VOL = [
 ("Volume One", "Days 1–45", ["Telling the Truth", "The Lies and the Names", "The Realm and Your Authority", "The Contracts"], 1, v1_end, "v1"),
 ("Volume Two", "Days 46–90 · Begin Again · The Jar · Day 90", ["The Bloodline", "The Playbook and the Structure", "God", "Brandi and Letting Go", "Becoming Her"], v2_start, v2_end, "v2"),
 ("Volume Three", "The Reference Library", ["Trauma and the Spiritual Realm Workbook", "The Whole Story, Volume II"], v3_start, v3_end, "v3"),
]

CSS = r"""
.cwrap{page:cover;width:8.5in;height:11in;break-after:page;position:relative;background:#fff;overflow:hidden}
.cwrap .cover{position:absolute;left:.3in;top:.3in;width:8.5in;height:11in;transform:scale(.929);transform-origin:top left;border-radius:22px;break-after:auto;page:auto;overflow:hidden}
.cwrap .cover .vol{position:absolute;left:0;right:0;top:5.0in;text-align:center;font:800 13pt 'Libre Franklin';letter-spacing:.38em;text-transform:uppercase;color:#fff3d6}
.cwrap .cover .lower .by{font:600 11pt/1.55 'Libre Franklin'}
.v2 .leather{background-image:radial-gradient(rgba(255,255,255,.10) 1px,transparent 1.4px),radial-gradient(rgba(0,0,0,.10) 1px,transparent 1.6px),linear-gradient(160deg,#9a63c0 0%,#7a4c9e 55%,#5d3a7e 100%) !important}
.v3 .leather{background-image:radial-gradient(rgba(255,255,255,.10) 1px,transparent 1.4px),radial-gradient(rgba(0,0,0,.10) 1px,transparent 1.6px),linear-gradient(160deg,#5f7ea8 0%,#4a6486 55%,#3a5273 100%) !important}
.v3 .cover{background:linear-gradient(180deg,#2a8f8a 0%,#d6598f 45%,#f4c9a5 70%,#e3a94b 100%)}
.spines{page:cover;width:8.5in;height:11in;break-after:page;padding:.5in .7in}
.spines h1{font:700 30pt 'Caveat';color:#7a4c9e;margin:0}
.strips{display:flex;gap:.35in;margin-top:.15in}
.strip{width:1.5in;height:8.6in;border:1.2px dashed #8f82a3;position:relative;overflow:hidden}
.strip .in{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.strip .t{writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap;text-align:center;color:#fff;font:700 24pt 'Caveat'}
.strip .t small{display:block;font:800 8.5pt 'Libre Franklin';letter-spacing:.25em;text-transform:uppercase;margin-top:6px}
.guide{page:cover;width:8.5in;height:11in;padding:.6in .75in}
.guide h1{font:700 34pt 'Caveat';color:#7a4c9e;margin:0 0 .05in}
.guide td,.guide th{font-size:9.5pt}
.mk{font-size:2px;line-height:0;color:rgba(255,255,255,.01)}
"""

def cover_page(vol, rng, arcs, a, b, cls):
    plate = {"v1": "el1", "v2": "el2", "v3": "el3"}[cls]
    if cls == "v3":
        return A.cover(plate, vol, ["The Reference", "Library"], arcs)
    sub = [rng] + [" · ".join(arcs[i:i + 2]) for i in range(0, len(arcs), 2)]
    return A.cover(plate, vol, ["The 90-Day", "Rebuild"], sub, photo="bigboy" if cls == "v1" else None)

def spines():
    colors = {"v1": "#27857f", "v2": "#7a4c9e", "v3": "#4a6486"}
    strips = ""
    for vol, rng, arcs, a, b, cls in VOL:
        strips += f'<div class="strip" style="background:{colors[cls]}"><div class="in"><div class="t">The 90-Day Rebuild<small>{esc(vol)} · {esc(rng.split(" · ")[0])} · {BRAND}</small></div></div></div>'
    return f"""<div class="spines"><h1>Spine Strips</h1><p class="small">Print on card stock or paper, cut along the dashed lines, and slide into the spine pocket of each binder. Trim width to your spine (1.5 in strips shown).</p><div class="strips">{strips}</div></div>"""

def guide():
    rows = "".join(f"<tr><td><strong>{esc(v)}</strong></td><td>{esc(r)}</td><td>pages {a}–{b}</td><td>{(b - a + 1) // 2} sheets</td></tr>" for v, r, _, a, b, _ in VOL)
    return f"""<div class="guide"><div class="band"></div><div class="kick">Print and bind</div><h1>Printing and Binding Guide</h1>
<p>Open <strong>the-90-day-rebuild.pdf</strong> and print each volume as a page range. All three start on a front-of-sheet page, so every day lands on two sheets.</p>
<table><thead><tr><th>Binder</th><th>Contents</th><th>Print range</th><th>Sheets</th></tr></thead><tbody>{rows}</tbody></table>
<h3>Driver settings</h3><ul style="line-height:1.55"><li>Paper: Letter, 24 lb pre-punched 3-hole · Two-sided, binding edge <strong>long edge (left)</strong></li><li>Scale: 100% / Actual size · Color on · Standard quality</li><li>Volume Two begins with the review page for Arc 4 (The Contracts), so you look back before you move on.</li></ul>
<h3>Covers</h3><ul style="line-height:1.55"><li>Print the three cover pages (pages 1–3 of this file) on <strong>65–80 lb matte white card stock</strong>, one side only, through the rear or bypass tray, with paper type set to heavy / cardstock.</li><li>Slide each into the clear front pocket of its binder. A thin white border around the color is normal on office inkjets.</li></ul>
<h3>Protect the holes</h3><ul style="line-height:1.55"><li>Put a <strong>self-adhesive hole reinforcement ring</strong> on each punched hole of the pages you will turn most: the arc dividers, the certificate, the Challenge Jar cards, and the first and last page of every arc. A sheet of 500 costs a few dollars.</li><li>Print the dividers and certificate on <strong>65 lb card stock</strong> instead of 24 lb, and punch them with a heavy-duty 3-hole punch.</li><li>Do not overfill: keep each binder under about 80 percent of its ring capacity, and turn pages by the outer edge, not the punched edge.</li><li>For pages you write on heavily, a clear heavy-duty sheet protector with a reinforced edge works too.</li></ul>
<h3>Binders</h3><ul style="line-height:1.55"><li>Three <strong>1.5 inch</strong> zip binders with a clear front and spine pocket (about 100 sheets per volume, with room for tabs, notes, and the Challenge Jar).</li><li>Tab at each arc divider (the colored pages) in Volumes One and Two, and at each Part and Book in Volume Three.</li></ul></div>"""

def build():
    body = "".join(cover_page(v, r, arcs, a, b, c) for v, r, arcs, a, b, c in VOL) + spines() + guide()
    html_path = os.path.join(lib.OUT, "binder-covers.html")
    pdf_path = os.path.join(lib.OUT, "binder-covers.pdf")
    open(html_path, "w").write(lib.page("Binder covers", body, CSS + A.CSS))
    lib.render_pdf(html_path, pdf_path)
    os.remove(html_path)
    print("volumes:", [(v, a, b, (b - a + 1) // 2) for v, r, _, a, b, c in VOL], "->", pdf_path)

if __name__ == "__main__":
    build()
