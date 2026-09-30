#!/usr/bin/env python3
"""Build every product to dist/ (HTML + PDF), fill links into emails/tracker.
   python3 build.py            -> draft build (missing links stay visible as {{TOKENS}})
   python3 build.py --release  -> refuses until links, testimony review, and team photos are done
"""
import csv, glob, hashlib, json, os, re, subprocess, sys, datetime
ROOT = os.path.dirname(os.path.abspath(__file__)); R = lambda *p: os.path.join(ROOT,*p)
RELEASE = "--release" in sys.argv
sys.path.insert(0, ROOT); from new_product import PALETTES, BORDERS, ORNS
BRAND = "7HE H0LY REUP"   # the ONE place the brand name lives. Change here and rebuild to update every footer.
FOOTERS = [
 "YOU SURVIVED. NOW WE REBUILD.",
 "BANDO 2 VINEYARD",
 "TRADING THE CORNER FOR THE CROWN",
 "YOU SURVIVED. NOW WE REBUILD.",
]
MEMORIAL = "IN MEMORY OF BRANDI RENEE &mdash; 12787&ndash;121721"
COPY = f"&copy; 2026 {BRAND}. All rights reserved. No part of this work may be reproduced, distributed, copied, transmitted, or commercially exploited without prior written permission, except as permitted by applicable law."
cfg = {k:v for k,v in json.load(open(R("links.config.json"))).items() if not k.startswith("_")}
problems = []
def fill(text):
    for k,v in cfg.items(): text = text.replace("{{%s}}"%k, v if v else "{{%s}}"%k)
    return text
def footer(i, off):
    m = FOOTERS[(i+off)%len(FOOTERS)]
    memorial = f'<div>{MEMORIAL}</div>' if (i+off)%2==0 else ''
    return f'<footer><div class="mission">{m}</div><div>{BRAND} &nbsp;&bull;&nbsp; Page {i}</div>{memorial}<div class="legal">{COPY}</div></footer>'
def build_product(pj):
    p = json.load(open(pj)); d = p["design"]; slug = p["slug"]
    pal = PALETTES[d["palette"]]; body = open(os.path.join(os.path.dirname(pj),"body.html")).read()
    team = sorted(glob.glob(R("photos","team","*.[jJpP][pPnN]*[gG]")))
    cover = R('photos','stages',f"stage-{d['cover_photo']}.png")
    body = body.replace("<!--COVER_PHOTO-->", f'<img class="cover-photo" src="../photos/stages/stage-{d["cover_photo"]}.png" alt="">' if os.path.exists(cover) else "")
    testimony = open(R("content","testimony.html")).read()
    if "REVIEW_ME" in testimony: problems.append("content/testimony.html still has the REVIEW_ME marker")
    gallery = '<div class="gallery">'+"".join(f'<img src="../photos/team/{os.path.basename(t)}" alt="">' for t in team[:4])+'</div>' if team else ""
    if not team: problems.append("photos/team/ is empty (add your real photos with Big Boy)")
    pages = body + f'<section class="page"><div class="band"></div>{testimony}{gallery}<!--FOOTER--></section>' \
                 + f'<section class="page"><div class="band"></div>{open(R("content","legal.html")).read()}<!--FOOTER--></section>'
    n = [0]
    def rep(_): n[0]+=1; return footer(n[0], d["footer_offset"])
    pages = re.sub(r"<!--FOOTER-->", rep, pages)
    html = open(R("template","base.html")).read()
    for k,v in dict(TITLE=p["title"],SUBTITLE=p["subtitle"],C_PRIMARY=pal[0],C_ACCENT=pal[1],C_THIRD=pal[2],C_TINT=pal[3],BORDER=BORDERS[d["border"]],PAGES=pages).items():
        html = html.replace("{{%s}}"%k, v)
    html = fill(html)
    out = R("dist",f"{slug}.html"); open(out,"w").write(html)
    chrome = next(iter(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")), "chromium")
    subprocess.run([chrome,"--headless","--no-sandbox","--disable-gpu","--no-pdf-header-footer",f"--print-to-pdf={R('dist',slug+'.pdf')}",f"file://{out}"],check=False,capture_output=True)
    sha = hashlib.sha256(open(out,"rb").read()).hexdigest()
    log = R("private","creation-log.csv")
    if os.path.exists(log):
        rows = list(csv.reader(open(log)))
        for r in rows[1:]:
            if r[1]==slug: r[4]=sha; r[5]=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
        csv.writer(open(log,"w",newline="")).writerows(rows)
    print("built", slug)
os.makedirs(R("dist","emails"),exist_ok=True)
for pj in sorted(glob.glob(R("products","*","product.json"))): build_product(pj)
for src,dst in [(R("products","next-right-step","tracker.html"),R("dist","tracker.html"))]+[(e,R("dist","emails",os.path.basename(e))) for e in sorted(glob.glob(R("emails","*.md")))]:
    if os.path.exists(src): open(dst,"w").write(fill(open(src).read()))
empty = [k for k,v in cfg.items() if not v]
if empty: problems.append("links.config.json missing: "+", ".join(empty))
for f in glob.glob(R("dist","**","*.*"),recursive=True):
    if f.endswith((".html",".md")) and re.search(r"\{\{[A-Z_]+\}\}",open(f).read()) and RELEASE: problems.append("unfilled tokens in "+os.path.relpath(f,ROOT))
if problems:
    print("\n".join(("BLOCKED: " if RELEASE else "NOTE: ")+x for x in dict.fromkeys(problems)))
    if RELEASE: sys.exit(1)
else: print("RELEASE READY" if RELEASE else "Draft build clean")
