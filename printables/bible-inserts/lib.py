"""Drawing helpers for the 7HE H0LY R3UP Bible Study Inserts bundle."""
import math
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit

LS = '/usr/share/fonts/truetype/liberation/'
DJ = '/usr/share/fonts/truetype/dejavu/'
for name, path in [
    ('Body', LS + 'LiberationSerif-Regular.ttf'),
    ('BodyB', LS + 'LiberationSerif-Bold.ttf'),
    ('BodyI', LS + 'LiberationSerif-Italic.ttf'),
    ('Sans', LS + 'LiberationSans-Regular.ttf'),
    ('SansB', LS + 'LiberationSans-Bold.ttf'),
    ('Head', DJ + 'DejaVuSerif-Bold.ttf'),
    ('Sym', DJ + 'DejaVuSans.ttf'),
]:
    pdfmetrics.registerFont(TTFont(name, path))

TURQ = HexColor('#1FA39F')
TEAL = HexColor('#0B5C61')
GOLD = HexColor('#D9A441')
PEACH = HexColor('#F4C7A1')
PINK = HexColor('#D77FA6')
PURPLE = HexColor('#8E5BB0')
DENIM = HexColor('#41607E')
IVORY = HexColor('#FBF5E9')
INK = HexColor('#262626')
GRAY = HexColor('#7A7A7A')
LINE = HexColor('#C4C4C4')
T_TURQ = HexColor('#E3F4F3')
T_PEACH = HexColor('#FCEBDD')
T_GOLD = HexColor('#FBF1DA')
WHITE = HexColor('#FFFFFF')

PAGE_W, PAGE_H = 792, 612          # US Letter landscape, points
INS_W, INS_H = 360, 540            # 5 x 7.5 in insert
WARN = []                          # overflow warnings
CUR = {'page': 0}


def lxx(n):
    """Chapter number of a Western Psalm in LXX / Greek-based numbering."""
    if n <= 8 or n >= 148:
        return str(n)
    if n in (9, 10):
        return '9'
    if 11 <= n <= 113:
        return str(n - 1)
    if n in (114, 115):
        return '113'
    if n == 116:
        return '114-115'
    if 117 <= n <= 146:
        return str(n - 1)
    if n == 147:
        return '146-147'


def ps(n, verses=''):
    v = (':' + verses) if verses else ''
    return f'Psalm {n}{v} (LXX {lxx(n)})'


def tracked(c, x, y, s, font, size, color, space=1.2, align='l'):
    c.setFillColor(color)
    w = pdfmetrics.stringWidth(s, font, size) + space * (len(s) - 1)
    if align == 'c':
        x -= w / 2
    elif align == 'r':
        x -= w
    t = c.beginText(x, y)
    t.setFont(font, size)
    t.setCharSpace(space)
    t.textOut(s)
    t.setCharSpace(0)
    c.drawText(t)


def cross(c, cx, cy, h, color, lw=None):
    w = h * 0.62
    t = h * 0.14
    c.setFillColor(color)
    c.rect(cx - t / 2, cy - h / 2, t, h, stroke=0, fill=1)
    c.rect(cx - w / 2, cy + h * 0.12 - t / 2, w, t, stroke=0, fill=1)


def sun(c, cx, cy, r, color, rays=12, lw=1.4):
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(lw)
    c.circle(cx, cy, r * 0.5, stroke=1, fill=0)
    for i in range(rays):
        a = math.pi * 2 * i / rays
        c.line(cx + math.cos(a) * r * 0.65, cy + math.sin(a) * r * 0.65,
               cx + math.cos(a) * r, cy + math.sin(a) * r)


def anchor(c, cx, cy, h, color, lw=2):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    top = cy + h / 2
    bot = cy - h / 2
    r = h * 0.09
    c.circle(cx, top - r, r, stroke=1, fill=0)
    c.line(cx, top - 2 * r, cx, bot)
    c.line(cx - h * 0.2, top - h * 0.3, cx + h * 0.2, top - h * 0.3)
    c.arc(cx - h * 0.32, bot, cx + h * 0.32, bot + h * 0.5, 200, 140)


def broken_chain(c, cx, cy, s, color, lw=2.2):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    for dx, ang in ((-s * 0.55, 28), (s * 0.55, -28)):
        c.saveState()
        c.translate(cx + dx, cy)
        c.rotate(ang)
        c.roundRect(-s * 0.42, -s * 0.2, s * 0.84, s * 0.4, s * 0.2, stroke=1, fill=0)
        c.restoreState()
    for k in (-1, 1):
        c.line(cx - s * 0.02, cy + k * s * 0.34, cx + s * 0.02, cy + k * s * 0.52)


def heart(c, cx, cy, s, color):
    c.setFillColor(color)
    p = c.beginPath()
    p.moveTo(cx, cy - s * 0.6)
    p.curveTo(cx - s * 1.2, cy + s * 0.1, cx - s * 0.5, cy + s * 0.9, cx, cy + s * 0.35)
    p.curveTo(cx + s * 0.5, cy + s * 0.9, cx + s * 1.2, cy + s * 0.1, cx, cy - s * 0.6)
    c.drawPath(p, stroke=0, fill=1)


def wrap(s, font, size, w):
    return simpleSplit(s, font, size, w)


class Panel:
    """A 5 x 7.5 in insert drawn top-down. (x, y) = lower-left corner."""
    M = 24

    def __init__(self, c, x, y, tag=''):
        self.c, self.x, self.y0 = c, x, y
        self.top = y + INS_H
        self.cy = self.top - 28
        self.tag = tag
        self.L = x + self.M
        self.R = x + INS_W - self.M
        self.w = self.R - self.L
        self.floor = y + 30
        self.stitch()

    # ---- frame ------------------------------------------------------------
    def stitch(self):
        c = self.c
        c.setStrokeColor(TURQ)
        c.setLineWidth(0.9)
        c.setDash(1.2, 3)
        c.roundRect(self.x + 8, self.y0 + 8, INS_W - 16, INS_H - 16, 9, stroke=1, fill=0)
        c.setDash()
        tracked(c, self.x + INS_W / 2, self.y0 + 14, '7HE H0LY R3UP', 'SansB', 5.8, TURQ, 1.6, 'c')

    def room(self):
        return self.cy - self.floor

    def need(self, h, what=''):
        if self.cy - h < self.floor:
            WARN.append(f'p{CUR["page"]} [{self.tag}] overflow by {self.floor - (self.cy - h):.0f}pt at "{what}"')

    # ---- text -------------------------------------------------------------
    def header(self, kicker, title, sub=None, size=16):
        c = self.c
        tracked(c, self.L, self.cy, kicker.upper(), 'SansB', 7, GOLD, 1.3)
        self.cy -= 17
        for ln in wrap(title, 'Head', size, self.w):
            c.setFillColor(TEAL)
            c.setFont('Head', size)
            c.drawString(self.L, self.cy, ln)
            self.cy -= size + 3
        c.setStrokeColor(GOLD)
        c.setLineWidth(2)
        c.line(self.L, self.cy + 1, self.L + 38, self.cy + 1)
        self.cy -= 10
        if sub:
            self.para(sub, 'BodyI', 9.3, GRAY, after=6)

    def para(self, s, font='Body', size=9.4, color=INK, lead=None, indent=0, after=5):
        lead = lead or size * 1.25
        lines = wrap(s, font, size, self.w - indent)
        self.need(len(lines) * lead + after, s[:30])
        self.c.setFillColor(color)
        self.c.setFont(font, size)
        for ln in lines:
            self.c.drawString(self.L + indent, self.cy - size * 0.85, ln)
            self.cy -= lead
        self.cy -= after

    def label(self, s, color=TEAL):
        self.need(14, s)
        tracked(self.c, self.L, self.cy - 6, s.upper(), 'SansB', 6.8, color, 1.0)
        self.cy -= 11

    def lines(self, n, gap=16.5, dotted=False):
        c = self.c
        self.need(n * gap, 'lines')
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        if dotted:
            c.setDash(1, 2.5)
        for _ in range(n):
            self.cy -= gap
            c.line(self.L, self.cy, self.R, self.cy)
        c.setDash()
        self.cy -= 3

    def field(self, label, n=2, gap=16.5):
        self.label(label)
        self.lines(n, gap)

    def gap(self, h=6):
        self.cy -= h

    def box(self, label, h, fill=None, x=None, w=None, cy=None, stroke=LINE, advance=True):
        c = self.c
        x = self.L if x is None else x
        w = self.w if w is None else w
        top = self.cy if cy is None else cy
        self.need(h, label)
        if fill:
            c.setFillColor(fill)
        c.setStrokeColor(stroke)
        c.setLineWidth(0.7)
        c.roundRect(x, top - h, w, h, 5, stroke=1, fill=1 if fill else 0)
        if label:
            tracked(c, x + 6, top - 10, label.upper(), 'SansB', 6.2, TEAL, 0.9)
        if advance:
            self.cy -= h + 6

    def cols(self, labels, h, n=None, gap=6):
        """Row of labelled boxes."""
        n = n or len(labels)
        w = (self.w - gap * (n - 1)) / n
        self.need(h, labels[0])
        top = self.cy
        for i, lab in enumerate(labels):
            self.box(lab, h, x=self.L + i * (w + gap), w=w, cy=top, advance=False)
        self.cy -= h + 6

    def note(self, s, title=None, fill=T_PEACH, font='BodyI', size=8.8):
        lines = wrap(s, font, size, self.w - 16)
        h = len(lines) * size * 1.25 + 12 + (10 if title else 0)
        self.need(h, 'note')
        c = self.c
        c.setFillColor(fill)
        c.setStrokeColor(fill)
        c.roundRect(self.L, self.cy - h, self.w, h, 5, stroke=0, fill=1)
        y = self.cy - 8
        if title:
            tracked(c, self.L + 8, y - 2, title.upper(), 'SansB', 6.4, TEAL, 0.9)
            y -= 10
        c.setFillColor(INK)
        c.setFont(font, size)
        for ln in lines:
            c.drawString(self.L + 8, y - size * 0.8, ln)
            y -= size * 1.25
        self.cy -= h + 6

    def checks(self, items, size=9.2, gap=4):
        c = self.c
        for it in items:
            lines = wrap(it, 'Body', size, self.w - 16)
            self.need(len(lines) * size * 1.25 + gap, it[:20])
            c.setFillColor(TURQ)
            c.setFont('Sym', size + 1)
            c.drawString(self.L, self.cy - size * 0.9, '☐')
            c.setFillColor(INK)
            c.setFont('Body', size)
            for ln in lines:
                c.drawString(self.L + 15, self.cy - size * 0.85, ln)
                self.cy -= size * 1.25
            self.cy -= gap

    def hchecks(self, items, size=8.8):
        c = self.c
        x = self.L
        y = self.cy - size - 1
        for it in items:
            w = pdfmetrics.stringWidth(it, 'Body', size)
            c.setFillColor(TURQ)
            c.setFont('Sym', size + 1)
            c.drawString(x, y, '\u2610')
            c.setFillColor(INK)
            c.setFont('Body', size)
            c.drawString(x + 14, y, it)
            x += 14 + w + 14
        self.cy -= size + 12

    def bullets(self, items, size=9.2, gap=3, color=INK):
        c = self.c
        for it in items:
            lines = wrap(it, 'Body', size, self.w - 12)
            self.need(len(lines) * size * 1.25 + gap, it[:20])
            c.setFillColor(GOLD)
            c.circle(self.L + 3, self.cy - size * 0.45, 1.7, stroke=0, fill=1)
            c.setFillColor(color)
            c.setFont('Body', size)
            for ln in lines:
                c.drawString(self.L + 12, self.cy - size * 0.85, ln)
                self.cy -= size * 1.25
            self.cy -= gap

    def soft(self, step, low='Hold this page and breathe once. That counts.'):
        self.note(step + '  Low-energy option: ' + low, 'Soft step · 10 minutes or less', T_TURQ, 'Body', 8.8)

    def verify(self, s='Check both sides, including mine. Read the source. Truth can withstand honest questions.'):
        self.note(s, None, T_GOLD, 'BodyI', 8.2)

    def fill_notes(self):
        r = self.room() - 6
        if r > 52:
            self.label('Notes')
            self.lines(int((self.room() - 6) / 16.5), dotted=True)

    def soft_h(self, step, low='Hold this page and breathe once. That counts.'):
        lines = wrap(step + '  Low-energy option: ' + low, 'Body', 8.8, self.w - 16)
        return len(lines) * 8.8 * 1.25 + 12 + 10 + 6

    def soap(self, ref=None, weights=(3, 4, 3, 3), reserve=0):
        c = self.c
        parts = [('S', 'Scripture', 'Write or paste the verse. Cite edition + book, chapter, verse.'),
                 ('O', 'Observation', 'What does it say? Who, what, where? What word stands out?'),
                 ('A', 'Application', 'One step. Small is real. What will I do today?'),
                 ('P', 'Prayer', 'Talk to God as you are. Short and honest counts.')]
        total_h = self.room() - reserve
        unit = total_h / sum(weights)
        for (ltr, name, hint), wgt in zip(parts, weights):
            start = self.cy
            h = unit * wgt
            c.setFillColor(TURQ)
            c.circle(self.L + 8, self.cy - 8, 8, stroke=0, fill=1)
            c.setFillColor(WHITE)
            c.setFont('Head', 9)
            c.drawCentredString(self.L + 8, self.cy - 11, ltr)
            tracked(c, self.L + 22, self.cy - 6, name.upper(), 'SansB', 7.4, TEAL, 1.1)
            self.cy -= 14
            if ltr == 'S' and ref:
                c.setFillColor(TEAL)
                c.setFont('BodyB', 9.4)
                c.drawString(self.L + 22, self.cy - 8, ref)
            else:
                c.setFillColor(GRAY)
                c.setFont('BodyI', 7.6)
                c.drawString(self.L + 22, self.cy - 7, hint)
            self.cy -= 12
            n = max(1, int((h - 26 - 4) / 16.5))
            self.lines(n)
            self.cy = min(self.cy, start - 26 - n * 16.5 - 3)
            self.cy = start - h


def circle_scale(p, label, lo, hi, n=5):
    c = p.c
    p.label(label)
    step = p.w / (n - 1)
    y = p.cy - 12
    c.setStrokeColor(LINE)
    c.line(p.L, y, p.R, y)
    for i in range(n):
        c.setFillColor(WHITE)
        c.setStrokeColor(TURQ)
        c.circle(p.L + i * step, y, 5.5, stroke=1, fill=1)
        c.setFillColor(GRAY)
        c.setFont('Sans', 6.5)
        c.drawCentredString(p.L + i * step, y - 2.2, str(i + 1))
    c.setFont('BodyI', 7.6)
    c.setFillColor(GRAY)
    c.drawString(p.L, y - 17, lo)
    c.drawRightString(p.R, y - 17, hi)
    p.cy -= 36
