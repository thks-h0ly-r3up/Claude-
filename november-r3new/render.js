const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + __dirname + '/r3new-november-2026.html', { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(1500);
  await p.pdf({ path: __dirname + '/THE-R3NEW-November-2026.pdf', width: '8.5in', height: '11in', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
