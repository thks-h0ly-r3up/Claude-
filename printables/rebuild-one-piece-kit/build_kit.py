#!/usr/bin/env python3
"""Builds the 7HE H0LY R3UP "Rebuild One Piece at a Time" printable kit.

Writes rebuild-one-piece-at-a-time-kit.html (self-contained, fonts embedded)
next to this script. Render to PDF with build.sh.

Scripture quotations are from the King James Version (public domain).
"""
import html
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS_CSS = os.environ.get("KIT_FONTS_CSS", os.path.join(HERE, "fonts_embedded.css"))

# ---------------------------------------------------------------- page map
P = dict(welcome=2, inside=3, plan=4, board=5, pieces=6, cards=8, bookmarks=12,
         jar=15, slips=16, days=20, hit=27, slipped=28, safe=29, bound=30,
         practical=31, money=32, tracker=33, prayers=34, review=35, cert=36,
         closing=37)
TOTAL = 37

FOOTS = [
    "D.O.A. IS GOD'S FAVORITE STARTING POINT",
    "BANDO 2 VINEYARD",
    "IN MEMORY OF BRANDI RENEE — 12787–121721",
    "TRADING THE CORNER FOR THE CROWN",
    "GOD DOESN'T CALL THE QUALIFIED. HE QUALIFIES THE CALLED.",
    "STILL HERE. STILL HIS. LET'S REBUILD.",
]

e = html.escape

# ---------------------------------------------------------------- content
WORDS = [
    # word, truth, verse, ref, action
    ("Identify",
     "You can't rebuild what you keep calling something else. Name it. God already knows what it is.",
     "Search me, O God, and know my heart: try me, and know my thoughts.", "Psalm 139:23",
     "Write the one thing you've been calling by a softer name. Then write what it's really called."),
    ("Surrender",
     "Surrender isn't losing. It's finally letting go of a wheel you were never built to drive.",
     "Trust in the LORD with all thine heart; and lean not unto thine own understanding.", "Proverbs 3:5",
     "Say it out loud: “God, I can't. You can.” Then name one thing you're handing over today."),
    ("Tell the Truth",
     "Secrets keep you sick. One true thing, told to one safe person, breaks their grip.",
     "Confess your faults one to another, and pray one for another, that ye may be healed.", "James 5:16",
     "Pick a safe person (not someone who used you). Tell them one true thing this week. Write their name here."),
    ("Release",
     "You can't hold the chain and the hand of God at the same time. Something has to go.",
     "Come unto me, all ye that labour and are heavy laden, and I will give you rest.", "Matthew 11:28",
     "Write what you're setting down on a slip. Fold it. Drop it in the jar. Leave it there."),
    ("Replace",
     "Empty doesn't stay empty. Whatever you don't plant in that hour, the old stuff will.",
     "And be not conformed to this world: but be ye transformed by the renewing of your mind.", "Romans 12:2",
     "Name your most dangerous hour of the day. Write what you're putting there instead."),
    ("Renew",
     "Mercy has a morning shift. You don't have to earn today. You just have to show up to it.",
     "Though our outward man perish, yet the inward man is renewed day by day.", "2 Corinthians 4:16",
     "Tomorrow, the first five minutes belong to God before the phone. Set the alarm now."),
    ("Heal",
     "Healing isn't a feeling. It's a practice. Some days it's just keeping the appointment.",
     "He healeth the broken in heart, and bindeth up their wounds.", "Psalm 147:3",
     "Book or keep one appointment this week: doctor, counselor, meeting, group. Write the date."),
    ("Forgive",
     "Forgiving frees you. It does not hand anybody the key back. Forgiveness is not access.",
     "Be ye kind one to another, tenderhearted, forgiving one another, even as God for Christ's sake hath forgiven you.", "Ephesians 4:32",
     "Write the debt you're releasing and, if it's you, say so. Add: “I release it. I keep my boundary.”"),
    ("Set Boundaries",
     "A boundary isn't a wall to punish somebody. It's a gate you finally learned to lock.",
     "Keep thy heart with all diligence; for out of it are the issues of life.", "Proverbs 4:23",
     "Choose one boundary. Write the exact sentence you'll say. Use the Boundary Builder."),
    ("Take Action",
     "Prayer and paperwork go together. Pray it, then pick up the phone.",
     "Be ye doers of the word, and not hearers only, deceiving your own selves.", "James 1:22",
     "Do the smallest piece of the thing you've been avoiding. Ten minutes. Then stop and mark it done."),
    ("Trust",
     "Trust gets rebuilt in small deposits, not big speeches. Yours and theirs.",
     "What time I am afraid, I will trust in thee.", "Psalm 56:3",
     "Keep one promise to yourself today exactly how you said it, exactly when you said it."),
    ("Grow",
     "Pruning hurts. A vineyard looks worse right after it's cut back. That's how it learns to bear.",
     "But grow in grace, and in the knowledge of our Lord and Saviour Jesus Christ.", "2 Peter 3:18",
     "Write what you're outgrowing, and what you want to grow in its place."),
    ("Keep Going",
     "Relapse is not resignation. Get up, tell somebody, learn the pattern, take the next right step.",
     "Let us not be weary in well doing: for in due season we shall reap, if we faint not.", "Galatians 6:9",
     "Write the last time you got back up after a fall. Then write the first thing you did."),
    ("Find Purpose",
     "Your worst chapter may be somebody's way out. Not to be used up. To be used well.",
     "For we are his workmanship, created in Christ Jesus unto good works.", "Ephesians 2:10",
     "Write one thing you survived that you could someday help another person walk through."),
    ("Encourage Others",
     "You can't pour from an empty cup, but you can pass a cup that God already filled.",
     "Comfort yourselves together, and edify one another, even as also ye do.", "1 Thessalonians 5:11",
     "Send one encouraging text today. “Thinking of you. Proud of you.” Write who you sent it to."),
    ("Freedom",
     "Free doesn't mean finished. It means the chains aren't the boss anymore.",
     "If the Son therefore shall make you free, ye shall be free indeed.", "John 8:36",
     "Finish both: “I'm free from…” and “I'm free to…”"),
]

BOOKMARKS = [
    ("Anchored", "Hebrews 6:19", "Which hope we have as an anchor of the soul, both sure and stedfast.", "anchor",
     "What's holding me steady today?"),
    ("Rooted", "John 15:5", "I am the vine, ye are the branches: He that abideth in me, and I in him, the same bringeth forth much fruit.", "vine",
     "What am I staying connected to?"),
    ("Supported", "Galatians 6:2", "Bear ye one another's burdens, and so fulfil the law of Christ.", "cross",
     "Who can carry this with me?"),
    ("Renewed", "Lamentations 3:22–23", "His compassions fail not. They are new every morning: great is thy faithfulness.", "sun",
     "What's new this morning?"),
    ("Restored", "Joel 2:25", "I will restore to you the years that the locust hath eaten.", "vine",
     "What am I asking God to restore?"),
    ("Near", "Psalm 34:18", "The LORD is nigh unto them that are of a broken heart; and saveth such as be of a contrite spirit.", "cross",
     "Where do I feel Him close?"),
    ("Rebuilt", "Nehemiah 2:18", "Let us rise up and build. So they strengthened their hands for this good work.", "anchor",
     "What piece am I building today?"),
    ("Small", "Zechariah 4:10", "For who hath despised the day of small things?", "sun",
     "What small thing counts today?"),
    ("Free", "Psalm 107:14", "He brought them out of darkness and the shadow of death, and brake their bands in sunder.", "cross",
     "What bands are breaking?"),
    ("Beauty", "Isaiah 61:3", "…beauty for ashes, the oil of joy for mourning, the garment of praise for the spirit of heaviness.", "vine",
     "What is God turning to beauty?"),
    ("New", "2 Corinthians 5:17", "Therefore if any man be in Christ, he is a new creature: old things are passed away; behold, all things are become new.", "sun",
     "What old thing am I leaving?"),
    ("Lifted", "Psalm 40:2", "He brought me up also out of an horrible pit, out of the miry clay, and set my feet upon a rock.", "anchor",
     "Where has He set my feet?"),
]

SLIPS = {
    "BODY": ("#d6598f", [
        "Drink a full glass of water. Right now. Then decide what's next.",
        "Eat something with protein. Hungry, angry, lonely, tired: you can't fight on empty.",
        "Take a shower and put on clean clothes, even if you're not going anywhere.",
        "Walk ten minutes outside. Phone in your pocket. Eyes up.",
        "Pick a bedtime for tonight and write it here: ______. Be in bed by then.",
        "Stretch for five minutes. Let your body know it's not in danger right now.",
        "Take your prescribed meds as directed. Questions? Call your pharmacist or doctor.",
        "Ten slow breaths: in for four, out for six. Do it again.",
        "Book one appointment you've been putting off: doctor, dentist, anything.",
        "Fill a water bottle and carry it all day. Finish it.",
        "Put your hands to work: dishes, laundry, scrub something until it shines.",
        "Rest for twenty minutes without guilt. Rest is not relapse.",
    ]),
    "MIND": ("#7a4c9e", [
        "Write what you're feeling in one word. Then look for a truer word.",
        "HALT check: Hungry? Angry? Lonely? Tired? Fix the first one you find.",
        "Write “Dear future me” and two sentences. Tape it where you'll see it.",
        "Mute or turn off one thing feeding the noise: a feed, a show, a person's page.",
        "Write three things that are true right now that nobody can take back.",
        "Set a 15-minute timer. Cravings crest and fall. Don't decide anything until it rings.",
        "List what is actually in your control today. Do the first one.",
        "Write one lie you've been believing. Write what God says beside it.",
        "Put your phone in another room for one hour.",
        "Write your reasons for staying free. Keep them where you'll see them.",
        "Do the thing you're dreading for five minutes only. Then you're allowed to stop.",
        "Sit with a hard feeling for two minutes without fixing it. Feelings aren't emergencies.",
    ]),
    "SPIRIT": ("#2f9e98", [
        "Read Psalm 23 out loud. Slowly.",
        "Pray three sentences: I need You. Here's what's true. Help me with the next thing.",
        "Write a prayer of honest complaint (read Psalm 13). God can take it.",
        "Read John 15:1–8 and underline every “abide.”",
        "Thank God for three ordinary things. Real ones, not church answers.",
        "Sit in silence for five minutes. Ask, “What's my next right step?” Then listen.",
        "Confess it plainly. No speech. Just the truth (1 John 1:9).",
        "Play one worship song and sing along. Off-key is fine.",
        "Read Lamentations 3:22–23. Write what's new this morning.",
        "Pray for someone still stuck where you used to be.",
        "Write down one time God showed up when you couldn't see it.",
        "Ask God for wisdom about a person who hurt you. Pray from a distance. Prayer never requires contact.",
    ]),
    "PEOPLE": ("#4a6486", [
        "Text a safe person: “Rough day. Can you talk?”",
        "Put a meeting, service, group, or class on your calendar this week. Do it now.",
        "Tell someone your plan for today out loud.",
        "Thank someone who showed up for you. Be specific.",
        "Call your sponsor, counselor, pastor, or support person. Five minutes counts.",
        "Ask for one specific thing you need. Not a speech. Just the thing.",
        "Send an encouraging text to someone else in recovery.",
        "Spend twenty minutes with someone who's good for you.",
        "Say no to one thing today without a long explanation. “No, I can't” is a full sentence.",
        "Mute, unfollow, or block one person or page that pulls you backward. Not hate. Distance.",
        "Sit by someone new at your meeting or service. Introduce yourself.",
        "Tell someone: “I'm not okay tonight.” Don't wait until you're worse.",
    ]),
    "PRACTICAL": ("#a5673f", [
        "Make your bed. First small win of the day.",
        "Open the mail you've been avoiding. Sort: now / this week / call.",
        "Write every bill and its due date on one page.",
        "Clear one drawer, shelf, or corner. Get rid of anything tied to the old life.",
        "Charge your phone and save your support numbers in it.",
        "Plan tomorrow's three meals.",
        "Find your ID, Social Security card, and birth certificate. Know where they are.",
        "Make the phone call you've been dodging. Write your questions first.",
        "Pack a small bag with essentials so you can leave fast if you ever need to.",
        "Update your resume or fill out one application.",
        "Do a load of laundry, start to finish.",
        "Write tomorrow's top three tasks tonight. Then stop.",
    ]),
}

DAYS = [
    dict(n=1, theme="Name It", pieces=[1, 2], bm="Anchored",
         note=("Real talk: I spent years calling it stress, calling it a phase, calling it “just this once.” "
               "You can't rebuild what you won't name. Today isn't for fixing anything. It's for telling the truth about "
               "what's on the table, to God first, because He's already seen it and He's still here. D.O.A. is God's favorite "
               "starting point. So start."),
         verse="Search me, O God, and know my heart: try me, and know my thoughts: and see if there be any wicked way in me, and lead me in the way everlasting.",
         ref="Psalm 139:23–24",
         prompts=["What have I been calling by a softer name?",
                  "What has it cost me? (money, people, time, health, peace)",
                  "What's still standing that God can build on?"],
         prayer="Lord, I'm done lying about where I am. Show me the truth and hold me while You do it. I can't, You can. Amen.",
         hard="If today is heavy, do only the first box and place piece #1. That counts."),
    dict(n=2, theme="Tell It", pieces=[3, 4], bm="Supported",
         note=("Secrets keep us sick. Tell one safe person one true thing this week. Not everything. One thing. "
               "Then start setting down what was never yours to carry. Some of what you're holding happened TO you, and that part "
               "isn't your fault. If it's abuse, telling the truth means telling someone who can help you stay safe. "
               "You don't have to carry this alone."),
         verse="Confess your faults one to another, and pray one for another, that ye may be healed.",
         ref="James 5:16",
         prompts=["Who is my safe person? (Not someone who used you.) When will I tell them?",
                  "What am I ready to set down: a grudge, guilt, a person, a grief?",
                  "Three sentences to the person or thing I'm releasing (never sent):"],
         prayer="God, I'm bringing You the thing I've been hiding. I'm not going to hide it from You or from one safe person. Take what I can't carry. Amen.",
         hard="If you can't name a safe person yet, put 988 or a helpline on your Safe People page. Start there."),
    dict(n=3, theme="Rebuild the Inside", pieces=[5, 6, 7], bm="Renewed",
         note=("The bando taught me to fill every hour with survival. Empty hours are doors: the old stuff knocks at the same time "
               "every day. Don't just close the door. Plant something there. That's the vineyard: same hours, new fruit. "
               "And healing? Healing is a practice. Some days it's a prayer. Some days it's just showing up to the appointment."),
         verse="And be not conformed to this world: but be ye transformed by the renewing of your mind.",
         ref="Romans 12:2",
         prompts=["My danger hours (time, place, person, feeling):",
                  "What I'm planting in those hours instead:",
                  "The appointment, meeting, or call I'm booking for healing:"],
         prayer="Father, fill the empty places with You. Renew my mind this morning like You renew Your mercies. Heal what I can't fix by myself. Amen.",
         hard="Bad day? Pull one BODY slip and one PEOPLE slip from the jar. Do both."),
    dict(n=4, theme="Draw the Line", pieces=[8, 9], bm="Rooted",
         note=("Baby, hear this: forgiving somebody is not handing them the key back. Forgiveness is between you and God. "
               "Access is between you and wisdom. You can release the debt and keep the gate locked. And if someone is dangerous, "
               "you don't owe them a conversation. You owe yourself a safe plan (page 29 has numbers)."),
         verse="Be ye kind one to another, tenderhearted, forgiving one another, even as God for Christ's sake hath forgiven you.",
         ref="Ephesians 4:32",
         prompts=["Who or what am I ready to release the debt on? (Include myself.)",
                  "Where do I need distance, limits, or a locked gate?",
                  "The exact sentence I will say:"],
         prayer="Lord, I release what I'm ready to release, and I ask You to help me with what I'm not. Give me wisdom for the gate. Protect me. Amen.",
         hard="Do not confront anyone who has hurt you today. Write it. Pray it. Tell a safe person instead."),
    dict(n=5, theme="Do the Thing", pieces=[10, 11], bm="Small",
         note=("Prayer and paperwork go together. I can pray all day, but the unopened bill is still unopened. Faith is not an excuse to skip "
               "the phone call. Do the small scary thing, then trust God with the part you can't control. Trust with people gets rebuilt "
               "one kept promise at a time, theirs and yours."),
         verse="But be ye doers of the word, and not hearers only, deceiving your own selves.",
         ref="James 1:22",
         prompts=["The thing I've been avoiding (10 minutes max today):",
                  "One promise to myself I'll keep exactly as I said it:",
                  "What I'm trusting God with that I can't control:"],
         prayer="God, give me courage for the small hard thing and peace about the big one I can't fix. I'm trusting You with what's Yours. Amen.",
         hard="If ten minutes is too much, do two. A started thing beats a perfect plan."),
    dict(n=6, theme="Stay Rooted", pieces=[12, 13], bm="Rebuilt",
         note=("Pruning hurts. Nobody tells you a vineyard looks worse right after it's cut back. Growth can feel like loss: old friends, "
               "old comforts, old identity. And if you stumbled this week? Relapse is not resignation. Tell somebody today, look for the pattern, "
               "change one thing, and take the next right step. Page 28 is for you."),
         verse="And let us not be weary in well doing: for in due season we shall reap, if we faint not.",
         ref="Galatians 6:9",
         prompts=["What am I outgrowing?",
                  "Where did I stumble or come close, and what did it teach me?",
                  "One thing I'll do at the same time every day:"],
         prayer="Lord, keep me rooted when it's dry. Prune what needs pruning. Let me be honest about the falls and quick to get back up. Amen.",
         hard="If you're in a spiral tonight, skip this page and go to page 27. Then call someone."),
    dict(n=7, theme="Walk Free", pieces=[14, 15, 16], bm="Free",
         note=("Free doesn't mean finished. It means the chains aren't the boss anymore. I'm still trading the corner for the crown, one honest "
               "step at a time, and so are you. Your worst chapter might be somebody's way out. Not to be used up, but to be used well. "
               "Look at your board. Look what you built with your own two hands."),
         verse="If the Son therefore shall make you free, ye shall be free indeed.",
         ref="John 8:36",
         prompts=["What's different since Day 1?",
                  "What has God rebuilt that I didn't expect?",
                  "Who can I encourage this week, and how?"],
         prayer="Jesus, thank You for every piece. I'm free from what You broke off and free to what You're calling me into. Keep me walking. Amen.",
         hard="Finished the week? Sign your certificate (page 36). Then print the daily pages again and go another round."),
]

# ---------------------------------------------------------------- svg helpers
def icon(kind, color="#7a4c9e", size=44):
    s = size
    if kind == "cross":
        body = (f'<rect x="20" y="4" width="8" height="40" rx="2" fill="{color}"/>'
                f'<rect x="9" y="14" width="30" height="8" rx="2" fill="{color}"/>'
                f'<circle cx="24" cy="18" r="2.6" fill="#fff"/>')
    elif kind == "anchor":
        body = (f'<g fill="none" stroke="{color}" stroke-width="3.4" stroke-linecap="round">'
                '<circle cx="24" cy="9" r="4.5"/><path d="M24 14 V40"/><path d="M15 21 H33"/>'
                '<path d="M8 30 C9 38 17 42 24 42 C31 42 39 38 40 30"/><path d="M8 30 l-2 -5 M40 30 l2 -5"/></g>')
    elif kind == "sun":
        rays = "".join(
            f'<line x1="{24+15*math.cos(math.radians(a)):.1f}" y1="{32-15*math.sin(math.radians(a)):.1f}" '
            f'x2="{24+21*math.cos(math.radians(a)):.1f}" y2="{32-21*math.sin(math.radians(a)):.1f}"/>'
            for a in range(20, 180, 20))
        body = (f'<g stroke="{color}" stroke-width="3" stroke-linecap="round">{rays}</g>'
                f'<path d="M12 32 A12 12 0 0 1 36 32 Z" fill="{color}"/>'
                f'<path d="M4 38 H44" stroke="{color}" stroke-width="3" stroke-linecap="round"/>')
    else:  # vine
        body = (f'<g fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round">'
                '<path d="M10 44 C10 30 20 26 24 14 C26 8 30 6 34 6"/></g>'
                f'<path d="M24 24 C14 22 12 14 14 10 C22 10 26 16 24 24 Z" fill="{color}"/>'
                f'<path d="M26 32 C34 32 40 26 40 20 C32 18 26 24 26 32 Z" fill="{color}" opacity=".85"/>')
    return f'<svg class="ico" viewBox="0 0 48 48" width="{s}" height="{s}">{body}</svg>'


def camo(w, h, seed, colors, n=46, opacity=1.0):
    rnd = random.Random(seed)
    out = [f'<svg class="camo" viewBox="0 0 {w} {h}" preserveAspectRatio="none" '
           f'width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">']
    for _ in range(n):
        cx, cy = rnd.uniform(0, w), rnd.uniform(0, h)
        rx, ry = rnd.uniform(w * .05, w * .16), rnd.uniform(h * .03, h * .10)
        rot = rnd.uniform(0, 180)
        col = rnd.choice(colors)
        pts = []
        k = 9
        for i in range(k):
            a = 2 * math.pi * i / k
            r = rnd.uniform(.72, 1.15)
            pts.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r))
        # smooth closed path via quadratic midpoints
        d = []
        for i in range(k):
            p0, p1 = pts[i], pts[(i + 1) % k]
            mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
            if i == 0:
                start = ((pts[-1][0] + pts[0][0]) / 2, (pts[-1][1] + pts[0][1]) / 2)
                d.append(f"M{start[0]:.1f},{start[1]:.1f}")
            d.append(f"Q{p0[0]:.1f},{p0[1]:.1f} {mid[0]:.1f},{mid[1]:.1f}")
        d.append("Z")
        out.append(f'<path d="{" ".join(d)}" fill="{col}" opacity="{opacity}" '
                   f'transform="rotate({rot:.0f} {cx:.1f} {cy:.1f})"/>')
    out.append("</svg>")
    return "".join(out)


# jigsaw geometry -----------------------------------------------------------
S = 144            # cell size in px (1.5in)
PITCH = 220        # spacing of pieces on cut sheets (2.45in)
PAD = 32           # room for outgoing tabs
GH = [[0] * 4 for _ in range(5)]   # horizontal edges between rows (0 = flat frame)
GV = [[0] * 5 for _ in range(4)]   # vertical edges between cols
for r in range(1, 4):
    for c in range(4):
        GH[r][c] = 1 if (r * 3 + c) % 2 == 0 else -1
for r in range(4):
    for c in range(1, 4):
        GV[r][c] = 1 if (r + c * 2) % 2 == 0 else -1


def edge(p0, p1, s):
    (x0, y0), (x1, y1) = p0, p1
    if s == 0:
        return f"L{x1:.1f},{y1:.1f}"
    dx, dy = x1 - x0, y1 - y0
    nx, ny = dy, -dx  # outward normal for clockwise traversal (y down)

    def pt(x, y):
        return f"{x0 + dx * x + nx * y * s:.1f},{y0 + dy * x + ny * y * s:.1f}"
    return (f"L{pt(.38, 0)} C{pt(.38, .05)} {pt(.32, .07)} {pt(.32, .13)} "
            f"C{pt(.32, .22)} {pt(.68, .22)} {pt(.68, .13)} "
            f"C{pt(.68, .07)} {pt(.62, .05)} {pt(.62, 0)} L{pt(1, 0)}")


def piece_path(r, c, ox, oy):
    tl, tr, br, bl = (ox, oy), (ox + S, oy), (ox + S, oy + S), (ox, oy + S)
    top = -GH[r][c]
    right = GV[r][c + 1]
    bottom = GH[r + 1][c]
    left = -GV[r][c]
    d = f"M{tl[0]},{tl[1]} " + edge(tl, tr, top) + " " + edge(tr, br, right) + " " + \
        edge(br, bl, bottom) + " " + edge(bl, tl, left) + " Z"
    return d


FILLS = ["#f8d5e4", "#e6d6f2", "#cdeceb", "#fbe3d0"]


def board_svg():
    size = 4 * S + 2 * PAD
    parts = [f'<svg viewBox="0 0 {size} {size}" width="{size / 96:.2f}in" height="{size / 96:.2f}in" '
             'xmlns="http://www.w3.org/2000/svg">']
    n = 1
    for r in range(4):
        for c in range(4):
            ox, oy = PAD + c * S, PAD + r * S
            parts.append(f'<path d="{piece_path(r, c, ox, oy)}" fill="#fffdf9" stroke="#b9a6cc" '
                         'stroke-width="1.6" stroke-dasharray="5 4"/>')
            parts.append(f'<circle cx="{ox + S / 2}" cy="{oy + S / 2}" r="22" fill="#f1eaf7"/>')
            parts.append(f'<text x="{ox + S / 2}" y="{oy + S / 2 + 9}" text-anchor="middle" '
                         f'font-family="Caveat" font-weight="700" font-size="32" fill="#7a4c9e">{n}</text>')
            n += 1
    parts.append("</svg>")
    return "".join(parts)


def piece_svg(r, c, label, num, fill, blank=False):
    ox, oy = PAD, PAD
    size = S + 2 * PAD
    word_lines = label.split(" ")
    if len(label) > 9 and len(word_lines) > 1:
        lines = [" ".join(word_lines[:-1]), word_lines[-1]] if len(word_lines) == 2 else \
            [" ".join(word_lines[:1]), " ".join(word_lines[1:])]
    else:
        lines = [label]
    fs = int(min(30, 84 / (0.44 * max(1, max(len(x) for x in lines)))))
    cy = oy + S / 2 + (4 if len(lines) == 1 else -6)
    txt = ""
    for i, ln in enumerate(lines):
        txt += (f'<text x="{ox + S / 2}" y="{cy + i * (fs + 1)}" text-anchor="middle" '
                f'font-family="Caveat" font-weight="700" font-size="{fs}" fill="#3b2b4a">{e(ln)}</text>')
    numtxt = "" if blank else (f'<text x="{ox + 12}" y="{oy + 20}" font-family="Libre Franklin" '
                               f'font-weight="800" font-size="10" fill="#7a4c9e">#{num}</text>')
    blank_lines = ""
    if blank:
        blank_lines = (f'<line x1="{ox + 22}" y1="{oy + S / 2 + 6}" x2="{ox + S - 22}" y2="{oy + S / 2 + 6}" '
                       'stroke="#8a7a99" stroke-width="1.4"/>'
                       f'<text x="{ox + S / 2}" y="{oy + S / 2 + 30}" text-anchor="middle" font-family="Libre Franklin" '
                       'font-size="8" fill="#8a7a99" letter-spacing="1.2">YOUR WORD</text>')
    return (f'<svg viewBox="0 0 {size} {size}" width="{size / 96:.2f}in" height="{size / 96:.2f}in" '
            'xmlns="http://www.w3.org/2000/svg" style="display:block">'
            f'<path d="{piece_path(r, c, ox, oy)}" fill="{fill}" stroke="#3b2b4a" stroke-width="1.6"/>'
            f'<rect x="{ox}" y="{oy}" width="{S}" height="{S}" fill="none" stroke="#3b2b4a" stroke-width=".8" '
            'stroke-dasharray="2 3" opacity=".55"/>'
            f'{numtxt}{txt}{blank_lines}</svg>')


# ---------------------------------------------------------------- page shell
pages = []


def page(inner, cls="", head="", foot=True):
    n = len(pages) + 1
    ft = ""
    if foot:
        left = FOOTS[(n - 1) % len(FOOTS)]
        ft = (f'<div class="foot"><span class="fl">{e(left)}</span>'
              f'<span class="fr">7HE H0LY R3UP by THKS &amp; CO. &nbsp;•&nbsp; {n}</span></div>')
    hd = ""
    if head:
        hd = (f'<div class="phead"><span class="pb">7HE H0LY R3UP</span>'
              f'<span class="ps">{e(head)}</span></div>')
    if cls in ("", "daypage", "jarpage") and foot:
        pages.append(f'<section class="page fit {cls}"><div class="topband"></div>{hd}<div class="zw">{inner}</div>{ft}</section>')
    else:
        pages.append(f'<section class="page {cls}"><div class="topband"></div>{hd}{inner}{ft}</section>')


def lines(k, cls="ln"):
    return "".join(f'<div class="{cls}"></div>' for _ in range(k))


def boxes(items):
    return "".join(f'<div class="ck"><span class="bx"></span><span>{it}</span></div>' for it in items)


def title(main, sub=""):
    s = f'<div class="sub">{sub}</div>' if sub else ""
    return f'<h2>{main}</h2>{s}'


# ---------------------------------------------------------------- 1 cover
def build_cover():
    camo_svg = camo(816, 1056, 7, ["#e9a4c4", "#c99ae0", "#f4c9dc", "#a98bd0", "#f7b3cf", "#9fd8d4"], n=90, opacity=.9)
    inner = f'''
    <div class="cover-bg">{camo_svg}</div>
    <div class="cover-sun"></div>
    <div class="cover-card">
      <div class="cv-brand">7HE H0LY R3UP</div>
      <div class="cv-by">by THKS &amp; CO.</div>
      <div class="cv-kicker">THE COMPLETE PRINTABLE REBUILD KIT</div>
      <h1>Rebuild<br>One Piece<br>at a Time</h1>
      <div class="cv-tag">Take one honest step.</div>
      <ul class="cv-list">
        <li><b>Rebuild Board</b> + 16 word pieces to cut &amp; glue</li>
        <li><b>16 Word Cards</b> with truth, Scripture &amp; a step</li>
        <li><b>12 Scripture Bookmarks</b></li>
        <li><b>60 Next Right Step Slips</b> for your jar</li>
        <li><b>7-Day Rebuild Plan</b> (one page per day)</li>
        <li><b>When It Hits</b> craving &amp; hard-moment plan</li>
        <li><b>If You Slipped</b> • <b>Boundary Builder</b> • <b>Safe People List</b></li>
        <li><b>Practical Rebuild</b> checklist • <b>Money Reset</b></li>
        <li><b>30-Day Tracker</b> • Prayers • Weekly Review • Certificate</li>
      </ul>
      <div class="cv-foot">37 pages • US Letter • Instant PDF download • Personal use</div>
    </div>
    <div class="cover-tagline">STILL HERE. STILL HIS. LET'S REBUILD.</div>
    <div class="cover-copy">© 2026 7HE H0LY R3UP by THKS &amp; CO. All rights reserved. Personal use only. No part of this work may be reproduced, distributed, copied, transmitted, or commercially exploited without prior written permission, except as permitted by applicable law.</div>
    '''
    page(inner, cls="cover", foot=False)


# ---------------------------------------------------------------- 2 welcome
def build_welcome():
    inner = f'''
    {title("Welcome to the worktable", "A note from Hellshaker")}
    <div class="letter">
      <p>Hey, it's Hellshaker.</p>
      <p>I made this kit for the version of me who didn't know where to start. I put it together with Big Boy right beside me,
      because he stayed beside me while I was learning how to stay beside myself.</p>
      <p>I know what the floor feels like. Addiction. Abuse. Grief. I lost my sister, Brandi Renee, and I wish she'd had somewhere to reach.
      So I'm building it now, one piece at a time.</p>
      <p>Here's what I learned: nobody rebuilds everything in a day. I tried. What works is one honest step, then the next, then the next.
      Then you look up and there's a whole wall of pieces you put there yourself.</p>
      <p>This kit gives your hands something honest to do (cut, glue, write, fold, pray) while your heart catches up.
      It also gives you real tools: a plan for when a craving hits, a way to draw a line with people, a checklist for the paperwork of life,
      and seven days to walk through on purpose.</p>
      <p>I'm not a doctor, a therapist, or a pastor. This kit is a companion, not a replacement, for real help.
      If you need more than paper tonight, turn to page {P["safe"]} and use those numbers. Asking for help is part of the rebuild.
      It is not proof that you're failing.</p>
      <p>Baby, I know what far gone looks like. Now let's see what God can do from there.</p>
      <p class="sig">Still here. Still His. Let's rebuild.<br><span>— Hellshaker</span></p>
    </div>
    <div class="cols2">
      <div class="pbox pink">
        <h4>This kit is for you if…</h4>
        <ul>
          <li>You're early in recovery, or thinking about starting.</li>
          <li>You're years in and fighting a hard week.</li>
          <li>You're grieving, healing from abuse, or starting over.</li>
          <li>You need something to do with your hands and something true to hold.</li>
        </ul>
      </div>
      <div class="pbox teal">
        <h4>Three moves. That's it.</h4>
        <ol>
          <li><b>Make it.</b> Cut &amp; glue your board, cards, and bookmarks.</li>
          <li><b>Walk it.</b> One page a day for 7 days (page {P["days"]}).</li>
          <li><b>Use it.</b> Keep the jar, the plan, and your list where you can reach them.</li>
        </ol>
      </div>
    </div>
    '''
    page(inner, head="Start here")


# ---------------------------------------------------------------- 3 inside
def build_inside():
    rows = [
        ("Rebuild Board + 16 pieces + 2 blank pieces", f"pp. {P['board']}–{P['pieces'] + 1}", "Cardstock"),
        ("16 Word Cards (truth • Scripture • step)", f"pp. {P['cards']}–{P['cards'] + 3}", "Cardstock"),
        ("12 Scripture Bookmarks", f"pp. {P['bookmarks']}–{P['bookmarks'] + 2}", "Cardstock"),
        ("Jar Labels, Tags &amp; Jar Rules", f"p. {P['jar']}", "Cardstock or paper"),
        ("60 Next Right Step Slips", f"pp. {P['slips']}–{P['slips'] + 3}", "Regular paper"),
        ("7-Day Rebuild Plan (daily pages)", f"pp. {P['plan']}, {P['days']}–{P['days'] + 6}", "Regular paper"),
        ("When It Hits (craving &amp; hard-moment plan)", f"p. {P['hit']}", "Regular paper"),
        ("If You Slipped", f"p. {P['slipped']}", "Regular paper"),
        ("Safe People + Support List", f"p. {P['safe']}", "Regular paper"),
        ("Boundary Builder", f"p. {P['bound']}", "Regular paper"),
        ("Practical Rebuild Checklist + Money Reset", f"pp. {P['practical']}–{P['money']}", "Regular paper"),
        ("30-Day Tracker • Prayers • Weekly Review", f"pp. {P['tracker']}–{P['review']}", "Regular paper"),
        ("Certificate of Completion", f"p. {P['cert']}", "Cardstock or paper"),
    ]
    tr = "".join(f"<tr><td class='bx-c'><span class='bx'></span></td><td>{a}</td><td class='c'>{b}</td><td class='c'>{c}</td></tr>"
                 for a, b, c in rows)
    inner = f'''
    {title("What's inside &amp; how to print", "Read this page first. It saves you ink and frustration.")}
    <table class="tbl">
      <thead><tr><th></th><th>Piece</th><th>Where</th><th>Print on</th></tr></thead>
      <tbody>{tr}</tbody>
    </table>
    <div class="cols2 mt">
      <div class="pbox purple">
        <h4>Print it right</h4>
        <ul>
          <li>Print at <b>100% / Actual Size</b>. Do not “fit to page.”</li>
          <li>Pages {P['board']}–{P['jar']}: color on <b>cardstock</b> (65–110 lb).</li>
          <li>Daily &amp; tool pages are <b>low-ink</b>. Print in black &amp; white if you want.</li>
          <li>Print single-sided. Reprint any page as often as you need. It's yours for personal use.</li>
        </ul>
      </div>
      <div class="pbox pink">
        <h4>Supplies (about what's in your junk drawer)</h4>
        <ul>
          <li>Scissors (or a paper trimmer)</li>
          <li>Glue stick or tape</li>
          <li>A jar. A mason jar is perfect.</li>
          <li>Pen, and a hole punch for bookmarks</li>
          <li>Twine, ribbon, or string (optional)</li>
          <li>A frame or a piece of poster board (optional)</li>
        </ul>
      </div>
    </div>
    <div class="scale">
      <div class="ruler"><span>1 in</span></div>
      <div class="scale-t"><b>Scale check.</b> This bar should measure exactly 1 inch on your print. If it doesn't, turn off “fit” or “shrink to printable area” and print again.
      Your pieces &amp; board only line up at 100%.</div>
    </div>
    <div class="fine">Not medical or mental-health treatment. Faith-centered creative and educational tool. No outcome is promised.
    Digital PDF download; nothing physical ships. Scripture quotations are from the King James Version (public domain).</div>
    '''
    page(inner, head="Inside")


# ---------------------------------------------------------------- 4 plan
def build_plan():
    trs = ""
    for d in DAYS:
        words = ", ".join(WORDS[i - 1][0] for i in d["pieces"])
        trs += (f"<tr><td class='dn'>{d['n']}</td><td><b>{d['theme']}</b></td>"
                f"<td>{words}</td><td class='c'>{d['bm']}</td><td class='c'>p. {P['days'] + d['n'] - 1}</td>"
                f"<td class='wr'></td></tr>")
    inner = f'''
    {title("Your 7-day rebuild", "Sixteen pieces. Seven days. One honest step at a time.")}
    <table class="tbl plan">
      <thead><tr><th>Day</th><th>Theme</th><th>Pieces to place</th><th>Bookmark</th><th>Page</th><th>Date done</th></tr></thead>
      <tbody>{trs}</tbody>
    </table>
    <div class="cols2 mt">
      <div class="pbox teal">
        <h4>Each day, about 20–30 minutes</h4>
        <ol>
          <li>Read the note. Read the Scripture twice.</li>
          <li>Write your three answers. Short is fine.</li>
          <li>Glue the day's piece(s) on your board.</li>
          <li>Read the day's word card and bookmark.</li>
          <li>Pull one slip from the jar and do it.</li>
          <li>Pray it. Check your boxes.</li>
        </ol>
      </div>
      <div class="pbox pink">
        <h4>Rules of the week</h4>
        <ul>
          <li><b>Miss a day?</b> Do the next one. Don't restart. Don't quit.</li>
          <li><b>Rough day?</b> Do the first box and place one piece. That counts.</li>
          <li><b>Don't do it perfect.</b> Do it honest.</li>
          <li><b>Don't do it alone.</b> Tell one safe person you're doing this.</li>
        </ul>
      </div>
    </div>
    <div class="callout">
      <b>Before you start:</b> if you're in danger, thinking about hurting yourself, or in withdrawal from alcohol or benzodiazepines
      (which can be medically dangerous to stop suddenly), <b>get medical help first.</b> Call 988, 911, or SAMHSA at 1-800-662-4357.
      The rebuild will still be here. Full list on page {P['safe']}.
    </div>
    <div class="mt why">
      <div class="lbl">Why I'm rebuilding (write it now; read it when it gets hard):</div>
      {lines(4)}
    </div>
    <div class="fields mt"><div class="f">Start date:</div><div class="f">My safe person:</div></div>
    '''
    page(inner, head="Plan")


# ---------------------------------------------------------------- 5 board
def build_board():
    inner = f'''
    <div class="board-title">
      <div class="bt-a">7HE H0LY R3UP</div>
      <div class="bt-b">Rebuild One Piece at a Time</div>
    </div>
    <div class="board-wrap">{board_svg()}</div>
    <div class="cols2 boardnote">
      <div class="pbox purple sm">
        <h4>Make your board</h4>
        <ol>
          <li>Print this page on cardstock. Mount on poster board or a frame back if you want it sturdy.</li>
          <li>Cut the pieces from pages {P['pieces']}–{P['pieces'] + 1}. <b>Easy cut:</b> trim along the dotted squares. <b>Puzzle cut:</b> cut the whole shape.</li>
          <li>Each day, glue the day's piece(s) on the matching number.</li>
        </ol>
      </div>
      <div class="pbox pink sm">
        <h4>Why a board?</h4>
        <p>On hard days you won't feel progress. The board will show it. Every piece you glue is proof you did the work,
        even the day you didn't feel like it.</p>
        <div class="fields"><div class="f">Started:</div><div class="f">Finished:</div></div>
      </div>
    </div>
    '''
    page(inner, cls="boardpage", foot=True)


# ---------------------------------------------------------------- 6-7 pieces
def build_pieces():
    tiles = []
    for i, (w, *_rest) in enumerate(WORDS):
        r, c = divmod(i, 4)
        tiles.append(piece_svg(r, c, w, i + 1, FILLS[i % 4]))
    tiles.append(piece_svg(0, 1, "", 0, "#fffdf9", blank=True))
    tiles.append(piece_svg(1, 2, "", 0, "#fffdf9", blank=True))
    for pg in range(2):
        chunk = tiles[pg * 9:(pg + 1) * 9]
        cells = "".join(f'<div class="pc">{t}</div>' for t in chunk)
        note = ("Cut on the solid line for a puzzle piece, or on the dotted square for easy pieces. Glue on the board at the matching number."
                if pg == 0 else
                "Pieces 10–16 + two blank pieces. Write your own word on the blank ones (the words only you know) and glue them in the margin or on the back of your frame.")
        inner = f'''
        {title(f"Word pieces {pg + 1} of 2", note)}
        <div class="pgrid">{cells}</div>
        <div class="scissors">✂ &nbsp;cut along the lines&nbsp; ✂</div>
        '''
        page(inner, cls="piecepage", head="Cut & glue")


# ---------------------------------------------------------------- 8-11 cards
def build_cards():
    def card(i, w):
        word, truth, verse, ref, action = w
        ic = ["anchor", "vine", "cross", "sun"][i % 4]
        colr = ["#d6598f", "#7a4c9e", "#2f9e98", "#4a6486"][i % 4]
        return f'''
        <div class="card" style="--c:{colr}">
          <div class="card-top"><span class="cn">#{i + 1}</span>{icon(ic, colr, 30)}</div>
          <div class="cword">{e(word)}</div>
          <div class="ctruth">{e(truth)}</div>
          <div class="cverse">“{e(verse)}”<span class="cref">— {e(ref)} (KJV)</span></div>
          <div class="cact"><b>Today's step</b><span>{e(action)}</span><i></i><i></i></div>
        </div>'''
    for pg in range(4):
        cs = "".join(card(pg * 4 + k, WORDS[pg * 4 + k]) for k in range(4))
        inner = f'''
        {title(f"Word cards {pg * 4 + 1}–{pg * 4 + 4}", "Cut on the dotted lines. Keep in order or shuffle. Pull one when you need a word.")}
        <div class="cgrid">{cs}</div>
        '''
        page(inner, cls="cardpage", head="Word cards")


# ---------------------------------------------------------------- 12-14 bookmarks
def build_bookmarks():
    def bm(i, b):
        theme, ref, txt, ic, prompt = b
        colr = ["#d6598f", "#7a4c9e", "#2f9e98", "#4a6486"][i % 4]
        cam = camo(160, 60, 100 + i, ["#f4c9dc", "#dcc5ee", "#c1e6e3", "#f8d9c4"], n=14)
        return f'''
        <div class="bm" style="--c:{colr}">
          <div class="hole"></div>
          <div class="bm-camo">{cam}</div>
          <div class="bm-theme">{e(theme)}</div>
          <div class="bm-ico">{icon(ic, colr, 46)}</div>
          <div class="bm-ref">{e(ref)}</div>
          <div class="bm-txt">{e(txt)}</div>
          <div class="bm-pr"><b>Today I'm choosing:</b><span>{e(prompt)}</span><i></i><i></i></div>
          <div class="bm-br">7HE H0LY R3UP</div>
        </div>'''
    for pg in range(3):
        bs = "".join(bm(pg * 4 + k, BOOKMARKS[pg * 4 + k]) for k in range(4))
        inner = f'''
        {title(f"Scripture bookmarks {pg * 4 + 1}–{pg * 4 + 4}", "Cut on the lines. Punch the circle. Add ribbon or twine. Give one away.")}
        <div class="bmrow">{bs}</div>
        <div class="fine center">Scripture from the King James Version (public domain). Cardstock recommended.</div>
        '''
        page(inner, cls="bmpage", head="Bookmarks")


# ---------------------------------------------------------------- 15 jar
def build_jar():
    labels = ["Next Right Step", "Honest Steps", "Pull One", "Just Start", "Done Jar"]
    lab = "".join(f'<div class="jlabel"><span>{e(t)}</span></div>' for t in labels)
    tags = "".join(f'<div class="jtag">{icon("anchor", "#7a4c9e", 30)}<b>{t}</b></div>'
                   for t in ["Still here.\nStill His.", "One piece\nat a time.", "Next right\nstep.", "Small steps\nstill count."])
    tags = tags.replace("\n", "<br>")
    legend = "".join(f'<span class="lg" style="--c:{c}">{k}</span>' for k, (c, _) in SLIPS.items())
    inner = f'''
    {title("The Next Right Step jar", "For the moments you don't know what to do next.")}
    <div class="cols2">
      <div class="pbox teal">
        <h4>Set it up</h4>
        <ol>
          <li>Cut the slips on pages {P['slips']}–{P['slips'] + 3}. Fold each in half.</li>
          <li>Drop them in a jar. Cut a label below, tape or glue it on.</li>
          <li>Set an empty <b>Done Jar</b> beside it.</li>
        </ol>
      </div>
      <div class="pbox pink">
        <h4>The rules of the jar</h4>
        <ol>
          <li><b>Pull one.</b> Don't shop for a better one. (If a slip isn't safe for you, put it back and pull again.)</li>
          <li><b>Do just that one,</b> even if it's five minutes.</li>
          <li><b>Move it to the Done Jar.</b> Watch it fill.</li>
        </ol>
      </div>
    </div>
    <div class="lbl mt">Jar labels: cut on the border</div>
    <div class="jlabels">{lab}</div>
    <div class="lbl mt">Gift tags: punch the top, tie to the jar</div>
    <div class="jtags">{tags}</div>
    <div class="lbl mt">Slip colors</div>
    <div class="legend">{legend}</div>
    <div class="fine">Body = take care of the temple. Mind = quiet the noise. Spirit = get with God. People = don't isolate. Practical = handle life.</div>
    '''
    page(inner, cls="jarpage", head="Jar")


# ---------------------------------------------------------------- 16-19 slips
def build_slips():
    allslips = []
    for k, (c, items) in SLIPS.items():
        for it in items:
            allslips.append((k, c, it))
    # interleave categories so every page has a mix
    cats = list(SLIPS.keys())
    ordered = []
    by = {k: [(k, c, it) for (kk, c, it) in allslips if kk == k] for k in cats}
    for i in range(12):
        for k in cats:
            ordered.append(by[k][i])
    for pg in range(4):
        chunk = ordered[pg * 15:(pg + 1) * 15]
        cells = ""
        for k, c, it in chunk:
            cells += (f'<div class="slip" style="--c:{c}"><div class="stag">{k}</div>'
                      f'<div class="stxt">{e(it)}</div></div>')
        note = "Cut on the dotted lines, fold, and drop in your jar." if pg < 3 else \
            "Slips 46–60. Bonus: make it yours. Write your own on the last blank ones."
        inner = f'''
        {title(f"Next Right Step slips {pg + 1} of 4", note)}
        <div class="sgrid">{cells}</div>
        '''
        page(inner, cls="slippage", head="Slips")
    # patch: last slip page gets no blank ones in grid; blank slips are on this page's header note only


# ---------------------------------------------------------------- 20-26 days
def build_days():
    for d in DAYS:
        chips = "".join(f'<span class="chip">#{i} {e(WORDS[i - 1][0])}</span>' for i in d["pieces"])
        pr = ""
        for j, q in enumerate(d["prompts"], 1):
            pr += f'<div class="q"><span class="qn">{j}</span><span class="qt">{e(q)}</span></div>{lines(2)}'
        scale = "".join(f'<span>{k}</span>' for k in range(0, 11))
        inner = f'''
        <div class="dayhead">
          <div class="daytag">DAY {d['n']}</div>
          <div class="daytheme">{e(d['theme'])}</div>
          <div class="dayfields"><div class="f">Date:</div></div>
        </div>
        <div class="chips">Place on your board: {chips}
          <span class="chip alt">Bookmark: {e(d['bm'])}</span></div>
        <div class="note"><b>Hellshaker says:</b> {e(d['note'])}</div>
        <div class="verse">“{e(d['verse'])}”<span>— {e(d['ref'])} (KJV). Read it twice, slowly.</span></div>
        <div class="work"><div class="lbl">Do the work</div>{pr}</div>
        <div class="dayrow">
          <div class="pbox teal sm">
            <h4>Pray it</h4>
            <p class="pray">{e(d['prayer'])}</p>
          </div>
          <div class="pbox pink sm">
            <h4>Pull one slip</h4>
            <p>Draw one from the jar. Do it. Write what it was:</p>
            <div class="ln"></div><div class="ln"></div>
          </div>
        </div>
        <div class="meter">
          <div class="mt1">Craving / stress today (0 = none, 10 = max)</div>
          <div class="scale10"><em>AM</em>{scale}<em>PM</em>{scale}</div>
        </div>
        <div class="checks">{boxes(["Prayed", "Moved my body", "Ate real food", "Talked to a person", "Kept my word", "Slept / rested", "Placed my piece", "Took one honest step"])}</div>
        <div class="hardbox"><b>If today was hard:</b> {e(d['hard'])}</div>
        '''
        page(inner, cls="daypage", head="7-day rebuild")


# ---------------------------------------------------------------- 27 when it hits
def build_hit():
    steps = [
        ("STOP", "Say it out loud: “This is a wave, not the ocean.” Set a 15-minute timer. You are not deciding anything until it rings."),
        ("NAME", "What is this? Run HALT: Hungry? Angry? Lonely? Tired? What set it off: a person, a place, a smell, a memory, a text?"),
        ("MOVE", "Change your room. Cold water on your face. Walk outside. Your body needs a new scene before your mind can follow."),
        ("CALL", "Call or text a person from page 29. Can't reach them? Call the next one. Leave a message. Keep going down the list."),
        ("PRAY", "Short and honest: “Lord, this wave is bigger than me. You aren't. Hold me till it passes.”"),
        ("WAIT", "Let the timer run. Cravings rise, peak, and fall. Most crest well before 30 minutes. Then pull a slip and do it."),
    ]
    cards = "".join(f'<div class="st"><div class="stn">{i}</div><div><b>{a}</b><span>{b}</span></div></div>'
                    for i, (a, b) in enumerate(steps, 1))
    inner = f'''
    {title("When It Hits", "Your plan for the next fifteen minutes. Fill this out while you're calm.")}
    <div class="steps6">{cards}</div>
    <div class="cols2 mt">
      <div class="pbox purple sm">
        <h4>Fill in before you need it</h4>
        <div class="lbl">My danger times:</div>{lines(1)}
        <div class="lbl">My top triggers (people, places, feelings):</div>{lines(2)}
        <div class="lbl">Three things I'll do instead:</div>{lines(3)}
      </div>
      <div class="pbox pink sm">
        <h4>My reasons (read these)</h4>
        {lines(6)}
      </div>
    </div>
    <div class="callout red">
      <b>If it's beyond you: get help now.</b> Call or text <b>988</b> (suicide &amp; crisis), call <b>911</b> for an emergency or overdose,
      or call SAMHSA at <b>1-800-662-4357</b> (free, 24/7, treatment referral). Calling for help isn't failing. It's the plan working.
      <br><b>Medical note:</b> stopping alcohol or benzodiazepines suddenly can cause seizures and can be life-threatening. Talk to a doctor or detox program first.
      If opioids or fentanyl are anywhere in your story: tolerance drops fast, so don't use alone, and ask a pharmacist about naloxone (Narcan).
    </div>
    '''
    page(inner, head="When It Hits")


# ---------------------------------------------------------------- 28 slipped
def build_slipped():
    inner = f'''
    {title("If You Slipped", "Relapse is not resignation. Shame says hide. God says come.")}
    <div class="lead">I understand why it happened. And you are still responsible for what you do next. Both are true. Start here.</div>
    <div class="steps6 two">
      <div class="st"><div class="stn">1</div><div><b>Get safe first</b><span>Are you in danger, or is anyone else? Overdose signs (can't wake, slow or no breathing, blue lips) mean call 911 now.</span></div></div>
      <div class="st"><div class="stn">2</div><div><b>Tell someone today</b><span>Not next week. Call a person from page 29. Say: “I slipped, and I need you.” Secrets are where a slip becomes a spiral.</span></div></div>
      <div class="st"><div class="stn">3</div><div><b>Refuse the shame spiral</b><span>“I did something wrong” is true and fixable. “I am wrong” is a lie. Confess it to God. He is not surprised, and He is not leaving.</span></div></div>
      <div class="st"><div class="stn">4</div><div><b>Find the pattern</b><span>What came before? Which hour, feeling, person, place? Write it below. A slip is information.</span></div></div>
      <div class="st"><div class="stn">5</div><div><b>Change one thing</b><span>One boundary, one habit, one hour, one contact. Not ten. One.</span></div></div>
      <div class="st"><div class="stn">6</div><div><b>Take the next right step</b><span>Pull a slip. Drink water. Eat. Sleep. Go to the meeting. Get back to the board. Piece by piece.</span></div></div>
    </div>
    <div class="cols2 mt">
      <div class="pbox purple sm">
        <h4>What happened (just the facts)</h4>{lines(4)}
        <div class="lbl">What came right before it:</div>{lines(2)}
      </div>
      <div class="pbox teal sm">
        <h4>What I'm changing</h4>{lines(3)}
        <div class="lbl">Who I told and when:</div>{lines(2)}
      </div>
    </div>
    <div class="callout">
      <b>Harm-reduction truth:</b> after time away, your tolerance is lower and the risk of overdose is higher. Never use alone. Keep naloxone (Narcan) close;
      many pharmacies provide it without a prescription. And a slip is a good time to talk to your counselor, doctor, or treatment program about your plan.
    </div>
    <div class="verse">“For a just man falleth seven times, and riseth up again.”<span>— Proverbs 24:16 (KJV)</span></div>
    '''
    page(inner, head="If You Slipped")


# ---------------------------------------------------------------- 29 safe people
def build_safe():
    rows = "".join("<tr><td></td><td></td><td></td><td></td></tr>" for _ in range(6))
    hot = [
        ("988", "Suicide &amp; Crisis Lifeline. Call or text 988, 24/7."),
        ("911", "Emergency, overdose, or immediate danger."),
        ("1-800-662-4357", "SAMHSA National Helpline. Free, confidential, 24/7 treatment referral."),
        ("1-800-799-7233", "National Domestic Violence Hotline. Or text START to 88788."),
        ("1-888-373-7888", "National Human Trafficking Hotline. Or text 233733."),
        ("1-800-222-1222", "Poison Control."),
        ("211", "Local help with food, housing, and more."),
    ]
    hh = "".join(f"<div class='hl'><b>{a}</b><span>{b}</span></div>" for a, b in hot)
    inner = f'''
    {title("Safe people &amp; support", "Fill this out today. Screenshot it. Put the numbers in your phone.")}
    <table class="tbl fill">
      <thead><tr><th style="width:28%">Name</th><th style="width:22%">Number</th><th style="width:26%">Good for (talk, ride, pray, practical)</th><th>Best times to call</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <div class="fine">A safe person is honest, doesn't use you, doesn't shame you, and can keep a confidence. It's okay if your list starts with one name and a hotline.</div>
    <div class="cols2 mt">
      <div class="pbox purple sm">
        <h4>My meetings, groups &amp; appointments</h4>
        {lines(6)}
      </div>
      <div class="pbox teal sm">
        <h4>My local ones</h4>
        <div class="lbl">Counselor / clinic:</div>{lines(1)}
        <div class="lbl">Sponsor / group leader:</div>{lines(1)}
        <div class="lbl">Church / faith community:</div>{lines(1)}
        <div class="lbl">Nearest ER / crisis center:</div>{lines(1)}
      </div>
    </div>
    <div class="lbl mt">Hotlines (U.S.)</div>
    <div class="hotgrid">{hh}</div>
    <div class="fine">Outside the U.S.? Search “crisis line” plus your country. Numbers can change; check that they still work before you need them.</div>
    '''
    page(inner, head="Safe people")


# ---------------------------------------------------------------- 30 boundaries
def build_bound():
    lev = [
        ("Open", "Trusted. Safe. Consistent. Full access to my life."),
        ("Limited", "Time-limited, in public, or with a third person. Trust is being rebuilt."),
        ("Distance", "Text or brief contact only. No private time. No money. No favors."),
        ("Closed", "No contact. No explanation owed. Safety comes first."),
    ]
    lv = "".join(f"<div class='lev l{i}'><b>{a}</b><span>{b}</span></div>" for i, (a, b) in enumerate(lev))
    rows = "".join("<tr><td></td><td></td><td></td><td></td></tr>" for _ in range(4))
    inner = f'''
    {title("Boundary Builder", "Forgiveness is not access. Grace is not enabling. A boundary is not hatred.")}
    <div class="lead">Understanding why someone is the way they are isn't the same as letting them back in. You can love them, pray for them, and keep the gate locked.</div>
    <div class="levels">{lv}</div>
    <table class="tbl fill tall mt">
      <thead><tr><th style="width:18%">Person / situation</th><th style="width:22%">What keeps happening</th><th style="width:16%">Access level</th><th>My boundary, in one sentence &amp; what I'll do if it's crossed</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <div class="cols2 mt">
      <div class="pbox pink sm">
        <h4>Sentences you can steal</h4>
        <ul>
          <li>“I love you, and I won't be around when you're using.”</li>
          <li>“I forgive you. I'm not available for that anymore.”</li>
          <li>“No, I can't. I'm not explaining.”</li>
          <li>“I'll talk when we can both be calm.”</li>
          <li>“I'm not lending money. That's my answer.”</li>
        </ul>
      </div>
      <div class="pbox teal sm">
        <h4>Read this twice</h4>
        <ul>
          <li>You don't need permission to protect yourself.</li>
          <li>Boundaries are for <b>your</b> behavior, not controlling theirs.</li>
          <li>If someone is dangerous, <b>don't confront them.</b> Make a safety plan with the hotline on page {P['safe']}.</li>
          <li>Going back before you're ready doesn't make you weak. Start again.</li>
        </ul>
      </div>
    </div>
    '''
    page(inner, head="Boundaries")


# ---------------------------------------------------------------- 31 practical
def build_practical():
    groups = [
        ("Papers", ["State ID or driver's license", "Social Security card", "Birth certificate (copy is fine)", "Insurance / Medicaid card", "List of my medications and doses", "A folder to keep it all together"]),
        ("Health", ["Primary care visit booked", "Dentist or vision (when ready)", "Counselor or recovery program", "Support group or meeting on my calendar", "Naloxone / medicine plan discussed with a pharmacist"]),
        ("Home", ["A safe place to sleep tonight", "Clear out things tied to the old life", "Food for the next 3 days", "Phone charged, numbers saved", "Call 211 if I need housing or food help"]),
        ("Work &amp; money", ["Resume started", "One application this week", "Bills listed with due dates (p. " + str(P['money']) + ")", "One phone call to a creditor or agency", "Open a basic bank account if I don't have one"]),
        ("Legal", ["Know every court and probation date", "Keep copies of paperwork", "Legal aid number saved (search “legal aid” + my county)", "Ask before I sign anything I don't understand"]),
        ("Faith &amp; people", ["Find one church, group, or study to try", "Pray at the same time daily", "One friend who is safe and sober", "Serve one small way this month"]),
    ]
    cols = ""
    for name, items in groups:
        cols += f'<div class="pbox purple sm"><h4>{name}</h4>{boxes(items)}</div>'
    inner = f'''
    {title("Practical rebuild checklist", "Prayer and paperwork go together. Check them off as you go.")}
    <div class="cols2 gap">{cols}</div>
    <div class="callout">
      <b>Don't do it all this week.</b> Pick <b>three</b> boxes. Do those. Then pick three more. Anybody who's ever rebuilt a life did it in small piles of paper and phone calls.
    </div>
    <div class="lbl mt">My three for this week:</div>{lines(3)}
    '''
    page(inner, head="Practical rebuild")


# ---------------------------------------------------------------- 32 money
def build_money():
    bills = "".join("<tr><td></td><td></td><td></td><td class='c'><span class='bx'></span></td></tr>" for _ in range(9))
    inner = f'''
    {title("Money reset", "One page. No shame. Just numbers and the next call.")}
    <div class="cols2">
      <div class="pbox teal sm">
        <h4>Money coming in this month</h4>
        <div class="fields"><div class="f">Work / benefits:</div><div class="f">$</div></div>
        <div class="fields"><div class="f">Other:</div><div class="f">$</div></div>
        <div class="fields"><div class="f"><b>Total in:</b></div><div class="f">$</div></div>
      </div>
      <div class="pbox pink sm">
        <h4>Must-pay first</h4>
        <ul>
          <li>Housing / shelter</li>
          <li>Utilities &amp; phone</li>
          <li>Food</li>
          <li>Transportation to work / meetings</li>
          <li>Court fines, child support, medicine</li>
        </ul>
      </div>
    </div>
    <table class="tbl fill mt">
      <thead><tr><th style="width:42%">Bill / debt</th><th style="width:18%">Amount</th><th style="width:22%">Due date</th><th class="c">Paid</th></tr></thead>
      <tbody>{bills}</tbody>
    </table>
    <div class="cols2 mt">
      <div class="pbox purple sm">
        <h4>The one call I'll make</h4>
        <div class="lbl">Who I'm calling &amp; when:</div>{lines(1)}
        <div class="lbl">What I'll say (write it first):</div>{lines(3)}
        <div class="fine">Many creditors, landlords, and agencies will set up a payment plan if you call before you're behind, or right after.</div>
      </div>
      <div class="pbox teal sm">
        <h4>Cut &amp; stack</h4>
        <div class="lbl">One thing I'm stopping spending on:</div>{lines(1)}
        <div class="lbl">What that money will go to:</div>{lines(1)}
        <div class="lbl">Goal for the next 30 days ($ or a bill paid):</div>{lines(2)}
      </div>
    </div>
    <div class="fine">Stewardship: what you do with a little shows what you're ready for. “He that is faithful in that which is least is faithful also in much.” (Luke 16:10, KJV)</div>
    '''
    page(inner, head="Money reset")


# ---------------------------------------------------------------- 33 tracker
def build_tracker():
    cols = ["Pray", "Move", "Eat", "Reach", "Keep", "Step"]

    def block(a, b):
        head = "".join(f"<th>{c}</th>" for c in cols)
        rows = "".join(f"<tr><td class='dn2'>{d}</td>" + "".join("<td><span class='bx'></span></td>" for _ in cols) + "</tr>"
                       for d in range(a, b + 1))
        return f"<table class='trk'><thead><tr><th>Day</th>{head}</tr></thead><tbody>{rows}</tbody></table>"
    inner = f'''
    {title("30-day tracker", "Fill a box for each thing you did. Don't chase perfect. Chase pattern.")}
    <div class="trkwrap">{block(1, 15)}{block(16, 30)}</div>
    <div class="legendline"><b>Pray</b> talked to God • <b>Move</b> walked/stretched • <b>Eat</b> real food • <b>Reach</b> talked to a person • <b>Keep</b> kept my word • <b>Step</b> one honest step</div>
    <div class="cols2 mt">
      <div class="pbox pink sm"><h4>Day 7 note to myself</h4>{lines(3)}</div>
      <div class="pbox teal sm"><h4>Day 30 note to myself</h4>{lines(3)}</div>
    </div>
    <div class="fine center">“I didn't become her overnight. I became her every time I chose not to go back.”</div>
    '''
    page(inner, head="30-day tracker")


# ---------------------------------------------------------------- 34 prayers
def build_prayers():
    prs = [
        ("Morning prayer", "Renew me",
         "Lord, it's me again. Thank You for another morning I didn't earn and You gave me anyway. Your mercies are new, and I need every one. "
         "Order my day. Guard my mouth, my eyes, and my hands. Show me the one honest step in front of me and give me the guts to take it. "
         "I'm not asking for a perfect day, just a faithful one. In Jesus' name, amen.", "Lamentations 3:22–23"),
        ("When the craving comes", "Hold me",
         "Jesus, this wave is bigger than me, and You are not. I'm not going to pretend I'm fine. I need You right now. Get me to my phone, get me to a person, "
         "get me through fifteen minutes. Break what's trying to break me. Set my feet on a rock. And Lord, if somebody's hearing this from the floor tonight, "
         "meet them there. Amen.", "Psalm 40:2"),
        ("Night prayer", "Let it go",
         "Father, here's my day: the good, the ugly, and the part I'd rather skip. Where I did right, thank You. Where I fell short, I'm not hiding it. Forgive me, and "
         "help me forgive myself where You already have. I hand You what I can't fix tonight. Guard my sleep. Tomorrow, let me wake up still Yours. Amen.", "1 John 1:9"),
        ("For the ones I love", "Cover them",
         "God, I lift up the people I love: the ones still bound, the ones who are far, the ones I have to love from a distance. Protect them. Send them people who will tell them the truth. "
         "Give me wisdom for what to do and what to leave with You. I trust You with what I can't control. Amen.", "Psalm 107:14"),
    ]
    blocks = ""
    for h, s, body, ref in prs:
        blocks += (f'<div class="prayer"><div class="ph"><b>{h}</b><em>{s}</em></div>'
                   f'<p>{e(body)}</p><div class="pref">{e(ref)}</div></div>')
    inner = f'''
    {title("Prayers for the rebuild", "Say them out loud. Change the words. Make them yours.")}
    {blocks}
    <div class="lbl mt">My own prayer:</div>{lines(4)}
    '''
    page(inner, head="Prayers")


# ---------------------------------------------------------------- 35 review
def build_review():
    inner = f'''
    {title("Weekly review", "Ten minutes, once a week. Print as many as you need.")}
    <div class="fields"><div class="f">Week of:</div><div class="f">Day count:</div></div>
    <div class="cols2 mt">
      <div class="pbox teal sm"><h4>What I did right</h4>{lines(4)}</div>
      <div class="pbox pink sm"><h4>Where I struggled (the pattern)</h4>{lines(4)}</div>
      <div class="pbox purple sm"><h4>One thing I'm changing</h4>{lines(3)}</div>
      <div class="pbox teal sm"><h4>Where I saw God</h4>{lines(3)}</div>
    </div>
    <div class="cols2 mt">
      <div class="pbox purple sm">
        <h4>How am I, 1–10?</h4>
        <div class="rate"><span>Body</span>{"".join(f"<i>{k}</i>" for k in range(1, 11))}</div>
        <div class="rate"><span>Mind</span>{"".join(f"<i>{k}</i>" for k in range(1, 11))}</div>
        <div class="rate"><span>Spirit</span>{"".join(f"<i>{k}</i>" for k in range(1, 11))}</div>
        <div class="rate"><span>People</span>{"".join(f"<i>{k}</i>" for k in range(1, 11))}</div>
        <div class="rate"><span>Practical</span>{"".join(f"<i>{k}</i>" for k in range(1, 11))}</div>
      </div>
      <div class="pbox pink sm">
        <h4>Scripture I'm carrying</h4>{lines(2)}
        <h4 style="margin-top:8px">Who I'm thanking / encouraging</h4>{lines(2)}
      </div>
    </div>
    <div class="pbox teal mt"><h4>My three next right steps</h4>
      {boxes(["<span class='ln inl'></span>", "<span class='ln inl'></span>", "<span class='ln inl'></span>"])}
    </div>
    <div class="fine center">Need to talk to someone about this week? Page {P['safe']}.</div>
    '''
    page(inner, head="Weekly review")


# ---------------------------------------------------------------- 36 certificate
def build_cert():
    inner = f'''
    <div class="cert">
      <div class="cert-in">
        <div class="ct-brand">7HE H0LY R3UP</div>
        <div class="ct-big">Rebuild One Piece at a Time</div>
        <div class="ct-sm">CERTIFICATE OF COMPLETION</div>
        <div class="ct-pre">Presented to</div>
        <div class="ct-line"></div>
        <div class="ct-name">(your name)</div>
        <p class="ct-body">for showing up, telling the truth, and building something honest,<br>one piece at a time.<br>
        <i>“For who hath despised the day of small things?” — Zechariah 4:10</i></p>
        <div class="ct-sign">
          <div><div class="ct-line s"></div><span>Date</span></div>
          <div><div class="ct-line s"></div><span>Signed (you)</span></div>
          <div><div class="ct-line s"></div><span>Witness (someone who saw you do it)</span></div>
        </div>
        <div class="ct-tag">Still here. Still His. Let's rebuild.</div>
      </div>
    </div>
    '''
    page(inner, cls="certpage", foot=False)


# ---------------------------------------------------------------- 37 closing
def build_closing():
    inner = f'''
    {title("What now?", "Finishing the week is the start. Here's how you keep building.")}
    <div class="cols2">
      <div class="pbox pink"><h4>1. Go another round</h4>
        <p>Reprint the daily pages and go again. The second time through, you'll be honest about things you weren't ready to touch the first time.</p></div>
      <div class="pbox teal"><h4>2. Keep the tools close</h4>
        <p>Keep the jar on your counter, the plan (p. {P['hit']}) on your fridge, the safe list (p. {P['safe']}) in your phone, and a bookmark in your Bible.</p></div>
      <div class="pbox purple"><h4>3. Bring somebody with you</h4>
        <p>Print a second kit. Hand someone a bookmark. Recovery isn't a solo mission, and your worst chapter may be somebody's way out.</p></div>
      <div class="pbox pink"><h4>4. Keep getting help</h4>
        <p>A kit is a companion. Keep going to meetings, counseling, church, doctors. Faith and practical help are not enemies.</p></div>
    </div>
    <div class="closing-quote">
      <p>Broken by overdose. Rebuilt by God. Unapologetically shaking hell for every soul still bound.</p>
      <p class="sm">D.O.A. is God's favorite starting point. Bando 2 Vineyard. Corner 2 Crown.</p>
    </div>
    <div class="pbox purple mt"><h4>Questions, or want to tell me how it went?</h4>
      <p>Reply to your order email, or use the Contact link on the 7HE H0LY R3UP store. I read and reply myself as time allows. — Hellshaker</p></div>
    <div class="fine legal">
      © 2026 7HE H0LY R3UP by THKS &amp; CO. All rights reserved. Personal use only. No part of this work may be reproduced, distributed, copied, transmitted,
      resold, or commercially exploited without prior written permission, except as permitted by applicable law. This kit is a faith-centered creative and educational tool.
      It is not medical, mental-health, or legal advice or treatment, and no specific outcome is promised. In an emergency call 911. For 24/7 crisis support call or text 988.
      Scripture quotations are from the King James Version (public domain).
    </div>
    <div class="last-tag">IN MEMORY OF BRANDI RENEE — 12787–121721</div>
    '''
    page(inner, head="Keep building")


# ---------------------------------------------------------------- css
CSS = r'''
@page { size: 8.5in 11in; margin: 0; }
:root{
  --pink:#d6598f; --purple:#7a4c9e; --teal:#2f9e98; --turq:#3fb6b0; --denim:#4a6486;
  --ink:#2b2430; --line:#cfc4d9; --blush:#fdf0f5; --lav:#f6f0fa; --mint:#eaf7f5; --cream:#fffdf9;
}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;background:#e9e2ee;font-family:'Libre Franklin',Arial,sans-serif;color:var(--ink);
  -webkit-print-color-adjust:exact;print-color-adjust:exact;}
.page{width:8.5in;height:11in;position:relative;overflow:hidden;background:#fff;padding:.42in .55in .55in;
  page-break-after:always;break-after:page;margin:0 auto;}
@media screen{.page{margin:.25in auto;box-shadow:0 4px 18px rgba(0,0,0,.18);}}
.topband{position:absolute;left:0;right:0;top:0;height:.09in;background:linear-gradient(90deg,var(--turq),var(--purple) 55%,var(--pink));}
.phead{display:flex;justify-content:space-between;align-items:baseline;margin:.06in 0 .04in;font-size:9px;letter-spacing:2px;font-weight:800;text-transform:uppercase;color:var(--purple);}
.phead .ps{color:var(--denim);}
h2{font-family:'Caveat',cursive;font-size:42px;line-height:1;margin:.02in 0 0;color:var(--pink);font-weight:700;}
.sub{font-size:11.5px;font-weight:600;color:var(--denim);margin:3px 0 10px;}
.foot{position:absolute;left:.55in;right:.55in;bottom:.22in;display:flex;justify-content:space-between;
  font-size:8px;letter-spacing:1.4px;font-weight:700;color:#8b7a99;border-top:1px solid var(--line);padding-top:5px;text-transform:uppercase;}
.fine{font-size:9px;color:#6d6377;line-height:1.4;margin-top:8px;}
.fine.center{text-align:center;}
.mt{margin-top:10px;}
.lbl{font-size:9.5px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;color:var(--denim);margin:6px 0 1px;}
.ln{border-bottom:1px solid var(--line);height:21px;}
.ln.inl{display:inline-block;width:100%;height:14px;}
.fields{display:flex;gap:18px;font-size:11px;font-weight:700;margin:5px 0;}
.fields .f{flex:1;border-bottom:1.5px solid var(--line);padding-bottom:2px;min-height:17px;}
.bx{display:inline-block;width:12px;height:12px;border:1.8px solid var(--ink);border-radius:3px;flex:0 0 auto;vertical-align:middle;}
.ck{display:flex;gap:7px;align-items:flex-start;font-size:10.3px;line-height:1.3;margin:4px 0;}
.ck .bx{margin-top:1px;}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.cols2.gap{gap:9px;}
.pbox{border:1.6px solid var(--line);border-radius:10px;padding:9px 12px 10px;font-size:11px;line-height:1.42;background:#fff;}
.pbox h4{margin:0 0 5px;font-size:10.5px;letter-spacing:1.4px;text-transform:uppercase;font-weight:800;}
.pbox.pink{background:var(--blush);border-color:#efb3cc;} .pbox.pink h4{color:var(--pink);}
.pbox.purple{background:var(--lav);border-color:#cfb5e3;} .pbox.purple h4{color:var(--purple);}
.pbox.teal{background:var(--mint);border-color:#a8dcd7;} .pbox.teal h4{color:var(--teal);}
.pbox.sm{font-size:10.4px;padding:8px 11px 9px;}
.pbox ul,.pbox ol{margin:0;padding-left:16px;} .pbox li{margin:2px 0;}
.pbox p{margin:0 0 4px;}
.callout{margin-top:10px;border:2px solid var(--pink);border-radius:10px;padding:9px 13px;font-size:10.4px;line-height:1.45;background:#fff8fb;}
.callout.red{border-color:#c0392b;background:#fff5f3;}
.lead{font-size:12px;font-weight:600;line-height:1.5;color:#453a52;margin:2px 0 10px;border-left:4px solid var(--turq);padding-left:11px;}
.tbl{width:100%;border-collapse:collapse;font-size:10.6px;}
.tbl th{background:var(--purple);color:#fff;font-size:9px;letter-spacing:1.2px;text-transform:uppercase;padding:6px 8px;text-align:left;}
.tbl td{padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:middle;}
.tbl tr:nth-child(even) td{background:#fbf8fd;}
.tbl .c{text-align:center;} .tbl .bx-c{width:26px;text-align:center;}
.tbl.plan td.dn{font-family:'Caveat',cursive;font-size:24px;font-weight:700;color:var(--pink);text-align:center;width:44px;}
.tbl.plan td{height:34px;} .tbl.plan td.wr{width:78px;}
.tbl.fill td{height:33px;border:1px solid var(--line);} .tbl.fill.tall td{height:62px;}
.tbl.fill tr:nth-child(even) td{background:#fff;}
.scale{display:flex;gap:14px;align-items:center;margin-top:12px;border:1.6px dashed var(--purple);border-radius:10px;padding:9px 12px;}
.ruler{width:1in;height:.32in;border:1.6px solid var(--ink);background:repeating-linear-gradient(90deg,var(--ink) 0,var(--ink) 1px,transparent 1px,transparent .125in);position:relative;flex:0 0 auto;}
.ruler span{position:absolute;bottom:-15px;left:0;font-size:8px;font-weight:800;}
.scale-t{font-size:10px;line-height:1.4;}
/* cover */
.cover{padding:0;background:#f7e9f1;}
.cover .topband{display:none;}
.cover-bg{position:absolute;inset:0;background:#f5dbe8;} .cover-bg svg{display:block;width:100%;height:100%;}
.cover-sun{position:absolute;left:0;right:0;bottom:0;height:4.2in;background:linear-gradient(0deg,rgba(63,182,176,.55),rgba(63,182,176,0) 95%);}
.cover-card{position:absolute;left:.6in;right:.6in;top:.65in;bottom:1.05in;background:rgba(255,253,249,.95);border-radius:20px;border:3px solid var(--purple);
  padding:.42in .5in .3in;box-shadow:0 8px 26px rgba(80,40,110,.25);}
.cv-brand{font-size:17px;font-weight:800;letter-spacing:6px;color:var(--teal);text-align:center;}
.cv-by{font-size:9px;letter-spacing:3px;text-align:center;color:var(--denim);font-weight:700;margin-bottom:.16in;}
.cv-kicker{font-size:11.5px;letter-spacing:3px;font-weight:800;color:var(--pink);text-align:center;}
.cover h1{font-family:'Bebas Neue','Caveat',sans-serif;font-weight:400;font-size:112px;line-height:.9;margin:.16in 0 .08in;text-align:center;color:var(--purple);letter-spacing:1px;}
.cv-tag{font-family:'Caveat',cursive;font-size:42px;text-align:center;color:var(--pink);font-weight:700;margin-bottom:.14in;}
.cv-list{list-style:none;margin:0;padding:.18in .22in;background:var(--lav);border-radius:14px;border:1.6px solid #cfb5e3;font-size:13.4px;line-height:1.55;}
.cv-list li{padding-left:18px;position:relative;margin:2px 0;} .cv-list li:before{content:"";position:absolute;left:2px;top:6px;width:8px;height:8px;background:var(--pink);border-radius:2px;}
.cv-foot{margin-top:.2in;text-align:center;font-size:10px;letter-spacing:1.6px;font-weight:800;color:var(--denim);text-transform:uppercase;}
.cover-tagline{position:absolute;bottom:.68in;left:0;right:0;text-align:center;font-weight:800;letter-spacing:4px;font-size:13px;color:#fff;text-shadow:0 1px 4px rgba(20,60,60,.6);}
.cover-copy{position:absolute;bottom:.14in;left:.6in;right:.6in;font-size:7px;line-height:1.35;color:#fff;text-align:center;text-shadow:0 1px 3px rgba(20,60,60,.6);}
/* letter */
.letter{font-size:11.2px;line-height:1.5;margin:.06in 0 .12in;} .letter p{margin:0 0 7px;}
.letter .sig{font-family:'Caveat',cursive;font-size:24px;line-height:1.05;color:var(--purple);font-weight:700;margin-top:10px;}
.letter .sig span{font-family:'Libre Franklin';font-size:11px;font-weight:700;color:var(--ink);}
/* board */
.boardpage{background:#fffdf9;}
.board-title{text-align:center;margin:.05in 0 .02in;} .bt-a{font-size:11px;letter-spacing:5px;font-weight:800;color:var(--teal);}
.bt-b{font-family:'Caveat',cursive;font-size:46px;font-weight:700;color:var(--pink);line-height:1;}
.board-wrap{display:flex;justify-content:center;border:5px solid var(--teal);border-radius:8px;background:#fff;width:7.1in;margin:0 auto;padding:0;}
.board-wrap svg{display:block;}
.boardnote{margin-top:10px;}
/* pieces */
.pgrid{display:grid;grid-template-columns:repeat(3,2.3in);grid-auto-rows:2.5in;justify-content:center;margin-top:.02in;}
.pc{width:2.3in;height:2.5in;display:flex;align-items:center;justify-content:center;}
.scissors{text-align:center;font-size:9px;letter-spacing:2px;color:#8b7a99;margin-top:3px;font-weight:700;}
.piecepage .sub{font-size:10.5px;}
/* cards */
.cgrid{display:grid;grid-template-columns:3.6in 3.6in;grid-auto-rows:4.5in;gap:0;margin:.03in -.05in 0;justify-content:center;}
.card{border:1.6px dashed #8b7a99;margin:0;padding:.15in .2in .12in;display:flex;flex-direction:column;background:#fff;position:relative;}
.card:before{content:"";position:absolute;left:0;right:0;top:0;height:.09in;background:var(--c);}
.card-top{display:flex;justify-content:space-between;align-items:center;margin-top:.05in;}
.cn{font-size:10px;font-weight:800;color:var(--c);letter-spacing:1px;}
.cword{font-family:'Caveat',cursive;font-size:56px;line-height:1;font-weight:700;color:var(--c);margin:2px 0 6px;}
.ctruth{font-size:15.5px;font-weight:700;line-height:1.4;color:var(--ink);}
.cverse{font-family:'Lora',serif;font-style:italic;font-size:13.2px;line-height:1.45;margin-top:12px;color:#4d4157;border-left:3px solid var(--c);padding-left:10px;}
.cref{display:block;font-family:'Libre Franklin';font-style:normal;font-size:10px;font-weight:700;letter-spacing:.6px;margin-top:4px;color:var(--c);}
.cact{margin-top:auto;background:#faf6fc;border:1.4px solid #ded2e8;border-radius:8px;padding:8px 11px 5px;font-size:12.6px;line-height:1.38;}
.cact b{display:block;font-size:10px;letter-spacing:1.4px;text-transform:uppercase;color:var(--c);margin-bottom:2px;}
.cact i{display:block;border-bottom:1px solid var(--line);height:19px;}
/* bookmarks */
.bmrow{display:flex;gap:.2in;justify-content:center;margin-top:.02in;}
.bm{width:1.6in;height:7.25in;border:1.6px dashed #8b7a99;border-radius:8px;position:relative;padding:.28in .12in .1in;text-align:center;overflow:hidden;background:#fffdf9;}
.hole{position:absolute;top:.09in;left:50%;margin-left:-.07in;width:.14in;height:.14in;border:1.4px dotted #8b7a99;border-radius:50%;}
.bm-camo{position:absolute;left:0;right:0;top:0;height:.62in;opacity:.9;} .bm-camo svg{width:100%;height:100%;display:block;}
.bm:before{content:"";position:absolute;left:0;right:0;top:.62in;height:4px;background:var(--c);}
.bm-theme{position:relative;font-family:'Caveat',cursive;font-size:40px;font-weight:700;color:var(--c);margin-top:.42in;line-height:1;}
.bm-ico{margin:8px 0;height:46px;}
.bm-ref{font-size:10.5px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:var(--c);}
.bm-txt{font-family:'Lora',serif;font-style:italic;font-size:13.6px;line-height:1.5;margin:.08in 0;color:#3f3449;}
.bm-pr{position:absolute;left:.11in;right:.11in;bottom:.3in;border-top:1.6px solid var(--c);padding-top:6px;text-align:left;font-size:10.4px;line-height:1.3;}
.bm-pr b{display:block;font-size:8.8px;letter-spacing:1.1px;text-transform:uppercase;color:var(--c);} .bm-pr i{display:block;border-bottom:1px solid var(--line);height:16px;}
.bm-pr span{display:block;margin-bottom:0;font-weight:600;}
.bm-br{position:absolute;bottom:.08in;left:0;right:0;font-size:7.5px;letter-spacing:2.5px;font-weight:800;color:#a99bb8;}
/* jar */
.jlabels{display:flex;flex-wrap:wrap;gap:.13in;margin-top:4px;}
.jlabel{width:2.25in;height:.85in;border:2px solid var(--purple);border-radius:8px;display:flex;align-items:center;justify-content:center;background:#fff8ee;outline:1.5px dashed #8b7a99;outline-offset:3px;}
.jlabel span{font-family:'Caveat',cursive;font-size:30px;font-weight:700;color:var(--purple);}
.jtags{display:flex;gap:.16in;margin-top:5px;}
.jtag{width:1.55in;height:1.6in;border:1.6px dashed #8b7a99;border-radius:10px 10px 50% 50%/10px 10px 22% 22%;text-align:center;padding-top:.22in;font-size:10px;line-height:1.3;color:var(--purple);background:#fbf3fa;position:relative;}
.jtag:before{content:"";position:absolute;top:.08in;left:50%;margin-left:-.06in;width:.12in;height:.12in;border:1.4px dotted #8b7a99;border-radius:50%;}
.jtag b{display:block;margin-top:4px;font-family:'Caveat',cursive;font-size:20px;line-height:1.05;}
.legend{display:flex;gap:8px;flex-wrap:wrap;margin-top:4px;} .lg{background:var(--c);color:#fff;font-size:9px;font-weight:800;letter-spacing:1.4px;padding:4px 12px;border-radius:14px;}
/* slips */
.sgrid{display:grid;grid-template-columns:repeat(3,2.44in);grid-auto-rows:1.76in;gap:0;justify-content:center;margin-top:.02in;}
.slip{border:1.3px dashed #8b7a99;padding:.11in .13in;position:relative;background:#fff;}
.slip:before{content:"";position:absolute;left:0;top:0;bottom:0;width:.07in;background:var(--c);}
.stag{display:inline-block;background:var(--c);color:#fff;font-size:8.6px;letter-spacing:1.6px;font-weight:800;padding:2px 8px;border-radius:9px;margin-bottom:5px;margin-left:.04in;}
.stxt{font-size:13.6px;line-height:1.4;font-weight:600;margin-left:.04in;color:#2b2430;}
.slippage .sub{margin-bottom:5px;}
/* day pages */
.dayhead{display:flex;align-items:flex-end;gap:12px;margin:.05in 0 4px;}
.daytag{background:var(--pink);color:#fff;font-weight:800;letter-spacing:2px;font-size:12px;padding:5px 13px;border-radius:20px;}
.daytheme{font-family:'Caveat',cursive;font-size:36px;white-space:nowrap;line-height:.95;font-weight:700;color:var(--purple);flex:1;}
.dayfields{width:1.9in;} .dayfields .f{border-bottom:1.5px solid var(--line);font-size:11px;font-weight:700;padding-bottom:2px;}
.chips{font-size:10px;font-weight:700;color:var(--denim);margin:2px 0 7px;display:flex;flex-wrap:wrap;gap:5px;align-items:center;}
.chip{background:var(--lav);border:1.4px solid #cfb5e3;border-radius:12px;padding:2px 9px;color:var(--purple);font-weight:800;font-size:9.6px;}
.chip.alt{background:var(--mint);border-color:#a8dcd7;color:var(--teal);}
.note{background:var(--blush);border-left:5px solid var(--pink);border-radius:6px;padding:8px 12px;font-size:10.6px;line-height:1.48;}
.verse{font-family:'Lora',serif;font-style:italic;font-size:12px;line-height:1.45;margin:8px 4px 4px;color:#3f3449;text-align:center;}
.verse span{display:block;font-family:'Libre Franklin';font-style:normal;font-size:9px;font-weight:800;letter-spacing:1px;color:var(--teal);margin-top:2px;}
.work{margin-top:4px;} .q{display:flex;gap:7px;align-items:flex-start;margin-top:5px;font-size:10.6px;font-weight:700;}
.qn{background:var(--purple);color:#fff;border-radius:50%;width:16px;height:16px;text-align:center;font-size:9.5px;line-height:16px;flex:0 0 auto;margin-top:0;}
.work .ln{height:20px;}
.dayrow{display:grid;grid-template-columns:1.15fr 1fr;gap:9px;margin-top:8px;}
.pray{font-style:italic;font-size:10.3px !important;line-height:1.42;}
.meter{margin-top:8px;} .mt1{font-size:9px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:var(--denim);margin-bottom:2px;}
.scale10{display:flex;gap:3px;align-items:center;font-size:9px;font-weight:700;}
.scale10 span{width:17px;height:17px;border:1.3px solid var(--line);border-radius:50%;text-align:center;line-height:15px;}
.scale10 em{font-style:normal;font-size:8px;font-weight:800;color:var(--purple);margin:0 3px 0 4px;letter-spacing:.8px;}
.checks{display:grid;grid-template-columns:repeat(4,1fr);gap:0 8px;margin-top:6px;}
.hardbox{margin-top:8px;border:1.6px dashed var(--purple);border-radius:8px;padding:6px 11px;font-size:10px;line-height:1.4;background:#fdfbff;}
/* steps */
.steps6{display:grid;grid-template-columns:1fr;gap:6px;} .steps6.two{grid-template-columns:1fr 1fr;gap:7px;}
.st{display:flex;gap:11px;align-items:flex-start;border:1.6px solid var(--line);border-radius:10px;padding:7px 11px;background:#fff;}
.stn{font-family:'Caveat',cursive;font-weight:700;font-size:34px;color:#fff;background:var(--pink);border-radius:50%;width:38px;height:38px;line-height:38px;text-align:center;flex:0 0 auto;}
.st:nth-child(2n) .stn{background:var(--purple);} .st:nth-child(3n) .stn{background:var(--teal);}
.st b{display:block;font-size:12px;letter-spacing:1.4px;text-transform:uppercase;color:var(--ink);margin-bottom:1px;}
.st span{font-size:10.4px;line-height:1.4;display:block;}
.steps6.two .st{padding:6px 9px;} .steps6.two .stn{width:30px;height:30px;line-height:30px;font-size:26px;} .steps6.two .st b{font-size:10.5px;} .steps6.two .st span{font-size:9.8px;}
/* boundaries */
.levels{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;}
.lev{border-radius:9px;padding:7px 9px;font-size:9.6px;line-height:1.35;color:#fff;} .lev b{display:block;font-size:12px;letter-spacing:1.6px;text-transform:uppercase;margin-bottom:2px;}
.lev.l0{background:var(--teal);} .lev.l1{background:var(--denim);} .lev.l2{background:var(--purple);} .lev.l3{background:var(--pink);}
/* hotlines */
.hotgrid{display:grid;grid-template-columns:1fr 1fr;gap:4px 12px;margin-top:3px;}
.hl{display:flex;gap:9px;align-items:baseline;font-size:9.6px;line-height:1.3;border-bottom:1px solid var(--line);padding:3px 0;}
.hl b{color:var(--pink);font-size:12px;min-width:98px;}
/* tracker */
.trkwrap{display:flex;gap:.2in;justify-content:center;}
.trk{border-collapse:collapse;font-size:9px;flex:1;} .trk th{background:var(--purple);color:#fff;padding:4px 2px;font-size:8.6px;letter-spacing:.6px;text-transform:uppercase;}
.trk td{border:1px solid var(--line);text-align:center;height:.44in;padding:0;} .trk td.dn2{font-family:'Caveat',cursive;font-weight:700;font-size:20px;color:var(--pink);width:.4in;}
.trk .bx{width:14px;height:14px;}
.legendline{font-size:9px;text-align:center;margin-top:7px;color:#5b5064;line-height:1.5;}
/* prayers */
.prayer{border:1.6px solid var(--line);border-radius:10px;padding:8px 13px 6px;margin-top:8px;background:#fff;}
.prayer:nth-of-type(odd){background:var(--blush);border-color:#efb3cc;}
.ph{display:flex;justify-content:space-between;align-items:baseline;}
.ph b{font-family:'Caveat',cursive;font-size:26px;color:var(--purple);font-weight:700;} .ph em{font-size:9px;letter-spacing:1.6px;text-transform:uppercase;font-style:normal;font-weight:800;color:var(--teal);}
.prayer p{margin:2px 0 3px;font-size:10.8px;line-height:1.5;font-style:italic;} .pref{font-size:8.6px;letter-spacing:1px;font-weight:800;color:var(--denim);text-align:right;text-transform:uppercase;}
/* review */
.rate{display:flex;align-items:center;gap:2px;font-size:8.6px;margin:5px 0;} .rate span{width:.58in;font-weight:800;letter-spacing:.5px;text-transform:uppercase;font-size:8px;}
.rate i{font-style:normal;width:.185in;height:.185in;border:1.2px solid var(--line);border-radius:50%;text-align:center;line-height:.16in;font-size:7.6px;background:#fff;}
/* certificate */
.certpage{background:#fffdf9;padding:.5in;} .cert{width:100%;height:100%;border:8px double var(--purple);border-radius:8px;padding:.14in;}
.cert-in{border:2px solid var(--pink);height:100%;border-radius:6px;padding:.5in .5in .3in;text-align:center;background:
 radial-gradient(circle at 50% 0%,rgba(63,182,176,.14),transparent 55%);position:relative;}
.ct-brand{font-size:14px;font-weight:800;letter-spacing:7px;color:var(--teal);}
.ct-big{font-family:'Caveat',cursive;font-weight:700;font-size:66px;line-height:.95;color:var(--pink);margin:.4in 0 .1in;}
.ct-sm{font-size:12px;letter-spacing:5px;font-weight:800;color:var(--purple);}
.ct-pre{font-family:'Lora',serif;font-style:italic;font-size:15px;margin-top:.5in;color:#5b5064;}
.ct-line{border-bottom:2px solid var(--ink);width:70%;margin:.42in auto 4px;} .ct-line.s{width:100%;margin:.55in 0 4px;}
.ct-name{font-size:9px;letter-spacing:2px;color:#8b7a99;text-transform:uppercase;font-weight:700;}
.ct-body{font-size:16px;line-height:1.75;margin:.7in .3in 0;font-family:'Lora',serif;color:#3f3449;} .ct-body i{font-size:12px;color:var(--teal);}
.ct-sign{display:grid;grid-template-columns:1fr 1fr 1.3fr;gap:.25in;margin-top:1.1in;font-size:9px;letter-spacing:1.2px;text-transform:uppercase;font-weight:800;color:#6d6377;}
.ct-tag{position:absolute;left:0;right:0;bottom:.26in;font-family:'Caveat',cursive;font-size:30px;font-weight:700;color:var(--purple);}
/* closing */
.closing-quote{margin:12px 0;text-align:center;background:linear-gradient(135deg,var(--purple),var(--pink));color:#fff;border-radius:14px;padding:.22in .35in;}
.closing-quote p{font-family:'Caveat',cursive;font-size:32px;line-height:1.15;font-weight:700;margin:0;} .closing-quote p.sm{font-family:'Libre Franklin';font-size:10px;letter-spacing:2.2px;font-weight:800;margin-top:9px;text-transform:uppercase;}
.legal{font-size:8px;line-height:1.45;}
.last-tag{text-align:center;font-size:9px;letter-spacing:3px;font-weight:800;color:var(--purple);margin-top:10px;}
'''


def build():
    build_cover(); build_welcome(); build_inside(); build_plan(); build_board(); build_pieces()
    build_cards(); build_bookmarks(); build_jar(); build_slips(); build_days(); build_hit(); build_slipped()
    build_safe(); build_bound(); build_practical(); build_money(); build_tracker(); build_prayers()
    build_review(); build_cert(); build_closing()
    assert len(pages) == TOTAL, (len(pages), TOTAL)
    # verify page map
    assert pages[P["board"] - 1].count("boardpage")
    assert pages[P["pieces"] - 1].count("piecepage")
    assert pages[P["cards"] - 1].count("cardpage")
    assert pages[P["bookmarks"] - 1].count("bmpage")
    assert pages[P["jar"] - 1].count("jarpage")
    assert pages[P["slips"] - 1].count("slippage")
    assert pages[P["days"] - 1].count("daypage")
    assert pages[P["cert"] - 1].count("certpage")
    fonts = open(FONTS_CSS, encoding="utf-8").read() if os.path.exists(FONTS_CSS) else ""
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Rebuild One Piece at a Time — The Complete Printable Rebuild Kit | 7HE H0LY R3UP</title>
<meta name="description" content="37-page printable rebuild kit: rebuilding board, word cards, Scripture bookmarks, Next Right Step jar slips, 7-day plan, craving plan, boundary builder, and more." />
<style>
{fonts}
{CSS}
</style>
</head>
<body>
{"".join(pages)}
<script>
function fitAll(){{
  document.querySelectorAll('.fit .zw').forEach(function(w){{
    var pg=w.closest('.page');
    var avail=pg.clientHeight-w.offsetTop-0.66*96;
    var lo=1,hi=1.7;
    for(var i=0;i<14;i++){{
      var mid=(lo+hi)/2; w.style.zoom=mid;
      if(w.getBoundingClientRect().height<=avail) lo=mid; else hi=mid;
    }}
    w.style.zoom=lo;
    w.querySelectorAll('.ruler').forEach(function(r){{r.style.zoom=1/lo;}});
  }});
}}
if(document.fonts&&document.fonts.ready){{document.fonts.ready.then(fitAll);}}else{{window.addEventListener('load',fitAll);}}
</script>
</body>
</html>'''
    out = os.path.join(HERE, "rebuild-one-piece-at-a-time-kit.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    print("wrote", out, len(doc) // 1024, "KB,", len(pages), "pages")


if __name__ == "__main__":
    build()
