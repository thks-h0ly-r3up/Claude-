'use strict';
const { send, readBody, supabase, sheets } = require('./_lib');

const SOURCES = ['instagram', 'tiktok', 'facebook', 'youtube', 'direct', 'other'];
const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return send(res, 405, { error: 'Method not allowed' });
  }
  try {
    const b = readBody(req);

    // Honeypot: real people never fill the hidden "company" field.
    if (b.company) return send(res, 200, { ok: true, id: null });

    const name = String(b.name || '').trim().slice(0, 100);
    const email = String(b.email || '').trim().toLowerCase().slice(0, 254);
    const handle = String(b.social_handle || '').trim().replace(/^@+/, '').replace(/[^A-Za-z0-9._-]/g, '').slice(0, 64);
    let source = String(b.source_platform || 'direct').trim().toLowerCase();
    if (!SOURCES.includes(source)) source = 'other';

    if (name.length < 1) return send(res, 400, { error: 'Please enter your name.' });
    if (!EMAIL_RE.test(email)) return send(res, 400, { error: 'Please enter a valid email address.' });

    const rows = await supabase('leads_funnel?on_conflict=email', {
      method: 'POST',
      prefer: 'resolution=merge-duplicates,return=representation',
      body: { name, email, social_handle: handle || null, source_platform: source }
    });
    const lead = Array.isArray(rows) ? rows[0] : rows;
    if (!lead || !lead.id) throw new Error('Lead was not saved');

    await sheets({
      action: 'upsert',
      id: lead.id,
      name: lead.name,
      email: lead.email,
      social_handle: lead.social_handle || '',
      source_platform: lead.source_platform,
      pdf_downloaded: lead.pdf_downloaded,
      app_clicked: lead.app_clicked,
      timestamp: lead.timestamp
    });

    return send(res, 200, { ok: true, id: lead.id });
  } catch (e) {
    console.error('lead error:', e && e.message);
    return send(res, 500, { error: 'Something went wrong. Please try again in a moment.' });
  }
};
