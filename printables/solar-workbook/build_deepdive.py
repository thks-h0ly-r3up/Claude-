#!/usr/bin/env python3
"""Builds the companion volume: Original Lights, The Deep Dive.

Reuses the look, helpers, and day data from build.py. Sky data (moon, sun, stars) is computed with
PyEphem for each date. Optional local rise/set times appear if data/location.txt exists:
    City, ST | latitude | longitude | IANA time zone      e.g.  Austin, TX | 30.27 | -97.74 | America/Chicago

Usage: python3 build_deepdive.py
"""
import datetime as dt
import math
import os
import re

import ephem
import ephem.stars as es

import build as b
from build import E, page, lines, day_date, week_of

HERE = b.HERE
b.BOOK = "Original Lights: The Deep Dive"
BRAND = b.BRAND

DD = b.parse(os.path.join(HERE, "data", "deepdive_days.txt"))
assert sorted(DD) == list(range(1, 92)), "deep dive days missing"

# ------------------------------------------------------------------ sky
BRIGHT = []
for name, star in es.stars.items():
    star.compute("2026/12/1")
    if star.mag <= 2.0 and name != "Polaris":
        BRIGHT.append((name, star))

PHASE_ANCHOR = {
    "New moon": ("Psalm 104:19", "“He made the moon to mark the seasons.”"),
    "Waxing crescent": ("Psalm 8:3", "“When I look at your heavens, the work of your fingers, the moon and the stars, which you have set in place.”"),
    "First quarter": ("Isaiah 40:26", "“He who brings out their host by number, calling them all by name.”"),
    "Waxing gibbous": ("Psalm 148:3", "“Praise him, sun and moon, praise him, all you shining stars!”"),
    "Full moon": ("Psalm 89:37", "“Like the moon it shall be established forever, a faithful witness in the skies.”"),
    "Waning gibbous": ("Psalm 121:6", "“The sun shall not strike you by day, nor the moon by night.”"),
    "Last quarter": ("Psalm 136:9", "“the moon and stars to rule over the night, for his steadfast love endures forever.”"),
    "Waning crescent": ("Job 38:33", "“Do you know the ordinances of the heavens?”"),
}
CON = {  # IAU abbreviations -> full names for the ones we meet
    "Vir": "Virgo", "Lib": "Libra", "Sco": "Scorpius", "Oph": "Ophiuchus", "Sgr": "Sagittarius", "Cap": "Capricornus",
    "Aqr": "Aquarius", "Psc": "Pisces", "Ari": "Aries", "Tau": "Taurus", "Gem": "Gemini", "Cnc": "Cancer", "Leo": "Leo",
    "Cet": "Cetus", "Eri": "Eridanus", "Ori": "Orion", "CMa": "Canis Major", "CMi": "Canis Minor", "Aur": "Auriga",
    "Per": "Perseus", "And": "Andromeda", "Peg": "Pegasus", "Cyg": "Cygnus", "Lyr": "Lyra", "Aql": "Aquila",
    "Boo": "Boötes", "CrB": "Corona Borealis", "Her": "Hercules", "UMa": "Ursa Major", "Lep": "Lepus", "PsA": "Piscis Austrinus",
    "Hya": "Hydra", "Crv": "Corvus", "Crt": "Crater", "Cen": "Centaurus", "Lup": "Lupus", "Sct": "Scutum", "Ser": "Serpens",
    "Del": "Delphinus", "Equ": "Equuleus", "Cas": "Cassiopeia", "Cep": "Cepheus", "LMi": "Leo Minor", "Sex": "Sextans",
}


def con_name(c):
    return CON.get(c, c)


def moon_phase_name(age, illum):
    if age < 1.0 or age > 28.5:
        return "New moon"
    if age < 6.4:
        return "Waxing crescent"
    if age < 8.4:
        return "First quarter"
    if age < 13.4:
        return "Waxing gibbous"
    if age < 16.1:
        return "Full moon"
    if age < 21.1:
        return "Waning gibbous"
    if age < 23.1:
        return "Last quarter"
    return "Waning crescent"


def utc(d):
    return d.datetime().replace(tzinfo=dt.timezone.utc) if hasattr(d, "datetime") else d


# location (optional)
LOC = None
loc_path = os.path.join(HERE, "data", "location.txt")
if os.path.exists(loc_path):
    parts = [x.strip() for x in open(loc_path, encoding="utf-8").read().strip().split("|")]
    if len(parts) == 4:
        from zoneinfo import ZoneInfo
        LOC = dict(name=parts[0], lat=parts[1], lon=parts[2], tz=ZoneInfo(parts[3]))


def local_times(d):
    """Sunrise, sunset, day length, moonrise, moonset in local time (needs data/location.txt)."""
    ob = ephem.Observer()
    ob.lat, ob.lon, ob.elevation = LOC["lat"], LOC["lon"], 0
    ob.pressure = 0
    ob.horizon = "-0:34"
    tz = LOC["tz"]
    start = dt.datetime(d.year, d.month, d.day, 0, 0, tzinfo=tz).astimezone(dt.timezone.utc)
    ob.date = ephem.Date(start.replace(tzinfo=None))
    fmt = lambda x: ephem.Date(x).datetime().replace(tzinfo=dt.timezone.utc).astimezone(tz).strftime("%-I:%M %p")
    out = {}
    try:
        sr = ob.next_rising(ephem.Sun()); ss = ob.next_setting(ephem.Sun(), start=sr)
        out["sunrise"], out["sunset"] = fmt(sr), fmt(ss)
        L = (ss - sr) * 24
        out["daylen"] = f"{int(L)} h {int(round((L - int(L)) * 60))} m"
    except Exception:
        pass
    ob.horizon = "-0:34"
    for key, fn in (("moonrise", ob.next_rising), ("moonset", ob.next_setting)):
        try:
            t = fn(ephem.Moon())
            if ephem.Date(t).datetime() < (start.replace(tzinfo=None) + dt.timedelta(days=1)):
                out[key] = fmt(t)
            else:
                out[key] = "none today"
        except Exception:
            out[key] = "none today"
    return out


EVENTS = {}   # utc date -> labels
ECL = []


def build_events():
    t0, t1 = ephem.Date("2026/10/24"), ephem.Date("2027/01/28")
    for fn, label in ((ephem.next_new_moon, "New moon"), (ephem.next_first_quarter_moon, "First quarter"),
                      (ephem.next_full_moon, "Full moon"), (ephem.next_last_quarter_moon, "Last quarter")):
        t = t0
        while True:
            t = fn(t)
            if t > t1:
                break
            d = ephem.Date(t).datetime()
            EVENTS.setdefault(d.date(), []).append((label, d))
            if label in ("New moon", "Full moon"):
                m = ephem.Moon(t); s = ephem.Sun(t)
                # ecliptic latitude of the moon near syzygy: eclipse possible if |beta| is small
                beta = abs(math.degrees(ephem.Ecliptic(m).lat))
                if beta < 1.55:
                    ECL.append((label, d, round(beta, 2)))
    t = ephem.Date("2026/10/24")
    while True:
        t = ephem.next_solstice(t)
        if t > t1:
            break
        EVENTS.setdefault(ephem.Date(t).datetime().date(), []).append(("Winter solstice (Northern Hemisphere)", ephem.Date(t).datetime()))
    for d_, lab in {dt.date(2026, 10, 21): "Orionids meteor shower peak (annual, approx.)", dt.date(2026, 11, 17): "Leonids meteor shower peak (annual, approx.)",
                    dt.date(2026, 12, 13): "Geminids meteor shower peak, Dec 13–14 (annual, approx.)", dt.date(2026, 12, 22): "Ursids meteor shower peak (annual, approx.)",
                    dt.date(2027, 1, 3): "Quadrantids meteor shower peak, Jan 3–4 (annual, approx.)"}.items():
        EVENTS.setdefault(d_, []).append((lab, None))


build_events()


def sky(n):
    return sky_for(day_date(n))


def sky_for(d):
    snap = ephem.Date(dt.datetime(d.year, d.month, d.day, 2, 0) + dt.timedelta(days=1))  # 02:00 UTC next day: evening in the US
    m, s = ephem.Moon(snap), ephem.Sun(snap)
    prev_new = ephem.previous_new_moon(snap)
    age = snap - prev_new
    illum = m.phase
    name = moon_phase_name(age, illum)
    waxing = age < 14.77
    nf = max(0, min(14, round(age if waxing else 29.53 - age)))
    # a bright star near the meridian at ~9 p.m. local sun time: its RA is the sun's RA + 9h
    target = (math.degrees(s.ra) / 15.0 + 9.0) % 24
    best = None
    for nm, st in BRIGHT:
        st.compute(snap)
        ra = math.degrees(st.ra) / 15.0
        diff = abs((ra - target + 12) % 24 - 12)
        dec = math.degrees(st.dec)
        if dec < -45:
            continue
        score = diff + (st.mag * 0.1)
        if best is None or score < best[0]:
            best = (score, nm, st, diff)
    star = best
    r = dict(date=d, age=age, illum=illum, phase=name, waxing=waxing, enoch=nf,
             moon_con=con_name(ephem.constellation(m)[0]), sun_con=con_name(ephem.constellation(s)[0]),
             sun_dec=math.degrees(s.dec), star=star[1], star_con=con_name(ephem.constellation(star[2])[0]),
             star_mag=star[2].mag, star_gap=star[3] * 60, star_dec=math.degrees(star[2].dec))
    r["events"] = EVENTS.get(d, [])
    if LOC:
        r["loc"] = local_times(d)
    return r


SKY = {n: sky(n) for n in range(1, 92)}


# ------------------------------------------------------------------ pages
def day_block(n):
    d = DD[n]; dd = b.DAYS[n]; k = SKY[n]
    date = k["date"]
    chips = [
        f'<span class="chip c2">Moon: {k["phase"]} · {k["illum"]:.0f}% lit · {k["age"]:.1f} days old · in {k["moon_con"]}</span>',
        f'<span class="chip c1">Sun: in {k["sun_con"]} · declination {k["sun_dec"]:+.1f}°</span>',
        f'<span class="chip c3">Star: {k["star"]} ({k["star_con"]}){" · low in the south" if k["star_dec"] < -20 else ""}</span>',
        f'<span class="chip c4">Enoch: {k["enoch"]}/14 light, {"growing" if k["waxing"] else "fading"}</span>',
    ]
    ev = "".join(f'<span class="chip" style="background:#b07d12">{E(lab)}{(" · " + dtm.strftime("%b %-d %H:%M") + " UTC") if dtm else ""}</span>' for lab, dtm in k["events"])
    rs = ""
    if LOC and k.get("loc"):
        L = k["loc"]
        rs = (f'<div class="small" style="margin-top:2px"><b>{E(LOC["name"])}:</b> sunrise {L.get("sunrise","–")}, sunset {L.get("sunset","–")}, '
              f'day length {L.get("daylen","–")}; moonrise {L.get("moonrise","–")}, moonset {L.get("moonset","–")}</div>')
    ref, quote = PHASE_ANCHOR[k["phase"]]
    return f"""<div class="dd">
<div class="dh"><span><b>Day {n}</b> · {date.strftime("%a %b %-d, %Y")} · Ethiopian {b.eth_str(date, True)}</span><span class="r">{E(dd["ref"])} · {E(dd["title"])}</span></div>
<div class="chips" style="margin:3px 0 2px;gap:3px">{''.join(chips)}{ev}</div>{rs}
<div class="cn"><div class="lab k">Canon deep dive</div>{E(DD[n]["canon"])}</div>
<div class="rd"><div class="lab">How God would want it read</div>{E(DD[n]["read"])}
<div class="anc">Sky anchor, {ref} (ESV): {E(quote)}</div></div>
<div class="nt"><span class="lab p">My notes</span><div class="ruled" style="flex:1"></div></div>
</div>"""


EXTRA_CSS = """
.dd{border-top:1.5px solid var(--line);padding:5px 0 3px;flex:1;display:flex;flex-direction:column;min-height:0}
.dd:first-child{border-top:0}
.dh{font-size:9.4pt;color:var(--denim2);display:flex;justify-content:space-between;gap:8px}
.dh .r{color:var(--purple);font-weight:700;text-align:right}
.dd .cn,.dd .rd{font-size:9.8pt;line-height:1.4;margin-top:4px}
.dd .cn{font-family:'DejaVu Serif',Georgia,serif}
.dd .rd{background:#f0fbfa;border-radius:6px;padding:4px 7px}
.dd .anc{font-size:8.4pt;color:var(--denim);margin-top:2px;font-style:italic}
.dd .nt{flex:1;display:flex;flex-direction:column;min-height:.25in;margin-top:3px}
.es{font-size:10.2pt;line-height:1.45}
.es p{margin:0 0 6px}
.es h3{font-size:12pt;color:var(--purple);margin:7px 0 3px}
.es ul{margin:2px 0 6px;padding-left:17px} .es li{margin-bottom:2px}
.warn{border:1.5px solid var(--gold);background:#fffaf0;border-radius:8px;padding:6px 10px;margin:6px 0}
"""


def essay(title, body, running="Companion"):
    return page(f'<h1 class="h-big" style="font-size:21pt">{E(title)}</h1><div class="es">{body}</div>', top_r=running)


def cover():
    inner = f"""
<div class="cv"></div><div class="stitch"></div><div class="stitch2"></div>
<div class="cvc">
  <div class="brand">{BRAND}</div>
  <div class="kicker">COMPANION TO THE SOLAR WORKBOOK</div>
  <h1 style="font-size:40pt">ORIGINAL LIGHTS<br>THE DEEP DIVE</h1>
  <div class="sub">The Ethiopian canon, the sky for each of the 91 days, and how to read both with Christ at the center.</div>
  <div class="sun" style="transform:scale(1.4);margin-top:.5in">{b.SUN_SVG % b.sun_rays()}</div>
  <div style="position:absolute;bottom:2.35in;font-size:8.2pt;letter-spacing:2.2px;color:#e6f7f6;font-weight:700">CANON · SKY · TRAUMA · ADDICTION · WARFARE · GRIEF</div>
  <div class="tag">You survived. Now we rebuild.</div>
  <div class="by">Written from the floor up by Hellshaker<br>and her loyal service dog, Big Boy</div>
  <div class="dt">SEASON ONE · PRELUDE OCT 24 · DAY 1 OCT 28, 2026 TO JAN 26, 2027</div>
</div>"""
    return page(inner, "cover", running=False).replace('<div class="body">', '<div class="body" style="padding:0">', 1)


def about_page():
    body = f"""
<p><b>{BRAND}</b> · Original Lights: The Deep Dive · Companion to The Solar Workbook · Created October 24, 2026 · Version 1.1 · © 2026 {BRAND}. All rights reserved. Personal use only.</p>
<p><b>Scripture.</b> Quotations are from the ESV Bible (The Holy Bible, English Standard Version), copyright © 2001 by Crossway, a publishing ministry of Good News Publishers. All rights reserved. They are marked ESV where they appear. Quotations from Sirach, Wisdom of Solomon, Baruch, 1 Enoch, and Jubilees are my paraphrases of common English translations, so verse numbers may differ slightly in the copy you own. Check them against a translation before you quote them.</p>
<p><b>What this book is.</b> A companion to the daily pages. For each of the 91 days it gives (1) a deeper look at the day’s verse through the Ethiopian canon, (2) what the sky actually looked like, computed from astronomical formulas, and (3) a plain word about how to read both, including where trauma, addiction, and spiritual warfare come in.</p>
<p><b>What this book is not.</b> It is not astrology or fortune-telling, and it will never tell you what a moon phase or a constellation “means” for your life. It is not therapy, medical care, addiction treatment, or crisis support, and the author is not a clinician. It does not tell you what happened to anyone’s soul. Prayer sits beside treatment, medication, safe housing, and safety planning. It does not replace them.</p>
<div class="warn"><b>If you are in danger or in crisis (US):</b> 911 · Call or text 988 · SAMHSA 1-800-662-4357 · Trafficking hotline 1-888-373-7888 (text 233733) · Domestic violence hotline 1-800-799-7233 (text START to 88788) · Dial 211 for local help. Confirm numbers before relying on them, and look up local options outside the US.</div>
<p><b>About the Ethiopian canon texts.</b> 1 Enoch (Henok) and Jubilees (Kufale) survive in full only in Ge’ez, the classical language of Ethiopia. The Ethiopian Orthodox Tewahedo Church receives them, along with Sirach, Wisdom of Solomon, and Baruch, as canon. Most other churches do not treat them all as Scripture, though Jude 14–15 quotes 1 Enoch 1:9. I treat them as ancient witnesses worth knowing, and I let the Bible carry the weight. Where a verse has no real parallel in the canon, I say so instead of inventing one.</p>
<p><b>How “exact” the sky is.</b> Each day’s moon, sun, and star data is computed for the evening of that date at 02:00 UTC the next day, which is about 9 p.m. Central, 10 p.m. Eastern, and 7 p.m. Pacific. Moon illumination and age are accurate to about a percent or better, and constellations use the modern IAU boundaries. Sunrise, sunset, and moonrise depend on where you stand, so they appear only if a location is added. Meteor-shower dates are annual and approximate.</p>"""
    return page(f'<h1 class="h-big">About This Companion</h1><div class="es">{body}</div>', top_r="Before you begin")


def read_this_way():
    body = """
<p>Signs get abused, so this book uses a short set of tests. Before you decide what any verse, canon text, dream, or sky event “means,” run it through these six. If it fails one, set it down.</p>
<table class="rt"><tr><th style="width:.3in">#</th><th style="width:1.6in">Test</th><th>The question</th></tr>
<tr><td>1</td><td><b>Christ</b></td><td>Does it point toward Jesus, and not toward me, a sign, a person, or a product?</td></tr>
<tr><td>2</td><td><b>Scripture</b></td><td>Does it agree with the clear teaching of the Bible read in context? Canon texts outside the Protestant Bible can add color but cannot override it.</td></tr>
<tr><td>3</td><td><b>Fruit</b></td><td>Does it lead toward love, truth, safety, humility, and responsibility, or toward fear, secrecy, shame, and control?</td></tr>
<tr><td>4</td><td><b>Freedom</b></td><td>Does it leave room to choose, to say no, to ask questions, to leave, and to get treatment?</td></tr>
<tr><td>5</td><td><b>Cost</b></td><td>Does it ask for money, silence, or loyalty to a leader in exchange for the “answer”?</td></tr>
<tr><td>6</td><td><b>Humility</b></td><td>Does it admit what it does not know, including about the dead?</td></tr></table>
<h3>What the Bible says about reading the sky</h3>
<ul>
<li><b>The lights are for time.</b> “Let them be for signs and for seasons, and for days and years” (Gen. 1:14, ESV). A sign marks something. It does not decide it.</li>
<li><b>The sky tells about God.</b> “The heavens declare the glory of God” (Ps. 19:1, ESV). “For his invisible attributes … have been clearly perceived, ever since the creation of the world, in the things that have been made” (Rom. 1:20, ESV).</li>
<li><b>Do not worship them.</b> Deuteronomy 4:19 warns against being drawn to bow down to the sun, moon, and stars. Jeremiah 10:2 says not to be dismayed at the signs of the heavens as the nations are. Isaiah 47:13–14 mocks those who gaze at the stars to tell the future.</li>
<li><b>They are praising Him.</b> “Praise him, sun and moon, praise him, all you shining stars!” (Ps. 148:3, ESV). He “determines the number of the stars; he gives to all of them their names” (Ps. 147:4, ESV).</li></ul>
<p>So this book will say, “Here is the sky tonight, and here is what the canon and Scripture say about the verse for the day.” It will not say, “This moon means a hard week for you.” If anyone tells you a star position decides your relationships, your sobriety, or your safety, that is a claim Scripture does not make.</p>
"""
    body2 = """<h3>Reading the sky chips on each day</h3>
<ul><li><b>Moon:</b> phase, how much of the visible face is lit, days since the new moon, and the constellation it stands in.</li>
<li><b>Sun:</b> the constellation behind it and its declination (how far north or south of the celestial equator, in degrees).</li>
<li><b>Star:</b> a bright star near due south around 9 p.m. local sun time, so you can find it. It is a landmark, not a message.</li>
<li><b>Enoch:</b> the moon’s light counted in fourteenths, the old way (see below).</li></ul>
<h3>A note on the moon and the calendar</h3>
<p>The Bible itself speaks of new moons and festivals (Num. 28:11; Ps. 81:3). The Enoch and Jubilees tradition, which this workbook follows for its 364-day count, argues for reckoning by the sun and warns against dating the festivals by the moon (Jubilees 6:36–37). Both appear in this canon. I show the moon because it is beautiful and real and because you asked for it, and I count the days by the sun.</p>
<p>1 Enoch also counts the moon’s light in fourteenths (chapters 73–74 and 78), growing for about two weeks and then fading for two. The “Enoch’s count” chip on each day is that old way of saying the same thing, and it is approximate.</p>"""
    return [essay("How to Read This Book", body, "Reading the sky"), essay("Reading the Sky Chips and the Moon", body2, "Reading the sky")]


def trauma_essay():
    body = """
<p>The canon does not hand trauma a tidy explanation. Read together, it says a few plain things.</p>
<h3>1. The cry is heard</h3>
<p>1 Enoch 9:3–11 pictures the souls of the killed and the groans of the oppressed going up to the gates of heaven, and the angels bringing the case before God. That is a canon witness that suffering inflicted on people is not invisible to heaven. Compare Exodus 3:7 and Genesis 4:10.</p>
<h3>2. Fear is described without blame</h3>
<p>Wisdom of Solomon 17 describes terror in the dark, and 17:12 says fear is the surrender of the help that reason offers. Sirach 40:5–7 describes troubled thoughts that disturb sleep. Neither blames the sufferer. They treat a frightened body and mind as something real that needs care.</p>
<h3>3. “Tested like gold” needs a warning label</h3>
<p>Sirach 2:1–6 and Wisdom 3:5–6 use refining language. In their setting it is about perseverance in faith. It is not a claim that God sends abuse, assault, or trafficking to refine a person. Job’s friends tried that reading and God rebuked them for it (Job 42:7). Human harm is human harm.</p>
<h3>4. Mourning is allowed</h3>
<p>Sirach 7:34 says to mourn with those who mourn. Sirach 38:16–23 says to weep for the dead and then to receive comfort and not be consumed. Both halves matter.</p>
<h3>5. How this book reads it</h3>
<ul><li>A trauma response is not evidence of weak faith or a demon.</li>
<li>Grounding, sleep, safety, and counseling are part of rebuilding, not substitutes for faith.</li>
<li>Nothing in these pages asks you to relive anything, name the harm, or forgive on a timeline.</li></ul>
<div class="warn">If remembering floods you, stop, look around the room, name five things you can see, and put the book down. A page is never worth your safety.</div>"""
    return essay("Trauma in the Canon", body, "Companion essay")


def addiction_essay():
    body = """
<p>Addiction as we name it today is not a category in these texts, but the canon knows what it is to be mastered by something.</p>
<h3>What it says about wine and bondage</h3>
<ul><li>Sirach 31:25–30 says not to try to prove yourself by wine, because wine has destroyed many. Sirach 19:1–2 says workers who are drunkards will not become rich, and that whoever despises small things will fall little by little.</li>
<li>Proverbs 23:29–35 describes the wounds and the pull of drink with a hard honesty.</li>
<li>Noah’s vineyard (Gen. 9:20–21; Jubilees 7) is a vineyard that bore fruit and then led to his fall. The same good thing can be misused. This is told without disgust and it does not end the story of Noah.</li></ul>
<h3>What it says about getting out</h3>
<ul><li><b>Prayer for freedom and a clean heart.</b> In Jubilees 1:19–21 Moses prays that the spirit of Belial not rule over Israel and that God create a clean heart in them, much like Psalm 51:10.</li>
<li><b>Return is open.</b> Sirach 17:24–26 says God gives a return to those who repent. Proverbs 24:16 says the righteous fall seven times and rise again.</li>
<li><b>Responsibility is real.</b> Sirach 5:5–7 warns against presuming on mercy. Sirach 15:11–20 says not to blame the Lord for your failing. God does not cause a relapse.</li>
<li><b>Medicine is allowed.</b> Sirach 38:1–14 says to honor the physician and to pray. Jubilees 10:10–13 says angels taught Noah remedies from plants. Jesus calls Himself a physician for the sick (Mark 2:17).</li></ul>
<h3>How this book reads it</h3>
<ul><li>Grace is not enabling, and understanding is not excusing. Hold both.</li>
<li>A relapse does not make a person disposable. It does call for a plan and for people.</li>
<li>Prayer does not replace treatment, detox with medical support, medication, or a recovery community.</li>
<li>Be careful of any teaching that sells a spiritual cure and tells you to drop real care.</li></ul>
<div class="warn">Withdrawal from alcohol and some other substances can be medically dangerous. Do not stop suddenly without a clinician. SAMHSA 1-800-662-4357 can help find treatment. In an emergency call 911.</div>"""
    return essay("Addiction and Bondage in the Canon", body, "Companion essay")


def warfare_essay():
    body = """
<p>The Enoch and Jubilees tradition has a much larger cast of spiritual beings than most Bibles do. It is worth knowing what these books say, and being careful about what they do not say.</p>
<h3>What the texts say</h3>
<ul><li><b>1 Enoch 6–16.</b> The Watchers, angels who descended and taught people forbidden things and fathered the giants. Chapter 10 has the angel Raphael bind Azazel and speaks of healing the earth. 15:8–12 says spirits came from the giants. Jude 6 and 2 Peter 2:4 both mention angels who sinned.</li>
<li><b>Jubilees 10.</b> After the flood Noah prays, evil spirits are bound, a tenth is left under Prince Mastema, and the angels teach Noah remedies from plants.</li>
<li><b>Jubilees 11, 17, 48.</b> Mastema sends ravens to eat the seed, urges the testing of Abraham, and opposes Moses at the Exodus. In each, God acts and the opposition fails.</li></ul>
<h3>What they do not say</h3>
<p>None of these books says every trauma response, illness, addiction, intrusive thought, or difficult person is demonic. None says spiritual warfare removes responsibility. And none says an exercise, a ritual, or a worksheet literally breaks a curse. Broken chains are a symbol of freedom, and freedom also takes people, time, and help.</p>
<h3>What the Bible adds</h3>
<ul><li>Ephesians 6:10–18 says our struggle is not only against flesh and blood, and then spends its words on truth, righteousness, peace, faith, and prayer.</li>
<li>James 4:7 says to submit to God and resist the devil. 1 Peter 5:8–9 says to be sober-minded and watchful.</li>
<li>Jesus loosed a woman from a bond (Luke 13:16), and the same Gospels also show Him healing ordinary illness without naming a demon.</li></ul>
<h3>A careful way to read it</h3>
<ul><li>Ask first what is physical, what is relational, what is a habit, and what is trauma. Then ask what is spiritual.</li>
<li>In Jubilees 11 the ravens were stopped with a plow. Practical defense is spiritual wisdom.</li>
<li>Do not accept a label that someone else pressures you into. Do not accept a “deliverance” that costs money, demands secrecy, or tells you to stop treatment.</li>
<li>Do not blame yourself for being targeted, and do not use “attack” to avoid a choice.</li></ul>"""
    return essay("Spiritual Warfare, Carefully", body, "Companion essay")


def soul_contract_essay():
    p1 = """
<p>This page touches a real loss and a real belief, so it is written slowly. The next pages say what Scripture does teach about why you are here.</p>
<h3>What a soul contract is</h3>
<p>A soul contract is the idea that before birth a soul agrees to a set of lessons, relationships, and sometimes the time and manner of its death. It comes from New Age and reincarnation-based teaching. <b>It is not in the Bible, and it is not in 1 Enoch, Jubilees, Sirach, Wisdom, or Baruch.</b> This book will not dress it in a verse. It says so plainly because the book is for people at risk, and a frame that sounds biblical and is not can hurt them.</p>
<h3>What the canon does say, which can sound close</h3>
<ul>
<li><b>God knows our days.</b> “In your book were written, every one of them, the days that were formed for me, when as yet there was none of them” (Ps. 139:16, ESV). Job 14:5 says a person’s days are determined. This is about God’s knowledge and care, not a deal the soul made.</li>
<li><b>Heavenly tablets.</b> 1 Enoch 81:1–2 and Jubilees 3:10 and 5:13 speak of things written on heavenly tablets: judgments, laws, and the names of the righteous. Jubilees 5:17–18 also says there is forgiveness written for those who turn. The tablets are not a script you signed.</li>
<li><b>Real choice.</b> Sirach 15:11–20 says God left people to their own choice, set fire and water before them, and does not cause our failing. Deuteronomy 30:19 says “choose life.”</li>
<li><b>God does not author evil.</b> “God cannot be tempted with evil, and he himself tempts no one” (James 1:13, ESV).</li>
<li><b>God can redeem harm without scripting it.</b> “You meant evil against me, but God meant it for good” (Gen. 50:20, ESV). Joseph’s brothers chose evil. God worked good beyond it.</li>
<li><b>A short life can be fulfilled.</b> Wisdom of Solomon 4:7–14 says the righteous who die early will be at rest, and 4:13 says that being perfected in a short time, he fulfilled long years. That is a hope about people God is pleased with. It is not a formula, and it does not say a death was arranged.</li></ul>
<h3>Why this book does not build on a “fulfilled soul contract” for an addiction loss</h3>
<ol>
<li>It can imply that an overdose or any death was agreed to or required, which can make God or the soul the author of something that addiction and a broken world caused.</li>
<li>It can close the door on grief, anger, and “what if” questions that need room.</li>
<li>For a woman still struggling who reads “her ending was written,” it can sound like “mine is too,” or “nothing I do matters.” That is the opposite of “choose life.”</li>
<li>It makes claims about an unseen soul that no one can check.</li></ol>
"""
    p2 = """
<h3>What you can honestly say instead</h3>
<div class="warn"><i>“[Name]’s life mattered. Their death is a real loss. I do not know everything about their last days or their soul, and I do not have to. God knew them fully (Ps. 139). The Judge of all the earth does right (Gen. 18:25). Their story moves me, and I am building something so someone else has a place to reach.”</i></div>
<p>No one can tell you where any person stands with God. What Scripture gives us to hold is this: He is near to the brokenhearted (Ps. 34:18, ESV), nothing “will be able to separate us from the love of God in Christ Jesus our Lord” (Rom. 8:39, ESV), and He is the just and merciful judge. The canon’s hope in Wisdom 3:1–3 is that the souls of the righteous are in God’s hand. It is a hope offered, not a verdict about one person.</p>
<h3>If you carry a belief about someone you lost</h3>
<p>If you privately sense purpose in how a loved one’s life has shaped yours, that is your testimony and your grief, and it is yours to keep. It helps to label it for what it is, a personal belief and not a teaching of Scripture, and to leave it out of any pages you share with others. Grief resources, if you want them: GRASP (Grief Recovery After a Substance Passing, grasphelp.org), GriefShare (griefshare.org), and 988 any time. Confirm current details.</p>
<div class="box"><div class="lab p">My own page (private)</div>
<div class="small"><b>What I know about the person I lost.</b></div><div class="ruled" style="height:.54in"></div>
<div class="small"><b>What I do not know, and may never.</b></div><div class="ruled" style="height:.54in"></div>
<div class="small"><b>What I want to say to them.</b></div><div class="ruled" style="height:.54in"></div>
<div class="small"><b>What I am choosing to do with what their life taught me.</b></div><div class="ruled" style="height:.54in"></div></div>"""
    return [essay("Soul Contracts, Heavenly Tablets, and Grief", p1, "Companion essay"),
            essay("Soul Contracts, Heavenly Tablets, and Grief (continued)", p2, "Companion essay")]



def why_here():
    p1 = """
<p>You asked how to wake up to why you are here. Scripture has a real answer, and it is bigger and kinder than a contract. Here is what it says, what it does not say, and how to tell the difference.</p>
<h3>What Scripture says about purpose</h3>
<ul>
<li><b>You are loved before you are useful.</b> Jesus heard “This is my beloved Son” before He did any ministry (Matt. 3:17). Start there.</li>
<li><b>You were made on purpose.</b> “For we are his workmanship, created in Christ Jesus for good works, which God prepared beforehand, that we should walk in them” (Eph. 2:10, ESV).</li>
<li><b>God finishes what He starts.</b> “I cry out to God Most High, to God who fulfills his purpose for me” (Ps. 57:2, ESV). “The LORD will fulfill his purpose for me; your steadfast love, O LORD, endures forever” (Ps. 138:8, ESV).</li>
<li><b>Pain can become comfort for others.</b> God “comforts us in all our affliction, so that we may be able to comfort those who are in any affliction, with the comfort with which we ourselves are comforted by God” (2 Cor. 1:3–4, ESV). That is what reaching back is.</li>
<li><b>Place and time are not random to God.</b> He “determined allotted periods and the boundaries of their dwelling place, that they should seek God” (Acts 17:26–27, ESV). “God settles the solitary in a home” (Ps. 68:6, ESV).</li>
<li><b>God can use what others meant for harm.</b> “You meant evil against me, but God meant it for good” (Gen. 50:20, ESV).</li></ul>
<h3>Providence is not a contract</h3>
<p>A contract says you agreed to it beforehand. Providence says God works with what actually happens, including adoptions, losses, and the strange coincidences that make a person say, “What are the odds?” Scripture lets you receive those details as meaningful, as a gift and a sign of care, without claiming you or anyone else signed for them. Where a family came together in a way that seems too specific to be chance, you can thank God for it and not need it explained.</p>
<h3>On a goodbye you cannot fully read</h3>
<p>A hug that felt like no other is love, and love is real whether or not the person knew it was the last. You may never know what was in someone’s heart that day, and you do not have to settle it. You do not owe anyone a performance to honor them. Love honors them. Guilt does not.</p>
<div class="warn"><b>If the night is the hardest time:</b> a pain that comes at night can be grief, trauma, or sleep. Tell a doctor or counselor about it, and keep 988 (call or text) in reach. Wanting your life to mean something is good. Pressure to prove it is not from God.</div>"""
    p2 = """
<h3>Seven steps to wake up to your calling</h3>
<ol>
<li><b>Start with who, not what.</b> You are beloved first. Say it out loud once today.</li>
<li><b>Tell the truth about the pain.</b> Write what hurts at night, plainly, without making it prettier. Get care for sleep and safety.</li>
<li><b>Take an inventory.</b> Four lists: what I have survived, what I am good at, what breaks my heart, and what people already thank me for. The overlap is a clue, not a verdict.</li>
<li><b>Run it through the six tests</b> on the “How to Read This Book” page: Christ, Scripture, fruit, freedom, cost, humility.</li>
<li><b>Take one small, real step this week.</b> “One who is faithful in a very little is also faithful in much” (Luke 16:10, ESV). A call, a meeting, one page of writing, one act of help.</li>
<li><b>Ask wise, safe people.</b> “Without counsel plans fail, but with many advisers they succeed” (Prov. 15:22, ESV). Choose people who respect your no and keep your confidence.</li>
<li><b>Hold it loosely and keep walking.</b> Moses waited forty years in the wilderness. A calling grows and gets revised. Certainty is not required for obedience.</li></ol>
<h3>Watch for these</h3>
<ul><li>Anyone who sells you your purpose, or says a “reading” will reveal it.</li>
<li>Any voice that says you must do this or something bad will happen. “God gave us a spirit not of fear but of power and love and self-control” (2 Tim. 1:7, ESV).</li>
<li>A calling that requires secrecy, a leader’s approval for everything, or dropping treatment.</li>
<li>The idea that you have to complete someone else’s story. Your purpose is yours.</li></ul>
<p>Esther was told, “Who knows whether you have not come to the kingdom for such a time as this?” (Esth. 4:14, ESV). Notice it is a question. The invitation is real. The certainty is not promised. Take the next faithful step.</p>"""
    p3 = """
<p>Private pages. Write in pencil. Nothing here has to be shared.</p>
<div class="box"><div class="lab">My story and the signs I notice</div><div class="small">The coincidences, family details, and moments that feel meaningful to me:</div><div class="ruled" style="height:1.5in"></div></div>
<div class="box" style="margin-top:8px"><div class="lab p">My personal belief (labeled as such)</div><div class="small">What I believe about soul contracts or destiny, in my own words. This is my belief and my testimony, not a teaching of Scripture:</div><div class="ruled" style="height:1.3in"></div></div>
<div class="box" style="margin-top:8px"><div class="lab k">The four lists</div>
<table class="rt"><tr><th>What I have survived</th><th>What I am good at</th></tr><tr><td style="height:.9in"></td><td></td></tr>
<tr><th>What breaks my heart</th><th>What people already thank me for</th></tr><tr><td style="height:.9in"></td><td></td></tr></table></div>
<div class="box" style="margin-top:8px"><div class="lab">What I think I am here for, in pencil, and my one small step this week</div><div class="ruled" style="height:1in"></div></div>"""
    return [essay("Why Am I Here? Calling, Not Contract", p1, "Companion essay"),
            essay("Waking Up to Your Calling", p2, "Companion essay"),
            essay("My Private Pages", p3, "Companion essay")]


def sky_calendar():
    rows = ""
    allev = []
    for d_, evs in sorted(EVENTS.items()):
        for lab, tm in evs:
            allev.append((d_, lab, tm))
    for d_, lab, tm in allev:
        n = (d_ - b.START).days + 1
        if not -3 <= n <= 91 or n == 0 and False:
            continue
        lbl = f"Day {n}" if n >= 1 else f"Prelude {n + 4}"
        t = f' · {tm.strftime("%H:%M")} UTC' if tm else ""
        rows += f"<tr><td>{d_.strftime('%a %b %-d, %Y')}</td><td>{lbl}</td><td>{E(lab)}{t}</td></tr>"
    pre_rows = ""
    for k in range(4):
        x = sky_for(b.PRE_START + dt.timedelta(days=k))
        pre_rows += f"<tr><td>{x['date'].strftime('%a %b %-d, %Y')}</td><td>Prelude {k+1}</td><td>Moon: {x['phase']}, {x['illum']:.0f}% lit, in {x['moon_con']}. Sun in {x['sun_con']}.</td></tr>"
    ecl = "No eclipses fall in this window." if not ECL else "Possible eclipse geometry: " + "; ".join(f"{l} {d.strftime('%b %-d')}" for l, d, _ in ECL)
    body = f"""
<p>Moon phases, the solstice, and annual meteor-shower peaks for the 91 days. UTC times are shown, so subtract 5 to 8 hours for US time zones.</p>
<table class="rt"><tr><th>Date</th><th style="width:.8in">Day</th><th>Event</th></tr>{pre_rows}{rows}</table>
<p style="margin-top:6px"><b>Eclipses:</b> {ecl} (checked from the Moon’s position at each new and full moon.)</p>
<p><b>The sun’s constellation.</b> The sun’s apparent position moves through the modern IAU constellations: Virgo until about October 30, Libra until about November 22, Scorpius for about a week (November 23–29), Ophiuchus from about November 30, Sagittarius from about December 18, and Capricornus from about January 20. The constellations are star patterns on a map. They are not “signs” that assign traits to a day or a person.</p>
<p><b>The solstice.</b> The winter solstice is the day the sun reaches its lowest point in the Northern Hemisphere. After it the days lengthen. In the Southern Hemisphere it is reversed.</p>"""
    return essay("The Sky for These 91 Days", body, "Sky calendar")


def location_page():
    if LOC:
        txt = f"<p>Sunrise, sunset, day length, moonrise, and moonset are shown for <b>{E(LOC['name'])}</b> on every day page.</p>"
    else:
        txt = ("<p>Sunrise, sunset, day length, moonrise, and moonset depend on exactly where you stand, so they are not on the day pages yet. "
               "To add them, put one line in <code>data/location.txt</code>, like <code>Austin, TX | 30.27 | -97.74 | America/Chicago</code>, and rebuild.</p>")
    body = txt + """<p>Until then, use the moon’s phase, the sun’s constellation and declination, and the evening star on each page. Those are the same everywhere on Earth for a given date and hour, apart from how high the star appears in your sky.</p>"""
    return body


def day_pages():
    out = []
    keys = []
    for n in range(1, 92, 3):
        grp = [m for m in range(n, min(n + 3, 92))]
        w = week_of(grp[0])
        head = (f'<div class="lab d">Week {w} · {E(b.WEEKS[w]["title"])} · Days {grp[0]}–{grp[-1]}</div>'
                '<div class="small" style="color:var(--denim)">The sky marks time and points to its Maker. It does not predict anyone’s day.</div>')
        inner = head + "".join(day_block(m) for m in grp)
        out.append((f"d{grp[0]}", page(inner, top_r=f"Deep dive · Days {grp[0]}–{grp[-1]}")))
    return out


def toc_page(toc):
    def row(label, pg):
        return f'<div class="row"><b>{E(label)}</b><span class="d"></span><span>{pg}</span></div>'
    parts = ['<div class="grp">Front matter</div>']
    for lab, key in [("About this companion", "about"), ("How to read this book", "read"), ("Reading the sky chips and the moon", "read2"), ("The sky for these 91 days", "sky"),
                     ("Trauma in the canon", "trauma"), ("Addiction and bondage in the canon", "addiction"),
                     ("Spiritual warfare, carefully", "warfare"), ("Soul contracts, heavenly tablets, and grief", "soul"),
                     ("Why am I here? Calling, not contract", "why"), ("Waking up to your calling", "why2"), ("My private pages", "why3")]:
        parts.append(row(lab, toc[key]))
    parts.append('<div class="grp">Day-by-day deep dive (three days per page)</div>')
    for n in range(1, 92, 3):
        e = min(n + 2, 91)
        parts.append(row(f"Days {n}–{e}", toc[f"d{n}"]))
    parts.append('<div class="grp">After the season</div>')
    parts.append(row("Closing page", toc["close"]))
    inner = f'<h1 class="h-big">Contents</h1><div class="toc">{"".join(parts)}</div>'
    return page(inner, top_r="Contents")


def closing():
    body = f"""
<p>You do not have to decode the sky, a verse, or a canon text to be loved by God or to take your next step. These pages are a way to look closer at things God made and wrote about, and to look at them with Jesus at the center.</p>
<p><b>Where this stops.</b> If anything here makes you more afraid, more secret, or less able to get care, set it down. The Bible’s own answer to confusion is Christ, truth, safe people, and the next faithful step.</p>
<div class="box"><div class="lab p">What I am taking from the deep dive</div>{lines(5)}</div>
{location_page()}
<div class="decl">You survived. Now we rebuild.</div>"""
    return page(f'<h1 class="h-big">Closing Page</h1><div class="es">{body}</div>', top_r="Closing")


def assemble():
    pages = [("cover", cover()), ("about", about_page()), ("toc", None), ("read", read_this_way()[0]), ("read2", read_this_way()[1]), ("sky", sky_calendar()),
             ("trauma", trauma_essay()), ("addiction", addiction_essay()), ("warfare", warfare_essay())]
    soul = soul_contract_essay()
    pages.append(("soul", soul[0]))
    pages.append(("soul2", soul[1]))
    wh = why_here()
    pages.append(("why", wh[0]))
    pages.append(("why2", wh[1]))
    pages.append(("why3", wh[2]))
    pages += day_pages()
    pages.append(("close", closing()))
    toc = {k: i + 1 for i, (k, _) in enumerate(pages)}
    pages[2] = ("toc", toc_page(toc))
    return pages


def main():
    import sys
    pages = assemble()
    body = "\n".join(h.replace("{{PN}}", str(i + 1)) for i, (_, h) in enumerate(pages))
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{BRAND} · Original Lights: The Deep Dive</title>'
           f'<style>{b.CSS}{EXTRA_CSS}</style></head><body>{body}</body></html>')
    out_html = os.path.join(HERE, "original-lights-deep-dive.html")
    open(out_html, "w", encoding="utf-8").write(doc)
    print(f"wrote {out_html} ({len(pages)} pages); eclipses flagged: {ECL}")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"))
        pg = br.new_page()
        pg.goto("file://" + out_html)
        pg.wait_for_timeout(500)
        over = pg.evaluate("""() => {
          const res = [];
          document.querySelectorAll('.page').forEach((P, i) => {
            const body = P.querySelector('.body'); if (!body) return;
            const bb = body.getBoundingClientRect(); let worst = 0;
            body.querySelectorAll('*').forEach(el => {
              if (el.closest('.ruled') && !el.classList.contains('ruled')) return;
              worst = Math.max(worst, el.getBoundingClientRect().bottom - bb.bottom);
            });
            if (body.scrollHeight > body.clientHeight + 1 || worst > 1) res.push([i + 1, Math.round(body.scrollHeight - body.clientHeight), Math.round(worst)]);
          });
          return res; }""")
        print("OVERFLOW:" if over else "no overflow detected", over or "")
        if "--shots" in sys.argv:
            os.makedirs(os.path.join(HERE, "_shots"), exist_ok=True)
            for idx in [int(x) for x in sys.argv[sys.argv.index("--shots") + 1].split(",")]:
                pg.query_selector_all(".page")[idx - 1].screenshot(path=os.path.join(HERE, "_shots", f"dd{idx:03d}.png"))
        pg.pdf(path=os.path.join(HERE, "original-lights-deep-dive.pdf"), width="8.5in", height="11in", print_background=True, prefer_css_page_size=True)
        br.close()
    print("wrote original-lights-deep-dive.pdf")


if __name__ == "__main__":
    main()
