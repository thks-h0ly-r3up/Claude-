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

// ---------- 7 designs ----------
const THEMES = [
  { id: '01-turquoise-leather', name: 'Turquoise Leather', ink: '#1f2d2e', paper: '#fffdf8', a: '#2fa7a0', b: '#1c6f6b', soft: '#e3f4f2', line: '#9fcfcb',
    head: 'linear-gradient(90deg,#1c6f6b,#2fa7a0 60%,#7fd0c8)', stitch: '#2fa7a0', motif: 'STITCHED LEATHER', pattern: '' },
  { id: '02-sunrise-gold', name: 'Sunrise Gold', ink: '#3a2a1c', paper: '#fffaf2', a: '#e8a43a', b: '#d9774b', soft: '#fdf0da', line: '#efc98c',
    head: 'linear-gradient(90deg,#f6c453,#f0955a 55%,#f3a79a)', stitch: '#e8a43a', motif: 'FIRST LIGHT', pattern: '' },
  { id: '03-pink-purple-ombre', name: 'Pink-Purple Ombré', ink: '#2b2430', paper: '#fdfaf8', a: '#d6598f', b: '#7a4c9e', soft: '#f6e9f3', line: '#d3b6d9',
    head: 'linear-gradient(90deg,#d6598f,#a45aa8 50%,#7a4c9e)', stitch: '#b25aa0', motif: 'OMBRÉ SKY', pattern: '' },
  { id: '04-weathered-denim', name: 'Weathered Denim', ink: '#1e2733', paper: '#fbfaf6', a: '#4a6486', b: '#2f4560', soft: '#e6ecf3', line: '#a9b9cc',
    head: 'repeating-linear-gradient(45deg,#3b5373 0 3px,#44607f 3px 6px)', stitch: '#e0b45a', motif: 'DENIM & STITCH', pattern: '' },
  { id: '05-warm-ivory-tooled', name: 'Warm Ivory & Tooled', ink: '#3a2e22', paper: '#fbf5e8', a: '#8a6a45', b: '#5e452b', soft: '#f1e7d2', line: '#cdb995',
    head: 'linear-gradient(90deg,#5e452b,#8a6a45 55%,#b99870)', stitch: '#8a6a45', motif: 'TOOLED LEATHER', pattern: '' },
  { id: '06-cow-print', name: 'Cow Print (Restrained)', ink: '#1a1a1a', paper: '#ffffff', a: '#2fa7a0', b: '#1a1a1a', soft: '#f1f1f1', line: '#b9b9b9',
    head: `#ffffff url("data:image/svg+xml,${cow}") center/260px 60px`, stitch: '#2fa7a0', motif: 'COW GIRL STRONG', pattern: 'cow' },
  { id: '07-camo', name: 'Camo (Restrained)', ink: '#26301a', paper: '#fbfaf4', a: '#5c6b3a', b: '#3f4a2a', soft: '#eceee0', line: '#b4bb94',
    head: `#d9d6b8 url("data:image/svg+xml,${camo}") center/260px 60px`, stitch: '#8a7a52', motif: 'HOLD THE LINE', pattern: 'camo' },
];

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
.page{ width:8.5in; height:11in; background:var(--paper); position:relative; overflow:hidden; padding:.3in .36in .24in; page-break-after:always; }
.page::before{ content:''; position:absolute; inset:.13in; border:2px solid var(--a); border-radius:10px; pointer-events:none; }
.page::after{ content:''; position:absolute; inset:.18in; border:1.2px dashed var(--stitch); border-radius:7px; pointer-events:none; }
.head{ background:${t.head}; border-radius:8px; padding:7px 12px; display:flex; justify-content:space-between; align-items:center; position:relative; margin-top:.02in; }
.head.pat{ border:1.5px solid var(--b); }
.head .tt{ ${t.pattern ? 'background:#fff;border:1.5px solid var(--b);border-radius:6px;padding:3px 10px;' : ''} }
.brand{ font-size:8px; letter-spacing:2.2px; font-weight:800; text-transform:uppercase; color:${t.pattern ? 'var(--b)' : '#fff'}; ${t.pattern ? '' : 'text-shadow:0 1px 2px rgba(0,0,0,.25);'} }
h1{ margin:0; font-family:'Caveat','Brush Script MT',cursive; font-size:30px; line-height:1; color:${t.pattern ? 'var(--b)' : '#fff'}; ${t.pattern ? '' : 'text-shadow:0 1px 2px rgba(0,0,0,.28);'} }
.tag{ font-size:8px; color:${t.pattern ? 'var(--b)' : '#fff'}; font-weight:600; letter-spacing:.4px; }
.motif{ font-size:7px; letter-spacing:2px; font-weight:800; color:${t.pattern ? 'var(--b)' : '#fff'}; opacity:.95; text-align:right; }
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

const brandHead = (title, motif) => `
<div class="head ${motif.pat ? 'pat' : ''}">
  <div class="tt"><div class="brand">7HE H0LY R3UP</div><h1>${title}</h1><div class="tag">You survived. Now we rebuild.</div></div>
  <div class="motif">${motif.text}</div>
</div>`;

// ---------- page 1: Daily Log ----------
function page1(t) {
  const pat = !!t.pattern;
  return `
<section class="page">
${brandHead('Daily Log', { text: t.motif, pat })}
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
${brandHead('What Happened — Full Detail', { text: t.motif, pat })}
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
  const hrs = ['5', '6', '7', '8', '9', '10', '11', '12', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
  return `<section class="pg por"><div class="ttl">DATE <span></span> DAY <span class="s"></span></div>
<div class="dly"><div>${hrs.map((h) => `<div class="hr"><b>${h}:00</b></div>`).join('')}</div>
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
    const body = page1(t) + page2(t);
    const html = docWrap(`7HE H0LY R3UP — Daily Tracker — ${t.name}`, baseCss(t), body);
    const hp = path.join(OUT, `daily-tracker-${t.id}.html`);
    fs.writeFileSync(hp, html);
    await render(hp, hp.replace('.html', '.pdf'));
    console.log('built', t.id);
  }

  const bland = docWrap('Blank Bland Calendars', blandCss, monthly() + weekly() + daily());
  const bp = path.join(OUT, 'blank-bland-calendars.html');
  fs.writeFileSync(bp, bland);
  await render(bp, bp.replace('.html', '.pdf'));
  console.log('built blank calendars');
  await browser.close();
})();
