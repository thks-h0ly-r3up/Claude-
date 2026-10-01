#!/usr/bin/env python3
"""Stamp a new blank product with a UNIQUE design fingerprint and a private creation record."""
import csv, hashlib, json, os, random, re, sys, datetime, shutil
ROOT = os.path.dirname(os.path.abspath(__file__))
PALETTES = [  # (primary, accent, third, tint) — all stay inside the pink/purple/turquoise/denim family
 ("#d6598f","#7a4c9e","#3fb6b0","#f3ecf8"), ("#7a4c9e","#d6598f","#4a6486","#f8ecf3"),
 ("#3fb6b0","#7a4c9e","#d6598f","#e8f6f5"), ("#4a6486","#d6598f","#3fb6b0","#eaeff5"),
 ("#c2478a","#5f4b8b","#2fa3a0","#f6eaf3"), ("#8e5ab5","#3fb6b0","#d6598f","#f1eaf7"),
 ("#e0679f","#4a6486","#7a4c9e","#fbeef4"), ("#2f9c97","#d6598f","#7a4c9e","#e6f4f3"),
]
BORDERS = ["2px solid var(--accent)","3px double var(--primary)","2px dashed var(--accent)","4px solid var(--third)","3px ridge var(--primary)"]
ORNS = ["🍇","⛓️‍💥","🌅","✝️","🫙","🌾","🌱","🐄"]
def main():
    if len(sys.argv) < 3: sys.exit('usage: new_product.py <slug> "<Title>" ["<Subtitle>"]')
    slug = re.sub(r'[^a-z0-9-]+','-',sys.argv[1].lower()).strip('-'); title = sys.argv[2]
    sub = sys.argv[3] if len(sys.argv) > 3 else ""
    d = os.path.join(ROOT,"products",slug)
    if os.path.exists(d): sys.exit(f"{slug} already exists")
    log = os.path.join(ROOT,"private","creation-log.csv"); os.makedirs(os.path.dirname(log),exist_ok=True)
    used = set()
    if os.path.exists(log):
        used = {r["design_fingerprint"] for r in csv.DictReader(open(log))}
    while True:  # never duplicate a design
        rng = random.Random(os.urandom(16))
        design = dict(palette=rng.randrange(len(PALETTES)), border=rng.randrange(len(BORDERS)),
                      ornament=rng.randrange(len(ORNS)), footer_offset=rng.randrange(12), cover_photo=rng.randrange(1,7))
        fp = hashlib.sha256(json.dumps(design,sort_keys=True).encode()).hexdigest()[:12]
        if fp not in used: break
        if len(used) >= len(PALETTES)*len(BORDERS)*len(ORNS): sys.exit("Design space exhausted — add palettes/ornaments")
    os.makedirs(d)
    json.dump(dict(slug=slug,title=title,subtitle=sub,design=design,fingerprint=fp),open(os.path.join(d,"product.json"),"w"),indent=2)
    body = open(os.path.join(ROOT,"template","page.blank.html")).read()
    open(os.path.join(d,"body.html"),"w").write(
      f'<section class="page"><div class="band"></div><div class="brand">7HE H0LY R3UP</div>'
      f'<h1>{title}</h1><div class="subtitle">{sub}</div><div class="orn">{ORNS[design["ornament"]]}</div>'
      f'<!--COVER_PHOTO--><!--FOOTER--></section>\n' + body*3)
    new = not os.path.exists(log)
    with open(log,"a",newline="") as f:
        w = csv.writer(f)
        if new: w.writerow(["created_utc","slug","title","design_fingerprint","content_sha256","last_built_utc"])
        w.writerow([datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),slug,title,fp,"",""])
    print(f"Created products/{slug}  (design {fp}). Private record: private/creation-log.csv")
if __name__ == "__main__": main()
