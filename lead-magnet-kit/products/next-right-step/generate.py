#!/usr/bin/env python3
"""Generates body.html for The Next Right Step (full guide + workbook). Edit the text here, then run:
   python3 products/next-right-step/generate.py && python3 build.py
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))

CRISIS = ('<div class="crisis">In crisis? Call/text <b>988</b> &bull; SAMHSA <b>1-800-662-4357</b> &bull; '
          'Emergency <b>911</b> &bull; Trafficking <b>1-888-373-7888</b> &bull; DV Hotline <b>1-800-799-7233</b></div>')

def ph(path, h="1.5in", pos="50% 22%", cap=""):
    c = f'<div style="font-size:10px;text-align:center;color:var(--denim);letter-spacing:1px;text-transform:uppercase;margin-bottom:4px">{cap}</div>' if cap else ""
    return f'<img src="../photos/{path}" alt="" style="width:100%;height:{h};object-fit:cover;object-position:{pos};border-radius:10px;border:2px solid var(--accent);margin:6px 0 2px">{c}'
def av(path, pos="50% 25%"):
    return (f'<img src="../photos/{path}" alt="" style="float:right;width:1.3in;height:1.3in;border-radius:50%;object-fit:cover;'
            f'object-position:{pos};border:3px solid var(--accent);margin:2px 0 6px 12px">')
CL = '<div style="clear:both"></div>'
def lines(n): return '<div class="row"><div class="line"></div></div>' * n
def box(t): return f'<div class="row"><div class="box"></div><div style="flex:1;font-size:13px">{t}</div></div>'
def verse(text, ref): return f'<div class="verse"><b>{ref} (ESV)</b>&ldquo;{text}&rdquo;</div>'
def page(inner, brand=""):
    b = f'<div class="brand">{brand}</div>' if brand else ""
    return f'<section class="page"><div class="band"></div>{b}{inner}{CRISIS}<!--FOOTER--></section>'

DAYS = [
 dict(t="Tell the Truth", v=[("The LORD is near to the brokenhearted and saves the crushed in spirit.", "Psalm 34:18"),
                              ("If we confess our sins, he is faithful and just to forgive us our sins and to cleanse us from all unrighteousness.", "1 John 1:9")],
  teach=["Nobody gets free by getting better at hiding. Most of us got real good at &ldquo;I'm fine.&rdquo; Fine kept the questions away. Fine kept the peace. And fine kept us right where we were.",
         "So day one is not about fixing anything. It's about naming it. Out loud. On paper. To God, who already knows, and to one safe person, who doesn't yet. That's it. That's the whole assignment.",
         "Telling the truth is not the same as beating yourself up. Shame says <i>you are the problem.</i> Truth says <i>this is the problem, and I'm not going to carry it alone anymore.</i> Shame keeps you hiding. Truth lets God in.",
         "And here's the balance we hold in this house: <b>I understand why you became this way. And you are still responsible for what you do next.</b> Both are true. Understanding is not excusing. Explaining is not permission."],
  nb=[("&ldquo;If they knew everything, they'd leave.&rdquo;","Some people might. The right ones won't. Start with one safe person, not everybody."),
      ("&ldquo;I have to fix it before I tell anybody.&rdquo;","You tell the truth so you don't have to fix it alone."),
      ("&ldquo;God's mad at me.&rdquo;","He is near to the brokenhearted. Psalm 34:18 does not say &lsquo;near to the ones who cleaned up first.&rsquo;")],
  tool="The Truth Inventory", intro="No one is grading this. Write it like nobody will ever read it. Facts, not self-hatred.",
  prompts=["What am I using, doing, or hiding right now?","What have I been calling &ldquo;fine&rdquo; that isn't fine?","Who is this costing besides me?","What am I most afraid will happen if I stop?","The one sentence I'm most afraid to say out loud is&hellip;"],
  tasks=["Complete the Truth Inventory (all five)","Say one true sentence out loud to God","Tell one safe person: &ldquo;I'm struggling.&rdquo;"],
  prayer="Lord, I'm done pretending. This is where I really am, and You already knew. I'm not asking You to be impressed. I'm asking You to meet me here. Give me the courage to say it to a real person today. In Jesus' name, amen.",
  hard="If the truth feels like too much today, write just one line. One line counts. If you're thinking about hurting yourself, stop reading and call or text 988 now."),
 dict(t="Get Safe", v=[("God is our refuge and strength, a very present help in trouble.", "Psalm 46:1"),
                        ("He drew me up from the pit of destruction, out of the miry bog, and set my feet upon a rock, making my steps secure.", "Psalm 40:2")],
  teach=["Before strategy, before feelings, before anything else: <b>are you safe tonight?</b> From a substance. From a person. From yourself. Safety comes first, and it's not weakness to say so.",
         "Get practical. Put three people and three numbers where you can reach them without thinking. When you're in the middle of a bad hour, you will not be creative. You'll grab whatever is closest. So make the right thing the closest thing.",
         "If someone is hurting you, controlling you, or forcing you, that is not your fault and it is not a failure of faith. Leaving is not simple. Nobody gets to shame you for how long it takes. When you're ready, and only when it's safe, there are people trained to help you plan it.",
         "And hear me on this: <b>forgiveness is not access.</b> You can forgive somebody and never let them back in your life. You never owe anyone a seat at your table because they said sorry."],
  nb=[("&ldquo;A good Christian doesn't need a safety plan.&rdquo;","Faith and preparation work together. Noah still built the ark."),
      ("&ldquo;I should be able to handle this alone.&rdquo;","Refuge means somewhere to run. Use it."),
      ("&ldquo;If I leave, I'm giving up on them.&rdquo;","Protecting yourself is not hatred. It's stewardship of what God gave you.")],
  tool="My Safety Plan", intro="Fill this in today while you're calm, so tonight you don't have to think.",
  prompts=["3 people I can call any hour (names + numbers)","3 numbers saved in my phone right now: 988 &bull; 1-800-662-4357 &bull; 911","One thing I will remove, hand off, or put out of reach tonight","Where I can go if home isn't safe (a person, a place)","What I will say when I call: &ldquo;I need help right now, and I don't want to be alone.&rdquo;"],
  tasks=["Save the three crisis numbers in my phone","Fill in my 3 people (or call SAMHSA if I have none yet)","Remove or hand off one thing within reach"],
  prayer="Father, be my refuge tonight. Guard my body and my mind. Put safe people in my path and give me the courage to use the phone when the hour gets loud. Cover me and everyone I love. In Jesus' name, amen.",
  hard="If someone monitors your phone or email, use a safe device and delete your browsing history after. Your safety comes before anything in this guide."),
 dict(t="Feed the Body", v=[("And he looked, and behold, there was at his head a cake baked on hot stones and a jar of water. And he ate and drank and lay down again.", "1 Kings 19:6"),
                             ("Come to me, all who labor and are heavy laden, and I will give you rest.", "Matthew 11:28")],
  teach=["Elijah was worn out, afraid, and begging God to let him die. And the first thing God did wasn't a sermon. It was bread, water, and a nap. Sometimes the holy thing is a sandwich and eight hours of sleep.",
         "Your body has been carrying a lot. If you've been using, not eating, not sleeping, or living on adrenaline, your body is running on empty, and an empty body makes everything feel worse: the cravings, the fear, the anger, the lies.",
         "<b>Important safety truth:</b> if you've been drinking heavily or using benzodiazepines, opioids, or other substances daily, do not just stop cold on your own. Withdrawal from some of these can be dangerous, even deadly. Call a doctor, an ER, or the SAMHSA helpline (1-800-662-4357) first. That's not weak. That's wise.",
         "This is where faith and practical help hold hands. Pray and take your medication as prescribed. Pray and go to the appointment. God gave doctors, nurses, and counselors. Use them."],
  nb=[("&ldquo;Real faith means I don't need a doctor.&rdquo;","Luke was a physician and he's in your Bible."),
      ("&ldquo;I'll quit alone. I don't need anybody.&rdquo;","Not all withdrawals are safe alone. Get medical guidance first."),
      ("&ldquo;Rest is laziness.&rdquo;","Jesus slept in a boat in a storm. Rest is obedience.")],
  tool="The H.A.L.T. Check", intro="When you're Hungry, Angry, Lonely, or Tired, everything is harder. Check these before you make any big decision.",
  prompts=["<b>H</b>ungry: when did I last eat something real? What can I eat today?","<b>A</b>ngry: what am I carrying that I haven't said out loud?","<b>L</b>onely: who have I actually talked to today?","<b>T</b>ired: how many hours did I sleep? What time will I go to bed tonight?","Medical: who is one doctor, clinic, or treatment line I will call this week?"],
  tasks=["Drink a full glass of water and eat something real","Set a bedtime and put the phone across the room","Call or book one medical or treatment contact"],
  prayer="Lord, You fed Elijah before You gave him another assignment. Feed me. Help me take care of this body You gave me. Give me sleep, give me wisdom about what I need, and give me the humility to ask for help. In Jesus' name, amen.",
  hard="If you can't do all three tasks today, do the water. That's a real win."),
 dict(t="Know Your Triggers", v=[("No temptation has overtaken you that is not common to man. God is faithful, and he will not let you be tempted beyond your ability, but with the temptation he will also provide the way of escape, that you may be able to endure it.", "1 Corinthians 10:13"),
                                  ("The steadfast love of the LORD never ceases; his mercies never come to an end; they are new every morning; great is your faithfulness.", "Lamentations 3:22-23")],
  teach=["The corner didn't only live on a street. It lives in a time of day, a payday, a text message, a person, a song, a smell, a feeling. If you don't know your triggers, they pick the time and the place. If you do, you get to pick.",
         "Most cravings feel like they'll last forever and don't. They rise, peak, and pass, often within fifteen to thirty minutes. You don't have to win forever. You just have to outlast the next fifteen minutes. That's a strategy you can actually use tonight.",
         "The Bible says God provides &ldquo;the way of escape.&rdquo; Notice it doesn't say &lsquo;the way of no temptation.&rsquo; It says a way out. Your job is to look for the door and walk through it before your mind talks you out of it: leave the room, call the person, drink the water, go outside, put your hands on something.",
         "A slip is not the end. It is information. It tells you what to plan for next time. Shame will tell you it means you're hopeless. It doesn't. His mercies are new every morning, and that includes tomorrow morning."],
  nb=[("&ldquo;A craving means I'm failing.&rdquo;","A craving means your body is remembering. It isn't a verdict."),
      ("&ldquo;I just need more willpower.&rdquo;","You need a plan, people, and a way out. Willpower alone runs out."),
      ("&ldquo;If I slip once, it's over.&rdquo;","Relapse is not resignation. Tell somebody and start at the next right step.")],
  tool="The 15-Minute Craving Plan", intro="Write this when you're calm. Use it when you're not.",
  prompts=["My top 3 triggers (people, places, feelings, times of day)","Where I am most likely to get pulled back this week","When a craving hits, first I will (move, water, step outside)","The person I call first (and their number)","My 15-minute rule: I wait, set the timer, then I decide again."],
  tasks=["Write my top 3 triggers","Pick my &ldquo;call first&rdquo; person and text them so they know","Practice the 15-minute wait once with a timer"],
  prayer="God, You said there's a way out. Open my eyes to it when the craving comes, and let my feet move toward it before my head talks me out of it. Give me fifteen minutes, then give me fifteen more. In Jesus' name, amen.",
  hard="If a craving is loud right now: set a timer for 15 minutes, drink water, and call someone. Don't decide anything until the timer goes off."),
 dict(t="Break the Isolation", v=[("Two are better than one, because they have a good reward for their toil. For if they fall, one will lift up his fellow. But woe to him who is alone when he falls and has not another to lift him up!", "Ecclesiastes 4:9-10"),
                                   ("Therefore, confess your sins to one another and pray for one another, that you may be healed.", "James 5:16")],
  teach=["Shame says hide. God says come out. Isolation is where relapse does its best work, and it's where the enemy whispers that nobody wants to hear it, nobody would understand, you're too much, you're too far gone.",
         "That's a lie. But it's a convincing one, because it's usually been rehearsed for years. The way you break a lie like that is not to argue with it in your head. You break it by letting a real person prove it wrong.",
         "You need people who know the truth about you. Not everybody. Not the internet. A few. A recovery group, a sponsor, a counselor, a pastor who actually knows what to do with this, a friend who stays. Look for people who tell the truth <i>and</i> stay.",
         "If church hurt you, I'm sorry. Spiritual abuse is real, and it's not God. There are churches and groups that do this well. Celebrate Recovery is one faith-based option, and AA and NA meetings are in almost every town. Try more than one. Fit matters."],
  nb=[("&ldquo;I don't want to burden anybody.&rdquo;","Letting people help is not a burden. It's how the body of Christ works."),
      ("&ldquo;Nobody would understand.&rdquo;","Somebody in a meeting room tonight has been exactly where you are."),
      ("&ldquo;I've been hurt by church, so I'm done.&rdquo;","Done with the people who hurt you, yes. Not done with God, and not done with community.")],
  tool="The Reach-Out Plan", intro="Reaching out is a skill. Use the script below until it feels normal.",
  prompts=["Script: &ldquo;Hey, I need help. I'm not okay and I don't want to do this alone. Can I call you today?&rdquo;","The person I will text before noon tomorrow","A meeting or group I'll attend this week (name, day, time)","A second option if the first one doesn't fit","What I'm afraid will happen, and what I'll do if it does"],
  tasks=["Send the reach-out text to one person","Find one meeting or group and put it on my calendar","Sit with one safe person for ten minutes, phone away"],
  prayer="Lord, break the lie that I'm too much or too far gone. Send me people who will sit in it with me and point me back to You. Give me the courage to walk in the room. In Jesus' name, amen.",
  hard="If you can't find a meeting, call SAMHSA at 1-800-662-4357 and ask for local groups and treatment. It's free, confidential, and they answer any hour."),
 dict(t="Own It Without Drowning", v=[("Whoever conceals his transgressions will not prosper, but he who confesses and forsakes them will obtain mercy.", "Proverbs 28:13"),
                                       ("There is therefore now no condemnation for those who are in Christ Jesus.", "Romans 8:1")],
  teach=["Grace is not permission. You can be fully forgiven and still owe repair. That's not God being harsh. That's how real relationships and real recovery work.",
         "Owning it is a plan, not a punishment. You name what's yours. You tell the truth. You make it right where it's safe and possible. You change the pattern. And you don't confuse guilt (<i>I did something wrong</i>) with shame (<i>I am something wrong</i>). God deals with guilt through forgiveness. He deals with shame through belonging.",
         "Now the other half, which people rarely say: <b>some of what you're carrying isn't yours.</b> If someone abused you, trafficked you, betrayed you, or manipulated you, that belongs to them, not to you. Don't take responsibility for what was done <i>to</i> you. Put it down.",
         "And repair never means walking back into danger. If contacting someone isn't safe, then the repair is changing your own life, and letting God carry what you can't. You don't have to reconcile with anyone who is still unsafe."],
  nb=[("&ldquo;I'm forgiven, so I don't owe anything.&rdquo;","Forgiven and accountable. Both."),
      ("&ldquo;It's all my fault.&rdquo;","Not everything. Sort what's yours from what was done to you."),
      ("&ldquo;Forgive means go back.&rdquo;","Forgiveness is release. Access is earned by safe behavior over time.")],
  tool="Own / Repair / Release", intro="Three columns. Be honest, be specific, and be kind to yourself.",
  prompts=["OWN: what I did that is mine to own (facts, not self-hatred)","REPAIR: one safe first step I can take (or &ldquo;none is safe right now&rdquo;)","RELEASE: what was done TO me that is not mine to carry","What I need to forgive myself for, and what I need God's help to forgive","One boundary I need in place before I repair anything"],
  tasks=["Write my OWN list (facts only)","Write one safe REPAIR step or mark none safe right now","Read my RELEASE list aloud and hand it to God"],
  prayer="Lord, show me what is mine and what isn't. Give me courage to repair what I can and grace to release what I can't. Take the shame, and leave me the lesson. In Jesus' name, amen.",
  hard="If this day stirs up old trauma, stop and get support. A trained counselor can walk you through this safely. You don't have to do it alone."),
 dict(t="Plant Something", v=[("I am the vine; you are the branches. Whoever abides in me and I in him, he it is that bears much fruit, for apart from me you can do nothing.", "John 15:5"),
                               ("So if the Son sets you free, you will be free indeed.", "John 8:36")],
  teach=["Somebody taught you to survive. The bando, the corner, the hustle: all of it was survival. But God didn't pull you out of the pit just so you could survive. He pulled you out so you could grow.",
         "Growing is slower than surviving, and it includes pruning. In a vineyard, you cut the branch so the vine can bear more fruit. Some of what's getting cut in your life isn't punishment. It's preparation.",
         "For years the search was for another plug, another source, another supply. Jesus says He is the vine, and that apart from Him you can do nothing. The Source was never on the corner. You don't have to keep looking.",
         "You will not become the woman or man God is calling you to be overnight. You become her every time you choose not to go back. Your job for the next thirty days is simple: pick a daily anchor, pick a weekly anchor, tell someone, and keep going. The next right step. Then the next."],
  nb=[("&ldquo;I've messed up too much for God to use me.&rdquo;","God doesn't call the qualified. He qualifies the called. And He starts with what's left."),
      ("&ldquo;I need to become perfect first.&rdquo;","You don't. You need to stay connected to the vine."),
      ("&ldquo;One relapse ruins everything.&rdquo;","It doesn't. Tell the truth, call your people, start at the next right step.")],
  tool="My Next 30 Days", intro="You finished the first seven. Now build the next thirty. (There's a calendar for it later in this guide.)",
  prompts=["My daily anchor (10 minutes with God at the same time every day)","My weekly anchor (a meeting, counselor, church, or group, day + time)","One thing I'm building (a skill, a job step, a budget, a hobby, a home)","The person I'll check in with every Sunday","What I want to be true 30 days from now"],
  tasks=["Choose my daily and weekly anchors","Put both on my calendar right now","Tell someone my plan for the next 30 days"],
  prayer="Jesus, You are the vine. I'm done running on my own supply. Keep me connected to You. Prune what needs pruning. Help me choose the next right thing tomorrow, and the day after that, and the day after that. In Your name, amen.",
  hard="If you missed a day or two, that's okay. Pick up where you left off. Progress here is measured in days you came back, not days you were perfect."),
]

out = []
# ---- cover
out.append('''<section class="page"><div class="band"></div><div class="brand">7HE H0LY REUP</div>
<h1>The Next Right Step</h1><div class="subtitle">A 7-Day Reset From the Floor</div><div class="subtitle" style="margin-top:4px">Guide &bull; Workbook &bull; Prayers &bull; 30-Day Plan</div><div class="orn">🍇</div>
<img class="cover-photo" src="../photos/team/05-leather-jacket-sunset.jpg" alt="" style="object-position:50% 8%"><p style="text-align:center;font-weight:700;margin-top:14px">Free from 7HE H0LY REUP</p>
<p style="text-align:center">You survived. Now we rebuild.</p><!--FOOTER--></section>''')

# ---- welcome letter
out.append(page('''<h2>Read This First</h2>
'''+ph('team/02-white-studio-hug.jpg','2.2in','50% 22%')+'''
<p>If you're holding this, something is wrong and you don't know where to go. That is exactly who I made this for.</p>
<p>I wish my sister, Brandi Renee, had somewhere to reach. I can't say it would have changed her outcome. I can build toward it for you. I built it for the person sitting in a car trying not to cry, the person who relapsed yesterday, the person who told nobody, the person who's years in and fighting a craving tonight, the person who was hurt by church, the person who thinks God is done with them.</p>
<p>I know what the floor feels like. I lost my sister to addiction, and I have survived homelessness, trafficking, abuse, addiction, and years of manipulation. I'm not finished, and I'm not a professional. I'm building as I go. <b>You survived. Now we rebuild.</b></p>
<p>This is a seven-day reset. One teaching page and one working page a day. No perfection required. Some days you'll do all of it. Some days you'll do one line. Both count.</p>
<p>I'm not a doctor, a therapist, or a lawyer. I'm a woman who keeps choosing the next right thing with Jesus as my foundation. This guide is not treatment. It's a hand held out. Use it <i>with</i> real help, not instead of it.</p>
'''+verse("But God, being rich in mercy, because of the great love with which he loved us, even when we were dead in our trespasses, made us alive together with Christ&mdash;by grace you have been saved&mdash;","Ephesians 2:4-5")+
'''<p class="sig" style="font-size:30px">Baby, I know what far gone looks like. Now let me show you what God can do from there. &mdash; Nikki &ldquo;Hellshaker&rdquo;</p>'''))

# ---- how to use
out.append(page('''<h2>How This Works</h2>
<table class="nb"><tr><th style="width:1.3in">Each day</th><th>What you do</th><th style="width:.8in">Time</th></tr>
<tr><td><b>Teaching page</b></td><td>Read the verse and the truth. Notice the &ldquo;Not this / But this&rdquo; lies and their replacements.</td><td>5 min</td></tr>
<tr><td><b>Working page</b></td><td>Fill in the tool. Do the three small things. Pray the prayer, or pray it your own way.</td><td>10&ndash;20 min</td></tr>
<tr><td><b>Tracker</b></td><td>Check your boxes in the free tracker: <a href="{{TRACKER_URL}}">{{TRACKER_URL}}</a></td><td>1 min</td></tr></table>
<h3>The seven days</h3>
<ol><li><b>Tell the Truth</b>: name where you are</li><li><b>Get Safe</b>: your people, your numbers, your plan</li><li><b>Feed the Body</b>: water, food, sleep, medical help</li><li><b>Know Your Triggers</b>: the 15-minute craving plan</li><li><b>Break the Isolation</b>: reach out and get in a room</li><li><b>Own It Without Drowning</b>: accountability without shame</li><li><b>Plant Something</b>: your next thirty days</li></ol>
<h3>Ground rules for this house</h3>
<ul><li><b>Understanding is not excusing.</b> I understand why. You're still responsible for what you do next.</li>
<li><b>Grace is not enabling.</b> Forgiveness is not access. Boundaries are not hatred.</li>
<li><b>Recovery is not perfection.</b> Relapse is not resignation.</li>
<li><b>Faith and real help are not enemies.</b> Pray and call. Scripture and a meeting.</li>
<li><b>You go at your own pace.</b> Missed a day? Pick up where you stopped.</li></ul>
<div class="verse"><b>Lamentations 3:22-23 (ESV)</b>The steadfast love of the LORD never ceases; his mercies never come to an end; they are new every morning; great is your faithfulness.</div>'''))

# ---- safety check
out.append(page('''<h2>Before You Start: A Safety Check</h2>
<p>Answer honestly. If you check anything in the red zone, do that first. Everything else in this guide can wait.</p>
<div class="tool" style="border-color:#c0392b"><span class="tag" style="background:#c0392b">Call Now: 911 or 988</span>
'''+box("I am thinking about hurting myself or ending my life")+box("I may have taken too much of something, or someone else has")+box("Someone is hurting me or threatening me right now")+box("I'm having seizures, severe shaking, hallucinations, or confusion (these can be signs of dangerous withdrawal)")+'''</div>
<div class="tool"><span class="tag">Get Help Today</span>
'''+box("I've been drinking heavily or using benzodiazepines, opioids, or other drugs every day and want to stop. <b>Do not stop alone without medical guidance.</b> Call SAMHSA 1-800-662-4357 or a doctor or ER")+box("I'm being controlled, forced, or exploited. Call the National Human Trafficking Hotline 1-888-373-7888 (text 233733)")+box("I'm afraid of a partner or family member. National Domestic Violence Hotline 1-800-799-7233 (text START to 88788)")+box("I have no one I can call. Call SAMHSA and ask about local groups and treatment")+'''</div>
<div class="verse"><b>Psalm 46:1 (ESV)</b>God is our refuge and strength, a very present help in trouble.</div>
<h3>Overdose reminders</h3>
<ul><li>Never use alone if you can help it. Tell someone or use a hotline service where available.</li>
<li>Ask your pharmacy or local health department about naloxone (Narcan) and keep it where people can find it.</li>
<li>If you think someone has overdosed: call 911, give naloxone if you have it, stay with them, and put them on their side.</li>
<li>Poison Control (any hour): 1-800-222-1222</li></ul>'''))

# ---- days
for i, d in enumerate(DAYS, 1):
    verses = "".join(verse(t, r) for t, r in d["v"])
    teach = "".join(f'<p style="font-size:14px;line-height:1.5;margin:6px 0">{x}</p>' for x in d["teach"])
    nb = '<table class="nb"><tr><th style="width:46%">Not this (the lie)</th><th>But this (the truth)</th></tr>' + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in d["nb"]) + "</table>"
    out.append(page(f'<h2>Day {i}: {d["t"]}</h2>{ph(f"stages/stage-{i if i<=6 else 6}.png","1.0in","50% 55%",f"Stage {i if i<=6 else 6} of 6 &bull; from the concrete to the harvest")}{verses}{teach}{nb}<h3>What stood out to me</h3>{lines(1)}', f"Day {i} of 7 &bull; Read"))
    prompts = "".join(f'<p style="margin:7px 0 0"><b>{n}.</b> {p}</p>{lines(2)}' for n, p in enumerate(d["prompts"], 1))
    tasks = "".join(box(t) for t in d["tasks"])
    out.append(page(f'''<h2>Day {i}: {d["t"]}</h2>
<div class="tool"><span class="tag">Tool: {d["tool"]}</span><p style="margin:2px 0;font-style:italic;color:var(--denim)">{d["intro"]}</p>{prompts}</div>
<div class="tool" style="border-color:var(--accent)"><span class="tag" style="background:var(--accent)">Do This Today</span>{tasks}</div>
<h3>Prayer</h3><p><i>{d["prayer"]}</i></p>
<p style="font-size:12px;background:var(--tint);border-radius:8px;padding:6px 10px"><b>Hard day?</b> {d["hard"]}</p>''', f"Day {i} of 7 &bull; Work"))

# ---- 5 lies
lies = [("&ldquo;I'm too far gone.&rdquo;","Nobody is beyond the reach of God. Ephesians 2 says God made us alive together with Christ when we were dead in our trespasses. Where you are is not too far for Him.","Ephesians 2:4-5"),
 ("&ldquo;If they knew the truth, they'd leave.&rdquo;","Some people might. The right ones won't. And God already knows and stays.","Psalm 34:18"),
 ("&ldquo;One slip and it's all ruined.&rdquo;","A slip is information, not a verdict. The righteous fall and rise again. Tell somebody and start at the next right step.","Proverbs 24:16"),
 ("&ldquo;I'll be okay when I get [that person/that thing/that money].&rdquo;","Only Jesus is the Source. People, things, and money are not the plug. They're just more supply that runs out.","John 15:5"),
 ("&ldquo;This is just how I am.&rdquo;","Your patterns are learned and they can be unlearned. Nobody is stuck. You can become someone new, one choice at a time.","2 Corinthians 5:17")]
lie_html = "".join(f'<div class="card2"><b class="h">The lie: {a}</b><p style="margin:3px 0"><b>The truth:</b> {b} <i>({c})</i></p></div>' for a, b, c in lies)
out.append(page('<h2>The 5 Lies That Keep People Bound</h2>'+av('team/04-cowprint-hug.jpg','60% 28%')+'<p>The enemy tells lies that sound like your own voice. Learn to spot them, and answer them with truth out loud.</p>'+CL+lie_html+
 verse("For the righteous falls seven times and rises again.","Proverbs 24:16")+
 '<h3>Write your own</h3><p>The lie I hear most often is&hellip;</p>'+lines(2)+'<p>The truth I'"'"'ll answer with is&hellip;</p>'+lines(2)))

# ---- boundaries
out.append(page('''<h2>Boundaries &amp; Forgiveness Are Not the Same as Access</h2>
'''+av('team/03-pink-camo-jacket.jpg','50% 24%')+'''
<p>You can forgive someone and still keep the door closed. You can love someone and still say no. Boundaries are not punishment. They are how you protect what God is rebuilding.</p>'''+CL+'''
<table class="nb"><tr><th style="width:38%">Situation</th><th>What you can say</th></tr>
<tr><td>Someone pressures you to use or drink</td><td>&ldquo;No thanks. I'm not doing that anymore.&rdquo; (No explanation needed.)</td></tr>
<tr><td>Old friends invite you to the old places</td><td>&ldquo;I love you, but I'm not going there. I can meet for coffee somewhere else.&rdquo;</td></tr>
<tr><td>Someone wants money and you know where it goes</td><td>&ldquo;I can't give you cash. I can buy you groceries or drive you to a meeting.&rdquo;</td></tr>
<tr><td>A person who hurt you wants back in</td><td>&ldquo;I forgive you, and I'm not letting you back in. Please respect that.&rdquo;</td></tr>
<tr><td>Family pressures you to &ldquo;just forgive and move on&rdquo;</td><td>&ldquo;Forgiving is between me and God. Trust and access are earned, and they're not available right now.&rdquo;</td></tr>
<tr><td>Someone uses Scripture to make you stay in danger</td><td>&ldquo;God doesn't ask me to stay somewhere I'm being harmed.&rdquo;</td></tr></table>
<p><b>Safety note:</b> if the person is dangerous, do not confront them in person. Don't announce a boundary to someone who may react violently. Talk to a hotline advocate about a safe plan first (1-800-799-7233).</p>
<h3>My boundaries this month</h3>'''+box("Someone I'm not answering right now: ______________________")+box("A place I'm not going: ______________________")+box("A thing I'm not doing: ______________________")+
 verse("For freedom Christ has set us free; stand firm therefore, and do not submit again to a yoke of slavery.","Galatians 5:1")))

# ---- relapse plan
out.append(page('''<h2>If I Slip: My Plan</h2>
<p>Write this while you're steady. Then when you're not, you don't have to think. You just follow the plan.</p>
<div class="tool"><span class="tag">First hour</span>'''+box("Get somewhere safe. If I've used a lot, or feel unwell: 911")+box("Call my person: name / number")+lines(1)+box("Drink water, eat something, don't use anything else tonight")+'''</div>
<div class="tool" style="border-color:var(--accent)"><span class="tag" style="background:var(--accent)">Same day</span>'''+box("Tell one safe person the truth. Not tomorrow. Today.")+box("Go to a meeting or call one (or SAMHSA 1-800-662-4357)")+box("Write what happened, what triggered it, and what I'll do differently")+lines(3)+'''</div>
<div class="tool" style="border-color:var(--third)"><span class="tag" style="background:var(--third)">Next 7 days</span>'''+box("Go back to the last thing that was working (a step, a meeting, a person)")+box("Tell my counselor, sponsor, or doctor")+box("Restart at the next right step, not at zero")+'''</div>
<p><b>Remember:</b> a slip is not the end of your story. Shame tells you to hide. God says come back. <i>&ldquo;There is therefore now no condemnation for those who are in Christ Jesus.&rdquo;</i> (Romans 8:1, ESV)</p>
<p><b>Medical note:</b> if you've been sober for a while and slip, your body may not tolerate the amount you used before. Overdose risk is higher after a break. Be careful, and get help.</p>'''))

# ---- partner agreement
out.append(page('''<h2>My Accountability Partner</h2>
<p>Recovery is not a solo sport. This page helps you ask for what you need and gives your partner clear expectations.</p>
<div class="tool"><span class="tag">Our agreement</span>
<p>My name: ____________________ &nbsp; My partner's name: ____________________</p>
<p>We will check in (how often, how): ______________________________</p>
<p>My partner will ask me: &ldquo;Did you do your next right step? Did you tell the truth today?&rdquo;</p>
<p>If I slip, I will tell my partner within: &nbsp;__ hours</p>
<p>My partner will respond with: (check) <span class="box" style="display:inline-block"></span> listening first &nbsp; <span class="box" style="display:inline-block"></span> helping me make the plan &nbsp; <span class="box" style="display:inline-block"></span> no shame or lectures</p>
<p>If either of us is in danger, we call: 911 &bull; 988 &bull; SAMHSA 1-800-662-4357</p>
<p>Signed: ______________________ &nbsp; ______________________ &nbsp; Date: __________</p></div>
<h3>Choosing a partner</h3>
<ul><li>Someone who tells the truth <i>and</i> stays.</li><li>Someone who's steady, not someone in crisis right now.</li><li>Someone who won't enable you and won't shame you.</li><li>Not someone who profits from you, uses, or is involved in your old life.</li></ul>
<h3>Scripts to reach out</h3>
<table class="nb"><tr><th>When</th><th>Text</th></tr>
<tr><td>Morning check-in</td><td>&ldquo;Day __. Doing my next right step. Praying for you too.&rdquo;</td></tr>
<tr><td>Craving</td><td>&ldquo;Craving is loud. Can you stay on the phone for 15 minutes?&rdquo;</td></tr>
<tr><td>After a slip</td><td>&ldquo;I slipped. I'm telling you because I said I would. Can we make a plan?&rdquo;</td></tr>
<tr><td>Hard emotions</td><td>&ldquo;Not using, but I'm really struggling. I don't want to be alone tonight.&rdquo;</td></tr></table>'''))

# ---- 30 day plan
cal = "".join(f"<div>{n}</div>" for n in range(1, 31))
out.append(page('''<h2>My Next 30 Days</h2>
'''+ph('team/01-field-sunrise-cross.jpg','1.15in','50% 45%')+'''
<p>Seven days was the seed. Now you water it. Put a check or a sticker in each box when you do your daily anchor. Missed one? Skip it and keep going. Don't quit the calendar.</p>
<div class="cal">'''+cal+'''</div>
<div class="tool"><span class="tag">My anchors</span>
<p><b>Daily anchor</b> (10 minutes with God, same time each day): </p>'''+lines(1)+'''<p><b>Weekly anchor</b> (meeting, counselor, church, group): </p>'''+lines(1)+'''<p><b>Person I check in with every Sunday:</b></p>'''+lines(1)+'''</div>
'''+verse("And let us not grow weary of doing good, for in due season we will reap, if we do not give up.","Galatians 6:9")))
out.append(page('''<h2>Weekly Check-In</h2>
<p>Sit down once a week, same day, and answer these. It takes fifteen minutes and it changes everything.</p>
<table class="nb"><tr><th style="width:30%"></th><th>Week 1</th><th>Week 2</th><th>Week 3</th><th>Week 4</th></tr>
<tr><td><b>Days I did my daily anchor</b></td><td style="height:.5in"></td><td></td><td></td><td></td></tr>
<tr><td><b>Meetings / sessions I went to</b></td><td style="height:.5in"></td><td></td><td></td><td></td></tr>
<tr><td><b>Cravings I outlasted</b></td><td style="height:.5in"></td><td></td><td></td><td></td></tr>
<tr><td><b>Slips (and what I learned)</b></td><td style="height:.6in"></td><td></td><td></td><td></td></tr>
<tr><td><b>One win</b></td><td style="height:.6in"></td><td></td><td></td><td></td></tr>
<tr><td><b>Who I told the truth to</b></td><td style="height:.5in"></td><td></td><td></td><td></td></tr>
<tr><td><b>My next right step</b></td><td style="height:.6in"></td><td></td><td></td><td></td></tr></table>
<h3>Rebuilding, one small piece at a time</h3>
<p>Recovery touches everything: sleep, money, work, family, trust. Don't try to fix it all at once. Pick one this month:</p>'''+box("Money: write down what I owe and one payment I can make")+box("Work: one application, one call, one training step")+box("Health: one appointment (dentist, doctor, counselor)")+box("Relationships: one apology made safely, or one boundary set")+box("Purpose: one thing I'm building (a class, a garden, a skill, a ministry step)")+
 '<p class="sig" style="font-size:26px">You did not become her overnight. You became her every time you chose not to go back.</p>'))

# ---- prayers
def pr(title, text): return f'<div class="card2"><b class="h">{title}</b><p style="margin:3px 0"><i>{text}</i></p></div>'
out.append(page('<h2>Prayers for Hard Moments</h2>'+av('team/06-stool-lace-vest.jpg','50% 18%')+'<p>Real prayers, short enough to pray with shaky hands. Change the words to sound like you. God isn&rsquo;t grading the grammar.</p>'+CL+
 pr("When the craving is loud","Jesus, I'm not going to win this one alone. Come stand between me and this. I'm going to drink water, move, and call somebody. Give me fifteen minutes, and then give me fifteen more. Amen.")+
 pr("When it's 3 a.m. and I can't sleep","Lord, You don't sleep, and You're not surprised by me. Quiet my mind. Take the things I can't fix tonight, and let me rest. Show me the one next right step in the morning. Amen.")+
 pr("After a slip","Father, I fell. I'm not going to hide it from You or from the people You've put in my life. I confess it, and I receive Your mercy, because Your Word says there's no condemnation for those in Christ. Help me get up and start at the next right step. Amen.")+
 pr("When I'm angry at God","God, I'm mad, and You already know. I don't understand why some things happened. I'm not going to pretend. But I'm still here, and I'm asking You to meet me in it. Amen.")+
 pr("For the person I love who is still bound","Lord, I can't save them. You can. Give me wisdom to love them without enabling them, and boundaries that protect me and them. Keep them alive today. Put people and doors and truth in their path. Amen.")+
 pr("For the person listening from the floor tonight","Lord, if someone is reading this from the floor tonight, be closer than the pain. Send help, send a phone number, send a person. Let them feel that they are seen and not alone. And give them the courage to take just one more step. In Jesus' name, amen.")))

# ---- scripture cards
cards = [("Psalm 34:18","The LORD is near to the brokenhearted and saves the crushed in spirit."),("Psalm 46:1","God is our refuge and strength, a very present help in trouble."),
 ("Matthew 11:28","Come to me, all who labor and are heavy laden, and I will give you rest."),("1 Corinthians 10:13","...God is faithful, and he will not let you be tempted beyond your ability, but with the temptation he will also provide the way of escape, that you may be able to endure it."),
 ("Lamentations 3:22-23","The steadfast love of the LORD never ceases; his mercies never come to an end; they are new every morning; great is your faithfulness."),("Romans 8:1","There is therefore now no condemnation for those who are in Christ Jesus."),
 ("John 8:36","So if the Son sets you free, you will be free indeed."),("2 Corinthians 12:9","My grace is sufficient for you, for my power is made perfect in weakness."),
 ("Joel 2:25","I will restore to you the years that the swarming locust has eaten."),("Galatians 6:9","And let us not grow weary of doing good, for in due season we will reap, if we do not give up.")]
out.append(page('<h2>Scripture Cards</h2>'+av('team/09-collage-panel-3.jpg','50% 32%')+'<p>Cut these out. Tape one to your mirror, your dashboard, your phone case. Say it out loud when the lie is loud.</p>'+CL+'<div class="cards">'+
 "".join(f'<div class="v">&ldquo;{t}&rdquo;<b>{r} (ESV)</b></div>' for r, t in cards)+'</div>'))

# ---- resources
out.append(page('''<h2>Where to Get Help</h2>
<table class="nb"><tr><th style="width:36%">Need</th><th>Where (U.S.)</th></tr>
<tr><td><b>Emergency</b></td><td>911</td></tr>
<tr><td><b>Suicide &amp; Crisis Lifeline</b></td><td>Call or text 988 &bull; 988lifeline.org</td></tr>
<tr><td><b>Addiction treatment referral (free, 24/7, confidential)</b></td><td>SAMHSA National Helpline 1-800-662-4357 &bull; findtreatment.gov</td></tr>
<tr><td><b>Human trafficking</b></td><td>National Human Trafficking Hotline 1-888-373-7888, text 233733 &bull; humantraffickinghotline.org</td></tr>
<tr><td><b>Domestic violence</b></td><td>National DV Hotline 1-800-799-7233, text START to 88788 &bull; thehotline.org</td></tr>
<tr><td><b>Poison / overdose questions</b></td><td>Poison Control 1-800-222-1222</td></tr>
<tr><td><b>Meetings (12-step)</b></td><td>Alcoholics Anonymous: aa.org &bull; Narcotics Anonymous: na.org</td></tr>
<tr><td><b>Faith-based recovery</b></td><td>Celebrate Recovery: celebraterecovery.com (find a church near you)</td></tr>
<tr><td><b>For families</b></td><td>Al-Anon: al-anon.org &bull; Nar-Anon: nar-anon.org</td></tr>
<tr><td><b>Sexual assault</b></td><td>RAINN 1-800-656-4673 &bull; rainn.org</td></tr></table>
<h3>How to make the first call</h3>
<ol><li>Say: &ldquo;I'm looking for help with (alcohol / drugs / safety). Where do I start?&rdquo;</li><li>Ask about cost and insurance. Many places have sliding scales or free options.</li><li>Ask about medical detox if you've been using daily.</li><li>Write down names and numbers as you go. Bring a person if you can.</li><li>If the first call doesn't work, call another. You only need one yes.</li></ol>
<p style="font-size:11.5px">Outside the U.S.? Search for your country's crisis line and emergency number and write them here: __________________________</p>'''))

# ---- closing
out.append(page('''<h2>You Did It. Now What?</h2>
'''+ph('team/07-collage-panel-1.jpg','1.7in','50% 32%')+'''
<p>Seven days is a seed, not a harvest. You didn't come this far to stop at a seed.</p>
<div class="cta">Keep going &rarr; Linktree: <a href="{{LINKTREE_URL}}">{{LINKTREE_URL}}</a></div>
<h3>Ways to keep walking</h3><ul>
<li><b>Free progress tracker:</b> <a href="{{TRACKER_URL}}">{{TRACKER_URL}}</a></li>
<li><b>Shop the tools:</b> Etsy <a href="{{STORE_URL}}">{{STORE_URL}}</a> &bull; Gumroad <a href="{{GUMROAD_URL}}">{{GUMROAD_URL}}</a> (7HE H0LY REUP)</li>
<li><b>Write to me:</b> <a href="mailto:{{GMAIL_ADDRESS}}">{{GMAIL_ADDRESS}}</a></li>
<li><b>Building your own resource?</b> <a href="{{TEMPLATE_CREATOR_URL}}">Template Creator</a> &bull; <a href="{{PLUGIN_CREATOR_URL}}">Plugin Creator</a></li></ul>
<h3>Where I'll be honest</h3><p>This guide is not treatment. If you take one thing from it, let it be this: <b>tell one real person today.</b> Then come tell me how it went.</p>
<h3>My commitment</h3><div class="tool"><span class="tag">In my own words</span><p>The next right step I'm taking is:</p>'''+lines(2)+'''<p>The person I'm telling is:</p>'''+lines(1)+'''<p>I'll do it by (date): ____________ &nbsp; Signed: ______________________</p></div>
'''+verse("And let us not grow weary of doing good, for in due season we will reap, if we do not give up.","Galatians 6:9")+
 '<p class="sig" style="text-align:center;font-size:30px">Baby, I know what far gone looks like. Now watch what God can do from there. &mdash; Nikki</p>'))

open(os.path.join(HERE, "body.html"), "w").write("\n".join(out))
print("wrote body.html:", len(out), "pages before testimony+legal")
