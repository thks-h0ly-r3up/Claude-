'use strict';
const { env } = require('./_lib');

/** Resolves the Supabase user for a request's "Authorization: Bearer <access_token>" header, or null. */
async function getUser(req) {
  const header = req.headers.authorization || '';
  const m = /^Bearer\s+(.+)$/i.exec(header);
  if (!m) return null;
  const base = env('SUPABASE_URL').replace(/\/+$/, '');
  const r = await fetch(base + '/auth/v1/user', {
    headers: { apikey: env('SUPABASE_ANON_KEY'), Authorization: 'Bearer ' + m[1] }
  });
  if (!r.ok) return null;
  const user = await r.json();
  return user && user.id ? user : null;
}

module.exports = { getUser };
