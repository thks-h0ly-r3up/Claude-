// Run: node chatbot/test.js
global.window = global;
require("./kb.js");
const E = require("./engine.js");
const cases = [
  ["how do I use github pages", "github-pages"],
  ["what is a pull request", "github-start"],
  ["explain SEO to me", "seo"],
  ["when should I post on instagram", "posting"],
  ["how do I make money selling a product", "money"],
  ["is there a god?", "og"],
  ["tell me about big boy", "testimony"],
  ["what do the Ethiopian books include", "canon"],
  ["I'm overwhelmed and tired", "step-now"],
  ["what should I avoid doing", "dos-donts"],
  ["hello", "welcome"],
];
let fail = 0;
for (const [q, want] of cases) {
  const r = E.answer(q, window.KB, window.CRISIS_KEYS);
  const got = r.entry && r.entry.id;
  const ok = got === want; if (!ok) fail++;
  console.log((ok ? "PASS " : "FAIL ") + JSON.stringify(q) + " -> " + got + (ok ? "" : " (wanted " + want + ")"));
}
const c = E.answer("I want to die", window.KB, window.CRISIS_KEYS);
console.log((c.crisis ? "PASS " : "FAIL ") + "crisis routing"); if (!c.crisis) fail++;
const n = E.answer("zzzz qqqq", window.KB, window.CRISIS_KEYS);
console.log((!n.entry ? "PASS " : "FAIL ") + "no-match fallback"); if (n.entry) fail++;
process.exit(fail ? 1 : 0);
