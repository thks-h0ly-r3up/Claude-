#!/usr/bin/env python3
"""Builds the 9-page A5 "Shattering Chains" printable kit.

Outputs:
  public/shattering-chains-7-day-kit.pdf   (served by the landing page)
  content/kit-copy.md                      (all kit copy, for Canva / editing)

Usage:
  APP_URL="https://your-app.example/download" python3 tools/build_kit.py
The Page 9 QR code encodes APP_URL (default: https://example.com/app).
Scripture is the King James Version (public domain).
"""
import math
import os
import random

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A5
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_PATH = os.path.join(ROOT, "public", "shattering-chains-7-day-kit.pdf")
MD_PATH = os.path.join(ROOT, "content", "kit-copy.md")
APP_URL = os.environ.get("APP_URL", "https://example.com/app")

W, H = A5  # 419.5 x 595.3 pt
M = 26  # page margin

NIGHT = HexColor("#0B1320")
INK = HexColor("#111827")
ORANGE = HexColor("#FF6B1A")
GOLD = HexColor("#FFB833")
CREAM = HexColor("#F6EFE0")
OLIVE = HexColor("#4B5320")
OLIVE_D = HexColor("#2E3512")
OLIVE_L = HexColor("#6B7A3A")
KHAKI = HexColor("#8A7B4F")
WHITE = HexColor("#FFFFFF")

DAYS = [
    {
        "title": "SIS, THE CHAIN WON'T BREAK ITSELF",
        "ref": "John 8:36",
        "verse": "If the Son therefore shall make you free, ye shall be free indeed.",
        "breakdown": "Girl, you have been swinging at this chain with your own two hands, and you're exhausted. New start, new plan, new promise to yourself. Same cell. Jesus doesn't say you might get free. He says \"free indeed\" - not free-ish, not free on your good days. Today isn't about trying harder, beautiful. It's about handing Him the key and letting Him do what only He can.",
        "habits": ["Read the verse out loud, twice", "Named ONE chain in writing (the real one)", "5 quiet minutes, phone in another room", "Told one safe sister I'm starting this"],
        "vault": "What chain have I been calling \"just how I am\"? Who taught me to carry it, and what has it cost my heart?",
        "prayer": "Jesus, I'm so tired of pretending I'm fine. I've been fighting this chain alone and it's still on me. Today I lay down the fight and pick up Your hand. You said the Son makes free, so make me free. Take the key. Start breaking it now. In Your name, amen.",
    },
    {
        "title": "OUT OF THE DARK, NO MORE HIDING",
        "ref": "Psalm 107:14",
        "verse": "He brought them out of darkness and the shadow of death, and brake their bands in sunder.",
        "breakdown": "Look at who does the work: HE brought them out. HE broke the bands. The dark you've been sitting in - the numbing, the 3 a.m. spiral, the smile you put on for everybody - is not your forever address. God isn't waiting for you to clean yourself up first. He walks right in, and the bands snap. Your part today, love: stop hiding the dark from the One who already sees it and loves you anyway.",
        "habits": ["Read the verse out loud, twice", "Said out loud where I'm stuck in the dark", "Deleted or blocked ONE trigger", "10 minutes walking, praying as I go"],
        "vault": "Where do I go to hide when it gets heavy? What am I afraid will happen if the light hits that place?",
        "prayer": "Father, You see the dark I've been sitting in, and I'm not hiding it anymore. Walk into that room and turn the light on. Break the bands I can't break. Pull me out of every place I keep running back to. I'm not bargaining anymore, I'm asking. Hold me while You do it. Amen.",
    },
    {
        "title": "REWRITE THE STORY IN YOUR HEAD",
        "ref": "Romans 12:2",
        "verse": "And be not conformed to this world: but be ye transformed by the renewing of your mind, that ye may prove what is that good, and acceptable, and perfect, will of God.",
        "breakdown": "Every cycle starts as a thought you believed. \"I'll never change.\" \"I'm too much.\" \"Nobody would choose me.\" Lies on repeat start to feel like truth. Transformation isn't a mood, sis, it's renewal - trading the old script for God's words one thought at a time. Catch the lie, say what He says, repeat. Do it until the old voice goes quiet and hers - the real you - gets loud.",
        "habits": ["Read the verse out loud, twice", "Caught 3 lies today and wrote them down", "Answered each lie with a verse or truth", "Cut ONE input feeding the old script"],
        "vault": "Write the three loudest lies in my head. Next to each, write what God actually says about me, His daughter.",
        "prayer": "Father, my mind has been playing old tapes for years. I renounce every lie I've agreed with. Renew my mind, God. Rewrite what my past and my pain wrote over me. Let me see myself the way You do: chosen, cherished, already free. Amen.",
    },
    {
        "title": "DROP ANCHOR WHEN THE STORM HITS",
        "ref": "Hebrews 6:19",
        "verse": "Which hope we have as an anchor of the soul, both sure and stedfast, and which entereth into that within the veil;",
        "breakdown": "Storms don't ask if you're ready. The old you reaches for the drink, the phone, the ex, the shutdown. An anchor doesn't stop the storm - it keeps you from drifting onto the rocks. Hope in Christ is that anchor: sure and steadfast. So decide BEFORE the storm hits what you'll do when it does. Have your anchor move ready: a verse, a call to your girl, a prayer out loud.",
        "habits": ["Read the verse out loud, twice", "Wrote my 'storm plan' (3 steps)", "Prayed it at my hardest hour of the day", "Texted my anchor sister a check-in"],
        "vault": "What are the 3 moments the storm hits me hardest? What will I do the second it starts?",
        "prayer": "Jesus, You are my anchor. When the storm hits and everything in me wants to run, hold me steady. Keep me from drifting back into what nearly sank me. I'm planting my hope in You, sure and steadfast. I'm not going anywhere. Amen.",
    },
    {
        "title": "SAY IT OUT LOUD. SHAME LOSES.",
        "ref": "1 John 1:9",
        "verse": "If we confess our sins, he is faithful and just to forgive us our sins, and to cleanse us from all unrighteousness.",
        "breakdown": "Secrets are a chain's favorite meal. Shame whispers stay quiet, girl; God says bring it into the light and I'll make you clean. Confession isn't groveling, it's agreeing with the truth so He can do what He promised. Faithful AND just: it's already paid for at the cross. So say it. Then walk out lighter, not carrying it right back in.",
        "habits": ["Read the verse out loud, twice", "Confessed the real thing to God, in detail", "Confessed to one trusted sister in Christ", "Forgave one person (or started to)"],
        "vault": "What have I never said out loud to anyone? What would it feel like to be fully known and still fully loved?",
        "prayer": "God, here it is - everything I've been hiding. No excuses, no editing. I agree with You that it's sin and I'm done carrying it. You said You're faithful and just to forgive, so I receive it. Wash me clean, and don't let shame pull me back. Amen.",
    },
    {
        "title": "SUIT UP, DAUGHTER OF THE KING",
        "ref": "Ephesians 6:11",
        "verse": "Put on the whole armour of God, that ye may be able to stand against the wiles of the devil.",
        "breakdown": "The enemy doesn't play fair and he doesn't take days off. Wiles means schemes - he knows your patterns and your soft spots. But you don't stand in your own strength, love, you stand dressed: truth, righteousness, peace, faith, salvation, the Word. The whole armour, not half. Today you get dressed on purpose, before the fight finds you.",
        "habits": ["Read the verse out loud, twice", "Prayed on each piece of armour by name", "Named the enemy's favorite scheme on me", "Did ONE hard thing I'd normally dodge"],
        "vault": "Where does the enemy always come at me? Which piece of armour am I leaving off right there?",
        "prayer": "Lord, I'm suiting up. Truth around my waist, righteousness on my chest, peace on my feet, faith as my shield, salvation on my head, Your Word in my hand. I know the schemes and I'm not falling for them. I stand in You, not in me. Amen.",
    },
    {
        "title": "NEW SUN, NEW MERCY",
        "ref": "Lamentations 3:22-23",
        "verse": "It is of the LORD'S mercies that we are not consumed, because his compassions fail not. They are new every morning: great is thy faithfulness.",
        "breakdown": "Seven days, sis. And if you stumbled somewhere in there, you're still here, and that's mercy. God's compassions don't run out or expire overnight. Every sunrise is a fresh receipt marked PAID. Freedom isn't one perfect week, it's coming back to Him every morning. The sun is up. Get up with it, wipe your face, and keep walking.",
        "habits": ["Read the verse out loud, twice", "Greeted the sunrise with a prayer", "Wrote 3 wins from this week", "Committed to the next 30 days"],
        "vault": "What has changed in me since Day 1? What do I want the next 30 days to look like?",
        "prayer": "Faithful God, thank You for seven days and every mercy that showed up new. I'm not perfect, but I'm Yours. Keep breaking what's left of these chains. Every morning I'll come back to You. The sun's up, and so am I. Amen.",
    },
]

PAYOUT_HEADLINE = ("Ready to track your 30-day journey daily? Scan here to unlock the full "
                   "Interactive Map, Private Prayer Vault, and Daily Audio Devotionals "
                   "inside the custom app.")


# ---------- drawing helpers ----------
def text_block(c, text, x, y, width, font="Helvetica", size=9, leading=None, color=INK):
    """Draw wrapped text with top at y; return the y below the block."""
    leading = leading or size * 1.32
    c.setFillColor(color)
    c.setFont(font, size)
    for line in simpleSplit(text, font, size, width):
        y -= leading
        c.drawString(x, y, line)
    return y


def text_height(text, width, font, size, leading=None):
    leading = leading or size * 1.32
    return len(simpleSplit(text, font, size, width)) * leading


def centered_block(c, text, cx, y, width, font, size, color, leading=None):
    leading = leading or size * 1.3
    c.setFillColor(color)
    c.setFont(font, size)
    for line in simpleSplit(text, font, size, width):
        y -= leading
        c.drawCentredString(cx, y, line)
    return y


def camo(c, x, y, w, h, seed=7, base=OLIVE, blobs=None):
    """Camouflage panel clipped to the given rect."""
    rnd = random.Random(seed)
    blobs = blobs or [OLIVE_D, OLIVE_L, KHAKI, NIGHT]
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, w, h)
    c.clipPath(p, stroke=0, fill=0)
    c.setFillColor(base)
    c.rect(x, y, w, h, stroke=0, fill=1)
    count = max(18, int(w * h / 2600))
    for _ in range(count):
        col = rnd.choice(blobs)
        bx = x + rnd.random() * w
        by = y + rnd.random() * h
        r = 10 + rnd.random() * 26
        c.setFillColor(col)
        pts = []
        n = 9
        for i in range(n):
            a = 2 * math.pi * i / n
            rr = r * (0.55 + rnd.random() * 0.7)
            pts.append((bx + rr * math.cos(a) * 1.5, by + rr * math.sin(a)))
        path = c.beginPath()
        path.moveTo(*pts[0])
        for i in range(n):
            p1 = pts[i]
            p2 = pts[(i + 1) % n]
            mid = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
            path.curveTo(p1[0], p1[1], p1[0], p1[1], mid[0], mid[1])
        path.close()
        c.drawPath(path, stroke=0, fill=1)
    c.restoreState()


def anchor(c, cx, cy, size, color=CREAM, lw=None):
    """Vector anchor centered at (cx, cy), roughly `size` tall."""
    s = size / 100.0
    lw = lw or max(1.5, 5 * s)
    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(lw)
    c.setLineCap(1)
    c.setLineJoin(1)
    top = cy + 50 * s
    # ring
    c.circle(cx, top - 8 * s, 8 * s, stroke=1, fill=0)
    # shank
    c.line(cx, top - 16 * s, cx, cy - 42 * s)
    # stock (crossbar)
    c.line(cx - 22 * s, top - 28 * s, cx + 22 * s, top - 28 * s)
    # curved arms
    p = c.beginPath()
    p.moveTo(cx - 40 * s, cy - 14 * s)
    p.curveTo(cx - 36 * s, cy - 52 * s, cx - 12 * s, cy - 50 * s, cx, cy - 42 * s)
    p.curveTo(cx + 12 * s, cy - 50 * s, cx + 36 * s, cy - 52 * s, cx + 40 * s, cy - 14 * s)
    c.drawPath(p, stroke=1, fill=0)
    # flukes
    for sign in (-1, 1):
        fx = cx + sign * 40 * s
        fy = cy - 14 * s
        tri = c.beginPath()
        tri.moveTo(fx, fy + 8 * s)
        tri.lineTo(fx + sign * 10 * s, fy - 8 * s)
        tri.lineTo(fx - sign * 8 * s, fy - 6 * s)
        tri.close()
        c.drawPath(tri, stroke=0, fill=1)
    c.restoreState()


def sunrise(c, cx, cy, radius, rays=22, ray_len=None, core=ORANGE, glow=GOLD, ray_color=GOLD):
    """Half sun over a horizon line at y=cy."""
    ray_len = ray_len or radius * 1.9
    c.saveState()
    p = c.beginPath()
    p.rect(cx - 2000, cy, 4000, 2000)
    c.clipPath(p, stroke=0, fill=0)
    c.setStrokeColor(ray_color)
    c.setLineWidth(3)
    for i in range(rays + 1):
        a = math.pi * i / rays
        c.line(cx + math.cos(a) * radius * 1.15, cy + math.sin(a) * radius * 1.15,
               cx + math.cos(a) * (radius + ray_len), cy + math.sin(a) * (radius + ray_len))
    c.setFillColor(glow)
    c.circle(cx, cy, radius * 1.08, stroke=0, fill=1)
    c.setFillColor(core)
    c.circle(cx, cy, radius * 0.86, stroke=0, fill=1)
    c.restoreState()


def chevron_divider(c, x, y, w, color=ORANGE, h=6, step=14):
    c.saveState()
    c.setFillColor(color)
    cx = x
    while cx + step <= x + w:
        p = c.beginPath()
        p.moveTo(cx, y)
        p.lineTo(cx + step / 2, y + h)
        p.lineTo(cx + step, y)
        p.lineTo(cx + step / 2, y + h * 0.35)
        p.close()
        c.drawPath(p, stroke=0, fill=1)
        cx += step
    c.restoreState()


def checkbox(c, x, y, size=9, color=INK):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(1.4)
    c.rect(x, y, size, size, stroke=1, fill=0)
    c.restoreState()


def label(c, text, x, y, color=ORANGE, size=7.5):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", size)
    c.drawString(x, y, text.upper())


# ---------- pages ----------
def page_cover(c):
    c.setFillColor(NIGHT)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    # sky gradient bands
    bands = ["#1B2440", "#3A2A4A", "#7A3B3B", "#C2571F", "#FF8A2B"]
    band_h = 34
    top_y = 300
    for i, hx in enumerate(bands):
        c.setFillColor(HexColor(hx))
        c.rect(0, top_y - (i + 1) * band_h + band_h * 0, W, band_h, stroke=0, fill=1)
    # fill area behind sun
    c.setFillColor(HexColor("#1B2440"))
    c.rect(0, top_y, W, H - top_y - 0, stroke=0, fill=1)
    # rebuild sky ordered top->bottom above horizon
    horizon = 240
    sky = ["#0B1320", "#1B2440", "#3A2A4A", "#7A3B3B", "#C2571F", "#FF8A2B"]
    seg = (H - horizon) / len(sky)
    for i, hx in enumerate(sky):
        c.setFillColor(HexColor(hx))
        c.rect(0, H - (i + 1) * seg, W, seg + 1, stroke=0, fill=1)
    sunrise(c, W / 2, horizon, 74, rays=26, ray_len=190)
    # camo ground
    camo(c, 0, 0, W, horizon, seed=11)
    c.setFillColor(ORANGE)
    c.rect(0, horizon - 3, W, 5, stroke=0, fill=1)
    # anchor over the sun
    anchor(c, W / 2, horizon + 46, 88, color=NIGHT, lw=6)
    # title panel
    c.setFillColor(NIGHT)
    c.rect(M - 6, 78, W - 2 * M + 12, 130, stroke=0, fill=1)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.rect(M - 6, 78, W - 2 * M + 12, 130, stroke=1, fill=0)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(W / 2, 190, "7-DAY  A5  BIBLE INSERT KIT")
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(W / 2, 152, "SHATTERING")
    c.setFillColor(ORANGE)
    c.drawCentredString(W / 2, 112, "CHAINS")
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(W / 2, 90, "RAW TRUTH.  REAL PRAYER.  REAL FREEDOM.")
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(W / 2, 40, "Print at 100% on A5 (148 x 210 mm). Fold or trim to tuck inside your Bible.")
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(W / 2, 26, "\"If the Son therefore shall make you free, ye shall be free indeed.\"  John 8:36")
    c.showPage()


def page_day(c, n, d):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    # header band
    hh = 64
    camo(c, 0, H - hh, W, hh, seed=20 + n)
    c.setFillColor(ORANGE)
    c.rect(0, H - hh - 4, W, 4, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(M, H - 20, "DAY %d OF 7" % n)
    anchor(c, W - M - 12, H - hh / 2, 38, color=CREAM, lw=2.4)
    title_font, title_size = "Helvetica-Bold", 17
    lines = simpleSplit(d["title"], title_font, title_size, W - 2 * M - 40)
    c.setFillColor(CREAM)
    c.setFont(title_font, title_size)
    ty = H - 40
    for ln in lines:
        c.drawString(M, ty, ln)
        ty -= 19

    y = H - hh - 14
    cw = W - 2 * M

    # core scripture
    label(c, "Core Scripture", M, y - 8)
    verse = "\"%s\"" % d["verse"]
    vh = text_height(verse, cw - 14, "Helvetica-BoldOblique", 9.5, 12.5)
    box_h = vh + 26
    c.setFillColor(WHITE)
    c.rect(M, y - 14 - box_h, cw, box_h, stroke=0, fill=1)
    c.setFillColor(ORANGE)
    c.rect(M, y - 14 - box_h, 4, box_h, stroke=0, fill=1)
    yy = text_block(c, verse, M + 12, y - 14 - 2, cw - 20, "Helvetica-BoldOblique", 9.5, 12.5, INK)
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M + 12, yy - 12, "- " + d["ref"].upper() + " (KJV)")
    y = y - 14 - box_h - 10

    # breakdown
    label(c, "The Breakdown", M, y - 6)
    y = text_block(c, d["breakdown"], M, y - 8, cw, "Helvetica", 8.4, 10.8, INK) - 6

    chevron_divider(c, M, y - 6, cw, ORANGE, 5, 12)
    y -= 12

    # tracker
    label(c, "Interactive Action Tracker", M, y - 8)
    y -= 14
    col_w = cw / 2 - 4
    for i, item in enumerate(d["habits"]):
        cx = M + (i % 2) * (col_w + 8)
        cy = y - (i // 2) * 24
        checkbox(c, cx, cy - 9, 8)
        block_bottom = text_block(c, item, cx + 13, cy + 1, col_w - 14, "Helvetica", 7.6, 9)
    y -= 2 * 24 + 2
    # prayer minutes + chain weight
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 7.4)
    c.drawString(M, y - 8, "PRAYER MINUTES:")
    px = M + 78
    for m in ("5", "10", "15", "20+"):
        checkbox(c, px, y - 10, 8)
        c.setFont("Helvetica", 7.4)
        c.drawString(px + 11, y - 8.5, m)
        px += 34 if m != "20+" else 0
    c.setFont("Helvetica-Bold", 7.4)
    c.drawString(M, y - 24, "CHAIN WEIGHT 1-10:")
    c.setFont("Helvetica", 7.4)
    c.drawString(M + 84, y - 24, "Before")
    c.setStrokeColor(INK)
    c.setLineWidth(1)
    c.circle(M + 116, y - 21.5, 6, stroke=1, fill=0)
    c.drawString(M + 128, y - 24, "After")
    c.circle(M + 154, y - 21.5, 6, stroke=1, fill=0)
    c.drawString(M + 170, y - 24, "Mood:")
    mx = M + 194
    for face in (":(", ":|", ":)"):
        c.circle(mx + 6, y - 21.5, 6, stroke=1, fill=0)
        c.drawCentredString(mx + 6, y - 24, face)
        mx += 17
    y -= 34

    # vault prompt
    label(c, "The Vault Prompt (private)", M, y - 6)
    vp = d["vault"]
    y = text_block(c, vp, M, y - 8, cw, "Helvetica-Oblique", 8.4, 10.8, INK) - 2
    prayer_top = 132
    ly = y - 9
    c.setStrokeColor(HexColor("#B9AE93"))
    c.setLineWidth(0.6)
    while ly > prayer_top + 10:
        c.line(M, ly, W - M, ly)
        ly -= 11

    # prayer panel
    c.setFillColor(NIGHT)
    c.rect(0, 0, W, prayer_top, stroke=0, fill=1)
    c.setFillColor(ORANGE)
    c.rect(0, prayer_top, W, 4, stroke=0, fill=1)
    label(c, "Daily Street-Worded Prayer", M, prayer_top - 18, GOLD, 8)
    text_block(c, d["prayer"], M, prayer_top - 20, cw - 6, "Helvetica-Bold", 8.4, 10.8, CREAM)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 6.8)
    c.drawString(M, 12, "SHATTERING CHAINS  |  DAY %d / 7" % n)
    anchor(c, W - M - 8, 18, 18, color=GOLD, lw=1.4)
    c.showPage()


def page_payout(c):
    c.setFillColor(NIGHT)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    sunrise(c, W / 2, H - 92, 42, rays=20, ray_len=90)
    anchor(c, W / 2, H - 92 + 22, 40, color=NIGHT, lw=3)
    c.setFillColor(ORANGE)
    c.rect(0, H - 94, W, 3, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(W / 2, H - 128, "THE PAYOUT GATEWAY  -  PAGE 9")
    chevron_divider(c, W / 2 - 70, H - 140, 140, ORANGE, 7, 14)
    yy = centered_block(c, "READY TO TRACK YOUR", W / 2, H - 146, W - 2 * M, "Helvetica-Bold", 20, CREAM, 23)
    yy = centered_block(c, "30-DAY JOURNEY DAILY?", W / 2, yy, W - 2 * M, "Helvetica-Bold", 20, ORANGE, 23)
    yy = centered_block(c, "Scan here to unlock the full Interactive Map, Private Prayer Vault, and Daily Audio Devotionals inside the custom app.",
                        W / 2, yy - 6, W - 2 * M - 10, "Helvetica-Bold", 10.5, CREAM, 14)
    # QR
    qr_size = 170
    qx = (W - qr_size) / 2
    qy = yy - 22 - qr_size
    c.setFillColor(GOLD)
    c.rect(qx - 12, qy - 12, qr_size + 24, qr_size + 24, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.rect(qx - 6, qy - 6, qr_size + 12, qr_size + 12, stroke=0, fill=1)
    widget = QrCodeWidget(APP_URL)
    b = widget.getBounds()
    bw, bh = b[2] - b[0], b[3] - b[1]
    d = Drawing(qr_size, qr_size, transform=[qr_size / bw, 0, 0, qr_size / bh, 0, 0])
    d.add(widget)
    renderPDF.draw(d, c, qx, qy)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(W / 2, qy - 30, "SCAN HERE")
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 8)
    c.drawCentredString(W / 2, qy - 44, "Camera on. Point. Tap the link. Keep going.")
    c.setFont("Helvetica", 7)
    c.drawCentredString(W / 2, qy - 56, APP_URL)
    # price strip
    camo(c, 0, 0, W, 54, seed=9)
    c.setFillColor(NIGHT)
    c.rect(M, 12, W - 2 * M, 30, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(W / 2, 30, "FULL APP ACCESS  |  $5 - $12 / MONTH  |  CANCEL ANYTIME")
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 7)
    c.drawCentredString(W / 2, 19, "Live Interactive Map  -  Tracker  -  Private Prayer Vault  -  Daily Audio")
    c.showPage()


# ---------- markdown export ----------
def write_markdown():
    out = ["# SHATTERING CHAINS - 7-Day A5 Bible Insert Kit (copy deck)", "",
           "Generated by `tools/build_kit.py` - single source of truth for the PDF. Scripture: KJV (public domain).", "",
           "## Design system (Canva / PDF)", "",
           "- **Page size:** A5 portrait, 148 x 210 mm, 3 mm bleed if printing commercially.",
           "- **Palette:** Night `#0B1320` - Sunrise Orange `#FF6B1A` - Gold `#FFB833` - Cream `#F6EFE0` - Camo Olive `#4B5320` / `#2E3512` / `#6B7A3A` / `#8A7B4F`.",
           "- **Type:** Headlines Helvetica/Inter Black, all caps. Body Inter/Helvetica 8.5 pt. Prayer panel bold cream on Night.",
           "- **Motifs:** half-sun with rays (sunrise), anchor icon in header + footer, camouflage panels for header band and cover ground, chevron dividers.",
           "", "## Page 1 - Cover", "",
           "- Sky gradient Night to Orange, half sun with rays on the horizon, camo ground, large anchor over the sun.",
           "- Title panel: `7-DAY A5 BIBLE INSERT KIT` / **SHATTERING** / **CHAINS** / `RAW TRUTH. REAL PRAYER. ZERO CYCLES.`",
           "- Footer verse: John 8:36.", ""]
    for i, d in enumerate(DAYS, 1):
        out += ["## Page %d - Day %d: %s" % (i + 1, i, d["title"]), "",
                "**Layout:** camo header band with day label + title + anchor; cream body; white scripture box with orange left bar; chevron divider; 2x2 checklist; prayer-minute boxes; chain-weight and mood circles; ruled journaling lines; Night prayer panel.", "",
                "### Core Scripture", "", "> \"%s\" - %s (KJV)" % (d["verse"], d["ref"]), "",
                "### The Breakdown", "", d["breakdown"], "",
                "### Interactive Action Tracker", ""]
        out += ["- [ ] " + h for h in d["habits"]]
        out += ["- [ ] Prayer minutes: 5 / 10 / 15 / 20+", "- Chain weight 1-10: before ( ) after ( )   Mood: :( :| :)", "",
                "### The Vault Prompt", "", d["vault"], "",
                "### Daily Street-Worded Prayer", "", d["prayer"], ""]
    out += ["## Page 9 - The Payout Gateway", "",
            "**Headline:** " + PAYOUT_HEADLINE, "",
            "- High-contrast QR code (encodes `APP_URL`; replace the URL and re-run the builder, or drop a branded QR in Canva).",
            "- Label: SCAN HERE. Price strip: FULL APP ACCESS | $5 - $12 / MONTH | CANCEL ANYTIME.", ""]
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(out))


def main():
    os.makedirs(os.path.dirname(PDF_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(MD_PATH), exist_ok=True)
    c = canvas.Canvas(PDF_PATH, pagesize=A5)
    c.setTitle("Shattering Chains - 7-Day A5 Bible Insert Kit")
    c.setAuthor("Shattering Chains")
    page_cover(c)
    for i, d in enumerate(DAYS, 1):
        page_day(c, i, d)
    page_payout(c)
    c.save()
    write_markdown()
    print("wrote", PDF_PATH)
    print("wrote", MD_PATH)


if __name__ == "__main__":
    main()
