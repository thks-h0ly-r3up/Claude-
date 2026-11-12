"""Panel renderers (each draws one 5 x 7.5 in insert)."""
import math
from lib import *


def short_ref(r):
    r = r.split(' (')[0].split(';')[0]
    return r


def table(p, headers, widths, nrows, rowh, hh=15, first_col_fill=None, row_labels=None):
    c = p.c
    sc = p.w / sum(widths)
    widths = [w * sc for w in widths]
    p.need(hh + nrows * rowh, 'table')
    top = p.cy
    c.setFillColor(T_TURQ)
    c.rect(p.L, top - hh, p.w, hh, stroke=0, fill=1)
    x = p.L
    for h, w in zip(headers, widths):
        tracked(c, x + 4, top - 10, h.upper(), 'SansB', 5.6, TEAL, 0.6)
        x += w
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.roundRect(p.L, top - hh - nrows * rowh, p.w, hh + nrows * rowh, 4, stroke=1, fill=0)
    for r in range(nrows + 1):
        y = top - hh - r * rowh
        c.line(p.L, y, p.R, y)
    x = p.L
    for w in widths[:-1]:
        x += w
        c.line(x, top, x, top - hh - nrows * rowh)
    if row_labels:
        c.setFillColor(TEAL)
        c.setFont('SansB', 7)
        for r, lab in enumerate(row_labels):
            c.drawString(p.L + 4, top - hh - r * rowh - rowh / 2 - 2.5, lab)
    p.cy = top - hh - nrows * rowh - 8


def grid(p, labels, cols, h):
    rows = [labels[i:i + cols] for i in range(0, len(labels), cols)]
    for r in rows:
        p.cols(r, h, n=cols)


def numbered(p, n, gap=18, start=1):
    c = p.c
    p.need(n * gap, 'numbered')
    for i in range(n):
        p.cy -= gap
        c.setFillColor(GOLD)
        c.setFont('SansB', 7)
        c.drawString(p.L, p.cy + 3, str(start + i))
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(p.L + 12, p.cy, p.R, p.cy)
    p.cy -= 4


def day_circles(p, n=30, cols=10, r=11):
    c = p.c
    step = p.w / cols
    rows = math.ceil(n / cols)
    p.need(rows * (r * 2 + 6), 'days')
    for i in range(n):
        cx = p.L + step * (i % cols) + step / 2
        cy = p.cy - r - (i // cols) * (r * 2 + 6)
        c.setStrokeColor(TURQ)
        c.setFillColor(WHITE)
        c.setLineWidth(0.9)
        c.circle(cx, cy, r, stroke=1, fill=1)
        c.setFillColor(GRAY)
        c.setFont('Sans', 6.8)
        c.drawCentredString(cx, cy - 2.4, str(i + 1))
    p.cy -= rows * (r * 2 + 6) + 6


# ---------------------------------------------------------------- women
def woman_a(p, w, idx, total):
    name, ref, note, found, q, step = w
    p.tag = name
    p.header(f'Women of the Word · {idx} of {total}', name, ref, size=15)
    if note:
        p.note(note, None, T_PEACH, 'BodyI', 8.4)
    p.label('Where we meet her')
    p.para(found, size=9, after=4)
    spare = p.room() - 206
    nl = max(4, int(spare / 16.5))
    n1 = int(round(nl * 0.62))
    p.field('Who is in the scene?', 1)
    p.field('Where and when?', 1)
    p.field('What happened, in my words', n1)
    p.field('Words that stand out', nl - n1)
    p.cols(['What she lost', 'What she did', 'Who saw her'], 52)
    p.checks(['Read the chapters before and after.', 'Compare two editions. Cite which.', 'Doctrinal question? Ask clergy or a scholar.'], 8.3, 2)


def woman_b(p, w):
    name, ref, note, found, q, step = w
    p.tag = name + ' B'
    p.header('Sit With Her · S.O.A.P.', name, None, size=15)
    p.para(q, 'BodyI', 9.3, TEAL, after=6)
    p.soap(ref=short_ref(ref), weights=(2.2, 3, 3, 2.6), reserve=p.soft_h(step) + 4)
    p.soft(step)


# ---------------------------------------------------------------- topics
def topic_a(p, d):
    p.tag = d['title']
    p.header(d['kicker'], d['title'], d['sub'], size=15)
    intro = d['intro']
    if intro.startswith('Content note') or intro.startswith('Textual'):
        p.note(intro, None, T_PEACH, 'BodyI', 8.6)
    elif intro:
        p.para(intro, size=9.2, after=5)
    refs = d['refs']
    check_h = 52
    share = (p.room() - check_h - 6) / max(1, len(refs))
    for ref, hint in refs:
        p.c.setFillColor(TEAL)
        p.c.setFont('BodyB', 9.6)
        p.c.drawString(p.L, p.cy - 9, ref)
        p.cy -= 12
        p.c.setFillColor(GRAY)
        p.c.setFont('BodyI', 8.2)
        p.c.drawString(p.L, p.cy - 8, 'Look for: ' + hint)
        p.cy -= 10
        n = max(1, int((share - 24) / 16.5))
        p.lines(min(n, 6))
        p.cy -= 2
    p.checks(['Read two chapters around it.', 'Compare two editions. Cite which.', 'Doctrinal question? Ask clergy or a scholar.'], 8.2, 1.5)


def topic_b(p, d):
    p.tag = d['title'] + ' B'
    p.header('Reflection', 'Sit With It', d['title'], size=15)
    n_prompts = len(d['prompts'])
    reserve = 82 + (46 if d.get('res') else 0)
    share = (p.room() - reserve) / n_prompts
    for q in d['prompts']:
        p.para(q, 'BodyB', 9.2, TEAL, after=1)
        n = max(2, int((share - 22) / 16.5))
        p.lines(n)
    if d.get('res'):
        p.note(d['res'], 'Help is real', T_GOLD, 'Body', 8.2)
    p.soft(d['step'], d['low'])


# ---------------------------------------------------------------- custom B panels
def b_craving(p, d):
    p.header('Tool', 'Craving Log', 'Notice it. Name it. Choose the next ten minutes.', 15)
    table(p, ['When / where', 'What I felt', 'What I needed', 'What I did'], [1, 1, 1, 1], 6, 46)
    p.soft(d['step'], d['low'])


def b_exits(p, d):
    p.header('Tool', 'My Exit Plan', 'Write it now, while it is quiet.', 15)
    p.field('The hours when it is hardest for me', 2)
    p.field('Exit one: I will', 2)
    p.field('Exit two: I will call or text', 1)
    p.field('Exit three: I will go to', 1)
    p.field('What I will do for ten minutes before I decide anything', 2)
    p.field('What I will tell myself when the craving says “just once”', 2)
    p.soft(d['step'], d['low'])


def b_days(p, d):
    p.header('Tool', '30 Days of Mercy', 'Color in a circle each day you showed up. Count mercy, not only days.', 15)
    day_circles(p, 30, 10, 11)
    p.note('If you slip, you start a new row. The days before still happened. You are not starting from zero.', None, T_GOLD, 'BodyI', 8.4)
    p.field('Milestones I want to remember (date and what it felt like)', 5)
    p.soft(d['step'], d['low'])


def b_slip(p, d):
    p.header('Tool', 'If I Slip: Mercy Plan', 'Lamentations 3:22–23 · Proverbs 24:16 · Micah 7:8', 15)
    steps = ['Breathe and drink water. Put your feet on the floor.', 'Tell one person today. Use the Team page.', 'Remove access if you can, for tonight.', 'Do the next small right thing: shower, food, bed.', 'Write what happened without calling yourself names.']
    for i, s in enumerate(steps, 1):
        p.c.setFillColor(TURQ)
        p.c.circle(p.L + 7, p.cy - 8, 7, stroke=0, fill=1)
        p.c.setFillColor(WHITE)
        p.c.setFont('SansB', 8)
        p.c.drawCentredString(p.L + 7, p.cy - 10.5, str(i))
        p.c.setFillColor(INK)
        p.c.setFont('Body', 9.2)
        p.c.drawString(p.L + 20, p.cy - 10, s)
        p.cy -= 22
    p.field('What happened, in plain words', 3)
    p.field('What I needed that I did not have', 2)
    p.field('The next right thing', 1)
    p.verify('Relapse is common in recovery and does not erase progress. Tell your care team.')


def b_triggers(p, d):
    p.header('Tool', 'Triggers & Replacements', 'People · Places · Times · Feelings', 15)
    table(p, ['Trigger', 'What I will do instead'], [1, 1.2], 9, 38)
    p.soft('Circle your top two triggers. Tell your support person about them.', 'Circle just one.')


def b_testimony(p, d):
    p.header('Tool', 'My Story in Three Lines', 'Share it only if and when it feels safe.', 15)
    p.field('Before', 4)
    p.field('The turn', 4)
    p.field('Now', 4)
    p.note('Spiritual language does not replace treatment, a sponsor, or a doctor. It can walk alongside them.', None, T_GOLD, 'BodyI', 8.4)
    p.soft(d['step'], d['low'])


def b_icancant(p, d):
    p.header('Tool', 'I Can’t / I Can', 'Love with edges.', 15)
    for _ in range(5):
        p.c.setFillColor(TEAL)
        p.c.setFont('BodyB', 9)
        p.c.drawString(p.L, p.cy - 10, 'I can’t')
        p.cy -= 14
        p.lines(1, 15)
        p.c.setFillColor(TEAL)
        p.c.setFont('BodyB', 9)
        p.c.drawString(p.L, p.cy - 6, 'but I can')
        p.cy -= 10
        p.lines(1, 15)
        p.cy -= 4
    p.note(d['res'], 'Support', T_GOLD, 'Body', 8.2)
    p.soft(d['step'], d['low'])


def b_lament(p, d):
    p.header('Tool', 'My Lament', 'Five lines. The cry first, then the rest.', 15)
    for lab, n in [('The cry: God, ...', 3), ('The complaint: Here is what hurts', 3), ('The ask: Please', 3), ('The trust: I remember', 3), ('The thanks: Already, You have', 3)]:
        p.field(lab, n)
    p.soft(d['step'], d['low'])


def b_mercies(p, d):
    p.header('Tool', 'What I Call to Mind', 'True today · Mercies already received', 15)
    p.label('Three true things about today')
    numbered(p, 3)
    p.label('Mercies already received (thank You for ...)')
    numbered(p, 6)
    p.soft(d['step'], d['low'])


def b_blueprint(p, d):
    p.header('Tool', 'The Rebuild Blueprint', 'One stone at a time.', 15)
    c = p.c
    y = p.cy
    bw, bh = 46, 13
    for r in range(3):
        for k in range(int(p.w // bw)):
            off = (bw / 2) if r % 2 else 0
            x = p.L + k * bw - off
            if x < p.L - 1 or x + bw > p.R + 1:
                continue
            c.setStrokeColor(PEACH)
            c.setFillColor(T_PEACH)
            c.rect(x, y - bh * (r + 1), bw - 2, bh - 2, stroke=1, fill=1)
    p.cy -= bh * 3 + 8
    grid(p, ['Rubble I can name', 'What still stands', 'My next stone (this week)', 'Who helps me build'], 2, 92)
    p.soft(d['step'], d['low'])


def b_bothsides(p, d):
    p.header('Tool', 'Both-Sides Check', 'Target the quote, not the whole community.', 15)
    p.field('1. What was claimed? (exact words, who, when)', 2)
    p.field('2. What does the source say in context? (cite edition)', 3)
    p.field('3. What is another credible view? (cite its source)', 3)
    p.field('4. What is the practical difference for my life?', 2)
    p.field('5. My next step', 1)
    p.verify('Check both sides, including mine. Open the source and check the pattern yourself.')
    p.soft(d['step'], d['low'])


def b_safetyplan(p, d):
    p.header('Tool', 'My Safety Plan', 'Fill in while you are okay. Use when you are not.', 15)
    p.field('1. My warning signs', 2, 15)
    p.field('2. Things I can do on my own (water, shower, walk, music)', 2, 15)
    p.field('3. People and places that help me feel okay', 2, 15)
    p.field('4. People I can ask for help (name and number)', 2, 15)
    p.field('5. Crisis line: 988 (US) · Other: ____________', 1, 15)
    p.field('6. Making my space safer', 2, 15)
    p.field('One reason I am still here', 1, 15)
    p.note(d['res'], 'Help is real', T_GOLD, 'Body', 8.2)


def b_careteam(p, d):
    p.header('Tool', 'My Care Team', 'Prayer and care can live together.', 15)
    p.cols(['Doctor / psychiatrist', 'Therapist / counselor'], 62)
    p.cols(['Priest / pastor', 'Peer or support group'], 62)
    p.field('Next appointment or next step (date)', 1)
    p.field('What I want them to know', 3)
    p.field('A question I am afraid to ask', 2)
    p.note(d['res'], 'Help is real', T_GOLD, 'Body', 8.2)
    p.soft(d['step'], d['low'])


# ---------------------------------------------------------------- custom A panels
def a_halt(p, d):
    p.header(d['kicker'], d['title'], d['sub'], 15)
    p.para(d['intro'], size=9, after=4)
    table(p, ['Day', 'H', 'A', 'L', 'T', 'Urge 0–5', 'Note'], [26, 22, 22, 22, 22, 44, 150], 14, 21)
    p.para('H = Hungry · A = Angry · L = Lonely · T = Tired. Mark any that fit.', 'BodyI', 8.2, GRAY, after=3)


def a_team(p, d):
    p.header(d['kicker'], d['title'], d['sub'], 15)
    table(p, ['Name', 'Role', 'Phone', 'Call me when ...'], [80, 58, 74, 100], 6, 36)
    p.note('Stopping alcohol or benzodiazepines suddenly can be life-threatening. Ask a medical provider before you stop.', 'Medical safety', T_PEACH, 'Body', 8.4)
    p.note('SAMHSA Helpline (US): 1-800-662-4357, free, 24/7 treatment referral and information. 988: crisis call or text.', 'Help is real', T_GOLD, 'Body', 8.2)
    p.field('One thing I will ask my team for this week', 2)


def a_ground(p, d):
    p.header(d['kicker'], d['title'], d['sub'], 15)
    p.note('Keep your eyes open if that feels safer. You can stop at any step. Pausing is a good choice.', 'Invitation', T_TURQ, 'Body', 8.6)
    for n, lab in [(5, 'things I can see'), (4, 'things I can touch'), (3, 'things I can hear'), (2, 'things I can smell'), (1, 'thing I can taste, or one slow breath')]:
        p.c.setFillColor(TURQ)
        p.c.setFont('Head', 13)
        p.c.drawString(p.L, p.cy - 13, str(n))
        p.c.setFillColor(INK)
        p.c.setFont('Body', 9)
        p.c.drawString(p.L + 18, p.cy - 11, lab)
        p.cy -= 15
        p.lines(1 if n < 4 else 2, 15)
    p.field('A prayer of thanks, short and true', 2)
    p.soft('Press your feet into the floor. Name the room you are in. Drink water.', 'Place a hand on your chest and breathe out slowly once.')


def a_window(p, d):
    p.header(d['kicker'], d['title'], d['sub'], 15)
    c = p.c
    bands = [('Too much', 'racing, panicked, angry, on guard', T_PEACH), ('My window', 'present, able to think and feel', T_TURQ), ('Too little', 'numb, foggy, frozen, far away', T_GOLD)]
    h = 58
    for name, sub, col in bands:
        c.setFillColor(col)
        c.roundRect(p.L, p.cy - h, p.w, h, 6, stroke=0, fill=1)
        tracked(c, p.L + 10, p.cy - 16, name.upper(), 'SansB', 8, TEAL, 1.2)
        c.setFillColor(INK)
        c.setFont('BodyI', 9)
        c.drawString(p.L + 10, p.cy - 30, sub)
        c.setStrokeColor(WHITE)
        c.setLineWidth(1)
        c.line(p.L + 10, p.cy - 46, p.R - 10, p.cy - 46)
        p.cy -= h + 5
    p.note('These are not diagnoses. They are a way to notice what is happening in my body so I can respond with care.', None, T_GOLD, 'BodyI', 8.4)
    p.field('My signs of too much (body, thoughts, behavior)', 3)
    p.field('My signs of too little', 3)


def b_safemoves(p, d):
    p.header('Tool', 'My Safe Moves', 'Choose what fits the moment. Skip what does not.', 15)
    p.label('When it is too much')
    p.checks(['Cold water on hands or face', 'Long slow exhale, longer than the inhale', 'Name five colors in the room', 'Step outside or open a window', 'Call or text: ____________'], 8.8, 2)
    p.label('When it is too little')
    p.checks(['Stretch or walk to the next room', 'Warm drink or something with a strong smell', 'Music I like', 'Pet Big Boy, or a pet, or something soft', 'Text one safe person: “Thinking of you.”'], 8.8, 2)
    p.field('My own safe moves', 3)
    p.soft('Pick the one move you are most likely to actually do. Put it on a sticky note.', 'Just say its name.')


def a_circles(p, d):
    p.header(d['kicker'], d['title'], d['sub'], 15)
    c = p.c
    cx = (p.L + p.R) / 2
    cy = p.cy - 128
    for r, col, lab in [(125, T_GOLD, 'Light touch'), (92, T_PEACH, 'Trusted, with care'), (58, T_TURQ, 'Safe people'), (26, WHITE, 'Me')]:
        c.setFillColor(col)
        c.setStrokeColor(TURQ)
        c.setLineWidth(0.9)
        c.circle(cx, cy, r, stroke=1, fill=1)
    for r, lab in [(125, 'LIGHT TOUCH'), (92, 'TRUSTED, WITH CARE'), (58, 'SAFE PEOPLE')]:
        tracked(c, cx, cy + r - 11, lab, 'SansB', 5.8, TEAL, 0.8, 'c')
    tracked(c, cx, cy - 2.5, 'ME', 'SansB', 8, TEAL, 1.2, 'c')
    p.cy -= 262
    p.field('Names in my safe circle', 2)
    p.field('Someone I need to move one ring outward, and why', 2)


def b_nopractice(p, d):
    p.header('Tool', 'Practice My No', 'A boundary is what I will do, not what I demand they do.', 15)
    p.field('A boundary I need', 2)
    p.field('What I will say (short, no explanation required)', 2)
    p.field('If they push, I will', 2)
    p.field('What I will do if the boundary is crossed', 2)
    p.field('Who has my back', 1)
    p.note('Examples: “I can’t make it.” “I’m not discussing that.” “I’ll call you when I’m ready.”', 'Try one', T_GOLD, 'BodyI', 8.4)
    p.soft('Say one “no” sentence out loud once, alone.', 'Whisper it.')


def b_bodymap(p, d):
    p.header('Tool', 'Body Check-In', 'Mark where you feel it: X tension · O numb · + ease', 15)
    c = p.c
    cx = (p.L + p.R) / 2
    top = p.cy - 4
    c.setStrokeColor(TURQ)
    c.setLineWidth(1.4)
    c.setFillColor(WHITE)
    c.circle(cx, top - 22, 18, stroke=1, fill=1)
    c.roundRect(cx - 34, top - 120, 68, 90, 18, stroke=1, fill=1)
    c.line(cx - 34, top - 52, cx - 74, top - 112)
    c.line(cx + 34, top - 52, cx + 74, top - 112)
    c.line(cx - 16, top - 120, cx - 22, top - 190)
    c.line(cx + 16, top - 120, cx + 22, top - 190)
    p.cy -= 200
    p.field('One word for how I feel', 1)
    p.field('What my body might need', 2)
    p.field('One kind thing I can do next', 2)
    p.soft('Pick one kind thing and do it for two minutes.', 'Put a hand where it hurts and say “I see you.”')


# ---------------------------------------------------------------- core templates
def verse_head(p, title, sub):
    p.header('Verse Map', title, sub, 15)


def vm_classic(p):
    verse_head(p, 'Classic Verse Map', 'One verse, mapped slowly.')
    p.field('Verse (edition, translator, book chapter:verse)', 3)
    grid(p, ['Who', 'What', 'Where', 'When'], 2, 46)
    p.field('Key words', 2)
    p.field('What it shows me about God', 2)
    p.field('What it shows me about my situation', 2)
    p.field('Cross-references', 2)
    p.checks(['Read the chapters before and after.'], 8.4)


def vm_word(p):
    verse_head(p, 'Word Study', 'Slow down on one word.')
    p.cols(['The word (as in my edition)', 'Original word / script'], 50)
    p.label('Language and source')
    p.hchecks(['Hebrew', 'Greek', 'Ge’ez', 'Other: ______'])
    p.field('Transliteration and basic meaning (cite lexicon)', 2)
    p.field('Where else it appears', 3)
    table(p, ['Edition / translator', 'How it renders the word'], [1, 1.2], 3, 32)
    p.field('What I learned', 2)
    p.verify('Check at least two sources. Note the edition, translator, and year.')


def vm_web(p):
    verse_head(p, 'Cross-Reference Web', 'Let Scripture explain Scripture.')
    c = p.c
    cx = (p.L + p.R) / 2
    cy = p.cy - 118
    R = 96
    sats = []
    for i in range(6):
        a = math.radians(90 + i * 60)
        sats.append((cx + math.cos(a) * R * 1.15, cy + math.sin(a) * R))
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    for sx, sy in sats:
        c.line(cx, cy, sx, sy)
    for sx, sy in sats:
        c.setFillColor(WHITE)
        c.setStrokeColor(TURQ)
        c.circle(sx, sy, 31, stroke=1, fill=1)
        c.setStrokeColor(LINE)
        c.line(sx - 22, sy - 4, sx + 22, sy - 4)
        c.line(sx - 22, sy - 14, sx + 22, sy - 14)
    c.setFillColor(T_TURQ)
    c.setStrokeColor(TURQ)
    c.circle(cx, cy, 36, stroke=1, fill=1)
    tracked(c, cx, cy - 2, 'MY VERSE', 'SansB', 6.5, TEAL, 0.8, 'c')
    p.cy -= 238
    p.field('What do these connections show?', 3)
    p.field('Where do they disagree or tension? (check both sides)', 2)


def vm_compare(p):
    verse_head(p, 'Compare the Editions', 'Where does an edition omit, shift, or soften a passage?')
    table(p, ['Edition / translator', 'Year', 'Key phrase as rendered'], [90, 30, 150], 4, 44)
    p.field('What differs?', 3)
    p.label('Does it change the meaning?')
    p.hchecks(['No', 'A little', 'A lot'])
    p.field('Which source tradition is each edition based on?', 2)
    p.field('Who could I ask? (clergy, scholar, library)', 1)
    p.verify('Cite exact edition, translator, book, chapter, verse. Use Western editions to document omissions, not to replace your tradition’s text.')


def vm_oia(p):
    verse_head(p, 'Observe · Interpret · Apply', 'Three steps, in order.')
    c = p.c
    for i, (lab, hint) in enumerate([('Observe', 'What does it say? List what is there.'), ('Interpret', 'What did it mean to the first hearers?'), ('Apply', 'What is one real step for me?')]):
        off = i * 22
        h = 118
        c.setFillColor(WHITE)
        c.setStrokeColor(TURQ)
        c.setLineWidth(0.9)
        c.roundRect(p.L + off, p.cy - h, p.w - off, h, 6, stroke=1, fill=1)
        tracked(c, p.L + off + 8, p.cy - 14, f'{i + 1}. {lab}'.upper(), 'SansB', 7.6, TEAL, 1.1)
        c.setFont('BodyI', 8)
        c.setFillColor(GRAY)
        c.drawString(p.L + off + 8, p.cy - 26, hint)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        for k in range(5):
            y = p.cy - 42 - k * 15
            c.line(p.L + off + 8, y, p.R - 8, y)
        p.cy -= h + 8
    p.field('Verse', 1)


def vm_chapter(p):
    verse_head(p, 'Passage Outline', 'See the shape before the details.')
    p.field('Book and chapter (edition)', 1)
    table(p, ['Verses', 'Heading / what happens'], [50, 230], 9, 29)
    p.field('The big idea in one sentence', 2)


def vm_prayer(p):
    verse_head(p, 'Pray the Verse', 'Let the text give you the words.')
    p.field('Verse (edition, book chapter:verse)', 3)
    p.field('What it says about God', 2)
    p.field('Thank You for ...', 2)
    p.field('Help me with ...', 2)
    p.field('I give You ...', 2)
    p.field('Amen. One line I want to remember', 1)


def vm_two(p):
    verse_head(p, 'Two Women, One Page', 'Compare, honor, and notice.')
    c = p.c
    cx = (p.L + p.R) / 2
    cy = p.cy - 100
    for dx, col in [(-48, T_TURQ), (48, T_PEACH)]:
        c.setFillColor(col)
        c.setStrokeColor(TURQ)
        c.setLineWidth(0.9)
        c.circle(cx + dx, cy, 88, stroke=1, fill=1)
    tracked(c, cx - 96, cy + 70, 'HER:', 'SansB', 6.8, TEAL, 1, 'c')
    tracked(c, cx + 96, cy + 70, 'HER:', 'SansB', 6.8, TEAL, 1, 'c')
    tracked(c, cx, cy + 10, 'BOTH', 'SansB', 6.8, TEAL, 1, 'c')
    p.cy -= 200
    p.field('Their stories (refs)', 2)
    p.field('What they share', 2)
    p.field('What surprised me', 2)
    p.soft('Write one respectful sentence to each woman.', 'Write one name.')


def soap_page(p, ref=None, sub='Scripture · Observation · Application · Prayer', weights=(3, 4, 3, 3), title='Classic S.O.A.P.', reserve=0, kicker='S.O.A.P.'):
    p.header(kicker, title, sub, 15)
    p.field('Date and place', 1)
    p.soap(ref=ref, weights=weights, reserve=reserve)


def soap_soft(p):
    p.header('S.O.A.P.', 'S.O.A.P. with Thanks', 'Start with what God has already done.', 15)
    p.field('Thanks first: one completed mercy', 2)
    p.soap(weights=(3, 3.6, 3, 2.6), reserve=84)
    p.soft('Do the one step you wrote under Application. Or half of it.', 'Write it on your hand.')


def soap_tracker(p):
    p.header('S.O.A.P.', '7-Day S.O.A.P. Tracker', 'Small and steady beats big and quit.', 15)
    table(p, ['Day', 'Scripture', 'One word I noticed', 'One step', 'Prayed'], [30, 76, 76, 76, 28], 7, 44,
          row_labels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    p.note('Missed a day? Skip it. Start where you are.', None, T_GOLD, 'BodyI', 8.6)
    p.field('What I noticed this week', 2)


def soap_ground(p):
    p.header('S.O.A.P.', 'S.O.A.P. with Grounding', 'Settle first. Then read.', 15)
    p.note('Sit. Breathe in for four, out for six, three times. Eyes open or closed. Press your feet to the floor.', 'Sanctuary', T_TURQ, 'Body', 8.8)
    p.field('A prayer of thanks, short and true', 2)
    p.soap(weights=(3, 3.6, 3, 3), reserve=0)


def mini_soap(p, n, lines):
    c = p.c
    total = n
    h_each = (p.room() - 4) / total
    for k in range(total):
        c.setFillColor(T_TURQ)
        c.roundRect(p.L, p.cy - 14, p.w, 14, 4, stroke=0, fill=1)
        tracked(c, p.L + 6, p.cy - 10, 'DATE ________   REF ____________________', 'SansB', 6, TEAL, 0.6)
        p.cy -= 18
        for ltr, ln in zip('SOAP', lines):
            c.setFillColor(TURQ)
            c.setFont('Head', 9)
            c.drawString(p.L, p.cy - 11, ltr)
            c.setStrokeColor(LINE)
            c.setLineWidth(0.5)
            for j in range(ln):
                y = p.cy - 13 - j * 14.5
                c.line(p.L + 14, y, p.R, y)
            p.cy -= 15 * ln - (ln - 1) * 0.5
            p.cy -= 4
        p.cy -= 6
    p.cy -= 0


def soap_mini2(p):
    p.header('S.O.A.P.', 'Mini S.O.A.P. x 2', None, 14)
    mini_soap(p, 2, [2, 3, 2, 2])


def soap_mini3(p):
    p.header('S.O.A.P.', 'Mini S.O.A.P. x 3', None, 14)
    mini_soap(p, 3, [1, 2, 1, 2])


def soap_boxes(p):
    p.header('S.O.A.P.', 'S.O.A.P. Boxes', 'For a visual thinker.', 15)
    c = p.c
    p.field('Verse reference', 1)
    h = (p.room() - 14) / 2 - 6
    for row in range(2):
        top = p.cy
        for col in range(2):
            ltr, name = 'SOAP'[row * 2 + col], ['Scripture', 'Observation', 'Application', 'Prayer'][row * 2 + col]
            x = p.L + col * (p.w / 2 + 3)
            w = p.w / 2 - 3
            p.box('', h, x=x, w=w, cy=top, advance=False)
            c.setFillColor(T_TURQ)
            c.setFont('Head', 40)
            c.drawString(x + w - 38, top - 38, ltr)
            tracked(c, x + 7, top - 12, name.upper(), 'SansB', 6.6, TEAL, 0.9)
        p.cy -= h + 6


def soap_art(p):
    p.header('S.O.A.P.', 'S.O.A.P. + Lettering Box', 'Letter the verse, then work it.', 15)
    p.box('Hand-lettering box', 150, stroke=TURQ)
    p.soap(weights=(1.6, 3, 2.6, 2.6), reserve=0)


def soap_teaching(p):
    p.header('S.O.A.P.', 'S.O.A.P. for a Teaching', 'Sermon, class, or podcast.', 15)
    p.cols(['Speaker', 'Date and place'], 34)
    p.field('The main passage (cite edition)', 1)
    p.field('The big idea in one sentence', 2)
    p.soap(weights=(2.2, 3.4, 3, 2.6), reserve=36)
    p.verify('Check both sides, including mine. Check the claim against the source.')


def soap_hard(p):
    p.header('S.O.A.P.', 'S.O.A.P. for a Hard Passage', 'You can stop at any point.', 15)
    p.note('Some passages hurt. Check in with yourself before you read.', 'Check-in', T_PEACH, 'Body', 8.6)
    p.checks(['I can stay with this today.', 'I need a break. That is okay.'], 8.8, 2)
    p.soap(weights=(2.2, 3.4, 3, 3), reserve=36)
    p.field('Who I will tell about this', 1)


def card_soap(c, x, y, w=360, h=252):
    c.setStrokeColor(TURQ)
    c.setLineWidth(0.8)
    c.setDash(1.2, 3)
    c.roundRect(x + 6, y + 6, w - 12, h - 12, 8, stroke=1, fill=0)
    c.setDash()
    tracked(c, x + 16, y + h - 20, 'S.O.A.P.', 'SansB', 8, GOLD, 1.5)
    tracked(c, x + w - 16, y + h - 20, 'DATE ________   REF __________________', 'SansB', 6, TEAL, 0.5, 'r')
    secs = [('S', 'Scripture'), ('O', 'Observation'), ('A', 'Application'), ('P', 'Prayer')]
    sy = y + h - 34
    sh = (h - 54) / 4
    for ltr, name in secs:
        c.setFillColor(TURQ)
        c.setFont('Head', 10)
        c.drawString(x + 16, sy - 12, ltr)
        c.setFillColor(GRAY)
        c.setFont('BodyI', 7.5)
        c.drawString(x + 30, sy - 11, name)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(x + 82 if False else x + 30, sy - 24, x + w - 16, sy - 24)
        c.line(x + 30, sy - 24 - 15, x + w - 16, sy - 24 - 15) if sh > 52 else None
        sy -= sh


def weekly(p):
    p.header('Reflection', 'Weekly Reflection', 'Week of ______________', 15)
    p.field('What I am thankful for (mercy already received)', 3)
    p.field('What was hard', 2)
    p.field('What my body told me', 2)
    p.field('Where I saw God, or where I did not and want to', 2)
    circle_scale(p, 'My energy this week', 'low', 'high')
    p.soft('Choose one thing for next week. Put it on a sticky note.', 'Choose half of one thing.')


def monthly(p):
    p.header('Reflection', 'Monthly Review', 'Month of ______________', 15)
    p.field('Three things I am grateful for', 3)
    p.field('What I learned about myself', 2)
    p.field('What I let go of', 2)
    p.field('What I want to keep', 2)
    p.field('Verses that stayed with me', 2)
    p.field('One small goal for next month', 1)
    circle_scale(p, 'How steady I felt this month', 'rocky', 'steady')


def thanks_log(p):
    p.header('Reflection', 'Thank You, Lord: Completed Mercy', 'List what God has already done.', 15)
    table(p, ['Date', 'What You did / what I received'], [48, 232], 13, 28)
    p.note('Gratitude and grief can sit at the same table. You do not have to pick.', None, T_GOLD, 'BodyI', 8.4)


def answered(p):
    p.header('Reflection', 'Answered Prayers', 'Including the “not yet” and the “not like that.”', 15)
    table(p, ['Asked', 'My prayer', 'Answered', 'How'], [36, 120, 36, 96], 8, 36)
    p.field('A prayer that was answered differently than I expected', 3)


def bothsides_page(p):
    p.header('Reflection', 'Both-Sides Check', 'Quote, source, other view, difference, step.', 15)
    p.field('1. The claim (exact words, who, when)', 2)
    p.field('2. The source in context (edition, translator, book chapter:verse)', 3)
    p.field('3. Another credible view (cite its source)', 3)
    p.field('4. The practical difference for my life', 3)
    p.field('5. My next step (10 minutes or less)', 1)
    p.verify('Check both sides, including mine. Read the sources. Truth can withstand honest questions.')


def teaching_notes(p):
    p.header('Reflection', 'Teaching Notes', None, 15)
    p.cols(['Speaker / source', 'Date'], 34)
    p.field('Main passage (edition)', 1)
    p.field('Notes', 8)
    p.box('Verify before I repeat it', 80, T_GOLD)
    p.checks(['Read the passage in context.', 'Compare two editions.'], 8.4, 1)


def feelings(p):
    p.header('Reflection', 'Feelings & Needs Check-In', 'Circle what is true. Pick one.', 15)
    words = ['tired', 'angry', 'sad', 'scared', 'numb', 'ashamed', 'hopeful', 'grateful', 'lonely', 'calm', 'overwhelmed', 'relieved', 'hurt', 'restless', 'safe', 'unsure', 'proud', 'grieving']
    c = p.c
    x = p.L
    y = p.cy - 4
    for wd in words:
        wd_w = pdfmetrics.stringWidth(wd, 'Body', 9.2) + 18
        if x + wd_w > p.R:
            x = p.L
            y -= 24
        c.setStrokeColor(TURQ)
        c.setFillColor(WHITE)
        c.setLineWidth(0.8)
        c.roundRect(x, y - 15, wd_w, 18, 9, stroke=1, fill=1)
        c.setFillColor(INK)
        c.setFont('Body', 9.2)
        c.drawString(x + 9, y - 9.5, wd)
        x += wd_w + 6
    p.cy = y - 28
    p.cols(['What I feel', 'What I need'], 52)
    p.field('One kind thing I will do', 2)
    p.field('Who I will tell', 1)
    p.soft('Name one feeling to a safe person, or to God.', 'Circle it again.')


def evening(p):
    p.header('Reflection', 'Evening Rest Prayer', 'Put the day down.', 15)
    p.field('What was heavy today', 3)
    p.field('What was good, even a little', 3)
    p.field('What I am giving back to God tonight', 3)
    p.field('What I want to ask for tomorrow', 2)
    p.note('Lord, I did what I could. I rest now. Amen.', 'A short prayer', T_TURQ, 'BodyI', 9)
    p.soft('Turn off one screen ten minutes earlier.', 'Close your eyes for three breaths.')


def letter_god(p):
    p.header('Reflection', 'A Letter to God', 'Say it plainly. Lament is allowed.', 15)
    p.para('Dear God,', 'BodyI', 9.6, TEAL, after=2)
    p.lines(14, 17)
    p.para('Your child,', 'BodyI', 9.6, TEAL, after=2)
    p.lines(1, 17)


def letter_young(p):
    p.header('Reflection', 'A Letter to My Younger Self', 'You survived. Tell her.', 15)
    p.para('Dear me,', 'BodyI', 9.6, TEAL, after=2)
    p.lines(14, 17)
    p.para('With love,', 'BodyI', 9.6, TEAL, after=2)
    p.lines(1, 17)


def topic_study(p):
    p.header('Topic Study', 'Topic Study Template', None, 15)
    p.field('Topic', 1)
    p.field('Key verses (cite edition, book chapter:verse)', 3)
    p.field('Definitions or words to check', 2)
    p.field('What the sources say (and where they differ)', 3)
    p.field('Questions I still have', 2)
    p.field('How this changes what I do', 2)
    p.verify()


def character_study(p):
    p.header('Topic Study', 'Character Study', 'A woman or man of Scripture.', 15)
    p.cols(['Name', 'Where found (refs)'], 34)
    p.cols(['Family / people', 'Place and time'], 40)
    p.field('What she faced', 3)
    p.field('What she did', 3)
    p.field('What God did', 3)
    p.field('What the text does not tell us', 2)
    p.field('What I see in myself', 2)


def book_overview(p):
    p.header('Topic Study', 'Book Overview', None, 15)
    p.cols(['Book (edition)', 'Author / tradition'], 34)
    p.cols(['Date and setting', 'Audience'], 34)
    p.field('Big idea', 2)
    p.field('Outline by chapter', 8)
    p.field('Key verses', 2)
    p.field('How it points to Christ', 2)


def theme_tracker(p):
    p.header('Topic Study', 'Theme Tracker', 'Follow one theme across books.', 15)
    p.field('Theme', 1)
    table(p, ['Book + verse', 'What it says', 'Notes'], [70, 120, 90], 10, 30)
    p.field('What I notice', 2)


def questions(p):
    p.header('Topic Study', 'Questions I’m Allowed to Ask', 'Honest questions are welcome here.', 15)
    table(p, ['My question', 'Sources to check', 'Who I could ask'], [120, 80, 80], 6, 44)
    p.verify('Truth can withstand honest questions.')
    p.field('What I found', 3)


def teach_back(p):
    p.header('Topic Study', 'Teach It Back', 'If I can explain it, I know it.', 15)
    p.field('The passage or topic', 1)
    p.field('In one sentence, to a friend', 2)
    p.field('A real-life picture or example', 3)
    p.field('A question they might ask', 2)
    p.field('What I am still unsure about', 2)
    p.soft('Explain it to someone out loud, or to Big Boy, or to the mirror.', 'Say the one sentence once.')


# journal
def j_lined(p):
    p.header('Journal', 'Journal · Lined', None, 14)
    p.para('Date ______________', size=9, after=2)
    p.lines(int((p.room() - 4) / 17), 17)


def j_dotted(p):
    c = p.c
    p.header('Journal', 'Journal · Dotted', None, 14)
    p.para('Date ______________', size=9, after=4)
    c.setFillColor(LINE)
    y = p.cy - 4
    while y > p.floor + 6:
        x = p.L
        while x <= p.R + 0.1:
            c.circle(x, y, 0.75, stroke=0, fill=1)
            x += 14
        y -= 14


def j_grid(p):
    c = p.c
    p.header('Journal', 'Journal · Grid', None, 14)
    p.para('Date ______________', size=9, after=4)
    c.setStrokeColor(HexColor('#DDDDDD'))
    c.setLineWidth(0.4)
    top = p.cy - 4
    bot = p.floor + 6
    x = p.L
    while x <= p.R + 0.1:
        c.line(x, top, x, bot)
        x += 14
    y = top
    while y >= bot:
        c.line(p.L, y, p.R, y)
        y -= 14


def j_dated(p):
    p.header('Journal', 'Daily Page', None, 14)
    p.cols(['Date', 'Mood (1–5)'], 30)
    p.label('Today I am ...')
    p.lines(2)
    p.lines(int((p.room() - 4) / 17), 17)


def j_prayer_list(p):
    p.header('Journal', 'Prayer List', 'Names, needs, and thank-yous.', 15)
    table(p, ['For', 'Prayer', 'Date', 'Done'], [60, 140, 34, 30], 14, 25)


def j_prayer_week(p):
    p.header('Journal', 'Weekly Prayer Requests', None, 15)
    table(p, ['Day', 'Praying for', 'Thankful for'], [34, 130, 116], 7, 44,
          row_labels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    p.field('Notes', 3)


def j_gratitude(p):
    p.header('Journal', 'Thank You Pages', 'Mercy already received.', 15)
    for i in range(3):
        p.field('Date ____________  I am thankful for', 3)
    p.field('One mercy I almost missed', 2)
    p.field('One thing that is better than it was', 2)


def j_doodle(p):
    p.header('Journal', 'Sketch & Doodle', 'Margin art, color tests, or just breathe.', 15)
    p.box('', p.room() - 8, stroke=TURQ)


def j_rebuild(p):
    p.header('Journal', 'Daily Rebuild Planner', '“You survived. Now we rebuild.”', 15)
    p.cols(['Date', 'Energy 1–5'], 30)
    p.label('Three small things today')
    for _ in range(3):
        p.c.setFillColor(TURQ); p.c.setFont('Sym', 11); p.c.drawString(p.L, p.cy - 13, '\u2610')
        p.c.setStrokeColor(LINE); p.c.setLineWidth(0.5); p.c.line(p.L + 16, p.cy - 14, p.R, p.cy - 14)
        p.cy -= 20
    p.cy -= 4
    p.field('One verse for today', 1)
    p.label('Body care')
    p.hchecks(['Water', 'Food', 'Movement', 'Sleep'], 9)
    p.field('One thing I am thankful for', 2)
    p.field('One person to reach out to', 1)
    p.field('Notes', 2)


def j_habits(p):
    p.header('Journal', '30-Day Habit Tracker', None, 15)
    p.field('Habit', 1)
    day_circles(p, 30, 10, 11)
    p.field('Habit', 1)
    day_circles(p, 30, 10, 11)
    p.field('Habit', 1)
    day_circles(p, 30, 10, 11)


def j_cornell(p):
    c = p.c
    p.header('Journal', 'Cornell Notes', None, 14)
    p.cols(['Topic / passage', 'Date'], 30)
    top = p.cy
    bot = p.floor + 70
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.line(p.L + 88, top, p.L + 88, bot)
    c.line(p.L, bot, p.R, bot)
    tracked(c, p.L, top - 8, 'CUES / QUESTIONS', 'SansB', 5.8, TEAL, 0.7)
    tracked(c, p.L + 96, top - 8, 'NOTES', 'SansB', 5.8, TEAL, 0.7)
    y = top - 26
    while y > bot + 4:
        c.line(p.L + 96, y, p.R, y)
        y -= 16.5
    tracked(c, p.L, bot - 12, 'SUMMARY', 'SansB', 5.8, TEAL, 0.7)
    for k in range(3):
        c.line(p.L, bot - 28 - k * 16, p.R, bot - 28 - k * 16)
    p.cy = p.floor


def j_frame(p):
    c = p.c
    p.header('Journal', 'Framed Page', 'Lettering, a verse, or a prayer.', 15)
    h = p.room() - 6
    c.setStrokeColor(TURQ)
    c.setLineWidth(1.4)
    c.roundRect(p.L, p.cy - h, p.w, h, 8, stroke=1, fill=0)
    c.setLineWidth(0.5)
    c.setStrokeColor(GOLD)
    c.roundRect(p.L + 5, p.cy - h + 5, p.w - 10, h - 10, 6, stroke=1, fill=0)
    p.cy = p.floor


def j_reading(p):
    p.header('Journal', 'Reading Plan Tracker', 'Color in a box as you read.', 15)
    p.field('Plan or book', 1)
    c = p.c
    cols, n = 10, 60
    step = p.w / cols
    for i in range(n):
        x = p.L + (i % cols) * step
        y = p.cy - (i // cols) * 24
        c.setStrokeColor(TURQ)
        c.setFillColor(WHITE)
        c.rect(x + 2, y - 20, step - 4, 20, stroke=1, fill=1)
        c.setFillColor(GRAY)
        c.setFont('Sans', 6.5)
        c.drawString(x + 4, y - 8, str(i + 1))
    p.cy -= (n // cols) * 24 + 8
    p.field('What stood out', 3)


def j_verse_week(p):
    p.header('Journal', 'Verse of the Week', None, 15)
    p.cols(['Week of', 'Reference (edition)'], 34)
    p.box('The verse, in my handwriting', 130, stroke=TURQ)
    p.field('Why this one', 2)
    p.field('Day by day: what I noticed', 6)


# ---------------------------------------------------------------- single-page versions (one insert per page)
def woman_single(p, w, idx, total):
    name, ref, note, found, q, step = w
    p.tag = name
    p.header(f'Women of the Word · {idx} of {total}', name, ref, size=15)
    if note:
        p.note(note, None, T_PEACH, 'BodyI', 8.2)
    p.label('Where we meet her')
    p.para(found, size=8.8, after=3)
    fixed = 30 + 30 + 14 + 14 + 33 + 52 + 6 + 34 + p.soft_h(step) + 6
    nl = max(4, int((p.room() - fixed) / 16.5))
    n1 = max(2, int(round(nl * 0.6)))
    p.field('Who is in the scene?', 1)
    p.field('Where and when?', 1)
    p.field('What happened, in my words', n1)
    p.field('Words that stand out', max(2, nl - n1))
    p.cols(['What she lost', 'What she did', 'Who saw her'], 46)
    p.para(q, 'BodyB', 8.8, TEAL, after=3)
    p.soft(step)


def topic_single(p, d):
    p.tag = d['title']
    p.header(d['kicker'], d['title'], d['sub'], size=15)
    intro = d['intro']
    if intro.startswith('Content note') or intro.startswith('Textual'):
        p.note(intro, None, T_PEACH, 'BodyI', 8.2)
    elif intro:
        p.para(intro, size=8.8, after=4)
    refs = d['refs']
    prompt_h = sum(len(wrap(q, 'BodyB', 8.8, p.w)) * 11 + 2 * 15 + 4 for q in d['prompts'])
    res_h = 0
    if d.get('res'):
        res_h = len(wrap(d['res'], 'Body', 7.8, p.w - 16)) * 9.8 + 28
    avail = p.room() - 24 - p.soft_h(d['step'], d['low']) - 8 - prompt_h - res_h
    n = max(1, min(3, int((avail / len(refs) - 22) / 16.5)))
    for ref, hint in refs:
        p.c.setFillColor(TEAL)
        p.c.setFont('BodyB', 9.2)
        p.c.drawString(p.L, p.cy - 9, ref)
        p.cy -= 11
        p.c.setFillColor(GRAY)
        p.c.setFont('BodyI', 7.8)
        p.c.drawString(p.L, p.cy - 8, 'Look for: ' + hint)
        p.cy -= 9
        p.lines(n)
    p.para('Check: read two chapters around it, compare two editions (cite which), ask clergy about doctrine.', 'BodyI', 7.6, GRAY, after=3)
    for q in d['prompts']:
        p.para(q, 'BodyB', 8.8, TEAL, after=0)
        p.lines(2, 15)
    if d.get('res'):
        p.note(d['res'], 'Help is real', T_GOLD, 'Body', 7.8)
    p.soft(d['step'], d['low'])
