'use strict';
const { send, readBody, supabase, env } = require('./_lib');
const { getUser } = require('./_auth');
const { priceIdFor, stripe } = require('./_stripe');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return send(res, 405, { error: 'Method not allowed' }); }
  try {
    const user = await getUser(req);
    if (!user) return send(res, 401, { error: 'Please sign in first.' });

    const tier = String(readBody(req).tier || '');
    const price = priceIdFor(tier);
    if (!price) return send(res, 400, { error: 'Unknown plan.' });

    const siteUrl = env('SITE_URL').replace(/\/+$/, '');

    // Reuse the Stripe customer if this user already has one.
    let customer;
    const rows = await supabase('subscriptions?select=stripe_customer_id,status&user_id=eq.' + encodeURIComponent(user.id));
    if (Array.isArray(rows) && rows[0]) {
      customer = rows[0].stripe_customer_id;
      if (['active', 'trialing'].includes(rows[0].status)) {
        return send(res, 409, { error: 'You already have an active plan. Use Manage billing to change it.' });
      }
    }

    const session = await stripe('checkout/sessions', {
      params: {
        mode: 'subscription',
        'line_items[0][price]': price,
        'line_items[0][quantity]': 1,
        customer: customer,
        customer_email: customer ? undefined : user.email,
        client_reference_id: user.id,
        allow_promotion_codes: 'true',
        success_url: siteUrl + '/app/?checkout=success',
        cancel_url: siteUrl + '/app/?checkout=cancelled',
        subscription_data: { metadata: { user_id: user.id, tier } },
        metadata: { user_id: user.id, tier }
      }
    });
    return send(res, 200, { url: session.url });
  } catch (e) {
    console.error('checkout error:', e && e.message);
    return send(res, 500, { error: 'Could not start checkout. Please try again.' });
  }
};
