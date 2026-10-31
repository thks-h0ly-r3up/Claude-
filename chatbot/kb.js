// Knowledge base for the 7HE H0LY R3UP guide.
// Each entry: keys (matching words/phrases), title, body (array of short paragraphs),
// step (a <=10 minute action), verify (how to check it yourself).
// RULES BAKED IN: no income guarantees, no fake urgency, no invented stats,
// scripture marked "confirm edition" until Nikki/clergy verify it.
window.KB = [
{
 id: "welcome", title: "Start here",
 keys: ["hello","hi","hey","start","help","what can you do","who are you","about"],
 body: [
  "I'm the 7HE H0LY R3UP guide. I help you learn GitHub, SEO, how people actually behave online, and what and when to post, and I keep pointing back to the OG: God Almighty.",
  "You survived. Now we rebuild. Pick a lane below or just ask me in your own words."
 ],
 step: "Tap one chip below. Ten minutes is plenty.",
 verify: "I'm a guide, not a church and not a lawyer or doctor. Check me. Truth can withstand honest questions."
},
{
 id: "og", title: "Who is the OG?",
 keys: ["og","who is god","who is the og","is there a god","god real","prove god","skeptic","doubt","atheist","what is there to lose","nothing to lose","crazy lady","why believe","who is this"],
 body: [
  "The OG is the original. The One who was here before your worst day and is still here after it: God Almighty. The Ethiopian Orthodox Tewahedo tradition calls Him Egziabher, 'Lord of the universe,' and 'Tewahedo' means 'made one,' the faith that Christ is fully God and fully man, united.",
  "I won't talk you into it. Here's the invitation: look at a real survivor's story, test it, ask the hard questions, and see what holds. You've already been carrying the weight alone. What's the cost of setting it down for ten minutes and asking Him to show up?",
  "Nobody here is spiritually above you. Nikki is a survivor still rebuilding, standing beside you, not over you."
 ],
 step: "Say one honest sentence out loud or on paper: 'God, if You're real, I'm tired. Show me.' That's it. Eyes open is fine.",
 verify: "Ask a priest or deacon from an Ethiopian Orthodox Tewahedo parish, and read the Gospel of John start to finish and judge it for yourself."
},
{
 id: "testimony", title: "Nikki's testimony",
 keys: ["testimony","nikki","story","big boy","bully","dog","survivor","her story","what happened"],
 body: [], // filled at runtime from testimony.js
 step: "Write down one thing in your own life you never expected to survive. Just one line.",
 verify: "A testimony is personal witness, not doctrine. Weigh it, then weigh Scripture and the Church's teaching separately."
},
{
 id: "github-start", title: "GitHub, from zero",
 keys: ["github","git","repo","repository","commit","push","branch","pull request","pr","fork","clone","version control"],
 body: [
  "GitHub is a storage-and-history shelf for your files. A repository (repo) is one project folder. A commit is a saved snapshot with a note. A branch is a safe copy to try changes. A pull request is you saying 'here's my change, review it, then merge it.'",
  "Why it matters for 7HE H0LY R3UP: your printables, devotionals and this chatbot live in a repo. GitHub Pages can turn the repo into a free website, so your work has a home you own.",
  "The loop: change a file, commit with a plain note ('Add day 3 devotional'), push, open a pull request, merge. Small commits. One idea each."
 ],
 step: "Open your repo, click a file, and read its history. Seeing that every change is saved takes the fear out of it.",
 verify: "docs.github.com has 'Quickstart for repositories' and 'About GitHub Pages.' Follow it with the page open next to you."
},
{
 id: "github-pages", title: "Publish this chatbot free",
 keys: ["publish","host","deploy","website","go live","domain","online","pages","github pages","hosting"],
 body: [
  "This chatbot is plain HTML, CSS and JavaScript, so there's no server and no monthly bill.",
  "In your repo: Settings, then Pages, then deploy from the branch you merged to, folder /root. Your site gets a github.io address. A custom domain is optional and costs money. Skip it until the work is earning."
 ],
 step: "Merge the branch, open Settings > Pages, pick the branch, save. Come back in a few minutes.",
 verify: "GitHub's own Pages docs show the current screens. Buttons move, so trust the docs over my memory."
},
{
 id: "seo", title: "SEO, plain English",
 keys: ["seo","search","google","rank","keywords","keyword","find me","search engine","traffic","blog","title tag","meta"],
 body: [
  "SEO is helping the right person find you when they're already searching. Not tricks. Answers.",
  "Four things that matter: (1) Write the exact question your reader types, as a headline. (2) Answer it plainly in the first few lines. (3) Give each page one clear topic, a clear title and a short description. (4) Link your pages to each other, and make the site load fast on a phone.",
  "Your reader's real searches sound like: 'how to start over after abuse,' 'Christian journal for anxiety,' 'what is the Ethiopian Orthodox canon.' Those are people hurting or hungry. Serve them, don't bait them.",
  "SEO is slow. Months, not days. Nobody can honestly promise you a ranking."
 ],
 step: "Type 3 questions a hurting person would search. Make each one a future page title.",
 verify: "Read Google's own 'SEO Starter Guide' from Google Search Central, and search your exact phrase to see who already answers it."
},
{
 id: "people", title: "How people operate",
 keys: ["people","psychology","behavior","behaviour","audience","trust","why people buy","customers","attention","scroll","emotion","connect","engagement","understand people","how people"],
 body: [
  "People don't buy from strangers. They move from seen to safe to trusted. That takes repeated, honest contact.",
  "A hurting person scrolls tired. Short sentences. One idea. No shame. They check: 'Is this person real? Do they get it? Will they judge me?' Answer those three before you ask for anything.",
  "Trauma changes attention. Some folks can't handle intensity. Give them an exit: eyes open, pause, skip. Control builds trust.",
  "Most people watch long before they speak. Count the silent ones. They're listening."
 ],
 step: "Re-read your last post as a tired stranger. Did it feel safe? Fix one line.",
 verify: "Notice your own behavior this week: what made YOU trust or unfollow someone? Your answer is real data."
},
{
 id: "posting", title: "What and when to post",
 keys: ["post","posting","when to post","what to post","schedule","content","calendar","consistency","frequency","time","instagram","tiktok","facebook","youtube","social","reels","hook","algorithm","viral","caption"],
 body: [
  "There is no magic hour. Anyone selling you one is guessing. Your best time is when YOUR people are awake and scrolling. Your own analytics will show it after a few weeks.",
  "Every post, same bones: (1) A hook naming a real struggle. (2) Direct teaching with a source. (3) A step under ten minutes. (4) 'Check the source yourself.' (5) The invitation to reach out.",
  "A sane rhythm for a one-woman operation: 3 posts a week you can keep up, one longer teaching a week, and one story post. Consistency beats volume. Rest isn't failure.",
  "Rotate: Teaching, Testimony, Practical Step, Question to the audience, and Scripture or History. If every post sells, nobody stays."
 ],
 step: "Draft one post right now using the five bones above. Save it. Don't post tonight if you're tired.",
 verify: "Use each platform's free insights for 4 weeks. Compare your own posts. Your numbers beat my advice."
},
{
 id: "dos-donts", title: "Do and don't",
 keys: ["do","dont","don't","avoid","mistake","wrong","rules","should i","shouldn't","bad idea","what not to do","pitfall","scam","fake"],
 body: [
  "DO: tell the truth, cite your source, name a real struggle, give one small step, answer comments by hand, rest.",
  "DON'T: promise income or healing, use fake countdowns or 'last chance' pressure, shame anyone's symptoms, say struggle means weak faith, attack whole groups or churches, post someone else's pain without permission, or claim to be healed all the way. You're still rebuilding. Say so.",
  "DON'T copy a bigger account's voice. Yours already works: Southern, short, fierce, kind."
 ],
 step: "Pick one DON'T you've done lately. Forgive yourself, fix the next post.",
 verify: "Check the FTC's 'Endorsement Guides' and platform rules for what you must disclose when you sell."
},
{
 id: "money", title: "Making money honestly",
 keys: ["money","income","sell","price","pricing","revenue","profit","earn","business","monetize","shopify","etsy","product","digital product","funnel","offer","pay","paid","charge","free"],
 body: [
  "Nobody can guarantee you income, including me. What I can show is a path that tends to be honest and sustainable.",
  "The Three Rounds (see the business model): Round 1 is free and generous. Round 2 is a low-cost printable or devotional. Round 3 is deeper, paid, and still optional. Nobody is ever pushed.",
  "Price low enough that a tight budget can say yes. Offer a free low-energy alternative of anything paid. Say plainly what the product is and isn't. It isn't therapy, and it isn't a promise.",
  "Track three numbers only: people who received something free, people who bought, and people who wrote back. That last one is the heart."
 ],
 step: "Write the one-sentence promise of your first paid product. If it guarantees results, cut that part.",
 verify: "Check your state's rules for selling digital goods and taxes, and ask an accountant before you count on any number."
},
{
 id: "canon", title: "Ethiopian canon, why it matters here",
 keys: ["ethiopian","canon","tewahedo","enoch","jubilees","geez","ge'ez","orthodox","81 books","books of the bible","meqabyan","amharic","scripture","bible","ethiopia"],
 body: [
  "The Ethiopian Orthodox Tewahedo Church holds a broader canon than most Western Bibles. It is commonly described as 81 books and includes works like 1 Enoch and Jubilees preserved in Ge'ez. Counts and lists vary by source, so check the exact list you're citing.",
  "In this project, Ethiopian tradition leads. Western translations are cited only to show omissions or differences, never as the base.",
  "Dead Sea Scrolls are historical and textual evidence. They are not canon or doctrine, and I'll always label which is which.",
  "I am not a scholar or a priest. For doctrine, ask your parish clergy."
 ],
 step: "Find the nearest Ethiopian Orthodox Tewahedo parish online and read how they describe their own canon.",
 verify: "Check the exact edition, translator, book, chapter and verse before you quote anything. Versification differs between traditions."
},
{
 id: "language", title: "The language we recognize",
 keys: ["language","voice","tone","street","slang","cowgirl","southern","brand voice","words","speak","talk like"],
 body: [
  "Street language flipped holy: the words folks already use for loyalty, betrayal, survival and respect, pointed at the One who actually earned it.",
  "'OG' means original, the one who was there first and stayed. That's God Almighty. Use it with respect, never as a joke at His expense.",
  "Keep it short. Keep it punchy. Raw language only where it serves the truth. Never glorify harm."
 ],
 step: "Rewrite one sentence of yours so a tired 16-year-old and a tired 60-year-old would both get it.",
 verify: "Read it out loud. If it sounds like a brochure, it isn't you yet."
},
{
 id: "step-now", title: "Give me a step",
 keys: ["step","next step","what now","where do i start","overwhelmed","too much","stuck","tired","exhausted","can't","cant","low energy"],
 body: [
  "Then we go small. One thing. Ten minutes or less.",
  "Pick ONE: (a) Drink water and breathe slowly, eyes open or closed. (b) Write one line to God, honest, any words. (c) Open this repo and read one file. (d) Draft one post and save it unposted."
 ],
 step: "Do (a) first. Then pick one more if you have it. Stopping there still counts.",
 verify: "If you feel unsafe or can't cope, reach a real person now (see the safety note below)."
}
];

window.CRISIS_KEYS = ["suicide","kill myself","end my life","want to die","self harm","self-harm","hurt myself","being abused","abuse right now","not safe"];
window.CRISIS_TEXT = [
  "I'm really glad you said that out loud. You matter, and you don't have to hold this alone.",
  "If you're in the U.S., call or text 988 (Suicide & Crisis Lifeline) right now. If you're in immediate danger, call 911. Outside the U.S., contact your local emergency number.",
  "I'm a guide, not a counselor, and this is bigger than a chatbot. Please reach a real person now. If you can, tell someone near you."
];

window.CHIPS = [
  "Who is the OG?",
  "Tell me Nikki's story",
  "GitHub from zero",
  "Explain SEO simply",
  "What should I post?",
  "How do I make money honestly?",
  "Do and don't"
];
