#!/usr/bin/env python3
"""Standalone landscape Certificate of Completion for the Rebuild kit."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
fonts = open(os.path.join(HERE, "fonts_embedded.css"), encoding="utf-8").read()
paw = ('<svg viewBox="0 0 64 64" width="38" height="38"><g fill="#7a4c9e">'
       '<ellipse cx="32" cy="42" rx="14" ry="11"/><ellipse cx="14" cy="26" rx="6" ry="8"/>'
       '<ellipse cx="26" cy="15" rx="6" ry="8"/><ellipse cx="38" cy="15" rx="6" ry="8"/>'
       '<ellipse cx="50" cy="26" rx="6" ry="8"/></g></svg>')
html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Certificate of Completion | 7HE H0LY R3UP</title>
<style>
{fonts}
@page {{ size: 11in 8.5in; margin: 0; }}
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--pink:#d6598f;--purple:#7a4c9e;--teal:#2f9e98;--turq:#3fb6b0;--denim:#4a6486;--ink:#2b2430}}
html,body{{width:11in;height:8.5in;font-family:'Libre Franklin',sans-serif;color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{width:11in;height:8.5in;padding:.38in;background:#fffdf9;position:relative;overflow:hidden}}
.band{{position:absolute;left:0;right:0;top:0;height:.1in;background:linear-gradient(90deg,var(--turq),var(--purple) 55%,var(--pink))}}
.frame{{height:100%;border:8px double var(--purple);border-radius:8px;padding:.12in}}
.in{{height:100%;border:2px solid var(--pink);border-radius:6px;padding:.3in .6in .2in;text-align:center;position:relative;
  background:radial-gradient(circle at 50% 0%,rgba(63,182,176,.16),transparent 60%)}}
.brand{{font-size:15px;font-weight:800;letter-spacing:8px;color:var(--teal)}}
.kick{{font-size:12px;letter-spacing:6px;font-weight:800;color:var(--purple);margin-top:.12in}}
h1{{font-family:'Bebas Neue';font-weight:400;font-size:74px;letter-spacing:3px;color:var(--purple);line-height:1;margin-top:.04in}}
.sub{{font-family:'Caveat',cursive;font-weight:700;font-size:44px;color:var(--pink);line-height:1;margin-top:.02in}}
.pre{{font-family:'Lora',serif;font-style:italic;font-size:17px;color:#5b5064;margin-top:.22in}}
.line{{border-bottom:2px solid var(--ink);width:6.2in;margin:.3in auto 4px}}
.lbl{{font-size:9px;letter-spacing:2.5px;color:#8b7a99;font-weight:700;text-transform:uppercase}}
.body{{font-family:'Lora',serif;font-size:17px;line-height:1.6;color:#3f3449;margin:.2in auto 0;width:7.6in}}
.verse{{font-family:'Lora',serif;font-style:italic;font-size:14px;color:var(--teal);margin-top:.06in}}
.checks{{display:flex;justify-content:center;gap:.3in;margin-top:.2in;font-size:12px;font-weight:700;color:var(--denim)}}
.checks span:before{{content:"";display:inline-block;width:13px;height:13px;border:2px solid var(--ink);border-radius:3px;margin-right:7px;vertical-align:-2px}}
.sign{{display:grid;grid-template-columns:1fr 1.2fr 1.2fr;gap:.35in;margin:.3in .3in 0;text-align:center}}
.sign .ln{{border-bottom:2px solid var(--ink);height:.34in}}
.love{{position:absolute;left:0;right:0;bottom:.5in;display:flex;justify-content:center;align-items:center;gap:12px;
  font-family:'Caveat',cursive;font-weight:700;font-size:30px;color:var(--purple)}}
.foot{{position:absolute;left:0;right:0;bottom:.14in;font-size:8.5px;letter-spacing:2.5px;font-weight:800;color:#8b7a99}}
</style></head><body><div class="page"><div class="band"></div><div class="frame"><div class="in">
<div class="brand">7HE H0LY R3UP</div>
<div class="kick">THIS CERTIFIES THAT</div>
<h1>Certificate of Completion</h1>
<div class="sub">Rebuild One Piece at a Time</div>
<div class="pre">Presented to</div>
<div class="line"></div><div class="lbl">your name</div>
<p class="body">for showing up, telling the truth, and building something honest, one piece at a time.<br>
Not perfect. <b>Still here.</b> Still His.</p>
<div class="verse">&ldquo;For who hath despised the day of small things?&rdquo; &mdash; Zechariah 4:10 (KJV)</div>
<div class="checks"><span>7-Day Rebuild</span><span>Board finished</span><span>30-Day Tracker</span><span>Another round</span></div>
<div class="sign">
 <div><div class="ln"></div><div class="lbl">Date</div></div>
 <div><div class="ln"></div><div class="lbl">Signed (you)</div></div>
 <div><div class="ln"></div><div class="lbl">Witness (someone who saw you do it)</div></div>
</div>
<div class="love">{paw}<span>Proud of you. &mdash; Hellshaker &amp; Big Boy</span></div>
<div class="foot">IN MEMORY OF BRANDI RENEE &mdash; 1-27-86 * 12-17-21 &nbsp;&bull;&nbsp; D.O.A. IS GOD'S FAVORITE STARTING POINT &nbsp;&bull;&nbsp; CORNER 2 CROWN</div>
</div></div></div></body></html>'''
open(os.path.join(HERE, "certificate-of-completion.html"), "w", encoding="utf-8").write(html)
print("wrote certificate-of-completion.html")
