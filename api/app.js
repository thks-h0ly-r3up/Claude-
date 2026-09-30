'use strict';
const { UUID_RE, env, supabase, sheets } = require('./_lib');

/** GET /api/app?id=<lead uuid>  -> records the app click, then 302s to APP_DOWNLOAD_URL. */
module.exports = async function handler(req, res) {
  let target;
  try {
    target = env('APP_DOWNLOAD_URL');
  } catch (e) {
    res.statusCode = 500;
    return res.end('App link is not configured.');
  }
  try {
    const url = new URL(req.url, 'http://localhost');
    const id = url.searchParams.get('id') || '';
    if (UUID_RE.test(id)) {
      const rows = await supabase('leads_funnel?id=eq.' + encodeURIComponent(id), {
        method: 'PATCH',
        prefer: 'return=representation',
        body: { app_clicked: true }
      });
      if (Array.isArray(rows) && rows.length) {
        await sheets({ action: 'update', id, fields: { app_clicked: true } });
      }
    }
  } catch (e) {
    console.error('app click tracking failed:', e && e.message);
  }
  res.statusCode = 302;
  res.setHeader('Location', target);
  res.setHeader('Cache-Control', 'no-store');
  res.end();
};
