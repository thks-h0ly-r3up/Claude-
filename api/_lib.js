'use strict';

const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

function env(name) {
  const value = process.env[name];
  if (!value) throw new Error('Missing environment variable: ' + name);
  return value;
}

function send(res, status, body) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(body));
}

function readBody(req) {
  const body = req.body;
  if (body && typeof body === 'object') return body;
  if (typeof body === 'string') {
    try { return JSON.parse(body); } catch (e) { return {}; }
  }
  return {};
}

/** Calls the Supabase PostgREST API with the service-role key (server only). */
async function supabase(path, { method = 'GET', body, prefer } = {}) {
  const base = env('SUPABASE_URL').replace(/\/+$/, '');
  const key = env('SUPABASE_SERVICE_ROLE_KEY');
  const headers = {
    apikey: key,
    Authorization: 'Bearer ' + key,
    'Content-Type': 'application/json'
  };
  if (prefer) headers.Prefer = prefer;
  const r = await fetch(base + '/rest/v1/' + path, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body)
  });
  const text = await r.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch (e) { data = text; }
  if (!r.ok) {
    const err = new Error('Supabase ' + r.status + ': ' + (typeof data === 'string' ? data : JSON.stringify(data)));
    err.status = r.status;
    throw err;
  }
  return data;
}

/** Pushes a change to the Google Sheets webhook. Never throws: the DB is the source of truth. */
async function sheets(payload) {
  const url = process.env.SHEETS_WEBHOOK_URL;
  const secret = process.env.SHEETS_WEBHOOK_SECRET;
  if (!url || !secret) return { skipped: true };
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 9000);
  try {
    const r = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(Object.assign({ secret }, payload)),
      redirect: 'follow',
      signal: ctrl.signal
    });
    return { ok: r.ok };
  } catch (e) {
    console.error('Sheets sync failed:', e && e.message);
    return { ok: false };
  } finally {
    clearTimeout(timer);
  }
}

module.exports = { UUID_RE, env, send, readBody, supabase, sheets };
