'use strict';
const { send } = require('./_lib');
const { TIERS } = require('./_stripe');

/** Public runtime config for the app (anon key is designed to be public; RLS protects the data). */
module.exports = async function handler(req, res) {
  if (req.method !== 'GET') { res.setHeader('Allow', 'GET'); return send(res, 405, { error: 'Method not allowed' }); }
  const url = process.env.SUPABASE_URL;
  const anon = process.env.SUPABASE_ANON_KEY;
  if (!url || !anon) return send(res, 500, { error: 'App is not configured yet.' });
  res.setHeader('Cache-Control', 'public, max-age=300');
  const tiers = {};
  Object.keys(TIERS).forEach((k) => { tiers[k] = { label: TIERS[k].label, price: TIERS[k].price }; });
  return send(res, 200, { supabaseUrl: url, supabaseAnonKey: anon, tiers });
};
