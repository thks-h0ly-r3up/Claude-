// Builds the 7HE H0LY R3UP daily tracker (7 designs) + blank bland calendars.
// Run: node build.js   (needs playwright). Outputs HTML + PDF next to this file.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const OUT = __dirname;

// ---------- patterns (restrained, print-light) ----------
const cow = encodeURIComponent(`<svg xmlns='http://www.w3.org/2000/svg' width='260' height='60'><g fill='#1d1d1d' opacity='.9'>
<path d='M10 30c8-14 26-10 30 2s-8 22-20 18-14-8-10-20z'/><path d='M70 12c10-8 28 0 24 12s-18 10-26 4-4-12 2-16z'/>
<path d='M120 34c12-10 30-2 26 12s-24 14-30 4-2-12 4-16z'/><path d='M180 10c8-6 24 2 20 14s-18 10-24 2 0-12 4-16z'/>
<path d='M222 30c10-8 28 2 24 16s-22 10-28 0-2-12 4-16z'/></g></svg>`);
const camo = encodeURIComponent(`<svg xmlns='http://www.w3.org/2000/svg' width='260' height='60'>
<g opacity='.85'><path d='M0 30c14-18 40-14 46 4s-20 24-34 18S-8 44 0 30z' fill='#5c6b3a'/>
<path d='M60 8c12-10 40-4 40 12s-24 18-36 10S52 16 60 8z' fill='#8a7a52'/>
<path d='M120 32c14-14 44-6 40 12s-28 16-38 8-10-14-2-20z' fill='#3f4a2a'/>
<path d='M180 6c14-8 38 0 36 16s-24 18-34 8-8-18-2-24z' fill='#5c6b3a'/>
<path d='M226 34c10-10 34-2 34 14s-26 14-34 6-6-14 0-20z' fill='#8a7a52'/></g></svg>`);
const chain = encodeURIComponent(`<svg xmlns='http://www.w3.org/2000/svg' width='120' height='20'><g fill='none' stroke='#9a8a7c' stroke-width='2'>
<rect x='4' y='4' width='22' height='12' rx='6'/><rect x='20' y='4' width='22' height='12' rx='6' transform='translate(0 0)'/>
<rect x='60' y='4' width='22' height='12' rx='6'/><rect x='76' y='4' width='22' height='12' rx='6'/></g></svg>`);

// ---------- faith-cowgirl icons (inline SVG, drawn in currentColor) ----------
const svg = (inner) => `<svg viewBox="0 0 32 32" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">${inner}</svg>`;
const ICONS = Object.fromEntries(['cross','anchor','jar','chain','hat','boot'].map((n) => [n, `<img src="assets/icons/${n}.png" class="i-${n}" alt="">`]));
const iconRow = (ids) => ids.map((i) => ICONS[i]).join('');

// ---------- 7 designs ----------
const jag = 'polygon(0 0,100% 0,100% 78%,96% 100%,92% 80%,87% 98%,81% 76%,75% 100%,69% 82%,62% 98%,55% 78%,48% 100%,41% 80%,34% 98%,27% 76%,20% 100%,13% 80%,7% 98%,0 78%)';
const pinkCamo = encodeURIComponent(`<svg xmlns='http://www.w3.org/2000/svg' width='260' height='60'>
<g opacity='.9'><path d='M0 30c14-18 40-14 46 4s-20 24-34 18S-8 44 0 30z' fill='#f48fb8'/>
<path d='M60 8c12-10 40-4 40 12s-24 18-36 10S52 16 60 8z' fill='#c2417f'/>
<path d='M120 32c14-14 44-6 40 12s-28 16-38 8-10-14-2-20z' fill='#7d2a56'/>
<path d='M180 6c14-8 38 0 36 16s-24 18-34 8-8-18-2-24z' fill='#f48fb8'/>
<path d='M226 34c10-10 34-2 34 14s-26 14-34 6-6-14 0-20z' fill='#e86aa0'/></g></svg>`);
const THEMES = [
  { id: '01-hot-pink-and-teal', name: 'Hot Pink & Teal', tex: 'tex-01-hot-pink-teal.jpg', ink: '#22232b', a: '#e6007e', b: '#0f7f82', soft: '#ffe9f3', line: '#f0a6cc', stitch: '#159a9c',
    motif: 'HOT PINK · TEAL · FAITH', wash: 'wash-pink', dh: ['crosswrap'], fl: ['paws'], fr: ['jar'] },
  { id: '02-turquoise-sunrise', name: 'Turquoise Sunrise', tex: 'tex-08-sunrise-sky.jpg', ink: '#1f2d2e', a: '#159a9c', b: '#123b3d', soft: '#e3f5f3', line: '#9fd3cf', stitch: '#e8aa4a',
    motif: 'TURQUOISE SUNRISE', wash: 'wash-gold', dh: ['hatpost'], fl: ['paws'], fr: ['bible'] },
  { id: '03-cow-print', name: 'Cow Print', tex: 'tex-03-cow-print.jpg', ink: '#1a1a1a', a: '#e6007e', b: '#1a1a1a', soft: '#f3f3f3', line: '#c4c4c4', stitch: '#159a9c',
    motif: 'COWGIRL STRONG', wash: 'wash-teal', dh: ['cow'], fl: ['paws'], fr: ['bully'] },
  { id: '04-ripped-denim', name: 'Ripped Denim', tex: 'tex-04-ripped-denim.jpg', ink: '#1e2733', a: '#3b5b83', b: '#243a57', soft: '#e3eaf3', line: '#a3b5cc', stitch: '#e6007e',
    motif: 'RIPPED · NOT BROKEN', wash: 'wash-teal', dh: ['denim'], fl: ['paws'], fr: ['jar'] },
  { id: '05-pink-camo', name: 'Pink Camo', tex: 'tex-05-pink-camo.jpg', ink: '#3a1d2e', a: '#c97a92', b: '#7d2a56', soft: '#fde6ef', line: '#efb3cb', stitch: '#e86aa0',
    motif: 'HOLD THE LINE', wash: 'wash-pink', dh: ['concho'], fl: ['paws'], fr: ['jar'] },
  { id: '06-mason-jar-cowgirl', name: 'Mason Jar Cowgirl', tex: 'tex-06-mason-jar-wood.jpg', ink: '#3a2e22', a: '#159a9c', b: '#6b4a2b', soft: '#e4f3ef', line: '#c5b48f', stitch: '#e6007e',
    motif: 'COUNTRY · FAITH · GRIT', wash: 'wash-gold', dh: ['jar'], fl: ['paws'], fr: ['hatpost'] },
  { id: '07-chain-break-anchor', name: 'Chain Break & Anchor', tex: 'tex-07-ombre-chain.jpg', ink: '#22232b', a: '#7a4c9e', b: '#c2186b', soft: '#f3eaf8', line: '#cdb6df', stitch: '#159a9c',
    motif: 'CHAINS BROKEN · ANCHORED', wash: 'wash-purple', dh: ['chain', 'anchor'], fl: ['paws'], fr: ['bully'] },
];
let CUR = THEMES[0];
const decSrc = (n) => (['chain', 'anchor', 'cross', 'hat', 'boot'].includes(n) ? `assets/icons/${n}.png` : `assets/cut/${n}.png`);
const decImgs = (list, cls = '') => list.map((n) => `<img class="d-${n} ${cls}" src="${decSrc(n)}" alt="">`).join('');

// ---------- helpers ----------
const lines = (n, h = 17) => Array.from({ length: n }, () => `<div class="ln" style="height:${h}px"></div>`).join('');
const box = (t) => `<span class="cb"></span>${t}`;
const circles = (n, start = 1) => Array.from({ length: n }, (_, i) => `<span class="num">${i + start}</span>`).join('');
const rows = (n, cols) => Array.from({ length: n }, () => `<tr>${cols.map(() => '<td></td>').join('')}</tr>`).join('');

const baseCss = (t) => `
@page { size: 8.5in 11in; margin: 0; }
:root{ --ink:${t.ink}; --paper:${t.paper}; --a:${t.a}; --b:${t.b}; --soft:${t.soft}; --line:${t.line}; --stitch:${t.stitch}; }
*{ box-sizing:border-box; }
html,body{ margin:0; padding:0; background:#ddd; color:var(--ink); font-family:'Libre Franklin','Helvetica Neue',Arial,sans-serif; font-size:10px; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
.page{ width:8.5in; height:11in; background:linear-gradient(${t.paper}ea,${t.paper}ea),url(assets/${t.tex}) center/cover; position:relative; overflow:hidden; padding:.3in .36in .24in; page-break-after:always; }
.page::before{ content:''; position:absolute; inset:.13in; border:2px solid var(--a); border-radius:10px; pointer-events:none; }
.page::after{ content:''; position:absolute; inset:.18in; border:1.2px dashed var(--stitch); border-radius:7px; pointer-events:none; }
.head{ background:${t.ov ? `linear-gradient(rgba(0,0,0,${t.ov}),rgba(0,0,0,${t.ov})),` : ''}url(assets/${t.tex}) center/cover; min-height:.78in; border-radius:8px; padding:7px 12px; display:flex; justify-content:space-between; align-items:center; position:relative; margin-top:.02in; }
.head.rip{ clip-path:${jag}; padding-bottom:13px; box-shadow:none;  }
.head.pat{ border:1.5px solid var(--b); }
.head .tt{ ${t.pattern ? 'background:#fff;border:1.5px solid var(--b);border-radius:6px;padding:3px 10px;' : ''} }
.brand{ font-size:8px; letter-spacing:2.2px; font-weight:800; text-transform:uppercase; color:${t.pattern ? 'var(--b)' : '#fff'}; ${t.pattern ? '' : 'text-shadow:0 1px 2px rgba(0,0,0,.25);'} }
h1{ margin:0; font-family:'Caveat','Brush Script MT',cursive; font-size:30px; line-height:1; color:${t.pattern ? 'var(--b)' : '#fff'}; ${t.pattern ? '' : 'text-shadow:0 1px 2px rgba(0,0,0,.28);'} }
.tag{ font-size:8px; color:${t.pattern ? 'var(--b)' : '#fff'}; font-weight:600; letter-spacing:.4px; }
.ic{ display:flex; gap:7px; justify-content:center; align-items:center; margin-bottom:2px; } .ic img{ height:36px; width:auto; filter:drop-shadow(0 1px 1px rgba(0,0,0,.35)); } .ic img.i-chain{ height:26px; }
.motif{ font-size:7px; letter-spacing:2px; font-weight:800; color:var(--b); text-align:center; background:rgba(255,255,255,.9); border:1.5px solid var(--b); border-radius:10px; padding:3px 9px 4px; }
.datebar{ display:grid; grid-template-columns:1.25fr 1.5fr 1.1fr; gap:6px; margin:6px 0 5px; }
.field{ border-bottom:1.3px solid var(--b); padding:0 2px 1px; font-weight:700; font-size:8.5px; color:var(--b); height:19px; display:flex; align-items:flex-end; }
.dow{ display:flex; gap:3px; align-items:flex-end; padding-bottom:1px; }
.dow span{ width:15px; height:15px; border:1.3px solid var(--b); border-radius:50%; text-align:center; font-size:8px; line-height:12.5px; font-weight:700; color:var(--b); }
.grid{ display:grid; grid-template-columns:1fr 1fr; gap:6px; }
.col{ display:flex; flex-direction:column; gap:5px; }
.sec{ border:1.3px solid var(--line); border-radius:7px; background:#fff; overflow:hidden; }
.sec>h2{ margin:0; background:var(--a); color:#fff; font-size:8.4px; letter-spacing:1.6px; text-transform:uppercase; padding:2.5px 7px; font-weight:800; display:flex; justify-content:space-between; }
.sec>h2 em{ font-style:normal; font-weight:600; letter-spacing:.3px; text-transform:none; opacity:.95; font-size:7.5px; }
.sec .in{ padding:4px 7px 5px; }
.lab{ font-weight:700; color:var(--b); font-size:8px; }
.row{ display:flex; gap:9px; align-items:center; flex-wrap:wrap; margin:4px 0; }
.cb{ display:inline-block; width:9px; height:9px; border:1.3px solid var(--b); border-radius:2px; margin-right:3px; vertical-align:-1.5px; background:#fff; }
.num{ display:inline-block; width:13px; height:13px; border:1.1px solid var(--b); border-radius:50%; text-align:center; font-size:7.5px; line-height:11px; margin-right:1.5px; color:var(--b); font-weight:700; }
.ln{ border-bottom:1px solid var(--line); }
.fill{ border-bottom:1.1px solid var(--line); display:inline-block; min-width:38px; height:11px; vertical-align:bottom; }
.fill.w{ min-width:66px; }
table{ width:100%; border-collapse:collapse; table-layout:fixed; }
th{ background:var(--soft); color:var(--b); font-size:7.3px; text-align:left; padding:2px 3px; border:1px solid var(--line); letter-spacing:.3px; }
td{ border:1px solid var(--line); height:21px; padding:0 3px; font-size:8.3px; }
td.k{ font-weight:700; color:var(--b); background:var(--soft); }
.small{ font-size:7.4px; color:#5a5560; }
.note{ margin-top:4px; text-align:center; font-size:7.4px; color:#5a5560; }
.foot{ position:absolute; left:.36in; right:.36in; bottom:.2in; text-align:center; font-size:7.2px; color:#5a5560; }
.foot b{ color:var(--b); }
.key{ display:grid; grid-template-columns:repeat(5,1fr); gap:3px 6px; margin:4px 0 0; }
.key div{ border:1px solid var(--line); border-radius:5px; padding:2px 4px; background:var(--soft); font-size:7.6px; }
.key b{ display:inline-block; min-width:12px; height:12px; border-radius:3px; background:var(--a); color:#fff; text-align:center; line-height:12px; margin-right:3px; font-size:8px; }
`;

const brandHead = (title) => `
<div class="hd">
  <div class="hd-photo"></div>
  <img class="hd-wash" src="assets/cut/${CUR.wash}.png" alt="">
  <div class="hd-lw"><div class="hd-label"><div class="brand">7HE H0LY R3UP</div><h1>${title}</h1><div class="tag">You survived. Now we rebuild.</div></div></div>
  <div class="hd-deco">${decImgs(CUR.dh)}</div>
</div>`;

// ---------- page 1: Daily Log ----------
function page1(t) {
  const pat = !!t.pattern;
  return `
<section class="page">
${brandHead('Daily Log')}
<div class="datebar">
  <div class="field">DATE: </div>
  <div class="dow"><span>S</span><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span></div>
  <div class="field">WOKE UP AT: </div>
</div>

<div class="sec" style="margin-bottom:5px"><h2>Check-In <em>Even one box counts. Skip what doesn't fit.</em></h2><div class="in">
  <div class="row"><span class="lab">Overall day (1 rough – 10 good):</span>${circles(10)}<span class="lab" style="margin-left:6px">Energy:</span>${circles(5)}</div>
  <div class="row"><span class="lab">My body is:</span>${box('Calm')}${box('On edge')}${box('Flooded')}${box('Shut down')}${box('Numb')}${box('Safe right now')}${box('Not safe — reach out')}</div>
</div></div>

<div class="grid">
<div class="col">

  <div class="sec"><h2>Sleep <em>last night + today</em></h2><div class="in">
    <div class="row"><span class="lab">Bed</span><span class="fill"></span><span class="lab">Asleep</span><span class="fill"></span><span class="lab">Up</span><span class="fill"></span><span class="lab">Total hrs</span><span class="fill" style="min-width:26px"></span></div>
    <div class="row"><span class="lab">Quality:</span>${box('Rough')}${box('Okay')}${box('Good')}<span class="lab" style="margin-left:4px">Woke up</span><span class="fill" style="min-width:20px"></span><span class="lab">times</span></div>
    <div class="row">${box('Nightmare')}${box('Night sweats')}${box('Ears ringing at bedtime')}${box('Nap')}<span class="fill" style="min-width:34px"></span></div>
    <div class="lab" style="margin-top:2px">Dreams / what woke me:</div>${lines(2, 21)}
  </div></div>

  <div class="sec"><h2>Food, Water &amp; Meds <em>have I eaten? have I drunk?</em></h2><div class="in">
    <div class="row">${box('<b>Haven\'t eaten yet</b>')}<span class="lab">First bite at</span><span class="fill"></span></div>
    <table><tr><th style="width:23%">Meal</th><th style="width:17%">Time</th><th>What I ate / how it sat</th></tr>
    <tr><td class="k">Breakfast</td><td></td><td></td></tr><tr><td class="k">Lunch</td><td></td><td></td></tr>
    <tr><td class="k">Dinner</td><td></td><td></td></tr><tr><td class="k">Snacks</td><td></td><td></td></tr></table>
    <div class="row" style="margin-top:3px"><span class="lab">Water:</span>${Array.from({ length: 8 }, () => '<span class="num">&nbsp;</span>').join('')}<span class="small">cups</span>${box('Caffeine')}${box('Skipped a meal')}</div>
    <div class="row"><span class="lab">Meds / supplements:</span>${box('AM')}${box('Mid')}${box('PM')}${box('Bed')}${box('Missed')}</div>
  </div></div>

  <div class="sec"><h2>Body &amp; Symptoms <em>write times — patterns matter</em></h2><div class="in" style="padding:3px 4px 4px">
    <table><tr><th style="width:30%">Symptom</th><th style="width:7%">Y</th><th style="width:20%">Time(s)</th><th style="width:15%">Ear / Side</th><th style="width:11%">1–10</th><th>Notes</th></tr>
    <tr><td class="k">Ear ringing</td><td></td><td></td><td>L &nbsp;R &nbsp;Both</td><td></td><td></td></tr>
    <tr><td class="k">Headache / pressure</td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td class="k">Dizzy / lightheaded</td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td class="k">Pain (where?)</td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td class="k">Nausea / stomach</td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td class="k">Heart racing / shaky</td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td class="k">Jaw / muscle tension</td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td class="k">Other:</td><td></td><td></td><td></td><td></td><td></td></tr></table>
    <div class="small" style="margin-top:2px">What I was doing when it hit: ____________________________</div>
  </div></div>

  <div class="sec"><h2>Anything Else <em>brain dump — nothing has to make sense</em></h2><div class="in">${lines(4, 21)}</div></div>

</div>
<div class="col">

  <div class="sec"><h2>Anything Happen? <em>quick timeline</em></h2><div class="in" style="padding:3px 4px 4px">
    <table><tr><th style="width:17%">Time</th><th>What happened</th><th style="width:21%">How I felt</th></tr>${rows(11, [1, 2, 3])}</table>
  </div></div>

  <div class="sec"><h2>What God Showed Me <em>prayers · dreams · words</em></h2><div class="in">
    <div class="row">${box('Morning prayer')}${box('Midday')}${box('Evening')}${box('Prayed in the hard moment')}</div>
    <div class="lab">Prayers I prayed / requests:</div>${lines(2, 21)}
    <div class="lab">What God showed me (dream · scripture · word · peace · sign):</div>${lines(2, 21)}
    <div class="lab">Prayers answered / mercy I saw:</div>${lines(1, 21)}
  </div></div>

  <div class="sec"><h2>People · Triggers · Big Boy</h2><div class="in">
    <div class="lab">Who I talked to / contact made:</div>${lines(1, 21)}
    <div class="lab">Trigger (who / what / where) &amp; what helped:</div>${lines(2, 21)}
    <div class="row" style="margin-top:3px"><span class="lab">Big Boy:</span>${box('Fed')}${box('Walked')}${box('Meds')}${box('Alerted me')}${box('Rested together')}</div>
  </div></div>

  <div class="sec"><h2>Thanks · Win · Next Step</h2><div class="in">
    <div class="lab">Thankful for (completed mercy):</div>${lines(2, 21)}
    <div class="row" style="margin-top:3px">${box('<b>10-min soft step:</b>')}<span class="fill w" style="min-width:140px"></span></div>
    <div class="row">${box('Low-energy version:')}<span class="fill w" style="min-width:128px"></span></div>
    <div class="row"><span class="lab">Tomorrow's one thing:</span><span class="fill" style="min-width:100px"></span></div>
  </div></div>

</div>
</div>
<div class="foot"><b>Page 1 of 2.</b> Flip for the full detail log. Personal record, not medical advice — bring patterns (ringing, sleep, dizziness) to your doctor.<br>Share only what feels safe. · We survived. Now let's go back — with truth and a hand out.</div>
</section>`;
}

// ---------- page 2: Detail log ----------
function page2(t) {
  const pat = !!t.pattern;
  const cats = [['B', 'Body / symptom'], ['M', 'Mind / emotion'], ['S', 'Sleep'], ['F', 'Food / water / meds'], ['G', 'God / prayer / word'],
    ['P', 'People / contact'], ['X', 'Safety / incident'], ['$', 'Money / work / legal'], ['H', 'Home / Big Boy'], ['W', 'Win / mercy']];
  return `
<section class="page">
${brandHead('What Happened — Full Detail')}
<div class="datebar" style="grid-template-columns:1.2fr 1fr 1.3fr">
  <div class="field">DATE: </div><div class="field">DAY: </div><div class="field">WHERE I WAS MOST OF THE DAY: </div>
</div>
<div class="sec" style="margin-bottom:5px"><h2>My Categories <em>write the letter in the CAT column</em></h2><div class="in">
  <div class="key">${cats.map(([k, v]) => `<div><b>${k}</b>${v}</div>`).join('')}</div>
</div></div>

<div class="sec"><h2>Detail Log <em>facts first, then feelings · who · where · what helped</em></h2><div class="in" style="padding:3px 4px 4px">
<table>
<tr><th style="width:8%">Time</th><th style="width:6%">CAT</th><th style="width:30%">What happened (just the facts)</th><th style="width:14%">Where / who</th><th style="width:14%">Body felt</th><th style="width:7%">0–10</th><th>What I did / what helped</th></tr>
${Array.from({ length: 17 }, () => '<tr><td style="height:25px"></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>').join('')}
</table>
</div></div>

<div class="grid" style="margin-top:5px">
  <div class="sec"><h2>Patterns I Noticed</h2><div class="in">
    <div class="row">${box('Ringing came with:')}<span class="small">stress · quiet · bedtime · noise · skipped meal · poor sleep</span></div>
    ${lines(3, 21)}
    <div class="row" style="margin-top:3px">${box('Worse after no food')}${box('Worse after bad sleep')}${box('Worse after contact')}</div>
  </div></div>
  <div class="sec"><h2>Tell My Doctor / Counselor / Lawyer</h2><div class="in">
    ${lines(3, 21)}
    <div class="row" style="margin-top:3px">${box('Screenshots / records saved')}${box('Dates &amp; names written')}${box('Told someone safe')}</div>
  </div></div>
</div>

<div class="sec" style="margin-top:5px"><h2>End-of-Day Close <em>nothing unfinished has to be carried tonight</em></h2><div class="in">
  <div class="row"><span class="lab">One thing I got through:</span><span class="fill" style="min-width:200px"></span><span class="lab">One thing I hand to God Almighty tonight:</span><span class="fill" style="min-width:150px"></span></div>
  <div class="row"><span class="lab">Closing prayer / declaration:</span><span class="fill" style="min-width:480px"></span></div>
  <div class="row">${box('Water by the bed')}${box('Phone charged')}${box('Big Boy settled')}${box('Took night meds')}${box('Ate something')}${box('Breathed — 3 slow ones')}</div>
</div></div>
<div class="foot"><b>Page 2 of 2.</b> 7HE H0LY R3UP · You survived. Now we rebuild. · Check the patterns, not the guilt. Your body is giving data, not a verdict.</div>
</section>`;
}


// ---------- calendar set pages (monthly / weekly / daily planner) ----------
const setCss = `
.mt{ width:100%; border-collapse:collapse; table-layout:fixed; margin-top:6px; }
.mt th{ background:var(--a); color:#fff; font-size:9px; letter-spacing:1.5px; padding:4px; border:1px solid var(--a); }
.mt td{ border:1.2px solid var(--line); height:92px; vertical-align:top; padding:3px 5px; background:#fff; }
.mt td b{ font-size:13px; color:var(--b); } .mt td.o{ background:var(--soft); opacity:.55; } .mt td.o b{ color:#999; font-weight:400; }
.mt td.today{ outline:2.5px solid var(--b); outline-offset:-2.5px; }
.mtitle{ font-family:'Caveat','Brush Script MT',cursive; font-size:40px; line-height:1; color:var(--b); margin:8px 0 0; letter-spacing:1px; }
.wkd{ border:1.3px solid var(--line); border-radius:7px; background:#fff; overflow:hidden; margin-bottom:5px; }
.wkd>h3{ margin:0; background:var(--a); color:#fff; font-size:10px; letter-spacing:1.4px; padding:2.5px 8px; display:flex; justify-content:space-between; font-weight:800; }
.wkd>h3 span{ font-weight:600; letter-spacing:.3px; font-size:8px; }
.wkd .in{ padding:3px 8px 4px; }
.hr2{ display:flex; border-bottom:1px solid var(--line); height:45px; font-size:9px; color:var(--b); font-weight:700; } .hr2 b{ width:44px; border-right:1px solid var(--line); padding:3px 0 0 3px; }
`;
const MONTH_START = 4; // Oct 1, 2026 is a Thursday (Sun=0)
function monthPage(t) {
  const dow = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
  const cells = [];
  for (let i = 0; i < 35; i++) {
    const d = i - MONTH_START + 1;
    if (d < 1) cells.push(`<td class="o"><b>${30 + d}</b></td>`);
    else if (d > 31) cells.push(`<td class="o"><b>${d - 31}</b></td>`);
    else cells.push(`<td class="${d === 24 ? 'today' : ''}"><b>${d}</b></td>`);
  }
  const trs = Array.from({ length: 5 }, (_, r) => `<tr>${cells.slice(r * 7, r * 7 + 7).join('')}</tr>`).join('');
  return `<section class="page">${brandHead('Monthly Calendar')}
<div class="mtitle">October 2026</div>
<table class="mt"><tr>${dow.map((d) => `<th>${d}</th>`).join('')}</tr>${trs}</table>
<div class="grid" style="margin-top:6px">
  <div class="sec"><h2>Month Focus</h2><div class="in">${lines(3, 19)}</div></div>
  <div class="sec"><h2>Appointments · Prayer Requests</h2><div class="in">${lines(3, 19)}</div></div>
</div>
<div class="sec" style="margin-top:6px"><h2>My Categories <em>mark days with the letter</em></h2><div class="in"><div class="key">${[['B','Body'],['M','Mind'],['S','Sleep'],['F','Food'],['G','God/Prayer'],['P','People'],['X','Safety'],['$','Money/Legal'],['H','Home/Big Boy'],['W','Win']].map(([k,v])=>`<div><b>${k}</b>${v}</div>`).join('')}</div></div></div>
<div class="foot"><b>October 2026.</b> You survived. Now we rebuild. · Today is circled.</div></section>`;
}
function weekPage(t) {
  const names = ['SATURDAY', 'SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY'];
  const dates = ['Oct 24', 'Oct 25', 'Oct 26', 'Oct 27', 'Oct 28', 'Oct 29', 'Oct 30'];
  const days = names.map((n, i) => `<div class="wkd"><h3>${n} <span>${dates[i]}, 2026</span></h3><div class="in">
    <div class="row" style="margin:1px 0 2px">${box('Prayed')}${box('Ate')}${box('Water')}${box('Slept')}${box('Meds')}${box('Ears ringing')}${box('Big Boy walked')}</div>
    ${lines(3, 18)}</div></div>`).join('');
  return `<section class="page">${brandHead('Weekly Plan')}
<div class="datebar" style="grid-template-columns:1fr 1fr"><div class="field">WEEK OF: Saturday, Oct 24 – Friday, Oct 30, 2026</div><div class="field">THIS WEEK'S FOCUS: </div></div>
${days}
<div class="grid"><div class="sec"><h2>Wins · Mercy I Saw</h2><div class="in">${lines(2, 17)}</div></div><div class="sec"><h2>Next Week's One Thing</h2><div class="in">${lines(2, 17)}</div></div></div>
<div class="foot"><b>Weekly.</b> Share only what feels safe. · We survived. Now let's go back — with truth and a hand out.</div></section>`;
}
function dayPage(t) {
  const hrs = ['6 AM','7','8','9','10','11','12 PM','1','2','3','4','5','6','7','8','9'];
  return `<section class="page">${brandHead('Daily Planner')}
<div class="datebar" style="grid-template-columns:2fr 1fr"><div class="field">SATURDAY, OCTOBER 24, 2026</div><div class="field">WEATHER / MOOD: </div></div>
<div class="grid" style="grid-template-columns:1.1fr 1fr">
<div class="sec"><h2>Today <em>write the time, then what</em></h2><div class="in" style="padding:3px 4px 4px"><table><tr><th style="width:24%">TIME</th><th>WHAT / WHERE / WHO</th></tr>${Array.from({ length: 15 }, () => '<tr><td style="height:46px"></td><td></td></tr>').join('')}</table></div></div>
<div class="col">
  <div class="sec"><h2>Top 3 Today</h2><div class="in">${[1,2,3].map((n)=>`<div class="row">${box('')}<span class="fill" style="min-width:150px"></span></div>`).join('')}</div></div>
  <div class="sec"><h2>To Do <em>one at a time</em></h2><div class="in">${Array.from({length:6},()=>`<div class="row">${box('')}<span class="fill" style="min-width:150px"></span></div>`).join('')}</div></div>
  <div class="sec"><h2>Prayers · What God Showed Me</h2><div class="in">${lines(5, 19)}</div></div>
  <div class="sec"><h2>Body Check <em>circle / check</em></h2><div class="in"><div class="row">${box('Ate')}${box('Water')}${box('Meds')}${box('Slept')}</div><div class="row">${box('Ears ringing')}${box('Headache')}${box('Dizzy')}</div><div class="row"><span class="lab">Big Boy:</span>${box('Fed')}${box('Walked')}</div></div></div>
  <div class="sec"><h2>Appointments / Calls</h2><div class="in">${lines(3, 21)}</div></div>
  <div class="sec"><h2>Thankful For</h2><div class="in">${lines(3, 21)}</div></div>
</div></div>
<div class="foot"><b>Daily.</b> The detailed log is on the next two pages. Even one box counts.</div></section>`;
}


// ---------- Oct 31 – Nov 2026 set ----------
const DOW = ['SUNDAY','MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY'];
const MON = ['January','February','March','April','May','June','July','August','September','October','November','December'];
const dt = (m, d) => new Date(2026, m, d);
const addDays = (d, n) => { const x = new Date(d); x.setDate(x.getDate() + n); return x; };
const short = (d) => `${MON[d.getMonth()].slice(0, 3)} ${d.getDate()}`;
const hdr = (t, title) => brandHead(title);
const novCss = `
.g3{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:6px; }
.mt.n td{ height:90px; } .mt.n td.to{ outline:2.5px solid var(--b); outline-offset:-2.5px; }
.sec.neg>h2{ background:var(--b); }
.wnote{ font-size:7.2px; color:#5a5560; margin-top:2px; }
`;
const randomSec = (n = 4, h = 19) => `<div class="sec"><h2>Random Things That Come to Me <em>ideas · words · memories</em></h2><div class="in">${lines(n, h)}</div></div>`;
const negSec = (nRows = 4, h = 26) => `<div class="sec neg"><h2>Negative Watch <em>what's coming against me</em></h2><div class="in" style="padding:3px 4px 4px">
  <table><tr><th style="width:34%">What's coming</th><th style="width:20%">From (thought · person · event)</th><th style="width:9%">0–10</th><th>Truth I'm standing on / what I'm doing</th></tr>
  ${Array.from({ length: nRows }, () => `<tr><td style="height:${h}px"></td><td></td><td></td><td></td></tr>`).join('')}</table>
  <div class="wnote">Naming it takes some of its power. A thought is not a fact. Safety first — reach out if it's more than you can hold.</div></div></div>`;

function novMonthPage(t) {
  const dow = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
  const start = dt(9, 25); // Sun Oct 25
  const cells = Array.from({ length: 42 }, (_, i) => {
    const d = addDays(start, i);
    const isNov = d.getMonth() === 10;
    const first = d.getDate() === 1 || i === 0;
    const label = d.getDate() === 1 || i === 0 ? `${MON[d.getMonth()].slice(0, 3)} ${d.getDate()}` : d.getDate();
    const cls = [isNov || (d.getMonth() === 9 && d.getDate() === 31) ? '' : 'o', d.getMonth() === 9 && d.getDate() === 31 ? 'to' : ''].join(' ');
    return `<td class="${cls}"><b>${label}</b></td>`;
  });
  const trs = Array.from({ length: 6 }, (_, r) => `<tr>${cells.slice(r * 7, r * 7 + 7).join('')}</tr>`).join('');
  return `<section class="page">${hdr(t, 'Monthly Calendar')}
<div class="mtitle">October 31 – November 2026</div>
<table class="mt n"><tr>${dow.map((d) => `<th>${d}</th>`).join('')}</tr>${trs}</table>
<div class="g3" style="margin-top:6px">
  <div class="sec"><h2>Random Things</h2><div class="in">${lines(4, 19)}</div></div>
  <div class="sec"><h2>Health This Month</h2><div class="in">${lines(2, 19)}<div class="row">${box('Doctor visit')}${box('Refill')}${box('Labs')}</div></div></div>
  <div class="sec neg"><h2>What's Coming Against Me</h2><div class="in">${lines(4, 19)}</div></div>
</div>
<div class="sec" style="margin-top:6px"><h2>My Categories <em>mark days with the letter</em></h2><div class="in"><div class="key">${[['B','Body'],['M','Mind'],['S','Sleep'],['F','Food'],['G','God/Prayer'],['P','People'],['X','Safety'],['$','Money/Legal'],['H','Home/Big Boy'],['W','Win']].map(([k,v])=>`<div><b>${k}</b>${v}</div>`).join('')}</div></div></div>
<div class="foot"><b>Oct 31 – Nov 30, 2026.</b> You survived. Now we rebuild. · Start day is boxed.</div></section>`;
}

function novWeekPage(t, start, n) {
  const end = addDays(start, 6);
  const days = Array.from({ length: 7 }, (_, i) => {
    const d = addDays(start, i);
    return `<div class="wkd"><h3>${DOW[d.getDay()]} <span>${short(d)}, 2026</span></h3><div class="in">
    <div class="row" style="margin:1px 0 2px">${box('Prayed')}${box('Ate')}${box('Water')}${box('Slept')}${box('Meds')}${box('Ears ringing')}${box('Big Boy walked')}</div>
    ${lines(3, 19)}</div></div>`;
  }).join('');
  return `<section class="page">${hdr(t, 'Weekly Plan')}
<div class="datebar" style="grid-template-columns:1.3fr 1fr"><div class="field">WEEK ${n}: ${DOW[start.getDay()].slice(0,3)} ${short(start)} – ${DOW[end.getDay()].slice(0,3)} ${short(end)}, 2026</div><div class="field">THIS WEEK'S FOCUS: </div></div>
${days}
<div class="g3">
  <div class="sec"><h2>Random Things</h2><div class="in">${lines(4, 19)}</div></div>
  <div class="sec"><h2>Health This Week</h2><div class="in"><div class="small">Ringing days <span class="fill" style="min-width:22px"></span> Avg sleep <span class="fill" style="min-width:22px"></span> hrs</div><div class="small" style="margin-top:3px">Days I ate 3x <span class="fill" style="min-width:22px"></span> Meds missed <span class="fill" style="min-width:22px"></span></div>${lines(2, 19)}</div></div>
  <div class="sec neg"><h2>What's Coming Against Me</h2><div class="in">${lines(4, 19)}</div></div>
</div>
<div class="foot"><b>Weekly.</b> Share only what feels safe. · We survived. Now let's go back — with truth and a hand out.</div></section>`;
}

function novDayPage(t, d) {
  const title = `${DOW[d.getDay()]}, ${MON[d.getMonth()].toUpperCase()} ${d.getDate()}, 2026`;
  const tbl = `<table><tr><th style="width:22%">TIME</th><th>WHAT / WHERE / WHO</th></tr>${Array.from({ length: 10 }, () => '<tr><td style="height:42px"></td><td></td></tr>').join('')}</table>`;
  const task = (n) => Array.from({ length: n }, () => `<div class="row" style="margin:3px 0">${box('')}<span class="fill" style="min-width:150px"></span></div>`).join('');
  return `<section class="page">${hdr(t, 'Daily Planner')}
<div class="datebar" style="grid-template-columns:2fr 1fr"><div class="field">${title}</div><div class="field">WEATHER / MOOD: </div></div>
<div class="grid" style="grid-template-columns:1.1fr 1fr">
<div class="col">
  <div class="sec"><h2>Today <em>write the time, then what</em></h2><div class="in" style="padding:3px 4px 4px">${tbl}</div></div>
  ${randomSec(6, 21)}
  ${negSec(5, 34)}
</div>
<div class="col">
  <div class="sec"><h2>Top 3 Today</h2><div class="in">${task(3)}</div></div>
  <div class="sec"><h2>To Do <em>one at a time</em></h2><div class="in">${task(6)}</div></div>
  <div class="sec"><h2>Health Today <em>circle / check</em></h2><div class="in">
    <div class="row">${box('Ears ringing')}<span class="lab">time</span><span class="fill"></span><span class="lab">1–10</span><span class="fill" style="min-width:18px"></span></div>
    <div class="row">${box('Headache')}${box('Dizzy')}${box('Nausea')}${box('Shaky')}${box('Pain')}</div>
    <div class="row"><span class="lab">Slept</span><span class="fill" style="min-width:24px"></span><span class="lab">hrs</span>${box('Rough')}${box('Okay')}${box('Good')}</div>
    <div class="row">${box('Breakfast')}${box('Lunch')}${box('Dinner')}${box('Snack')}</div>
    <div class="row"><span class="lab">Water:</span>${Array.from({ length: 8 }, () => '<span class="num">&nbsp;</span>').join('')}</div>
    <div class="row">${box('Meds AM')}${box('PM')}${box('Missed')}<span class="lab">Notes</span><span class="fill w"></span></div>
  </div></div>
  <div class="sec"><h2>Prayers · What God Showed Me</h2><div class="in"><div class="row" style="margin:1px 0 3px"><span class="lab">Scripture today:</span><span class="fill" style="min-width:200px"></span></div>${lines(5, 21)}</div></div>
  <div class="sec"><h2>Appointments / Calls</h2><div class="in">${lines(3, 21)}</div></div>
  <div class="sec"><h2>Thankful For</h2><div class="in">${lines(3, 21)}</div></div>
</div></div>
<div class="foot"><b>Daily.</b> The detailed log pages are at the back. Even one box counts.</div></section>`;
}

function novBody(t) {
  CUR = t;
  const weeks = [dt(9, 31), dt(10, 7), dt(10, 14), dt(10, 21), dt(10, 28)];
  const days = Array.from({ length: 31 }, (_, i) => addDays(dt(9, 31), i));
  return (novMonthPage(t) + weeks.map((w, i) => novWeekPage(t, w, i + 1)).join('') + days.map((d) => novDayPage(t, d)).join('') + page1(t) + page2(t)).replace(/<\/section>/g, `${decor()}</section>`);
}


const scrapCss = (t) => `
@font-face{ font-family:'Alfa'; src:url(assets/fonts/AlfaSlab.woff2) format('woff2'); }
@font-face{ font-family:'Kaushan'; src:url(assets/fonts/Kaushan.woff2) format('woff2'); }
@font-face{ font-family:'Franklin'; font-weight:400; src:url(assets/fonts/Franklin400.woff2) format('woff2'); }
@font-face{ font-family:'Franklin'; font-weight:600; src:url(assets/fonts/Franklin600.woff2) format('woff2'); }
@font-face{ font-family:'Franklin'; font-weight:800; src:url(assets/fonts/Franklin800.woff2) format('woff2'); }
html,body{ font-family:'Franklin','Helvetica Neue',Arial,sans-serif; }
.page{ background:radial-gradient(circle at 100% 100%,${t.a}2e,transparent 36%),radial-gradient(circle at 0 20%,${t.b}1f,transparent 30%),#fbf3e4; padding-bottom:.2in; }
.page::before{ border-radius:5px; border-width:1.6px; }
.page>:not(.foot):not(.dec){ zoom:.94; }
.hd{ position:relative; height:1.02in; margin:.03in 0 .12in; }
.hd-photo{ position:absolute; left:0; right:0; top:0; bottom:7px; background:url(assets/${t.tex}) center 45%/cover; clip-path:polygon(0 0,100% 0,100% 88%,97% 100%,94% 90%,90% 99%,85% 88%,80% 100%,74% 91%,68% 99%,62% 89%,56% 100%,50% 90%,44% 99%,38% 88%,32% 100%,26% 91%,20% 99%,14% 89%,8% 100%,4% 90%,0 98%); }
.hd-wash{ position:absolute; left:-.35in; top:-.3in; height:1.5in; opacity:.9; }
.hd-lw{ position:absolute; left:.12in; top:.1in; filter:drop-shadow(0 2px 2px rgba(0,0,0,.4)); transform:rotate(-1.2deg); }
.hd-label{ background:#fbf3e4; padding:5px 18px 8px 14px; clip-path:polygon(0 3%,5% 0,12% 4%,22% 0,36% 3%,50% 0,64% 4%,78% 0,90% 3%,100% 1%,99% 40%,100% 70%,98% 100%,88% 96%,74% 100%,60% 95%,44% 100%,30% 96%,16% 100%,6% 96%,0 99%,1% 55%); }
.hd .brand{ font-size:7px; letter-spacing:2.6px; font-weight:800; color:var(--b); text-shadow:none; }
.hd h1{ font-family:'Alfa',Georgia,serif; font-size:23px; letter-spacing:.6px; text-transform:uppercase; color:var(--a); text-shadow:none; line-height:1.08; margin:1px 0 0; }
.hd .tag{ font-family:'Kaushan',cursive; font-size:10.5px; color:var(--b); letter-spacing:.2px; font-weight:400; }
.hd-deco{ position:absolute; right:.1in; bottom:-.02in; display:flex; align-items:flex-end; gap:6px; }
.hd-deco img{ height:.98in; width:auto; filter:drop-shadow(0 2px 2px rgba(0,0,0,.4)); }
.hd-deco img.d-chain{ height:.5in; } .hd-deco img.d-anchor{ height:.86in; } .hd-deco img.d-cow,.hd-deco img.d-denim{ height:.82in; transform:rotate(5deg); } .hd-deco img.d-concho{ height:.8in; } .hd-deco img.d-hatpost{ height:1.1in; margin-top:-.2in; }
.sec{ background:rgba(255,255,255,.93); box-shadow:0 1px 3px rgba(0,0,0,.13); }
.sec>h2{ font-family:'Franklin'; }
.mtitle{ font-family:'Kaushan',cursive; font-size:32px; color:var(--a); letter-spacing:.5px; }
.dec{ position:absolute; bottom:.17in; display:flex; align-items:flex-end; gap:5px; z-index:3; }
.dec img{ height:1.05in; width:auto; filter:drop-shadow(0 2px 2px rgba(0,0,0,.35)); }
.dl{ left:.3in; } .dl img{ height:.62in; opacity:.88; transform:rotate(-10deg); } .dr{ right:.3in; }
.dr img.d-bible{ height:.85in; } .dr img.d-hatpost{ height:1.15in; } .dr img.d-bully{ height:1.15in; }
.foot{ left:1.5in; right:1.7in; bottom:.3in; font-size:7.4px; }
`;
const decor = () => `<div class="dec dl">${decImgs(CUR.fl)}</div><div class="dec dr">${decImgs(CUR.fr)}</div>`;

const docWrap = (title, css, body) => `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>${title}</title>
<meta name="description" content="Printable daily tracker — 7HE H0LY R3UP.">
<style>${css}</style></head><body>${body}</body></html>`;

// ---------- blank bland calendars ----------
const blandCss = `
@page land { size: 11in 8.5in; margin: 0; }
@page por { size: 8.5in 11in; margin: 0; }
.pg{ page:land; }
.pg.por{ page:por; }
*{ box-sizing:border-box; }
html,body{ margin:0; font-family:Arial,Helvetica,sans-serif; color:#222; background:#fff; -webkit-print-color-adjust:exact; }
.pg{ width:11in; height:8.5in; padding:.4in; page-break-after:always; position:relative; overflow:hidden; }
.pg.por{ width:8.5in; height:11in; }
.ttl{ display:flex; gap:24px; align-items:flex-end; border-bottom:2px solid #222; padding-bottom:4px; margin-bottom:6px; font-size:14px; font-weight:700; }
.ttl span{ flex:1; border-bottom:1px solid #888; height:20px; } .ttl span.s{ flex:.6; }
.cal{ width:100%; border-collapse:collapse; table-layout:fixed; height:calc(100% - 100px); }
.cal th{ border:1px solid #444; background:#eee; font-size:11px; padding:3px; height:20px; }
.cal td{ border:1px solid #444; vertical-align:top; padding:3px 4px; }
.wk{ width:100%; border-collapse:collapse; table-layout:fixed; height:calc(100% - 50px); }
.wk td{ border:1px solid #444; vertical-align:top; padding:4px 6px; font-weight:700; font-size:12px; }
.wk td i{ display:block; margin-top:4px; height:100%; background:repeating-linear-gradient(transparent 0 21px,#ccc 21px 22px); }
.lbl{ font-size:11px; font-weight:700; margin:6px 0 2px; }
.leg{ display:flex; gap:10px; margin-top:6px; font-size:11px; } .leg div{ flex:1; border-bottom:1px solid #888; height:18px; }
.dly{ display:grid; grid-template-columns:1.2fr 1fr; gap:14px; height:calc(100% - 52px); }
.hr{ display:flex; border-bottom:1px solid #999; height:53px; font-size:11px; } .hr b{ width:42px; border-right:1px solid #999; padding:2px 0 0 3px; }
.box{ border:1px solid #444; padding:6px; margin-bottom:8px; font-size:11px; font-weight:700; }
.box i{ display:block; height:100%; background:repeating-linear-gradient(transparent 0 23px,#ccc 23px 24px); margin-top:4px; }
`;
function monthly() {
  const days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
  return `<section class="pg"><div class="ttl">MONTH <span></span> YEAR <span class="s"></span></div>
<table class="cal"><tr>${days.map((d) => `<th>${d}</th>`).join('')}</tr>${Array.from({ length: 6 }, () => `<tr>${days.map(() => '<td></td>').join('')}</tr>`).join('')}</table>
<div class="lbl">NOTES / KEY (write your own categories)</div><div class="leg"><div></div><div></div><div></div><div></div></div></section>`;
}
function weekly() {
  const days = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'NOTES'];
  const cell = (d) => `<td>${d}<i></i></td>`;
  return `<section class="pg"><div class="ttl">WEEK OF <span></span> TO <span></span></div>
<table class="wk"><tr>${cell(days[0])}${cell(days[1])}${cell(days[2])}${cell(days[3])}</tr><tr>${cell(days[4])}${cell(days[5])}${cell(days[6])}${cell(days[7])}</tr></table></section>`;
}
function daily() {
  return `<section class="pg por"><div class="ttl">DATE <span></span> DAY <span class="s"></span></div>
<div class="dly"><div><div class="hr" style="height:24px;background:#eee;font-weight:700"><b style="width:90px">TIME</b><span style="padding:4px 6px">WHAT</span></div>${Array.from({ length: 15 }, () => '<div class="hr" style="height:52px"><b style="width:90px"></b></div>').join('')}</div>
<div><div class="box" style="height:34%">TO DO<i></i></div><div class="box" style="height:34%">NOTES<i></i></div><div class="box" style="height:22%">APPOINTMENTS / CALLS<i></i></div></div></div></section>`;
}

(async () => {
  const browser = await chromium.launch();
  const render = async (htmlPath, pdfPath, landscape = false) => {
    const page = await browser.newPage();
    await page.goto('file://' + htmlPath, { waitUntil: 'load' });
    await page.pdf({ path: pdfPath, preferCSSPageSize: true, printBackground: true });
    await page.close();
  };

  for (const t of THEMES) {
    const html2 = docWrap(`7HE H0LY R3UP — Oct 31–Nov 2026 — ${t.name}`, baseCss(t) + setCss + novCss + scrapCss(t), novBody(t));
    const hp2 = path.join(OUT, `nov-set-${t.id}.html`);
    fs.writeFileSync(hp2, html2);
    await render(hp2, hp2.replace('.html', '.pdf'));
    console.log('built nov', t.id);
  }

  const bland = docWrap('Blank Bland Calendars', blandCss, monthly() + weekly() + daily());
  const bp = path.join(OUT, 'blank-bland-calendars.html');
  fs.writeFileSync(bp, bland);
  await render(bp, bp.replace('.html', '.pdf'));
  console.log('built blank calendars');
  await browser.close();
})();
