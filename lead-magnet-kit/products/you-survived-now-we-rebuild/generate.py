#!/usr/bin/env python3
"""Generates body.html for 'You Survived. Now We Rebuild.' (7-day devotional).
   Edit the text here, then: python3 products/you-survived-now-we-rebuild/generate.py && python3 build.py
   Every page below has exactly one <!--FOOTER--> so page numbers and the table of contents stay in sync.
"""
import os, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = "7HE H0LY REUP"
TODAY = datetime.date.today().strftime("%B %d, %Y").replace(" 0", " ")

def lines(n): return '<div class="row"><div class="line"></div></div>' * n
def box(t): return f'<div class="row"><div class="box"></div><div style="flex:1;font-size:13px">{t}</div></div>'
def verse(text, ref): return f'<div class="verse"><b>{ref} (ESV)</b>{text}</div>'
def page(inner, brand=""):
    b = f'<div class="brand">{brand}</div>' if brand else ""
    return f'<section class="page"><div class="band"></div>{b}{inner}<!--FOOTER--></section>'
MINI = ('<div class="crisis">Need help right now? Call/text <b>988</b> &bull; SAMHSA <b>1-800-662-4357</b> &bull; '
        'Emergency <b>911</b> &bull; Local resources: <b>211</b></div>')
S = '<span class="lbl s">Scripture says</span>'
M = '<span class="lbl m">My story</span>'
A = '<span class="lbl a">Application</span>'

DAYS = [
 dict(t="Tell God the Truth Before You Know How to Clean It Up", tag="Psalm 142",
  ground="Look around and name five things you can see. Keep your eyes open the whole time. If that doesn't help, hold something cool or textured instead, or skip this and go straight to the Scripture.",
  presence="Lord, whatever is true about where I am right now, be in it with me. Amen.",
  intro="The heading of Psalm 142 places David in a cave. It is a prayer with no polish on it.",
  passage=[("With my voice I cry out to the LORD; with my voice I plead for mercy to the LORD. I pour out my complaint before him; I tell my trouble before him.","Psalm 142:1-2"),
           ("Look to the right and see: there is none who takes notice of me; no refuge remains to me; no one cares for my soul. I cry to you, O LORD; I say, &ldquo;You are my refuge, my portion in the land of the living.&rdquo;","Psalm 142:4-5")],
  teach=[(S,"David doesn't clean this up before he prays it. He names his trouble, his fear, and his loneliness (&ldquo;no one cares for my soul&rdquo;) and then turns toward God as his refuge in the same breath. He also says that in the path he walks, others have &ldquo;hidden a trap&rdquo; for him (verse 3). The Bible does not hide how raw honest prayer can be."),
         (M,"For a long time I thought I had to get myself together before I could pray. I didn't know how to be honest with God and honest with people at the same time. I still don't always."),
         (A,"You are allowed to start with the mess. Honesty with God is where you begin, not where you stay: the next step is usually a person, a plan, and a place to get help. David's feeling that no one cares is real to him, and it is not God's verdict on your worth.")],
  decl=["I can tell God the truth before I know how to clean it up.","Honesty is where I start. It is not where I have to stay.","I do not have to explain my pain to be allowed to bring it."],
  lens=("#human","Shame makes the body brace and the mouth go quiet.","#truthmode","God invites honest complaint. It is not faithlessness.","#futureyou","Truth-telling is the first brick of anything I rebuild."),
  prompts=["If I could say one true thing to God with no clean-up, it would be&hellip;","Where have I been performing &ldquo;fine,&rdquo; and what has it been costing me?","Who, if anyone, has earned a small piece of my truth? (&ldquo;No one yet&rdquo; is a real answer.)"],
  action="Say or write one honest sentence to God. Whisper it, type it, or scribble it. If it is safe and you are able, tell one trusted person one true sentence. If you have no one yet: text or call 988, or call SAMHSA at 1-800-662-4357 (free, any hour). You do not have to give details to reach out.",
  sup="Lord, I don't have the words, and I don't have it together. This is what is true right now: ____________. I'm not asking You to be impressed. I'm asking You to be my refuge. Show me one safe person or one safe step. Keep me from pretending today. In Jesus' name, amen."),

 dict(t="The God Who Sees", tag="Genesis 16",
  ground="Place a hand on something nearby: a table, your leg, a blanket. Notice its temperature and texture. Keep your eyes open if you like. Skip this if touch isn't comfortable and try listening for three sounds instead.",
  presence="Lord, You see where I am. Let me know I am not invisible. Amen.",
  intro="Hagar was an Egyptian servant in Abram and Sarai's household. She was treated harshly, and she ran.",
  passage=[("The angel of the LORD found her by a spring of water in the wilderness&hellip; And he said, &ldquo;Hagar, servant of Sarai, where have you come from and where are you going?&rdquo; She said, &ldquo;I am fleeing from my mistress Sarai.&rdquo;","Genesis 16:7-8"),
           ("So she called the name of the LORD who spoke to her, &ldquo;You are a God of seeing,&rdquo; for she said, &ldquo;Truly here I have seen him who looks after me.&rdquo;","Genesis 16:13")],
  teach=[(S,"Sarai gave Hagar to Abram to bear a child, and when Hagar conceived, Sarai &ldquo;dealt harshly with her, and she fled&rdquo; (verse 6). God finds Hagar alone in the wilderness, calls her by name, and asks her what is true: where she has come from and where she is going. She answers honestly. Then she names God &ldquo;a God of seeing.&rdquo; The text also records that the angel told her to return (verse 9). That is what happened to her in her story. It is not an instruction for anyone in danger today to go back to someone who hurts them."),
         (A,"When you have been used, controlled, or ignored, it is easy to believe nobody saw it. Hagar's story says God saw someone with no power, no status, and no safe place to go. Being seen does not mean everything is fixed. It means you are not alone in it, and it can be the start of getting safe."),
         (A,"Safety is not disobedience. Leaving a dangerous situation is not simple, and no one gets to shame you for how long it takes. If someone is hurting or controlling you, a trained advocate can help you plan: National Domestic Violence Hotline 1-800-799-7233 (text START to 88788) or the National Human Trafficking Hotline 1-888-373-7888 (text 233733).")],
  decl=["God sees me where I am.","Getting safe is wise. It is not weak.","Forgiving someone does not mean I owe them access to me."],
  lens=("#human","A body that has been controlled learns to stay small and watch the room.","#truthmode","Scripture records what happened to Hagar. It does not tell survivors to stay in danger.","#futureyou","Safety first. Then stability. Then strength."),
  prompts=["Where did I learn that nobody was looking out for me?","What would it mean if God saw what happened and it mattered to Him?","What one safety step would feel real to me right now, not perfect?"],
  action="Pick one safety step: save 988, SAMHSA (1-800-662-4357) and a hotline number in your phone or on paper where only you will find it; name one place you could go if you had to leave; or set one thing out of reach tonight. If someone monitors your phone, use a safe device and clear your history after. If you have no phone, dial 211 from any public phone or ask a library to help.",
  sup="Father, You are a God of seeing. See me here. Let me feel the difference between being watched and being seen. Put safe people and safe places within reach. Give me courage for one step, and protect everyone who is still trapped tonight. In Jesus' name, amen."),

 dict(t="Bread, Water, and Rest", tag="1 Kings 19",
  ground="Breathe in through your nose for a count of four and out slowly for six, three times, eyes open. If breathing exercises make you feel worse, skip them: press your feet into the floor or splash cool water on your hands instead.",
  presence="Lord, meet my body where it is tonight. Amen.",
  intro="Elijah had just seen God do enormous things. Then Queen Jezebel threatened his life, and he ran.",
  passage=[("But he himself went a day's journey into the wilderness and came and sat down under a broom tree. And he asked that he might die&hellip; And he lay down and slept under a broom tree. And behold, an angel touched him and said to him, &ldquo;Arise and eat.&rdquo;","1 Kings 19:4-5"),
           ("And the angel of the LORD came again a second time and touched him and said, &ldquo;Arise and eat, for the journey is too great for you.&rdquo;","1 Kings 19:7")],
  teach=[(S,"Elijah is afraid, exhausted, and asking to die. God's first response is not a lecture. It is food, water, and sleep, twice, and then the journey continues (verses 5-8). Later, God meets him not in the wind, the earthquake, or the fire, but in &ldquo;a low whisper&rdquo; (verses 11-13)."),
         (A,"Here is a plain-language way to think about it, not a diagnosis: when a body decides it is in danger, it can push you toward fighting, running, freezing, or shutting down. After long stretches of that, people often crash into exhaustion, numbness, or despair. That is not weak faith. It is a body that has been carrying too much."),
         (A,"So tend the body. Water, real food, sleep, medication as prescribed, and medical care matter. If you have been drinking heavily or using opioids, benzodiazepines, or other drugs every day, do not stop suddenly on your own: withdrawal from some substances can be dangerous. Call a doctor, an ER, or SAMHSA (1-800-662-4357) first. Prayer belongs beside that care, not in place of it.")],
  decl=["Rest is not laziness.","My body has been carrying a lot.","Needing help with the basics does not make me a failure."],
  lens=("#human","Exhaustion can look like apathy, anger, or hopelessness.","#truthmode","God tends Elijah's body before addressing his despair.","#futureyou","Stability starts with sleep, food, and someone who knows my plan."),
  prompts=["What is my body asking for that I keep overriding?","When I feel unsafe, what does my body tend to do: fight, run, freeze, or try to please?","What would &ldquo;enough&rdquo; look like today? Not a whole life. Just today."],
  action="Do the smallest basic you can: a full glass of water, something real to eat, and a bedtime you can keep. If food or housing is hard right now, call 211 for local food, shelter, and clinic options. If you have been using daily and want to stop, call SAMHSA or a doctor first.",
  sup="Lord, You fed Elijah before You gave him another assignment. Feed me. Give me sleep. Give me the humility to ask for help with the basics and the wisdom to find safe care. Meet me in the quiet places, even when I can't hear much. In Jesus' name, amen."),

 dict(t="When I Don't Do What I Want", tag="Romans 7-8",
  ground="Press your feet flat on the floor and notice the weight of your body in the chair or bed. Look at a color in the room and name it. Keep your eyes open. If your body wants to move instead, stand and stretch.",
  presence="Lord, I'm here, and so are You. Let me be honest without being crushed. Amen.",
  intro="Paul wrote to believers in Rome. In this passage he describes an honest, painful struggle with doing what he does not want to do.",
  passage=[("For I do not understand my own actions. For I do not do what I want, but I do the very thing I hate&hellip; For I do not do the good I want, but the evil I do not want is what I keep on doing.","Romans 7:15, 19"),
           ("Wretched man that I am! Who will deliver me from this body of death? Thanks be to God through Jesus Christ our Lord!","Romans 7:24-25a"),
           ("There is therefore now no condemnation for those who are in Christ Jesus.","Romans 8:1")],
  teach=[(S,"Paul does not hide the struggle. He also does not stay in it: the answer to &ldquo;who will deliver me?&rdquo; is &ldquo;thanks be to God through Jesus Christ,&rdquo; and chapter 8 begins with &ldquo;no condemnation.&rdquo; Christians disagree about exactly which stage of Paul's life this passage describes, so hold that with humility. What is plain is that honest struggle and Christ as deliverer sit side by side."),
         (A,"A craving is a signal, not a verdict. It usually rises, peaks, and passes. What you do next is where your choices live. &ldquo;No condemnation&rdquo; does not mean &ldquo;no consequences,&rdquo; and understanding why you struggle is not the same as excusing what you do. Both are true: I understand why you learned to survive like that, and we have to look at what it is costing you now."),
         (A,"Relapse does not make anyone disposable. It is information: where the plan had a hole, what the trigger was, who you didn't call. Willpower alone runs out. Support, a plan, and honest people do not.")],
  decl=["A craving is a signal, not a verdict.","There is no condemnation for me in Christ, and there is still work to do.","I do not have to fight this alone."],
  lens=("#human","Cravings and shame can hit the body at the same time.","#truthmode","Honest struggle is in the Bible. Excuses are not.","#futureyou","Small, repeated choices with support become a pattern."),
  prompts=["What are my top three triggers (people, places, feelings, times of day)?","Where do I need help instead of more willpower?","If I slipped this week, what could I learn without beating myself up?"],
  action="Write your top three triggers and one &ldquo;way out&rdquo; for each: leave, call, drink water, go outside, put your hands on something. Then choose your &ldquo;call first&rdquo; person and text them so they know. When a craving hits, set a 15-minute timer before you decide anything.",
  sup="Lord, You know the things I keep doing that I hate. I confess them without hiding. Give me a way out before I need it, and people who will pick up the phone. Thank You that there is no condemnation for me in Christ. Teach me what to change. In Jesus' name, amen."),

 dict(t="Jesus Wept", tag="John 11",
  ground="Put one hand on your chest or your stomach and notice it move as you breathe, without changing it. Keep your eyes open. If this brings up too much, put your hand on a table instead or skip it.",
  presence="Lord, be with me in the grief. I don't need to explain it. Amen.",
  intro="Lazarus, the brother of Mary and Martha, has died. When Jesus arrives, Lazarus has already been in the tomb four days.",
  passage=[("Now when Mary came to where Jesus was and saw him, she fell at his feet, saying to him, &ldquo;Lord, if you had been here, my brother would not have died.&rdquo; When Jesus saw her weeping, and the Jews who had come with her also weeping, he was deeply moved in his spirit and greatly troubled.","John 11:32-33"),
           ("And he said, &ldquo;Where have you laid him?&rdquo; They said to him, &ldquo;Lord, come and see.&rdquo; Jesus wept.","John 11:34-35")],
  teach=[(S,"Mary says out loud what many people feel: &ldquo;If you had been here.&rdquo; Jesus does not correct her. He is deeply moved and troubled, and He weeps, even though the story goes on to show He will raise Lazarus. Tears and belief are in the same scene. The passage does not say every loved one is restored in this life, and it does not explain why some people are not."),
         (M,"I lost my sister to addiction. I can't tell you why God allowed it, and I won't pretend to. What I know is that He can meet you in the grief without a tidy explanation. I wish she had somewhere to reach, and I can't say it would have changed her outcome."),
         (A,"You do not have to hurry grief, clean it up, or turn it into a lesson. Anger and questions can be part of it. You may also be grieving years, safety, versions of yourself, or people who are still alive but not safe. If grief turns toward thoughts of hurting yourself, please call or text 988.")],
  decl=["Jesus makes room for grief.","I do not have to explain my pain to be allowed to feel it.","Missing them does not mean I'm stuck."],
  lens=("#human","Grief lives in the body: heavy chest, tired eyes, sudden waves.","#truthmode","&ldquo;Everything happens for a reason&rdquo; is not in this passage. Jesus weeps.","#futureyou","Honoring what I lost can be part of what I build."),
  prompts=["Who or what am I grieving (people, years, safety, a former self)?","What do I wish I could say to them, or to God?","What would honor them that is not self-destructive?"],
  action="Give your grief a small container: say their name out loud, write a short letter you don't have to send, or light a candle for five minutes. Some churches and community groups host grief support. Ask, or call 211 to find one near you.",
  sup="Jesus, You wept at a grave. Meet me at mine. I bring You the anger, the questions, and the ache. I don't need an explanation to know You are near. Hold the people I miss, help me grieve without going under, and show me one way to honor them. In Your name, amen."),

 dict(t="Wise as Serpents: Trust Is Not Automatic", tag="John 2 &bull; Matthew 10",
  ground="Notice where your body feels most tense and name it. Then find something in the room that feels steady and look at it for ten seconds. Keep your eyes open. Skip if it isn't helping.",
  presence="Lord, give me wisdom, and keep me from shame while I learn. Amen.",
  intro="Jesus was loved and followed by crowds. John tells us something surprising about how He handled trust.",
  passage=[("But Jesus on his part did not entrust himself to them, because he knew all people and needed no one to bear witness about man, for he himself knew what was in man.","John 2:24-25"),
           ("Behold, I am sending you out as sheep in the midst of wolves, so be wise as serpents and innocent as doves.","Matthew 10:16")],
  teach=[(S,"In John 2:23-25, many people believed in Jesus because of the signs, but He &ldquo;did not entrust himself to them.&rdquo; He loved them and He was still discerning. In Matthew 10:16 He tells His disciples to be wise as serpents and innocent as doves. Paul also writes: &ldquo;If possible, so far as it depends on you, live peaceably with all&rdquo; (Romans 12:18), and Colossians 3:13 calls believers to forgive as the Lord forgave."),
         (A,"Forgiveness releases a debt. Trust is rebuilt by consistent, safe behavior over time. You can forgive someone and never give them access to you again. Boundaries protect; they are not punishment. Nobody gets to use Scripture to pressure you to stay in danger or hand your safety back to someone who has not changed."),
         (A,"If you have been hurt by people who used faith to control you, that is spiritual abuse, and it is not what Jesus does. And where you did harm, understanding your history is not an excuse: safe accountability, repair when it is safe, and changed behavior matter. Leaving danger is not simple. A hotline advocate can help you plan.")],
  decl=["Forgiveness does not automatically restore trust or access.","A boundary can protect without becoming punishment.","I can be kind and careful at the same time."],
  lens=("#human","Trauma can make trust feel like a trap or a test I keep failing.","#truthmode","Jesus loved people and did not entrust Himself to everyone.","#futureyou","Discernment is a skill I can practice."),
  prompts=["Where have I confused forgiveness with access?","Who has shown me steady care over time, not just kind words?","What boundary would protect what I am rebuilding?"],
  action="Write one boundary sentence and say it out loud once, alone: &ldquo;I forgive you, and I'm not letting you back in.&rdquo; &ldquo;No, thank you. I'm not doing that anymore.&rdquo; If the person may react with violence, do not announce it. Talk to a hotline advocate first (1-800-799-7233).",
  sup="Lord, give me wisdom without bitterness. Show me who is safe and who is not. Heal what I learned about trust from people who used me. Where I have caused harm, give me courage for honest, safe repair. Keep me innocent as a dove and wise as a serpent. In Jesus' name, amen."),

 dict(t="Tended Ground", tag="John 15",
  ground="Notice something growing or alive nearby: a plant, a tree through a window, even your own pulse. Look at it and take one slow breath. Keep your eyes open. If nothing is near, look at your hands.",
  presence="Lord, meet me here, and help me stay connected to You. Amen.",
  intro="On the night before His crucifixion, Jesus told His disciples He was the vine, and they were the branches.",
  passage=[("I am the true vine, and my Father is the vinedresser. Every branch in me that does not bear fruit he takes away, and every branch that does bear fruit he prunes, that it may bear more fruit.","John 15:1-2"),
           ("Abide in me, and I in you. As the branch cannot bear fruit by itself, unless it abides in the vine, neither can you, unless you abide in me.","John 15:4")],
  teach=[(S,"The center of the passage is abiding: staying connected to Jesus. Fruit comes from that connection, not from striving alone. The vinedresser prunes the branches that bear fruit &ldquo;that it may bear more fruit&rdquo; (verse 2). A few lines later, Jesus says, &ldquo;apart from me you can do nothing&rdquo; (verse 5)."),
         (A,"A vineyard is not a bando. It is tended over seasons: watered, trimmed, protected, waited on. Pruning in a vine is cutting away what drains it. I don't read that as God causing what was done to you; Scripture doesn't say that. It is about what needs to be released so growth can happen. Isaiah 61:4 speaks of rebuilding &ldquo;the ancient ruins,&rdquo; a promise given to Israel that I take as an encouragement and not a personal guarantee."),
         (A,"You will not rebuild everything by sundown. Choose a daily anchor, a weekly source of support, and one thing you're building. Then repeat. You survived. Now we rebuild, one tended day at a time.")],
  decl=["I stay connected one day at a time.","Growth takes seasons, and I can be patient with mine.","I don't have to rebuild everything by sundown."],
  lens=("#human","Progress can feel invisible, and that is normal.","#truthmode","Abiding is the point. Fruit is what follows, not what I force.","#futureyou","A small anchor kept daily builds peace, stability, and purpose."),
  prompts=["What in my life needs tending (sleep, honesty, community, money, faith)?","What might need pruning: a habit, a relationship, a story I keep telling myself?","What small fruit have I already seen, even a little?"],
  action="Choose one daily anchor (10 minutes with God at the same time each day) and one weekly support (a meeting, counselor, church, or friend). Put both on a calendar or write them where you will see them. If you are short on money or transportation, a phone call, library computer, or free group counts.",
  sup="Jesus, You are the vine. Keep me connected to You when I'm tired, when I slip, and when I'm doing well. Teach me what to release and what to tend. Give me people, patience, and one next right step. I don't have to be finished to belong to You. In Your name, amen."),
]

pages = []   # (toc_title or None, html)
def add(title, html): pages.append((title, html))

# 1 cover
add("Cover", f'''<section class="page"><div class="band"></div><div class="brand">{BRAND}</div>
<h1 style="font-size:52px">You Survived.<br>Now We Rebuild.</h1><div class="subtitle">A 7-Day Devotional for People Rebuilding</div>
<img class="cover-photo" src="../photos/team/03-pink-camo-jacket.jpg" alt="" style="height:4.7in;object-position:50% 8%">
<p style="text-align:center;font-weight:700;margin-top:14px;font-size:14px">Sanctuary &bull; Scripture &bull; Reflection &bull; Soft Action &bull; Prayer</p>
<p style="text-align:center;font-size:12.5px">Brokenness is not the destination. Here is a next step you can actually take.</p><!--FOOTER--></section>''')

# 2 copyright
add("Copyright, Creation Date &amp; Notes", page(f'''<h2>Copyright &amp; Notes</h2>
<p><b>You Survived. Now We Rebuild.</b><br>A 7-Day Devotional for People Rebuilding<br>Created {TODAY}</p>
<p>&copy; 2026 {BRAND}. All rights reserved. No part of this work may be reproduced, distributed, copied, transmitted, or commercially exploited without prior written permission, except as permitted by applicable law. Personal-use license: one individual, non-transferable, for personal use and printing only.</p>
<p><b>Scripture.</b> Scripture quotations are from the ESV&reg; Bible (The Holy Bible, English Standard Version&reg;), &copy; 2001 by Crossway, a publishing ministry of Good News Publishers. Used by permission. All rights reserved.</p>
<h3>How to read the labels in this devotional</h3>
<p><span class="lbl s">Scripture says</span> What the passage explicitly says, read in its context.</p>
<p><span class="lbl m">My story</span> My personal testimony. It is mine, not a claim about what will happen to you.</p>
<p><span class="lbl a">Application</span> Interpretation and practical application. Thoughtful people may see it differently. Test it against Scripture and wise counsel.</p>
<p>Symbols (broken chains, vineyards, anchors) are creative imagery, not literal promises. Nothing in these pages is a guarantee of healing, an outcome, or a spiritual result.</p>
<h3>Important</h3>
<p>This is a devotional and reflection tool. It is not medical, mental health, legal, or professional advice and is not a substitute for treatment, counseling, safe housing, safety planning, or emergency services. The author is not a licensed professional. Please read the full notices on the last page.</p>
<p><b>If you are in danger or crisis:</b> 911 &bull; 988 (call or text) &bull; SAMHSA 1-800-662-4357 &bull; Trafficking Hotline 1-888-373-7888 &bull; DV Hotline 1-800-799-7233</p>'''))

# 3 TOC (filled later)
add("Table of Contents", page('<h2>Table of Contents</h2>%%TOC%%'))

# 4 what's ahead
rows = "".join(f'<tr><td><b>Day {i}</b></td><td>{d["t"]}</td><td>{d["tag"]}</td></tr>' for i, d in enumerate(DAYS, 1))
add("What's Ahead", page(f'''<h2>What&rsquo;s Ahead</h2>
<p>Seven days. Each day takes about 15 to 30 minutes, and you can do it in pieces. You can skip any exercise, do it your own way, or come back to it later. Nothing here asks you to relive your story.</p>
<table class="nb"><tr><th style="width:.8in">Day</th><th>Title</th><th style="width:1.3in">Passage</th></tr>{rows}</table>
<h3>Each day has five parts</h3>
<ol><li><b>Sanctuary:</b> a short, optional grounding exercise and a prayer for presence.</li>
<li><b>Scripture &amp; Teaching:</b> a passage in context, plain explanation, and application.</li>
<li><b>Sacred Reflection:</b> three prompts with space to write. Grief, anger, doubt, and hope are all welcome.</li>
<li><b>Soft Action:</b> one small, realistic step. Not a life overhaul.</li>
<li><b>Supplication:</b> a guided prayer for when you can't find your own words.</li></ol>
<h3>Three lenses you&rsquo;ll see</h3>
<p><b>#human</b> what this feels like in a real body and life. &nbsp;<b>#truthmode</b> what is true and what Scripture supports. &nbsp;<b>#futureyou</b> what repeated small choices can build.</p>'''))

# 5 introduction
add("Introduction", page(f'''<h2>Introduction: Built on the Floor</h2>
<p>This was not built on a clean stage. It was built on the floor.</p>
<p>I lost my sister to addiction. I have survived homelessness, trafficking, abuse, addiction, and more than a decade of manipulation in a destructive relationship. There came a point when I was alone, terrified of people, and struggling to trust anybody. When I reached for help, too often I found strings attached: people who could talk recovery and quote Scripture and still see somebody's wounds as a business opportunity, and places that handed me a watered-down verse and told me to pray it away.</p>
<p>I needed somewhere that could hold the truth about trauma without pushing God out of the room. Somewhere I could tell the truth without being treated like a project, a paycheck, or a failure of faith. I wish my sister had somewhere like that to reach. I can't say it would have changed her outcome. I can build toward making that kind of support easier to find for somebody who is still here.</p>
<p>My American Bully, Big Boy, stood beside me through some of my loneliest days. God met me while I was still trying to get up. I know what it means to go looking for another plug. In my own testimony I call God the OG Plug, my way of pointing old language toward the Source of my hope. That is my metaphor, not a title from Scripture.</p>
<p>I am building as I go. I have not arrived, and I am not qualified to treat anybody. I'm a woman reaching back with what I've learned, what Scripture actually teaches, and something practical you can use.</p>
<p><b>You survived. Now we rebuild.</b> Brokenness is not the destination. Baby, you do not have to rebuild your whole life before sundown. But we do need to choose what happens next.</p>
<p class="sig">&mdash; Nikki &ldquo;Hellshaker&rdquo; Heller</p>'''))

# 6 before you begin
add("Before You Begin", page(f'''<h2>Before You Begin</h2>
<div class="tool" style="border-color:#c0392b"><span class="tag" style="background:#c0392b">Safety first</span>
<p style="margin:3px 0">If you are thinking about hurting yourself, may have overdosed, or are in danger right now, stop and call <b>911</b> or call/text <b>988</b>. Everything else can wait.</p></div>
<h3>Your permissions</h3>
<ul><li>You may keep your eyes open, skip an exercise, or do a different one.</li>
<li>You may write one line instead of five. You may write nothing and just pray.</li>
<li>You never have to write down details that hurt. Use words like &ldquo;that night&rdquo; or &ldquo;what happened.&rdquo;</li>
<li>If a page stirs up more than you can hold, stop and reach for support: a counselor, a trusted person, 988, or SAMHSA (1-800-662-4357).</li>
<li>If you can only do one part a day, do the Soft Action.</li></ul>
<h3>If your situation is hard right now</h3>
<p>No phone, no privacy, no money, unstable housing, no ride, or nobody to call are real limits. Each day offers options that fit fewer resources. Dialing <b>211</b> connects many people with local food, shelter, and clinic help. A library can offer a phone, computer, and quiet.</p>
<h3>Faith and practical help</h3>
<p>Prayer belongs beside treatment, medical care, safe housing, and safety planning. It does not replace them. If you have been using heavily every day, do not stop suddenly on your own; withdrawal from some substances can be dangerous. Call a doctor, an ER, or SAMHSA first.</p>
<h3>Your sanctuary right now</h3>'''+box("Where I'll read this (any place counts): ______________________________")+box("When I'll try it (any time counts): ______________________________")+box("One person who knows I'm doing this (optional): ______________________________")))

# 7-20 days
for i, d in enumerate(DAYS, 1):
    verses = "".join(verse(t, r) for t, r in d["passage"])
    teach = "".join(f'<p style="margin:6px 0;font-size:13.2px;line-height:1.5">{lab} {txt}</p>' for lab, txt in d["teach"])
    decl = '<div class="decl">' + "".join(f"<div>&ldquo;{x}&rdquo;</div>" for x in d["decl"]) + '</div>'
    lens = d["lens"]; lensline = "".join(f'<b>{lens[k]}</b> {lens[k+1]} &nbsp;' for k in (0, 2, 4))
    add(f"Day {i}: {d['t']}", page(f'''<div class="brand">Day {i} of 7 &bull; Read</div><h2 style="font-size:29px">{d["t"]}</h2>
<div class="tool" style="margin-top:12px"><span class="tag">1 &bull; Sanctuary (optional)</span><p style="margin:2px 0;font-size:12.5px">{d["ground"]}</p><p style="margin:3px 0;font-size:12.5px"><i>Prayer for presence: {d["presence"]}</i></p></div>
<h3>2 &bull; Scripture &amp; Teaching</h3><p style="font-size:12.5px;margin:2px 0;color:var(--denim)"><i>{d["intro"]}</i></p>{verses}{teach}{decl}<div class="lens">{lensline}</div>'''))
    prompts = "".join(f'<p style="margin:8px 0 0"><b>{n}.</b> {p}</p>{lines(4)}' for n, p in enumerate(d["prompts"], 1))
    add(None, page(f'''<div class="brand">Day {i} of 7 &bull; Write</div><h2 style="font-size:29px">{d["t"]}</h2>
<div class="tool" style="margin-top:12px"><span class="tag">3 &bull; Sacred Reflection</span><p style="margin:2px 0;font-size:12px;color:var(--denim)"><i>Write as much or as little as you want. All of it is welcome to God.</i></p>{prompts}</div>
<div class="tool" style="border-color:var(--accent)"><span class="tag" style="background:var(--accent)">4 &bull; Soft Action</span><p style="margin:2px 0;font-size:13px">{d["action"]}</p>{box("I did this &nbsp;&nbsp; <span style='color:var(--denim)'>&#9702; part of it &nbsp;&#9702; not today, and that's okay</span>")}</div>
<h3>5 &bull; Supplication</h3><p style="font-size:13px"><i>{d["sup"]}</i></p>{MINI}'''))

# final reflection
add("Final Reflection", page(f'''<h2>Final Reflection</h2>
<p>You made it through seven days. However much or little you did, you showed up. Take a few minutes and look back.</p>
<p style="margin:8px 0 0"><b>1.</b> The day that meant the most to me, and why:</p>{lines(3)}
<p style="margin:8px 0 0"><b>2.</b> Something I told the truth about that I hadn't before:</p>{lines(3)}
<p style="margin:8px 0 0"><b>3.</b> Something that felt hard, or that I skipped, and what that tells me:</p>{lines(3)}
<p style="margin:8px 0 0"><b>4.</b> What I learned about God, and what I'm still asking Him:</p>{lines(3)}
<p style="margin:8px 0 0"><b>5.</b> One thing I'm carrying forward:</p>{lines(3)}
{verse("And let us not grow weary of doing good, for in due season we will reap, if we do not give up.","Galatians 6:9")}'''))

# progress review
prow = "".join(f'<tr><td><b>Day {i}</b><br><span style="font-size:11px">{d["t"]}</span></td><td style="height:.62in"></td><td></td></tr>' for i, d in enumerate(DAYS, 1))
add("Progress Review", page(f'''<h2>Progress Review</h2>
<p>This is not a grade. It is a map of what you did and what to do next.</p>
<table class="nb"><tr><th style="width:2.3in">Day</th><th>What I did (any amount counts)</th><th style="width:2.2in">What I'm carrying forward</th></tr>{prow}</table>
<div class="tool"><span class="tag">Honest check</span>{box("I told the truth to God")}{box("I took at least one safety or health step")}{box("I reached out to at least one person or resource")}{box("I noticed a trigger or a craving and made a plan")}{box("I let myself grieve or rest")}</div>'''))

# next-step challenge
add("Next-Step Challenge", page(f'''<h2>Next-Step Challenge</h2>
<p>You don't have to rebuild your whole life before sundown. Here is what comes next: thirty small days.</p>
<div class="tool"><span class="tag">My 30-day anchors</span>
<p><b>Daily anchor</b> (10 minutes with God, same time each day):</p>{lines(1)}
<p><b>Weekly support</b> (a meeting, counselor, church, or friend; day and time):</p>{lines(1)}
<p><b>One thing I'm building</b> (a skill, job step, budget, home, hobby):</p>{lines(1)}
<p><b>The person I'll check in with every Sunday:</b></p>{lines(1)}</div>
<div class="cal" style="grid-template-columns:repeat(10,1fr)">{"".join(f"<div style='height:.42in'>{n}</div>" for n in range(1,31))}</div>
<p style="font-size:12px">Mark a day when you keep your daily anchor. Missed one? Skip it and keep going. Don't quit the calendar.</p>
{box("If I slip, I will tell one person within 24 hours and start again at the next right step.")}
{verse("I am the vine; you are the branches. Whoever abides in me and I in him, he it is that bears much fruit, for apart from me you can do nothing.","John 15:5")}'''))

# closing prayer
add("Closing Prayer", page(f'''<h2>Closing Prayer</h2>
<p style="font-size:15px;line-height:1.7"><i>Lord Jesus, thank You for meeting me here. Thank You for every honest word I said, and for the ones I couldn't say yet. You know what I carried in with me, and You are not scared of any of it.</i></p>
<p style="font-size:15px;line-height:1.7"><i>Keep me safe. Give me wisdom about who and what to trust. Give me the courage to ask for help and the humility to receive it. Where I have been hurt, be my refuge. Where I have done harm, give me honesty and a safe way to repair it. Hold the people I love and the people I have lost.</i></p>
<p style="font-size:15px;line-height:1.7"><i>I'm not finished, and I don't have to be. Help me take the next right step, and then the next one. Keep me connected to You when I'm strong and when I stumble. And if someone is reading this from the floor tonight, be closer than the pain, send help, and give them courage for one more step. In Jesus' name, amen.</i></p>
<div style="text-align:center;margin-top:24px;font-family:Caveat,cursive;font-size:36px;color:var(--primary)">You survived.<br>Now we rebuild.</div>'''))

# certificate
add("Certificate of Completion", f'''<section class="page"><div class="band"></div>
<div class="cert"><div class="brand">{BRAND}</div><h1>Certificate of Completion</h1>
<p style="font-size:14px">This certifies that</p><div class="nm"></div><div class="cap">Participant name</div>
<p style="font-size:14px;margin-top:22px">has completed the 7-day devotional</p>
<p style="font-family:Caveat,cursive;font-size:38px;color:var(--accent);margin:2px 0">You Survived. Now We Rebuild.</p>
<div class="nm" style="margin-top:12px"></div><div class="cap">Completed devotional title / notes</div>
<div class="sg"><div>Date</div><div>Signature</div></div>
<p style="font-size:11px;margin-top:22px;color:var(--denim)">Completion is about showing up, not perfection.</p></div><!--FOOTER--></section>''')

# resources
add("Where to Get Help", page(f'''<h2>Where to Get Help</h2>
<table class="nb"><tr><th style="width:36%">Need</th><th>Where (U.S.)</th></tr>
<tr><td><b>Emergency</b></td><td>911</td></tr>
<tr><td><b>Suicide &amp; Crisis Lifeline</b></td><td>Call or text 988 &bull; 988lifeline.org</td></tr>
<tr><td><b>Addiction treatment referral (free, 24/7, confidential)</b></td><td>SAMHSA National Helpline 1-800-662-4357 &bull; findtreatment.gov</td></tr>
<tr><td><b>Local food, housing, clinics</b></td><td>Dial 211 &bull; 211.org</td></tr>
<tr><td><b>Human trafficking</b></td><td>National Human Trafficking Hotline 1-888-373-7888, text 233733 &bull; humantraffickinghotline.org</td></tr>
<tr><td><b>Domestic violence</b></td><td>National DV Hotline 1-800-799-7233, text START to 88788 &bull; thehotline.org</td></tr>
<tr><td><b>Sexual assault</b></td><td>RAINN 1-800-656-4673 &bull; rainn.org</td></tr>
<tr><td><b>Poison / overdose questions</b></td><td>Poison Control 1-800-222-1222</td></tr>
<tr><td><b>Meetings</b></td><td>aa.org &bull; na.org &bull; celebraterecovery.com (faith-based) &bull; al-anon.org &bull; nar-anon.org (for families)</td></tr></table>
<h3>Making the first call</h3>
<ol><li>Say: &ldquo;I'm looking for help with (drugs / alcohol / safety / housing). Where do I start?&rdquo;</li>
<li>Ask about cost and insurance. Many places have sliding scales or free options.</li>
<li>Ask about medical detox if you've been using daily.</li>
<li>Write down names and numbers as you go. Bring a person if you can.</li>
<li>If the first call doesn't work, call another. You only need one yes.</li></ol>
<p style="font-size:11.5px">Outside the U.S.? Look up your country's crisis line and emergency number and write them here: ______________________________</p>
<h3>Keep going with 7HE H0LY REUP</h3>
<p>Linktree: <a href="{{{{LINKTREE_URL}}}}">{{{{LINKTREE_URL}}}}</a><br>Etsy: <a href="{{{{STORE_URL}}}}">{{{{STORE_URL}}}}</a><br>Gumroad: <a href="{{{{GUMROAD_URL}}}}">{{{{GUMROAD_URL}}}}</a><br>Email: <a href="mailto:{{{{GMAIL_ADDRESS}}}}">{{{{GMAIL_ADDRESS}}}}</a></p>'''))

# ---- TOC with computed page numbers (page number = position in final book; build.py numbers footers the same way)
toc_rows = ""
for idx, (title, html) in enumerate(pages, 1):
    if title and title not in ("Cover", "Table of Contents"):
        toc_rows += f"<tr><td>{title}</td><td>{idx}</td></tr>"
n = len(pages)
toc_rows += f"<tr><td>My Testimony (Where This Came From)</td><td>{n+1}</td></tr><tr><td>Important Notices &amp; Disclaimers</td><td>{n+2}</td></tr>"
out = [h.replace("%%TOC%%", f'<table class="toc">{toc_rows}</table>') for _, h in pages]
open(os.path.join(HERE, "body.html"), "w").write("\n".join(out))
print("wrote body.html:", n, "pages before testimony + legal")
