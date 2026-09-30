'use strict';
const { UUID_RE, send, readBody, supabase, sheets } = require('./_lib');

const EVENTS = { pdf_downloaded: 'pdf_downloaded', app_clicked: 'app_clicked' };

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return send(res, 405, { error: 'Method not allowed' });
  }
  try {
    const b = readBody(req);
    const id = String(b.id || '');
    const field = EVENTS[String(b.event || '')];
    if (!UUID_RE.test(id) || !field) return send(res, 400, { error: 'Bad request' });

    const rows = await supabase('leads_funnel?id=eq.' + encodeURIComponent(id), {
      method: 'PATCH',
      prefer: 'return=representation',
      body: { [field]: true }
    });
    if (!Array.isArray(rows) || rows.length === 0) return send(res, 404, { error: 'Lead not found' });

    await sheets({ action: 'update', id, fields: { [field]: true } });
    return send(res, 200, { ok: true });
  } catch (e) {
    console.error('track error:', e && e.message);
    return send(res, 500, { error: 'Tracking failed' });
  }
};
