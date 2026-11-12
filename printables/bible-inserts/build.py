#!/usr/bin/env python3
"""Builds 7HE_H0LY_R3UP_Bible_Study_Inserts_Bundle.pdf (100 pages, US Letter landscape)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from reportlab.pdfgen import canvas
from lib import *
import lib
from data import *
from templates import *

TOTAL = 100
OUT = os.path.join(os.path.dirname(__file__), '7HE_H0LY_R3UP_Bible_Study_Inserts_Bundle.pdf')
STD_NOTE = 'Cut on the dashed lines  ·  Finished size 5 × 7.5 in (127 × 190.5 mm)  ·  Print at 100% / Actual Size  ·  Cut the center gutter first'
PAGES = []          # dict(sec, toc, draw)


# ------------------------------------------------------------------ frame bits
def slug(c, n, sec, note, ty=15):
    c.setFillColor(GRAY)
    c.setFont('Sans', 6.5)
    c.drawString(18, PAGE_H - ty, '7HE H0LY R3UP  ·  ' + sec)
    c.drawRightString(PAGE_W - 18, PAGE_H - ty, f'Page {n} of {TOTAL}')
    c.setFont('Sym', 7)
    c.drawString(PAGE_W / 2 - pdfmetrics.stringWidth(note, 'Sans', 6.5) / 2 - 12, 15, '✂')
    c.setFont('Sans', 6.5)
    c.drawCentredString(PAGE_W / 2, 15, note)


def ticks(c, x, y, w, h):
    c.setStrokeColor(INK)
    c.setLineWidth(0.4)
    for cx, cy in [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]:
        sx = -1 if cx == x else 1
        sy = -1 if cy == y else 1
        c.line(cx + sx * 3, cy, cx + sx * 11, cy)
        c.line(cx, cy + sy * 3, cx, cy + sy * 11)


def cutrect(c, x, y, w, h, r=0):
    c.setStrokeColor(INK)
    c.setLineWidth(0.9)
    c.setDash(5, 3)
    if r:
        c.roundRect(x, y, w, h, r, stroke=1, fill=0)
    else:
        c.rect(x, y, w, h, stroke=1, fill=0)
    c.setDash()


def scissors(c, x, y):
    c.setFillColor(INK)
    c.setFont('Sym', 8)
    c.drawString(x, y, '✂')


def two(sec, fa, fb, toc=None, note=STD_NOTE):
    def draw(c, n):
        lib.CUR['page'] = n
        slug(c, n, sec, note)
        pa = Panel(c, 18, 36, 'A')
        fa(pa)
        pa.fill_notes()
        pb = Panel(c, 414, 36, 'B')
        fb(pb)
        pb.fill_notes()
        for x in (18, 414):
            cutrect(c, x, 36, INS_W, INS_H)
            ticks(c, x, 36, INS_W, INS_H)
            scissors(c, x - 13, 36 + INS_H - 3)
    PAGES.append(dict(sec=sec, toc=toc or sec, draw=draw))


def raw(sec, draw, toc=None):
    PAGES.append(dict(sec=sec, toc=toc or sec, draw=draw))


# ------------------------------------------------------------------ cover
def draw_cover(c, n):
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(TURQ)
    c.roundRect(24, 24, PAGE_W - 48, PAGE_H - 48, 20, stroke=0, fill=1)
    # tooled border diamonds
    c.setFillColor(TEAL)
    for i in range(0, 60):
        x = 48 + i * 11.8
        if x > PAGE_W - 48:
            break
        for y in (44, PAGE_H - 44):
            c.saveState(); c.translate(x, y); c.rotate(45); c.rect(-2.2, -2.2, 4.4, 4.4, stroke=0, fill=1); c.restoreState()
    c.setStrokeColor(IVORY)
    c.setLineWidth(1.4)
    c.setDash(5, 4)
    c.roundRect(40, 40, PAGE_W - 80, PAGE_H - 80, 14, stroke=1, fill=0)
    c.setDash()
    # ombre band
    c.saveState()
    p = c.beginPath(); p.roundRect(24, 24, PAGE_W - 48, PAGE_H - 48, 20); c.clipPath(p, stroke=0, fill=0)
    steps = 80
    for i in range(steps):
        t = i / (steps - 1)
        col = HexColor('#%02x%02x%02x' % (int(0xD7 + (0x8E - 0xD7) * t), int(0x7F + (0x5B - 0x7F) * t), int(0xA6 + (0xB0 - 0xA6) * t)))
        c.setFillColor(col)
        c.rect(24 + i * (PAGE_W - 48) / steps, 24, (PAGE_W - 48) / steps + 1, 58, stroke=0, fill=1)
    # sunrise rising from the band
    p2 = c.beginPath(); p2.rect(24, 82, PAGE_W - 48, 200); c.clipPath(p2, stroke=0, fill=0)
    for r, col in [(120, PEACH), (92, GOLD), (62, IVORY)]:
        c.setFillColor(col)
        c.circle(PAGE_W / 2, 82, r, stroke=0, fill=1)
    c.restoreState()
    for i in range(14):
        a = math.radians(10 + i * (160 / 13))
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.1)
        c.line(PAGE_W / 2 + math.cos(a) * 132, 82 + math.sin(a) * 132, PAGE_W / 2 + math.cos(a) * 168, 82 + math.sin(a) * 168)
    # text
    tracked(c, PAGE_W / 2, PAGE_H - 78, '7HE H0LY R3UP', 'SansB', 13, IVORY, 4, 'c')
    cross(c, PAGE_W / 2, PAGE_H - 118, 30, GOLD)
    tracked(c, PAGE_W / 2, PAGE_H - 160, 'BIBLE STUDY', 'SansB', 17, GOLD, 8, 'c')
    c.setFillColor(IVORY)
    c.setFont('Head', 52)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 218, 'Inserts Bundle')
    c.setFont('BodyI', 17)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 248, 'You survived. Now we rebuild.')
    c.setFont('Body', 12.5)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 280, '100 print-ready pages for the courageous woman’s study Bible')
    items = ['Women of the Bible', 'Addiction & Recovery', 'Trauma & Healing', 'Topics Most Won’t Talk About']
    c.setFont('SansB', 8.6)
    tw = sum(pdfmetrics.stringWidth(i, 'SansB', 8.6) for i in items) + 3 * 40
    x = PAGE_W / 2 - tw / 2
    for k, i in enumerate(items):
        c.setFillColor(PEACH)
        c.drawString(x, PAGE_H - 306, i)
        x += pdfmetrics.stringWidth(i, 'SansB', 8.6)
        if k < 3:
            c.setFillColor(GOLD)
            c.circle(x + 20, PAGE_H - 303, 2, stroke=0, fill=1)
            x += 40
    c.setFont('Sans', 8.2)
    c.setFillColor(IVORY)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 326, 'Verse maps  ·  S.O.A.P.  ·  Bookmarks  ·  Stickers  ·  Journal & reflection pages  ·  Topic templates  ·  Cut lines & size notes on every sheet')
    broken_chain(c, 90, PAGE_H - 78, 22, GOLD)
    anchor(c, PAGE_W - 90, PAGE_H - 78, 36, GOLD, 2)
    tracked(c, PAGE_W / 2, 56, 'PRINT AT HOME  ·  US LETTER  ·  INSTANT PDF', 'SansB', 7.5, IVORY, 2.4, 'c')


# ------------------------------------------------------------------ read pages (front matter)
def blocks(c, x, y, w, items):
    for kind, txt in items:
        if kind == 'h':
            y -= 4
            tracked(c, x, y - 8, txt.upper(), 'SansB', 8, TEAL, 1.2)
            y -= 16
        elif kind == 'k':
            c.setFillColor(GOLD)
            c.setFont('Head', 15)
            c.drawString(x, y - 14, txt)
            y -= 24
        else:
            font, size, color, ind = {'p': ('Body', 9.8, INK, 0), 'i': ('BodyI', 9.6, GRAY, 0), 'b': ('Body', 9.6, INK, 12), 's': ('BodyI', 8.6, GRAY, 0)}[kind]
            lines = wrap(txt, font, size, w - ind)
            c.setFillColor(color)
            c.setFont(font, size)
            if kind == 'b':
                c.setFillColor(GOLD)
                c.circle(x + 3, y - size * 0.45, 1.8, stroke=0, fill=1)
                c.setFillColor(color)
            for ln in lines:
                c.drawString(x + ind, y - size * 0.85, ln)
                y -= size * 1.28
            y -= 4
    if y < 36:
        WARN.append(f'p{lib.CUR["page"]} read page text overflow {36 - y:.0f}pt')
    return y


def read_page(c, n, sec, title, left, right):
    lib.CUR['page'] = n
    c.setFillColor(GRAY); c.setFont('Sans', 6.5)
    c.drawString(18, PAGE_H - 15, '7HE H0LY R3UP  ·  ' + sec)
    c.drawRightString(PAGE_W - 18, PAGE_H - 15, f'Page {n} of {TOTAL}')
    c.setFillColor(TURQ)
    c.rect(0, PAGE_H - 70, PAGE_W, 40, stroke=0, fill=1)
    c.setFillColor(IVORY)
    c.setFont('Head', 20)
    c.drawString(36, PAGE_H - 58, title)
    cross(c, PAGE_W - 50, PAGE_H - 50, 20, GOLD)
    blocks(c, 36, PAGE_H - 84, 340, left)
    blocks(c, 416, PAGE_H - 84, 340, right)
    if left:
        c.setStrokeColor(LINE); c.setLineWidth(0.6)
        c.line(PAGE_W / 2, 40, PAGE_W / 2, PAGE_H - 90)
    tracked(c, PAGE_W / 2, 16, '7HE H0LY R3UP  ·  YOU SURVIVED. NOW WE REBUILD.', 'SansB', 6.2, TURQ, 1.5, 'c')


def welcome(c, n):
    left = [('h', 'Welcome, friend'),
            ('p', 'You survived. Now we rebuild. These inserts are made to sit inside your study Bible and meet you where you are: tired, angry, grateful, or all three on the same Tuesday.'),
            ('p', 'Some pages are tender. Some are loud. All of them are yours. Use what helps. Skip what does not. Come back when you can.'),
            ('h', 'What is inside (100 pages)'),
            ('b', '27 Women of the Word: verse map + S.O.A.P. for each woman'),
            ('b', '9 Addiction & Recovery sets, with craving, relapse-mercy, and family pages'),
            ('b', '8 Trauma & Healing sets: grounding, lament, boundaries, rebuild'),
            ('b', '12 Topics Most Won’t Talk About: abuse, church hurt, anger at God, doubt, despair, loss, divorce, shame, mental health, and forgiveness'),
            ('b', 'Verse maps, S.O.A.P. in 11 layouts, reflection pages, topic and character study templates'),
            ('b', 'Journal pages, trackers, memory cards, declarations, bookmarks, and sticker sheets'),
            ('h', 'A word on Scripture'),
            ('p', 'This bundle gives references only. No verse text is reproduced, so you can write from the edition you trust. Book names, verse numbers, and which books are included vary between the Ethiopian Orthodox Tewahedo canon, Greek (LXX)-based editions, and Western Bibles. Psalm numbers in LXX-based editions typically run one behind Western numbering for much of the Psalter, and we show both. Your edition’s table of contents is the final word.'),
            ('p', 'Cite your edition, translator, book, chapter, and verse when you write. Western translations are useful to document omissions or differences, not to replace your tradition’s text.')]
    right = [('h', 'Check both sides, including mine'),
             ('p', 'Do not take my word for it. Open the source and check the pattern yourself. Search the exact phrase, read the verses around it, confirm the edition, translator, and date, and ask clergy or a trusted scholar about doctrine. Truth can withstand honest questions.'),
             ('h', 'Care notes'),
             ('p', 'Trauma and recovery pages carry content notes. You never have to finish a page. Grounding steps are invitations: eyes open is fine, and pausing is always allowed. Struggling does not mean weak faith, and praying harder is not a replacement for care.'),
             ('h', 'Disclaimer'),
             ('p', '7HE H0LY R3UP shares lived experience and carefully sourced study tools. This is not medical, mental-health, legal, or pastoral counsel and does not diagnose or treat anything. Spiritual practice can sit beside professional care, not in place of it. If you are in danger, call 911 (US) or your local emergency number. For crisis support, call or text 988 (US). Phone numbers change; confirm them before you rely on them.'),
             ('h', 'Personal-use license'),
             ('p', 'Print for yourself, your own Bible, and a small group you personally lead. Do not share, resell, or redistribute the files, edit and resell them, or upload them anywhere. Commercial or large-group use needs written permission.'),
             ('s', '© 2026 7HE H0LY R3UP. All rights reserved. First edition, November 2026.')]
    read_page(c, n, 'Welcome & Terms', 'Welcome & Terms', left, right)


def instructions(c, n):
    left = [('h', 'Print'),
            ('b', 'Paper: US Letter, 8.5 × 11 in, landscape. Choose Actual Size or 100%, never Fit to Page.'),
            ('b', 'For inserts, 20–24 lb paper keeps your Bible from bulging. Cardstock (65–110 lb) is for bookmarks and dividers. Matte sticker paper is for sticker sheets.'),
            ('b', 'Do a test on page 4 first: the ruler squares should measure exactly 1 inch.'),
            ('b', 'Print single-sided for tip-in inserts so nothing shows through. Double-sided is fine for binders.'),
            ('h', 'Cut'),
            ('b', 'Every sheet has dashed cut lines and corner ticks. Cut the center gutter first, then cut just inside each dashed line.'),
            ('b', 'A paper trimmer gives the cleanest edge. Scissors work. Keep text at least 0.3 in from any edge you trim.'),
            ('b', 'Each sheet’s bottom edge note gives its finished size.'),
            ('h', 'Fit to your Bible'),
            ('b', 'Inserts finish at 5 × 7.5 in, which suits most 6 × 9 in study Bibles. Hold one up to your page. If it is too big, trim up to 0.25 in from the outside edge. Text stays safe.'),
            ('b', 'Dotted turquoise stitching is decoration. It is not a cut line.')]
    right = [('h', 'Attach'),
             ('b', 'Tip-in: run a thin line of repositionable tape or a dry glue stick along the binding edge of the insert, and press it to the gutter side of your page. Avoid wet glue. Bible paper wrinkles.'),
             ('b', 'Or tuck an insert in with a washi-tape tab, or punch it for a binder.'),
             ('b', 'Test on a spare page first.'),
             ('h', 'Bookmarks and stickers'),
             ('b', 'Bookmarks finish at 2 × 6 in. Punch the marked dot for a tassel.'),
             ('b', 'Stickers print on sticker paper. Cut on the dashed outlines. Cutting-machine files are not included.'),
             ('h', 'Troubleshooting'),
             ('b', 'Edges cut off: your printer has a hard margin. This file uses a 0.25 in margin. Check Actual Size.'),
             ('b', 'Colors look different: screens and printers differ. Use best quality.'),
             ('b', 'Too much ink: print in grayscale or draft mode.'),
             ('h', 'Go at your own pace'),
             ('p', 'No streaks. No shame. Open a page, do one small thing, close it. That counts. We survived. Now let’s rebuild.')]
    read_page(c, n, 'Instructions', 'How to Print, Cut, and Use', left, right)


def sizeguide(c, n):
    lib.CUR['page'] = n
    read_page(c, n, 'Size & Cut Guide', 'Size & Cut Guide', [], [])
    rows = [('Inserts (two per sheet)', '5 × 7.5 in', '127 × 190.5 mm'),
            ('Divider with tab', '5 × 7.5 in + 0.35 in tab', '127 × 190.5 + 9 mm'),
            ('S.O.A.P. cards (four per sheet)', '5 × 3.5 in', '127 × 89 mm'),
            ('Memory verse cards (eight per sheet)', '2.5 × 3.5 in', '63.5 × 89 mm'),
            ('Bookmarks (five per sheet)', '2 × 6 in', '51 × 152 mm'),
            ('Round stickers (28 per sheet)', '1.25 in diameter', '32 mm'),
            ('Label stickers (24 per sheet)', '2 × 0.75 in', '51 × 19 mm'),
            ('Page flags (50 per sheet)', '1.75 × 0.5 in', '44 × 13 mm')]
    x, y = 36, PAGE_H - 96
    tracked(c, x, y, 'TEMPLATE', 'SansB', 7, TEAL, 1.2)
    tracked(c, x + 230, y, 'FINISHED SIZE', 'SansB', 7, TEAL, 1.2)
    tracked(c, x + 340, y, 'METRIC', 'SansB', 7, TEAL, 1.2)
    y -= 6
    for a, b, d in rows:
        y -= 21
        c.setStrokeColor(LINE); c.setLineWidth(0.5)
        c.line(x, y - 6, x + 460, y - 6)
        c.setFillColor(INK); c.setFont('Body', 10)
        c.drawString(x, y, a)
        c.drawString(x + 230, y, b)
        c.setFillColor(GRAY)
        c.drawString(x + 340, y, d)
    # legend + test squares
    lx = 540
    tracked(c, lx, PAGE_H - 96, 'LEGEND', 'SansB', 7, TEAL, 1.2)
    c.setStrokeColor(INK); c.setLineWidth(0.9); c.setDash(5, 3); c.line(lx, PAGE_H - 118, lx + 60, PAGE_H - 118); c.setDash()
    c.setFillColor(INK); c.setFont('Body', 10); c.drawString(lx + 72, PAGE_H - 121, 'Cut here')
    c.setStrokeColor(TURQ); c.setLineWidth(0.9); c.setDash(1.2, 3); c.line(lx, PAGE_H - 142, lx + 60, PAGE_H - 142); c.setDash()
    c.drawString(lx + 72, PAGE_H - 145, 'Stitching: decoration only')
    c.setFillColor(INK); c.setFont('Sym', 11); c.drawString(lx, PAGE_H - 170, '✂')
    c.setFont('Body', 10); c.drawString(lx + 72, PAGE_H - 169, 'Start cutting here')
    tracked(c, lx, PAGE_H - 214, 'PRINT TEST (SHOULD MEASURE 1 IN)', 'SansB', 7, TEAL, 1.2)
    c.setStrokeColor(INK); c.setLineWidth(0.8)
    c.rect(lx, PAGE_H - 296, 72, 72, stroke=1, fill=0)
    for k in range(1, 4):
        c.line(lx + 72 + 8, PAGE_H - 224 - k * 18, lx + 72 + 14, PAGE_H - 224 - k * 18)
    c.setFont('Body', 9); c.drawString(lx + 86, PAGE_H - 262, '1 in')
    c.line(lx, PAGE_H - 316, lx + 216, PAGE_H - 316)
    for k in range(4):
        c.line(lx + k * 72, PAGE_H - 311, lx + k * 72, PAGE_H - 321)
    c.drawString(lx, PAGE_H - 334, '3 in line')
    y = 250
    c.setFillColor(INK); c.setFont('BodyI', 9.6)
    for ln in wrap('If the square measures less than 1 inch, your printer scaled the page. Reprint at Actual Size or 100%. All text sits at least 0.3 in inside every cut line, so trimming up to 0.25 in from an outer edge is safe.', 'BodyI', 9.6, 460):
        c.drawString(36, y, ln); y -= 13
    PAGES_META['size_done'] = True


PAGES_META = {}


def toc(c, n):
    lib.CUR['page'] = n
    read_page(c, n, 'Contents', 'Contents', [], [])
    rows = list(TOC_ROWS)
    half = (len(rows) + 1) // 2
    for col, chunk in enumerate([rows[:half], rows[half:]]):
        x = 36 + col * 380
        y = PAGE_H - 104
        for label, a, b in chunk:
            c.setFillColor(INK); c.setFont('Body', 10.4)
            c.drawString(x, y, label)
            pg = f'{a}' if a == b else f'{a}–{b}'
            c.setFont('SansB', 9); c.setFillColor(TEAL)
            c.drawRightString(x + 340, y, pg)
            c.setStrokeColor(LINE); c.setDash(1, 2.5); c.setLineWidth(0.5)
            w = pdfmetrics.stringWidth(label, 'Body', 10.4)
            c.line(x + w + 6, y + 2, x + 340 - pdfmetrics.stringWidth(pg, 'SansB', 9) - 6, y + 2)
            c.setDash()
            y -= 22


TOC_ROWS = []


# ------------------------------------------------------------------ bookmarks
def bm_frame(c, i, accent):
    x = 36 + i * 144
    y = 90
    c.setStrokeColor(accent)
    c.setLineWidth(0.9)
    c.setDash(1.2, 3)
    c.roundRect(x + 7, y + 7, 130, 418, 8, stroke=1, fill=0)
    c.setDash()
    c.setFillColor(accent)
    c.rect(x, y + 432 - 14, 144, 14, stroke=0, fill=1)
    c.setFillColor(WHITE); c.setStrokeColor(INK); c.setLineWidth(0.6)
    c.circle(x + 72, y + 432 - 34, 4.5, stroke=1, fill=1)
    return x, y


def bookmarks(kind):
    accents = [TURQ, GOLD, PINK, PURPLE, DENIM]

    def draw(c, n):
        lib.CUR['page'] = n
        slug(c, n, 'Bookmarks', 'Cut on the dashed lines  ·  Bookmark 2 × 6 in (51 × 152 mm)  ·  Punch the small circle for a tassel  ·  Print on cardstock at 100%')
        for i in range(5):
            x, y = bm_frame(c, i, accents[i])
            cx = x + 72
            top = y + 432 - 58
            if kind == 'verse':
                tracked(c, cx, top, 'VERSE KEEPER', 'SansB', 7.5, TEAL, 1.6, 'c')
                sun(c, cx, top - 26, 12, accents[i] if accents[i] != GOLD else GOLD)
                c.setFillColor(GRAY); c.setFont('BodyI', 7.8); c.drawCentredString(cx, top - 56, 'Reference')
                c.setStrokeColor(LINE); c.setLineWidth(0.5)
                c.line(x + 22, top - 70, x + 122, top - 70)
                c.drawCentredString(cx, top - 90, '') if False else None
                for k in range(11):
                    c.line(x + 22, top - 96 - k * 22, x + 122, top - 96 - k * 22)
                tracked(c, cx, y + 36, 'YOU SURVIVED. NOW WE REBUILD.', 'SansB', 4.6, accents[i], 0.8, 'c')
            elif kind == 'decl':
                items = [('I am seen.', 'Genesis 16:13'), ('Mercy is new this morning.', 'Lamentations 3:22–23'), ('I can ask for help and still be faithful.', 'Galatians 6:2'),
                         ('I am allowed to take up space.', ps(18, '19')), ('I survived. Now I rebuild.', 'Nehemiah 2:18')][i]
                heart(c, cx, top - 12, 8, accents[i])
                yy = top - 62
                for ln in wrap(items[0], 'Head', 12, 104):
                    c.setFillColor(TEAL); c.setFont('Head', 12); c.drawCentredString(cx, yy, ln); yy -= 17
                c.setStrokeColor(GOLD); c.setLineWidth(1.5); c.line(cx - 16, yy - 4, cx + 16, yy - 4)
                yy -= 22
                for ln in wrap(items[1], 'BodyI', 8.6, 104):
                    c.setFillColor(GRAY); c.setFont('BodyI', 8.6); c.drawCentredString(cx, yy, ln); yy -= 11
                c.setStrokeColor(LINE); c.setLineWidth(0.5)
                c.setFillColor(GRAY); c.setFont('BodyI', 7.6); c.drawCentredString(cx, yy - 18, 'My own')
                for k in range(7):
                    c.line(x + 22, yy - 40 - k * 20, x + 122, yy - 40 - k * 20)
                tracked(c, cx, y + 36, '7HE H0LY R3UP', 'SansB', 5.6, accents[i], 1.2, 'c')
            elif kind == 'women':
                name, ref, line = [('Hagar', 'Genesis 16', 'The God who sees me.'), ('Hannah', '1 Samuel 1', 'I poured out my soul.'), ('Ruth', 'Ruth 1–4', 'Where you go, I will go.'),
                                   ('Rizpah', '2 Samuel 21', 'She kept watch.'), ('Mary Magdalene', 'John 20', 'I have seen the Lord.')][i]
                tracked(c, cx, top, 'WOMEN OF THE WORD', 'SansB', 6, TEAL, 1.2, 'c')
                c.setFillColor(accents[i]); c.circle(cx, top - 34, 18, stroke=0, fill=1)
                c.setFillColor(WHITE); c.setFont('Head', 18); c.drawCentredString(cx, top - 40, name[0])
                yy = top - 76
                for ln in wrap(name, 'Head', 13, 106):
                    c.setFillColor(TEAL); c.setFont('Head', 13); c.drawCentredString(cx, yy, ln); yy -= 16
                c.setFillColor(GRAY); c.setFont('BodyI', 8.8); c.drawCentredString(cx, yy - 4, ref)
                yy -= 28
                for ln in wrap(line, 'Body', 9, 100):
                    c.setFillColor(INK); c.setFont('Body', 9); c.drawCentredString(cx, yy, ln); yy -= 12
                c.setStrokeColor(LINE); c.setLineWidth(0.5)
                for k in range(9):
                    c.line(x + 22, yy - 20 - k * 20, x + 122, yy - 20 - k * 20)
            else:
                t = ['Today’s Soft Steps', 'My Safe People', 'Thank You, Lord', 'I’m Allowed to Ask', 'My Verse This Week'][i]
                tracked(c, cx, top, 'CHECK-IN', 'SansB', 6.4, TEAL, 1.4, 'c')
                c.setFillColor(TEAL); c.setFont('Head', 11.5)
                yy = top - 24
                for ln in wrap(t, 'Head', 11.5, 108):
                    c.drawCentredString(cx, yy, ln); yy -= 14
                c.setStrokeColor(GOLD); c.setLineWidth(1.5); c.line(cx - 16, yy, cx + 16, yy)
                yy -= 14
                opts = [['Water', 'Food', 'Breath', 'Reached out', 'Prayed one sentence', 'Outside 5 min', 'Rested'],
                        ['Name: _______', 'Name: _______', 'Name: _______', 'Name: _______', 'Name: _______', '988 (US)', 'My team list'],
                        ['1. _________', '2. _________', '3. _________', '4. _________', '5. _________', '6. _________', '7. _________'],
                        ['Question 1', 'Question 2', 'Question 3', 'Who to ask', 'Source to check', 'Edition', 'What I found'],
                        ['Reference', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat · Sun']][i]
                for o in opts:
                    c.setFillColor(accents[i]); c.setFont('Sym', 10); c.drawString(x + 18, yy - 2, '☐')
                    c.setFillColor(INK); c.setFont('Body', 8.8); c.drawString(x + 34, yy, o)
                    yy -= 24
                c.setStrokeColor(LINE); c.setLineWidth(0.5)
                for k in range(3):
                    c.line(x + 22, yy - 6 - k * 20, x + 122, yy - 6 - k * 20)
                tracked(c, cx, y + 36, 'YOU SURVIVED. NOW WE REBUILD.', 'SansB', 4.6, accents[i], 0.8, 'c')
        for i in range(5):
            x = 36 + i * 144
            cutrect(c, x, 90, 144, 432)
            ticks(c, x, 90, 144, 432)
    return draw


# ------------------------------------------------------------------ stickers
def icon(c, kind, cx, cy, s, col):
    if kind == 'cross':
        cross(c, cx, cy, s, col)
    elif kind == 'sun':
        sun(c, cx, cy, s * 0.5, col, 10, 1.3)
    elif kind == 'anchor':
        anchor(c, cx, cy, s, col, 1.8)
    elif kind == 'chain':
        broken_chain(c, cx, cy, s * 0.55, col, 1.8)
    elif kind == 'heart':
        heart(c, cx, cy, s * 0.3, col)


def stickers_round(c, n):
    lib.CUR['page'] = n
    slug(c, n, 'Stickers', 'Round stickers 1.25 in (32 mm)  ·  Print on matte sticker paper at 100%  ·  Cut on the dashed outlines (art bleeds past the line)')
    labels = [('S.O.A.P.', 'cross'), ('PRAY', 'heart'), ('VERSE', 'sun'), ('THANKS', 'heart'), ('ANSWERED', 'sun'), ('LAMENT', 'chain'), ('REST', 'sun'),
              ('DONE', 'cross'), ('FAST', 'anchor'), ('HELP', 'anchor'), ('SAFE', 'anchor'), ('BREATHE', 'sun'), ('ASK', 'cross'), ('CHECK THE SOURCE', 'cross'),
              ('REBUILD', 'chain'), ('WORD STUDY', 'cross'), ('MEMORY', 'heart'), ('NOTE', 'sun'), ('CALL SOMEONE', 'heart'), ('GRACE', 'cross'), ('MERCY', 'heart'),
              ('FREE', 'chain'), ('HER STORY', 'heart'), ('TRUTH', 'cross'), ('COURAGE', 'sun'), ('STRONG', 'anchor'), ('SEEN', 'sun'), ('YES', 'cross')]
    cols = [TURQ, GOLD, PINK, PURPLE, DENIM, PEACH, TEAL]
    for k, (txt, ic) in enumerate(labels):
        cx = 72 + (k % 7) * 108
        cy = 90 + 54 + (k // 7) * 108
        cy = 612 - cy
        col = cols[(k + k // 7) % 7]
        dark = col in (GOLD, PEACH)
        c.setFillColor(col)
        c.circle(cx, cy, 47, stroke=0, fill=1)
        c.setStrokeColor(IVORY if not dark else INK)
        c.setLineWidth(0.8)
        c.setDash(1.2, 2.5)
        c.circle(cx, cy, 40, stroke=1, fill=0)
        c.setDash()
        fg = INK if dark else IVORY
        icon(c, ic, cx, cy + 12, 22, fg)
        ls = wrap(txt, 'SansB', 7.6, 66)
        yy = cy - 14 - (len(ls) - 1) * 4
        for ln in ls:
            tracked(c, cx, yy, ln, 'SansB', 7.2, fg, 0.7, 'c')
            yy -= 9
        cutrect(c, cx - 45, cy - 45, 90, 90, 45)


def stickers_labels(c, n):
    lib.CUR['page'] = n
    slug(c, n, 'Stickers', 'Label stickers 2 × 0.75 in (51 × 19 mm)  ·  Print on matte sticker paper at 100%  ·  Cut on the dashed outlines')
    labs = ['Today’s Verse', 'Prayer Request', 'Answered Prayer', 'Thank You, Lord', 'Check the Source', 'Soft Step', 'Sermon Notes', 'Memory Verse',
            'Women of the Word', 'Lament', 'Boundaries', 'I Need to Ask', 'Rest Day', 'Fasting Day', 'Feast Day', 'Safe Person', 'Appointment', 'Journal Here',
            'Cross-Reference', 'Word Study', 'Big Idea', 'Declaration', 'Both Sides', 'Rebuild Day']
    cols = [TURQ, GOLD, PINK, PURPLE, DENIM, TEAL]
    for k, t in enumerate(labs):
        x = 72 + (k % 4) * 162
        y = 612 - (90 + (k // 4) * 72) - 54
        col = cols[(k // 4 + k) % 6]
        c.setFillColor(T_TURQ if col in (TURQ, TEAL) else T_GOLD if col == GOLD else T_PEACH)
        c.roundRect(x - 2, y - 2, 148, 58, 8, stroke=0, fill=1)
        c.setFillColor(col)
        c.roundRect(x, y, 10, 54, 5, stroke=0, fill=1)
        c.setFillColor(INK)
        c.setFont('Head', 9.2)
        c.drawString(x + 18, y + 33, t)
        c.setStrokeColor(LINE if False else col)
        c.setLineWidth(0.5)
        c.line(x + 18, y + 12, x + 134, y + 12)
        c.line(x + 18, y + 24, x + 134, y + 24)
        cutrect(c, x, y, 144, 54, 6)


def stickers_flags(c, n):
    lib.CUR['page'] = n
    slug(c, n, 'Stickers', 'Page flags 1.75 × 0.5 in (44 × 13 mm)  ·  Print on sticker paper at 100%  ·  Cut on the dashed outlines  ·  Fold over a page edge or use as tabs')
    names = ['VERSE', 'PRAYER', 'NOTE', 'ASK', 'THANKS', 'LAMENT', 'S.O.A.P.', 'SOURCE', 'REST', 'HELP']
    cols = [TURQ, GOLD, PINK, PURPLE, DENIM]
    for i in range(5):
        for j in range(10):
            x = 36 + i * 144 + 9
            y = 54 + 504 - (j + 1) * 50.4 + 7
            col = cols[i]
            c.setFillColor(col)
            p = c.beginPath()
            p.moveTo(x, y); p.lineTo(x + 126, y); p.lineTo(x + 114, y + 18); p.lineTo(x + 126, y + 36); p.lineTo(x, y + 36); p.close()
            c.drawPath(p, stroke=0, fill=1)
            dark = col == GOLD
            tracked(c, x + 8, y + 14, names[j], 'SansB', 7.5, INK if dark else IVORY, 1.1)
            c.setStrokeColor(INK); c.setLineWidth(0.8); c.setDash(4, 3)
            c.drawPath(p, stroke=1, fill=0)
            c.setDash()


# ------------------------------------------------------------------ cards pages
def soap_cards(c, n):
    lib.CUR['page'] = n
    slug(c, n, 'S.O.A.P. Cards', 'S.O.A.P. cards 5 × 3.5 in (127 × 89 mm)  ·  Cut on the dashed lines  ·  Print at 100% on cardstock or paper')
    for r in range(2):
        for col in range(2):
            x = 18 + col * 396
            y = 36 + (1 - r) * 288
            card_soap(c, x, y)
            cutrect(c, x, y, 360, 252)
            ticks(c, x, y, 360, 252)


def memory_cards(c, n):
    lib.CUR['page'] = n
    slug(c, n, 'Memory Verse Cards', 'Cards 2.5 × 3.5 in (63.5 × 89 mm)  ·  Cut on the dashed lines  ·  Print on cardstock at 100%')
    for r in range(2):
        for col in range(4):
            x = 18 + col * 192
            y = 48 + (1 - r) * 264
            c.setStrokeColor(TURQ); c.setLineWidth(0.8); c.setDash(1.2, 3)
            c.roundRect(x + 5, y + 5, 170, 242, 8, stroke=1, fill=0); c.setDash()
            c.setFillColor(TURQ); c.rect(x, y + 252 - 22, 180, 22, stroke=0, fill=1)
            tracked(c, x + 90, y + 252 - 15, 'MEMORY VERSE', 'SansB', 7, IVORY, 1.6, 'c')
            sun(c, x + 90, y + 252 - 42, 9, GOLD)
            c.setFillColor(GRAY); c.setFont('BodyI', 7.6)
            c.drawString(x + 16, y + 252 - 64, 'Reference (edition)')
            c.setStrokeColor(LINE); c.setLineWidth(0.5)
            c.line(x + 16, y + 252 - 72, x + 164, y + 252 - 72)
            c.drawString(x + 16, y + 252 - 88, 'The words')
            for k in range(6):
                c.line(x + 16, y + 252 - 104 - k * 16, x + 164, y + 252 - 104 - k * 16)
            c.drawString(x + 16, y + 252 - 208, 'Said aloud')
            c.setFillColor(TURQ); c.setFont('Sym', 11)
            c.drawString(x + 70, y + 252 - 210, '☐ ☐ ☐')
            c.setFillColor(GRAY); c.setFont('BodyI', 7.2)
            c.drawCentredString(x + 90, y + 20, 'You survived. Now we rebuild.')
            cutrect(c, x, y, 180, 252, 6)
            ticks(c, x, y, 180, 252)


# ------------------------------------------------------------------ dividers
def divider_panel(title, kicker, blurb, bullets, rng, tabpos, color, icon_kind):
    def fn(p):
        c = p.c
        # tab
        tx = p.x + 24 + tabpos * 90
        c.setFillColor(color)
        c.roundRect(tx, p.top, 118, 26, 6, stroke=0, fill=1)
        tracked(c, tx + 59, p.top + 9, kicker.upper(), 'SansB', 6.6, IVORY if color not in (GOLD, PEACH) else INK, 1, 'c')
        cx = p.x + INS_W / 2
        p.cy = p.top - 70
        icon(c, icon_kind, cx, p.cy, 54, color)
        p.cy -= 50
        c.setFillColor(TEAL)
        for ln in wrap(title, 'Head', 22, p.w):
            c.setFont('Head', 22)
            c.drawCentredString(cx, p.cy, ln)
            p.cy -= 28
        c.setStrokeColor(GOLD); c.setLineWidth(2); c.line(cx - 22, p.cy + 8, cx + 22, p.cy + 8)
        p.cy -= 14
        for ln in wrap(blurb, 'BodyI', 10.4, p.w - 20):
            c.setFillColor(INK); c.setFont('BodyI', 10.4)
            c.drawCentredString(cx, p.cy, ln)
            p.cy -= 14
        p.cy -= 14
        p.label('In this section')
        p.bullets(bullets, 9.4)
        p.cy -= 8
        p.note('Pages ' + rng, 'Where to find it', T_TURQ, 'SansB', 8.6)
        p.field('Notes', 5)
    return fn


def divider_page(sec, a, b, note):
    def draw(c, n):
        lib.CUR['page'] = n
        slug(c, n, sec, note, 7)
        for x, spec in ((18, a), (414, b)):
            pnl = Panel(c, x, 36, 'D')
            spec(pnl)
            path = c.beginPath()
            tabs = spec.tabbox
            path.moveTo(x, 36); path.lineTo(x, 36 + INS_H)
            path.lineTo(tabs[0], 36 + INS_H); path.lineTo(tabs[0], 36 + INS_H + 26); path.lineTo(tabs[0] + 118, 36 + INS_H + 26)
            path.lineTo(tabs[0] + 118, 36 + INS_H); path.lineTo(x + INS_W, 36 + INS_H); path.lineTo(x + INS_W, 36); path.close()
            c.setStrokeColor(INK); c.setLineWidth(0.9); c.setDash(5, 3)
            c.drawPath(path, stroke=1, fill=0); c.setDash()
            scissors(c, x - 13, 36 + INS_H - 3)
    return draw


# ------------------------------------------------------------------ assemble
def build():
    # --- front
    raw('Cover', draw_cover, 'Cover')
    raw('Welcome & Terms', welcome, 'Welcome, Terms & Care Notes')
    raw('Instructions', instructions, 'Instructions')
    raw('Size & Cut Guide', sizeguide, 'Size & Cut Guide')
    raw('Contents', toc, 'Contents')
    # --- women
    for i, w in enumerate(WOMEN, 1):
        two('Women of the Word', (lambda p, w=w, i=i: woman_a(p, w, i, len(WOMEN))), (lambda p, w=w: woman_b(p, w)), 'Women of the Word (27 women)')
    # --- topic sets
    def topic_set(sec, data, toc):
        for d in data:
            a = d.get('custom_a')
            fa = {'halt': a_halt, 'team': a_team, 'ground': a_ground, 'window': a_window, 'circles': a_circles}.get(a)
            fa_f = (lambda p, d=d, fa=fa: fa(p, d)) if fa else (lambda p, d=d: topic_a(p, d))
            b = d.get('custom_b')
            bmap = {'craving': b_craving, 'exits': b_exits, 'days': b_days, 'slip': b_slip, 'triggers': b_triggers, 'testimony': b_testimony,
                    'icancant': b_icancant, 'lament': b_lament, 'mercies': b_mercies, 'blueprint': b_blueprint, 'bothsides': b_bothsides,
                    'safetyplan': b_safetyplan, 'careteam': b_careteam, 'safemoves': b_safemoves, 'nopractice': b_nopractice, 'bodymap': b_bodymap}
            fb = bmap.get(b)
            fb_f = (lambda p, d=d, fb=fb: fb(p, d)) if fb else (lambda p, d=d: topic_b(p, d))
            two(sec, fa_f, fb_f, toc)
    topic_set('Addiction & Recovery', ADDICTION, 'Addiction & Recovery')
    topic_set('Trauma & Healing', TRAUMA, 'Trauma & Healing')
    topic_set('Topics Most Won’t Talk About', HARD, 'Topics Most Won’t Talk About')
    # --- verse maps
    for a, b in [(vm_classic, vm_web), (vm_word, vm_compare), (vm_oia, vm_chapter), (vm_prayer, vm_two)]:
        two('Verse Maps', a, b, 'Verse Maps')
    # --- SOAP
    two('S.O.A.P.', lambda p: soap_page(p), soap_soft, 'S.O.A.P. Templates')
    two('S.O.A.P.', soap_tracker, soap_ground, 'S.O.A.P. Templates')
    two('S.O.A.P.', soap_mini2, soap_mini3, 'S.O.A.P. Templates')
    two('S.O.A.P.', soap_boxes, soap_art, 'S.O.A.P. Templates')
    raw('S.O.A.P.', soap_cards, 'S.O.A.P. Templates')
    two('S.O.A.P.', soap_teaching, soap_hard, 'S.O.A.P. Templates')
    # --- reflection
    for a, b in [(weekly, monthly), (thanks_log, answered), (bothsides_page, teaching_notes), (feelings, evening), (letter_god, letter_young)]:
        two('Reflection', a, b, 'Reflection Templates')
    # --- topic templates
    for a, b in [(topic_study, character_study), (book_overview, theme_tracker), (questions, teach_back)]:
        two('Topic Templates', a, b, 'Topic & Study Templates')
    # --- journal
    for a, b in [(j_lined, j_dotted), (j_grid, j_dated), (j_prayer_list, j_prayer_week), (j_gratitude, j_doodle), (j_rebuild, j_habits), (j_cornell, j_frame), (j_reading, j_verse_week)]:
        two('Journal', a, b, 'Journal & Tracker Pages')
    # --- dividers
    dnote = 'Divider with tab  ·  Finished size 5 × 7.5 in + 0.35 in tab  ·  Cut around the tab on the dashed line  ·  Print on cardstock at 100%'
    def mk(title, kicker, blurb, bullets, key, tabpos, color, ic):
        f = divider_panel(title, kicker, blurb, bullets, '{%s}' % key, tabpos, color, ic)
        f.tabbox = (0, 0)
        return f
    # tab x positions are resolved per panel at draw time; store absolute positions
    def dv(title, kicker, blurb, bullets, key, tabpos, color, ic, px):
        def f(p):
            rng = SECTION_RANGES[key]
            divider_panel(title, kicker, blurb, bullets, rng, tabpos, color, ic)(p)
        f.tabbox = (px + 24 + tabpos * 90, 0)
        return f
    d1 = dv('Women of the Word', 'Women', 'Twenty-seven women, named and unnamed. Their stories, read slowly and without shame.', ['Verse map + S.O.A.P. for each woman', 'Content notes on every hard story', 'A soft step you can do in ten minutes'], 'Women of the Word', 0, TURQ, 'heart', 18)
    d2 = dv('Addiction & Recovery', 'Recovery', 'Honest pages for the fight inside, and for the people who love someone in it.', ['Craving log, exit plan, and 30 days of mercy', 'If I Slip: a mercy plan', 'Team page and help lines'], 'Addiction & Recovery', 1, GOLD, 'chain', 414)
    two_div = divider_page('Dividers', d1, d2, dnote)
    PAGES.append(dict(sec='Dividers', toc='Section Dividers', draw=two_div))
    d3 = dv('Trauma & Healing', 'Healing', 'Lament, grounding, boundaries, and the slow work of rebuilding the wall.', ['Grounding and body check-in', 'Lament and “where was God?”', 'Boundaries and the rebuild blueprint'], 'Trauma & Healing', 2, PINK, 'anchor', 18)
    d4 = dv('Topics Most Won’t Talk About', 'Hard Topics', 'The questions people whisper. Asked out loud, with sources, and with care.', ['Abuse, church hurt, anger at God, doubt', 'Loss, divorce, shame, mental health', 'Safety plan and forgiveness without reconciliation'], 'Topics Most Won’t Talk About', 1, PURPLE, 'cross', 414)
    PAGES.append(dict(sec='Dividers', toc='Section Dividers', draw=divider_page('Dividers', d3, d4, dnote)))
    # --- extras
    raw('Memory Verse Cards', memory_cards, 'Memory Verse Cards')
    two('Declarations', decl_a, decl_b, 'Declarations')
    two('Help Is Real', help_a, help_b, 'Help Is Real (Resources)')
    two('Fast & Feast Tracker', fast_a, fast_b, 'Fast & Feast Tracker')
    for k, nm in [('verse', 'Verse Keeper'), ('decl', 'Declarations'), ('women', 'Women of the Word'), ('check', 'Check-Ins')]:
        raw('Bookmarks', bookmarks(k), 'Bookmarks')
    raw('Stickers', stickers_round, 'Stickers')
    raw('Stickers', stickers_labels, 'Stickers')
    raw('Stickers', stickers_flags, 'Stickers')
    two('Closing', closing_a, closing_b, 'Closing & Certificate')
    assert len(PAGES) == TOTAL, f'expected {TOTAL} pages, got {len(PAGES)}'
    # ranges
    order = []
    for i, pg in enumerate(PAGES, 1):
        SECTION_RANGES.setdefault(pg['sec'], [i, i])[1] = i
    for k, v in list(SECTION_RANGES.items()):
        SECTION_RANGES[k] = f'{v[0]}–{v[1]}' if v[0] != v[1] else f'{v[0]}'
    seen = {}
    for i, pg in enumerate(PAGES, 1):
        seen.setdefault(pg['toc'], [i, i])[1] = i
    for k, (a, b) in seen.items():
        TOC_ROWS.append((k, a, b))
    c = canvas.Canvas(OUT, pagesize=(PAGE_W, PAGE_H))
    c.setTitle('7HE H0LY R3UP Bible Study Inserts Bundle')
    c.setAuthor('7HE H0LY R3UP')
    c.setSubject('100 print-ready Bible study inserts')
    for i, pg in enumerate(PAGES, 1):
        pg['draw'](c, i)
        c.showPage()
    c.save()


SECTION_RANGES = {}


# ---- extra panels
def decl_a(p):
    p.header('Declarations', 'Truth I Can Stand On', 'Short, true, and mine. Say one aloud.', 15)
    items = [('I am allowed to rest.', 'Mark 6:31'), ('I am seen.', 'Genesis 16:13'), ('Mercy is new.', 'Lamentations 3:22–23'), ('I can ask for help.', 'Galatians 6:2'),
             ('I am not alone in the fire.', 'Isaiah 43:2'), ('My story is not over.', ps(118, '17')), ('I can take up space.', ps(18, '19')), ('God Almighty gets the glory.', ps(115, '1'))]
    for t, r in items:
        p.checks([t], 10.4, 0)
        p.c.setFillColor(GRAY); p.c.setFont('BodyI', 8.2)
        p.c.drawString(p.L + 15, p.cy - 7, r)
        p.cy -= 22
    p.note('Declarations are agreement with what God has said, not magic words, and not a replacement for care.', None, T_GOLD, 'BodyI', 8.4)


def decl_b(p):
    p.header('Declarations', 'Write My Own', 'Start with “I am,” “I can,” or “I will.”', 15)
    for i in range(6):
        p.field(f'{i + 1}. Declaration', 1)
        p.field('Because (Scripture ref + edition)', 1)
    p.soft('Say your favorite one out loud once.', 'Whisper it.')


def help_a(p):
    p.header('Help Is Real', 'Numbers to Keep (US)', 'Free, confidential, and made for this.', 15)
    rows = [('Emergency', '911'), ('988 Suicide & Crisis Lifeline', 'Call or text 988'), ('SAMHSA Helpline (treatment referral)', '1-800-662-4357'),
            ('National Domestic Violence Hotline', '1-800-799-7233 · text START to 88788'), ('RAINN Sexual Assault Hotline', '1-800-656-4673'),
            ('Crisis Text Line', 'Text HOME to 741741'), ('Childhelp National Child Abuse Hotline', '1-800-422-4453'), ('NAMI HelpLine', '1-800-950-6264')]
    for a, b in rows:
        p.c.setFillColor(TEAL); p.c.setFont('BodyB', 9.4); p.c.drawString(p.L, p.cy - 10, a)
        p.cy -= 13
        p.c.setFillColor(INK); p.c.setFont('Body', 9.4); p.c.drawString(p.L, p.cy - 8, b)
        p.cy -= 12
        p.c.setStrokeColor(LINE); p.c.setLineWidth(0.5); p.c.line(p.L, p.cy - 2, p.R, p.cy - 2)
        p.cy -= 8
    p.note('Outside the US: findahelpline.com lists services by country. Numbers change. Confirm before you rely on them.', None, T_GOLD, 'BodyI', 8.4)


def help_b(p):
    p.header('Help Is Real', 'My Local Numbers', 'Fill in while you are okay.', 15)
    p.field('Emergency number where I live', 1)
    p.field('Crisis line where I live', 1)
    p.field('My safe person 1 (name, number)', 1)
    p.field('My safe person 2 (name, number)', 1)
    p.field('My priest or pastor', 1)
    p.field('My doctor or therapist', 1)
    p.field('A place I can go if home is not safe', 2)
    p.field('A ride I can ask for', 1)
    p.soft('Put one number in your phone under a name only you would recognize.', 'Write one number here.')


def fast_a(p):
    p.header('Fast & Feast', 'Fast & Feast Tracker', 'Follow your priest’s guidance for your church’s calendar.', 15)
    c = p.c
    cols = 7
    cw = p.w / cols
    ch = 38
    p.need(5 * ch, 'fast grid')
    for r in range(5):
        for col in range(cols):
            d = r * 7 + col + 1
            x = p.L + col * cw
            y = p.cy - r * ch
            c.setStrokeColor(LINE); c.setFillColor(WHITE); c.setLineWidth(0.6)
            c.rect(x, y - ch, cw, ch, stroke=1, fill=1)
            if d <= 31:
                c.setFillColor(GRAY); c.setFont('Sans', 6.6); c.drawString(x + 3, y - 9, str(d))
    p.cy -= 5 * ch + 8
    p.para('Mark: F fast · + feast · P prayed · R rested', 'BodyI', 8.4, GRAY, after=4)
    p.field('Month and season', 1)
    p.field('What I am fasting from or for', 2)
    p.field('Prayer focus', 2)


def fast_b(p):
    p.header('Fast & Feast', 'Fasting Notes', None, 15)
    p.note('If you are pregnant or nursing, have a medical condition, take medication, or have ever struggled with disordered eating, talk with your doctor and your priest about how to adapt. Your worth is not measured by what you eat.', 'Care first', T_PEACH, 'Body', 8.6)
    p.field('What I noticed in my body', 3)
    p.field('What I noticed in my heart', 3)
    p.field('What I am thankful for', 3)
    p.field('How I broke the fast, and who I shared it with', 2)
    p.soft('Eat something kind to your body today. Thank God for it.', 'Say thanks once.')


def closing_a(p):
    p.header('Closing', 'Go Back With Truth and a Hand Out', None, 15)
    p.para('I’m Nikki, founder of 7HE H0LY R3UP—a survivor rebuilding through faith, with Big Boy, my American Bully service dog, beside me. I share lived experience, carefully sourced teaching, and practical steps for the next stretch of rebuilding.', 'Body', 9.4, after=6)
    p.para('If this meets you where you are, reach out through this page. Share only what feels safe. What step are you working on?', 'Body', 9.4, after=6)
    p.verify('Check both sides, including mine. Read the sources. Truth can withstand honest questions.')
    p.para('We survived. Now let’s go back—with truth and a hand out. Souls are attached to my obedience. God Almighty gets the glory.', 'BodyB', 10, TEAL, after=8)
    p.field('A closing prayer in my own words', 5)
    p.soft('Pick one insert from this bundle and put it in your Bible today.', 'Choose it. That counts.')


def closing_b(p):
    c = p.c
    cx = (p.L + p.R) / 2
    p.cy -= 4
    c.setStrokeColor(GOLD); c.setLineWidth(2.2)
    c.roundRect(p.L - 4, p.y0 + 52, p.w + 8, INS_H - 100, 10, stroke=1, fill=0)
    c.setStrokeColor(TURQ); c.setLineWidth(0.8)
    c.roundRect(p.L + 2, p.y0 + 58, p.w - 4, INS_H - 112, 8, stroke=1, fill=0)
    cross(c, cx, p.top - 76, 28, GOLD)
    tracked(c, cx, p.top - 118, 'CERTIFICATE OF COMPLETION', 'SansB', 8.6, TEAL, 2, 'c')
    c.setFillColor(TEAL); c.setFont('Head', 18); c.drawCentredString(cx, p.top - 148, 'You Showed Up')
    c.setFillColor(INK); c.setFont('BodyI', 10)
    c.drawCentredString(cx, p.top - 174, 'This certifies that')
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    c.line(p.L + 20, p.top - 206, p.R - 20, p.top - 206)
    c.drawCentredString(cx, p.top - 230, 'did the work of rebuilding, one honest page at a time.')
    c.setFont('Body', 9.6)
    c.drawCentredString(cx, p.top - 262, 'You survived. Now we rebuild.')
    c.line(p.L + 20, p.top - 330, p.L + 130, p.top - 330)
    c.line(p.R - 130, p.top - 330, p.R - 20, p.top - 330)
    c.setFont('Sans', 6.6); c.setFillColor(GRAY)
    c.drawCentredString(p.L + 75, p.top - 341, 'DATE')
    c.drawCentredString(p.R - 75, p.top - 341, 'SIGNATURE')
    p.cy = p.floor
    anchor(c, cx, p.top - 400, 40, TURQ, 2)
    broken_chain(c, cx - 60, p.top - 400, 18, GOLD)
    broken_chain(c, cx + 60, p.top - 400, 18, GOLD)
    tracked(c, cx, p.y0 + 70, 'GOD ALMIGHTY GETS THE GLORY', 'SansB', 6.4, TEAL, 1.6, 'c')


if __name__ == '__main__':
    build()
    for w in WARN:
        print('WARN', w)
    print('pages', len(PAGES), '->', OUT)
