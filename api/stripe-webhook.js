'use strict';
const { send, supabase, env } = require('./_lib');
const { stripe, tierForPriceId, verifySignature } = require('./_stripe');

function readRaw(req) {
  return new Promise((resolve, reject) => {
    if (typeof req.body === 'string') return resolve(req.body);
    if (Buffer.isBuffer(req.body)) return resolve(req.body.toString('utf8'));
    const chunks = [];
    req.on('data', (c) => chunks.push(Buffer.isBuffer(c) ? c : Buffer.from(c)));
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}

async function syncSubscription(sub) {
  const userId = sub.metadata && sub.metadata.user_id;
  if (!userId) {
    console.error('subscription without user_id metadata:', sub.id);
    return;
  }
  const item = sub.items && sub.items.data && sub.items.data[0];
  const tier = (item && tierForPriceId(item.price && item.price.id)) || (sub.metadata && sub.metadata.tier);
  if (!['starter', 'vault', 'full'].includes(tier)) throw new Error('Unknown tier for subscription ' + sub.id);
  const periodEnd = sub.current_period_end || (item && item.current_period_end);
  await supabase('subscriptions?on_conflict=user_id', {
    method: 'POST',
    prefer: 'resolution=merge-duplicates,return=minimal',
    body: {
      user_id: userId,
      stripe_customer_id: typeof sub.customer === 'string' ? sub.customer : sub.customer.id,
      stripe_subscription_id: sub.id,
      tier,
      status: sub.status,
      current_period_end: periodEnd ? new Date(periodEnd * 1000).toISOString() : null,
      cancel_at_period_end: !!sub.cancel_at_period_end,
      updated_at: new Date().toISOString()
    }
  });
}

async function handler(req, res) {
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return send(res, 405, { error: 'Method not allowed' }); }
  let raw;
  try {
    raw = await readRaw(req);
    if (!verifySignature(raw, req.headers['stripe-signature'], env('STRIPE_WEBHOOK_SECRET'))) {
      return send(res, 400, { error: 'Invalid signature' });
    }
    const event = JSON.parse(raw);
    const obj = event.data && event.data.object;

    if (event.type === 'checkout.session.completed' && obj && obj.mode === 'subscription' && obj.subscription) {
      // Fetch the full subscription so tier/status/period are authoritative.
      const sub = await stripe('subscriptions/' + encodeURIComponent(obj.subscription), { method: 'GET' });
      if (!sub.metadata || !sub.metadata.user_id) sub.metadata = Object.assign({}, sub.metadata, obj.metadata);
      await syncSubscription(sub);
    } else if (['customer.subscription.created', 'customer.subscription.updated', 'customer.subscription.deleted'].includes(event.type)) {
      await syncSubscription(obj);
    }
    return send(res, 200, { received: true });
  } catch (e) {
    console.error('webhook error:', e && e.message);
    // 500 makes Stripe retry, which is what we want for transient DB errors.
    return send(res, 500, { error: 'Webhook handling failed' });
  }
}

module.exports = handler;
// Stripe signature verification needs the exact raw body.
module.exports.config = { api: { bodyParser: false } };
