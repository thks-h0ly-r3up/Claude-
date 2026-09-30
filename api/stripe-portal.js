'use strict';
const { send, supabase, env } = require('./_lib');
const { getUser } = require('./_auth');
const { stripe } = require('./_stripe');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return send(res, 405, { error: 'Method not allowed' }); }
  try {
    const user = await getUser(req);
    if (!user) return send(res, 401, { error: 'Please sign in first.' });
    const rows = await supabase('subscriptions?select=stripe_customer_id&user_id=eq.' + encodeURIComponent(user.id));
    if (!Array.isArray(rows) || !rows[0]) return send(res, 404, { error: 'No billing account found.' });
    const session = await stripe('billing_portal/sessions', {
      params: { customer: rows[0].stripe_customer_id, return_url: env('SITE_URL').replace(/\/+$/, '') + '/app/' }
    });
    return send(res, 200, { url: session.url });
  } catch (e) {
    console.error('portal error:', e && e.message);
    return send(res, 500, { error: 'Could not open billing. Please try again.' });
  }
};
