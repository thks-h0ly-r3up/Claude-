"""Convert the workbook / Volume II markdown into the designed book body."""
import re
import markdown
from lxml import html as LH, etree

from lib import esc, BRAND

SMALL = {"and","of","the","to","a","an","in","for","with","on","at","from","by","or","but","nor","vs"}
KEEP = {"II","III","IV","VI","VII","VIII","IX","C-PTSD","MAT","PTSD","DID","OG","CPS","HALT","AA","NA","THE"}

def smart_title(s):
    letters = [c for c in s if c.isalpha()]
    if not letters or sum(c.isupper() for c in letters) / len(letters) < 0.8:
        return s
    m0 = re.match(r"^(\d+(?:\.\d+)?\.?\s+)(.*)$", s)
    if m0:
        return m0.group(1) + smart_title(m0.group(2))
    words = s.split(" ")
    out = []
    for i, w in enumerate(words):
        core = re.sub(r"[^A-Za-z\-]", "", w)
        if core in KEEP and core not in ("THE",):
            out.append(w); continue
        lw = w.lower()
        if i > 0 and re.sub(r"[^a-z]", "", lw) in SMALL and not out[-1].endswith((":", "—")):
            out.append(lw)
        else:
            out.append(re.sub(r"[A-Za-z][A-Za-z']*", lambda m: m.group(0)[0].upper() + m.group(0)[1:].lower(), w))
    t = " ".join(out)
    t = t.replace("Thks", BRAND)
    return t

def mk(k):
    return f'<span class="mk">§H{k}§</span>'

# ----------------------------------------------------------------------------
def _writing(block):
    out = ['<div class="writing">']
    for ln in block.split("\n"):
        if not ln.strip():
            continue
        if re.fullmatch(r"[\s_]+", ln):
            out.append('<div class="wl"></div>')
            continue
        row = '<div class="wrow">'
        for part in re.split(r"(_{3,})", ln):
            if re.fullmatch(r"_{3,}", part):
                row += '<span class="fill"></span>'
            elif part.strip():
                row += f'<span class="tx">{esc(part.strip())}</span>'
        out.append(row + "</div>")
    out.append("</div>")
    return "".join(out)

def _prep(md):
    fences = []
    def grab(m):
        fences.append(_writing(m.group(1)))
        return f"\n\n@@FENCE{len(fences)-1}@@\n\n"
    md = re.sub(r"^```[^\n]*\n(.*?)\n```[ \t]*$", grab, md, flags=re.M | re.S)
    # underscore runs -> tokens (so markdown never reads them as emphasis / rules)
    md = re.sub(r"_{3,}", lambda m: f"@@U{len(m.group(0))}@@", md)
    # keep horizontal rules from turning the line above them into a setext heading
    md = re.sub(r"\n*^-{3,}[ \t]*$\n*", "\n\n---\n\n", md, flags=re.M)
    # blank line before a list that directly follows a paragraph line
    lines = md.split("\n")
    out = []
    li = re.compile(r"^\s*([-*+]|\d+\.)\s")
    for i, ln in enumerate(lines):
        if li.match(ln) and out and out[-1].strip() and not li.match(out[-1]) \
                and not out[-1].lstrip().startswith((">", "|", "#")) and not out[-1].startswith((" ", "\t")):
            out.append("")
        out.append(ln)
    return "\n".join(out), fences

def _fill(n):
    w = min(max(n * 0.40, 2.6), 24)
    return f'<span class="fill" style="width:{w:.1f}em"></span>'

def classify_bq(el, txt):
    ps = el.findall("p")
    text = txt(el)
    if text.startswith("For Brandi Renee"):
        return "epigraph"
    if len(ps) == 1 and len(text) < 420 and re.search(r"[—–]\s*(?:[1-3]\s)?[A-Z][A-Za-z]+\.?\s*\d", text) and len(el) == 1:
        return "verse"
    if el.find(".//h2") is not None:
        return "decl"
    if re.match(r'^[“"\']?\s*(Father|Jesus|Lord|God|Holy Spirit|Dear)\b', text):
        return "prayer"
    return "decl"

def convert(md_text, chapter_breaks=False, start_key=100, epigraph_first=True):
    md_text, fences = _prep(md_text)
    body = markdown.markdown(md_text, extensions=["tables", "sane_lists"])
    body = re.sub(r"<p>@@FENCE(\d+)@@</p>", lambda m: fences[int(m.group(1))], body)
    body = re.sub(r"@@U(\d+)@@", lambda m: _fill(int(m.group(1))), body)

    root = LH.fragment_fromstring(body, create_parent="div")
    kids = list(root)
    headings = []        # (level, text, key)
    key = start_key
    seen_h = False
    first_h2_done = False

    def txt(el):
        return re.sub(r"\s+", " ", "".join(el.itertext())).strip()

    i = 0
    new = []
    while i < len(kids):
        el = kids[i]
        tag = el.tag
        if tag == "h1":
            full = txt(el)
            m = re.match(r"^(.*?)\s+—\s+(.*)$", full)
            if m and re.match(r"(PART|BOOK)\s", m.group(1)):
                kicker, title = smart_title(m.group(1)), smart_title(m.group(2))
            elif ":" in full and full.upper().startswith("CLOSING"):
                kicker, title = "Closing", smart_title(full.split(":", 1)[1].strip())
            elif m:
                kicker, title = smart_title(m.group(1)), smart_title(m.group(2))
            else:
                kicker, title = "", smart_title(full)
            sub = ""
            j = i + 1
            if j < len(kids) and kids[j].tag == "h3" and not re.match(r"(WORK|STEP|STAGE|CONTRACT)", txt(kids[j])):
                sub = txt(kids[j]); i = j
            toc_text = (kicker + " — " if kicker else "") + title
            headings.append((1, toc_text, key))
            op = LH.fromstring(
                f'<section class="opener"><div class="kicker">{esc(kicker)}</div><h1>{esc(title)}{mk(key)}</h1>'
                f'<div class="orn"></div>' + (f'<div class="sub">{esc(sub)}</div>' if sub else "") +
                f'<div class="bm">{esc(BRAND)}</div></section>')
            new.append(op); key += 1; seen_h = True
        elif tag == "h2":
            full = txt(el)
            title = smart_title(full)
            cls = "chapter" if (chapter_breaks or re.match(r"(RESOURCES|CLOSING|APPENDIX)", full)) else ""
            first_h2_done = True
            el.text = title
            for c in list(el):
                el.remove(c)
            if cls:
                el.set("class", cls)
            el.append(LH.fromstring(mk(key)))
            headings.append((2, title, key)); key += 1
            new.append(el)
        elif tag == "h3" and re.match(r"WORK\b", txt(el)):
            wrap = LH.fromstring('<div class="work"></div>')
            el.text = smart_title(txt(el)) if False else txt(el)
            for c in list(el):
                el.remove(c)
            wrap.append(el)
            j = i + 1
            while j < len(kids) and kids[j].tag not in ("h1", "h2", "h3", "hr"):
                wrap.append(kids[j]); j += 1
            i = j - 1
            new.append(wrap)
        elif tag == "blockquote":
            if not seen_h and not first_h2_done and epigraph_first:
                el.set("class", "epigraph")
            else:
                el.set("class", classify_bq(el, txt))
            new.append(el)
        else:
            new.append(el)
        i += 1

    # tidy horizontal rules
    final = []
    for n_i, el in enumerate(new):
        if el.tag == "hr":
            prev = final[-1] if final else None
            nxt = new[n_i + 1] if n_i + 1 < len(new) else None
            if prev is None or nxt is None:
                continue
            if prev.tag == "hr" or (prev.get("class") or "") == "opener":
                continue
            if nxt.tag in ("hr", "h1") or (nxt.get("class") or "").startswith("opener") or (nxt.tag == "h2" and "chapter" in (nxt.get("class") or "")):
                continue
        final.append(el)

    for el in final:
        for t in el.iter("table"):
            rows = t.findall(".//tr")
            ncols = len(rows[0]) if rows else 0
            if ncols >= 9:
                t.set("class", "wide")
            for tr in t.findall(".//tbody/tr"):
                if not txt(tr):
                    tr.set("class", "blank")
        for u in el.iter("ul"):
            items = u.findall("li")
            if items and all((li.text or "").lstrip().startswith("[ ]") for li in items):
                u.set("class", "chk")
        for bq in el.iter("blockquote"):
            if not bq.get("class"):
                bq.set("class", classify_bq(bq, txt))

    out = "".join(etree.tostring(e, encoding="unicode", method="html") for e in final)
    # checkboxes
    out = out.replace("[ ]", '<span class="box"></span>')
    out = out.replace('<ul class="chk"><li>', '<ul class="chk"><li>')
    return out, headings
