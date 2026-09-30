'use strict';
const crypto = require('crypto');
const { env } = require('./_lib');

const TIERS = {
  starter: { env: 'STRIPE_PRICE_STARTER', label: 'Starter', price: 5 },
  vault: { env: 'STRIPE_PRICE_VAULT', label: 'Vault', price: 8 },
  full: { env: 'STRIPE_PRICE_FULL', label: 'Full Access', price: 12 }
};

function priceIdFor(tier) {
  return TIERS[tier] ? process.env[TIERS[tier].env] : undefined;
}

function tierForPriceId(priceId) {
  return Object.keys(TIERS).find((t) => process.env[TIERS[t].env] === priceId) || null;
}

/** Stripe REST call using form encoding (no SDK needed). Nested keys use bracket notation. */
async function stripe(path, { method = 'POST', params } = {}) {
  const base = process.env.STRIPE_API_BASE || 'https://api.stripe.com';
  const body = params ? encodeForm(params) : undefined;
  const r = await fetch(base + '/v1/' + path, {
    method,
    headers: {
      Authorization: 'Bearer ' + env('STRIPE_SECRET_KEY'),
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error('Stripe ' + r.status + ': ' + ((data.error && data.error.message) || 'request failed'));
  return data;
}

function encodeForm(obj, prefix, out = []) {
  Object.keys(obj).forEach((k) => {
    const v = obj[k];
    const key = prefix ? prefix + '[' + k + ']' : k;
    if (v === undefined || v === null) return;
    if (typeof v === 'object') encodeForm(v, key, out);
    else out.push(encodeURIComponent(key) + '=' + encodeURIComponent(String(v)));
  });
  return out.join('&');
}

/** Verifies a Stripe-Signature header against the raw request body. */
function verifySignature(rawBody, header, secret, toleranceSec = 300, now = Date.now()) {
  if (!header || !secret) return false;
  const parts = {};
  String(header).split(',').forEach((kv) => {
    const i = kv.indexOf('=');
    if (i > 0) (parts[kv.slice(0, i).trim()] = parts[kv.slice(0, i).trim()] || []).push(kv.slice(i + 1).trim());
  });
  const t = parts.t && parts.t[0];
  const sigs = parts.v1 || [];
  if (!t || !sigs.length) return false;
  if (Math.abs(now / 1000 - Number(t)) > toleranceSec) return false;
  const expected = crypto.createHmac('sha256', secret).update(t + '.' + rawBody).digest('hex');
  const exp = Buffer.from(expected, 'utf8');
  return sigs.some((s) => {
    const got = Buffer.from(s, 'utf8');
    return got.length === exp.length && crypto.timingSafeEqual(got, exp);
  });
}

module.exports = { TIERS, priceIdFor, tierForPriceId, stripe, verifySignature };
