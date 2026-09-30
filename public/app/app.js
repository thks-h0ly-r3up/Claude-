/* Shattering Chains - 30-day paid app (vanilla JS, Supabase Auth + Stripe billing).
 * Tiers: starter (map + tracker) < vault (+ prayer vault) < full (+ audio devotionals).
 * All user text is rendered with textContent via h(); nothing user-supplied is ever set as HTML. */
(function () {
  'use strict';

  var root = document.getElementById('root');
  var S = {
    cfg: null, sb: null, session: null, sub: null, rank: 0,
    days: [], progress: {}, vault: [], vaultLoaded: false,
    booting: true, error: null, toast: null, authSent: null, polling: false, busy: false
  };
  var saveTimers = {};
  var audio = { el: null, playing: null };
  var TIER_RANK = { starter: 1, vault: 2, full: 3 };
  var WEEKS = { 1: 'WEEK 1 - SHATTER THE CHAINS', 8: 'WEEK 2 - HEAL THE HEART', 15: 'WEEK 3 - STAND FIRM', 22: 'WEEK 4 - RUN YOUR RACE', 29: 'FINALE - NEW SUN' };

  // ---------- tiny DOM helper ----------
  function h(tag, attrs) {
    var el = document.createElement(tag);
    var a = attrs || {};
    Object.keys(a).forEach(function (k) {
      var v = a[k];
      if (v === null || v === undefined || v === false) return;
      if (k === 'class') el.className = v;
      else if (k.indexOf('on') === 0) el.addEventListener(k.slice(2), v);
      else if (k === 'value' || k === 'checked' || k === 'disabled') el[k] = v;
      else el.setAttribute(k, v === true ? '' : v);
    });
    for (var i = 2; i < arguments.length; i++) append(el, arguments[i]);
    return el;
  }
  function append(el, c) {
    if (c === null || c === undefined || c === false) return;
    if (Array.isArray(c)) { c.forEach(function (x) { append(el, x); }); return; }
    el.appendChild(c.nodeType ? c : document.createTextNode(String(c)));
  }
  function mount(node) { root.textContent = ''; root.appendChild(node); }
  function showToast(msg) {
    S.toast = msg;
    var t = document.getElementById('toast');
    if (t) { t.textContent = msg; t.classList.remove('hidden'); }
    clearTimeout(showToast._t);
    showToast._t = setTimeout(function () { var el = document.getElementById('toast'); if (el) el.classList.add('hidden'); S.toast = null; }, 3200);
  }

  // ---------- shared UI ----------
  var BTN = 'block w-full text-center font-display text-2xl uppercase tracking-wide py-4 border-4 border-cream active:translate-y-0.5 disabled:opacity-60 ';
  function btnPrimary(label, onclick, extra) { return h('button', { type: 'button', class: BTN + 'bg-sun text-night ' + (extra || ''), onclick: onclick }, label); }
  function btnGhost(label, onclick) { return h('button', { type: 'button', class: BTN + 'bg-night text-cream', onclick: onclick }, label); }
  function chevrons() { return h('div', { class: 'h-2 my-5', 'aria-hidden': 'true', style: 'background:linear-gradient(135deg,transparent 75%,#FF6B1A 75%) 0 0/20px 8px,linear-gradient(225deg,transparent 75%,#FF6B1A 75%) 0 0/20px 8px' }); }
  function label(text, color) { return h('p', { class: 'text-xs font-extrabold tracking-widest ' + (color || 'text-gold') }, String(text).toUpperCase()); }
  function toastEl() { return h('div', { id: 'toast', role: 'status', class: 'hidden fixed left-1/2 -translate-x-1/2 bottom-24 z-50 max-w-[90%] bg-cream text-night font-bold text-sm px-4 py-3 border-4 border-sun' }, S.toast || ''); }

  function shell(active, body) {
    var nav = [
      { id: 'map', text: 'MAP', href: '#/map' },
      { id: 'vault', text: 'VAULT', href: '#/vault' },
      { id: 'account', text: 'ACCOUNT', href: '#/account' }
    ];
    return h('div', { class: 'pb-28' },
      h('div', { class: 'camo h-2 border-b-4 border-sun' }),
      body,
      toastEl(),
      h('nav', { class: 'fixed bottom-0 inset-x-0 z-40 bg-night border-t-4 border-sun', 'aria-label': 'Main' },
        h('div', { class: 'max-w-md mx-auto grid grid-cols-3' },
          nav.map(function (n) {
            return h('a', { href: n.href, 'aria-current': active === n.id ? 'page' : null,
              class: 'py-4 text-center font-display text-xl tracking-wide ' + (active === n.id ? 'bg-sun text-night' : 'text-cream') }, n.text);
          }))));
  }

  // ---------- data ----------
  function api(path, opts) {
    var o = opts || {};
    var headers = { 'Content-Type': 'application/json' };
    if (S.session) headers.Authorization = 'Bearer ' + S.session.access_token;
    return fetch(path, { method: o.method || 'POST', headers: headers, body: o.body ? JSON.stringify(o.body) : undefined })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { if (!r.ok) throw new Error(d.error || 'Something went wrong.'); return d; }); });
  }

  function loadSubscription() {
    return S.sb.from('subscriptions').select('tier,status,current_period_end,cancel_at_period_end').maybeSingle().then(function (res) {
      var sub = res.data || null;
      var ok = sub && (sub.status === 'active' || sub.status === 'trialing');
      S.sub = sub;
      S.rank = ok ? TIER_RANK[sub.tier] || 0 : 0;
    });
  }
  function loadProgress() {
    return S.sb.from('progress').select('*').then(function (res) {
      S.progress = {};
      (res.data || []).forEach(function (r) { S.progress[r.day] = r; });
    });
  }
  function loadVault() {
    return S.sb.from('vault_entries').select('*').order('created_at', { ascending: false }).then(function (res) {
      if (res.error) throw res.error;
      S.vault = res.data || [];
      S.vaultLoaded = true;
    });
  }

  function loadAll() {
    S.error = null;
    return loadSubscription().then(function () {
      if (S.rank >= 1) return loadProgress();
    }).then(function () {
      if (S.rank >= 2) return loadVault();
    });
  }

  function progressRow(day) {
    var d = S.days[day - 1];
    var p = S.progress[day];
    return p || { day: day, habits: d.habits.map(function () { return false; }), prayer_minutes: 0, chain_before: null, chain_after: null, completed: false };
  }
  function isDone(day) { return !!(S.progress[day] && S.progress[day].completed); }
  function currentDay() {
    for (var i = 1; i <= 30; i++) if (!isDone(i)) return i;
    return 31;
  }
  function doneCount() { var n = 0; for (var i = 1; i <= 30; i++) if (isDone(i)) n++; return n; }

  function saveProgress(day, patch, immediate) {
    var row = Object.assign({}, progressRow(day), patch);
    row.user_id = S.session.user.id;
    S.progress[day] = row;
    clearTimeout(saveTimers[day]);
    function go() {
      var payload = {
        user_id: row.user_id, day: day, habits: row.habits, prayer_minutes: row.prayer_minutes,
        chain_before: row.chain_before, chain_after: row.chain_after, completed: !!row.completed,
        completed_at: row.completed ? (row.completed_at || new Date().toISOString()) : null
      };
      return S.sb.from('progress').upsert(payload, { onConflict: 'user_id,day' }).then(function (res) {
        if (res.error) { showToast('Could not save. Check your connection.'); return false; }
        S.progress[day].completed_at = payload.completed_at;
        return true;
      });
    }
    if (immediate) return go();
    saveTimers[day] = setTimeout(go, 500);
    return Promise.resolve(true);
  }

  // ---------- audio ----------
  function stopAudio() {
    if (audio.el) { audio.el.pause(); audio.el = null; }
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    audio.playing = null;
  }
  function devotionalScript(d, n) {
    return 'Day ' + n + '. ' + d.title.toLowerCase() + '. ' + d.ref + '. ' + d.verse + ' ... ' + d.breakdown +
      ' ... Let\'s pray. ' + d.prayer;
  }
  function pickVoice() {
    var voices = window.speechSynthesis.getVoices() || [];
    var en = voices.filter(function (v) { return /^en/i.test(v.lang); });
    var fem = en.filter(function (v) { return /female|samantha|karen|moira|tessa|zira|susan|hazel|serena|victoria|google uk english female|google us english/i.test(v.name); });
    return (fem[0] || en[0] || null);
  }
  function toggleAudio(day, button) {
    if (audio.playing === day) { stopAudio(); button.textContent = 'PLAY DEVOTIONAL'; return; }
    stopAudio();
    var d = S.days[day - 1];
    audio.playing = day;
    button.textContent = 'STOP';
    var done = function () { audio.playing = null; button.textContent = 'PLAY DEVOTIONAL'; };
    if (d.audio_url) {
      audio.el = new Audio(d.audio_url);
      audio.el.addEventListener('ended', done);
      audio.el.play().catch(function () { done(); showToast('Could not play audio.'); });
    } else if ('speechSynthesis' in window) {
      var u = new SpeechSynthesisUtterance(devotionalScript(d, day));
      var v = pickVoice();
      if (v) u.voice = v;
      u.rate = 0.92;
      u.pitch = 1.05;
      u.onend = done;
      u.onerror = done;
      window.speechSynthesis.speak(u);
    } else {
      done();
      showToast('Audio is not supported on this device.');
    }
  }

  // ---------- views ----------
  function viewLoading(msg) {
    return h('div', { class: 'min-h-screen flex items-center justify-center p-8 text-center' },
      h('div', null, h('p', { class: 'font-display text-4xl uppercase' }, 'Shattering ', h('span', { class: 'text-sun' }, 'Chains')),
        h('p', { class: 'mt-3 font-semibold text-cream/70' }, msg || 'Loading...')));
  }

  function viewError(msg) {
    return h('div', { class: 'p-6 pt-16' },
      h('p', { class: 'font-display text-4xl uppercase' }, 'Hold up'),
      h('p', { class: 'mt-3 font-semibold' }, msg),
      h('div', { class: 'mt-6' }, btnPrimary('Try again', function () { location.reload(); })));
  }

  function viewAuth() {
    var emailInput = h('input', { id: 'auth-email', type: 'email', autocomplete: 'email', inputmode: 'email', required: true, maxlength: '254',
      placeholder: 'you@email.com', class: 'w-full border-4 border-cream bg-night px-4 py-4 text-lg font-semibold text-cream placeholder-cream/40' });
    var errEl = h('p', { class: 'hidden mt-3 border-l-4 border-sun bg-sun/10 px-3 py-2 text-sm font-bold', role: 'alert' });
    var btn = h('button', { type: 'submit', class: BTN + 'bg-sun text-night mt-4' }, 'Email me a sign-in link');
    var form = h('form', { novalidate: true, onsubmit: function (ev) {
      ev.preventDefault();
      var email = emailInput.value.trim().toLowerCase();
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { errEl.textContent = 'Enter a valid email address.'; errEl.classList.remove('hidden'); return; }
      errEl.classList.add('hidden');
      btn.disabled = true; btn.textContent = 'Sending...';
      S.sb.auth.signInWithOtp({ email: email, options: { emailRedirectTo: location.origin + '/app/' } }).then(function (res) {
        if (res.error) { btn.disabled = false; btn.textContent = 'Email me a sign-in link'; errEl.textContent = res.error.message || 'Could not send the link.'; errEl.classList.remove('hidden'); return; }
        S.authSent = email; render();
      });
    } }, h('label', { for: 'auth-email', class: 'block text-xs font-extrabold tracking-widest text-gold mb-1' }, 'EMAIL'), emailInput, errEl, btn);

    return h('div', { class: 'min-h-screen' },
      h('div', { class: 'bg-gradient-to-b from-[#1B2440] via-[#7A3B3B] to-[#FF8A2B] px-6 pt-14 pb-10 text-center' },
        h('p', { class: 'text-xs font-extrabold tracking-[.3em] text-gold' }, '30-DAY JOURNEY'),
        h('h1', { class: 'font-display text-6xl leading-[.95] uppercase mt-3' }, 'Shatter', h('br'), h('span', { class: 'text-sun' }, 'The Chains')),
        h('p', { class: 'mt-4 font-semibold text-cream/95' }, 'Your interactive map, daily tracker, private prayer vault and audio devotionals.')),
      h('div', { class: 'camo h-8 border-t-4 border-sun' }),
      h('div', { class: 'px-6 pt-8' },
        S.authSent
          ? h('div', { class: 'border-4 border-gold bg-olived p-5' },
              h('p', { class: 'font-display text-3xl uppercase' }, 'Check your ', h('span', { class: 'text-gold' }, 'inbox')),
              h('p', { class: 'mt-3 font-semibold' }, 'We sent a sign-in link to ' + S.authSent + '. Tap it on this device to open your journey. Check spam if you don\'t see it.'),
              h('button', { type: 'button', class: 'mt-4 underline font-bold', onclick: function () { S.authSent = null; render(); } }, 'Use a different email'))
          : [h('h2', { class: 'font-display text-4xl uppercase leading-none' }, 'Sign in ', h('span', { class: 'text-sun' }, 'or join')),
             h('p', { class: 'mt-3 font-semibold text-cream/80' }, 'No password. We\'ll email you a one-tap link.'),
             h('div', { class: 'mt-5' }, form)]));
  }

  function tierCard(key, cfgTier, feats, highlight) {
    return h('div', { class: 'border-4 p-4 mt-4 ' + (highlight ? 'border-sun bg-olived' : 'border-cream bg-night') },
      highlight ? h('span', { class: 'inline-block bg-sun text-night text-[11px] font-extrabold tracking-widest px-2 py-1 mb-2' }, 'BEST VALUE') : null,
      h('div', { class: 'flex items-end justify-between' },
        h('h3', { class: 'font-display text-3xl uppercase' }, cfgTier.label),
        h('p', { class: 'font-display text-4xl leading-none' }, '$' + cfgTier.price, h('span', { class: 'text-base font-body font-extrabold text-cream/70' }, '/mo'))),
      h('ul', { class: 'mt-3 space-y-2 font-semibold text-sm' }, feats.map(function (f) { return h('li', { class: 'flex gap-2' }, h('span', { class: 'text-sun', 'aria-hidden': 'true' }, '●'), f); })),
      h('div', { class: 'mt-4' }, btnPrimary('Choose ' + cfgTier.label, function (ev) {
        var b = ev.currentTarget; b.disabled = true; b.textContent = 'Opening checkout...';
        api('/api/stripe-checkout', { body: { tier: key } }).then(function (d) { location.href = d.url; })
          .catch(function (e) { b.disabled = false; b.textContent = 'Choose ' + cfgTier.label; showToast(e.message); });
      }, highlight ? '' : 'bg-cream')));
  }

  function viewPaywall() {
    var t = S.cfg.tiers;
    var checkoutBanner = null;
    if (S.polling) checkoutBanner = h('div', { class: 'border-4 border-gold bg-olived p-4 mb-4 font-bold', role: 'status' }, 'Confirming your payment... this takes a few seconds.');
    return h('div', { class: 'px-6 pt-10 pb-16' },
      h('p', { class: 'text-xs font-extrabold tracking-[.3em] text-gold' }, 'UNLOCK YOUR 30 DAYS'),
      h('h1', { class: 'font-display text-5xl uppercase leading-none mt-2' }, 'Pick your ', h('span', { class: 'text-sun' }, 'plan')),
      h('p', { class: 'mt-3 font-semibold text-cream/80' }, 'Recurring monthly subscription. Change or cancel anytime from Account.'),
      h('div', { class: 'mt-4' }, checkoutBanner),
      tierCard('starter', t.starter, ['30-day interactive map', 'Daily habit and prayer tracker', 'Daily scripture and breakdowns'], false),
      tierCard('vault', t.vault, ['Everything in Starter', 'Private Prayer Vault, locked to you', 'Journal every Vault Prompt'], false),
      tierCard('full', t.full, ['Everything in Vault', 'Daily audio devotionals', 'Listen hands-free, anywhere'], true),
      h('button', { type: 'button', class: 'mt-8 underline font-bold text-cream/80', onclick: function () { S.sb.auth.signOut(); } }, 'Sign out (' + S.session.user.email + ')'));
  }

  function viewMap() {
    var cur = currentDay();
    var done = doneCount();
    var pct = Math.round((done / 30) * 100);
    var offsets = [50, 74, 50, 26];
    var list = [];
    S.days.forEach(function (d, i) {
      var n = i + 1;
      if (WEEKS[n]) list.push(h('div', { class: 'mt-6 mb-2 bg-olived border-l-8 border-sun px-3 py-2' }, h('p', { class: 'font-display text-xl tracking-wide' }, WEEKS[n])));
      var state = isDone(n) ? 'done' : (n === cur ? 'current' : 'locked');
      var circle = h('span', { class: 'flex items-center justify-center w-16 h-16 rounded-full border-4 font-display text-2xl ' +
        (state === 'done' ? 'bg-gold text-night border-cream' : state === 'current' ? 'bg-sun text-night border-cream pulse-ring' : 'bg-night text-cream/40 border-cream/30') },
        state === 'done' ? '✓' : state === 'locked' ? '🔒' : String(n));
      var node = h('a', { href: state === 'locked' ? null : '#/day/' + n, 'aria-disabled': state === 'locked' ? 'true' : null,
        'aria-label': 'Day ' + n + ', ' + d.title + ', ' + state, class: 'flex flex-col items-center w-28 text-center ' + (state === 'locked' ? 'pointer-events-none' : '') },
        circle,
        h('span', { class: 'mt-1 text-[10px] font-extrabold tracking-widest ' + (state === 'locked' ? 'text-cream/40' : 'text-gold') }, 'DAY ' + n),
        h('span', { class: 'text-[11px] font-bold leading-tight ' + (state === 'locked' ? 'text-cream/40' : 'text-cream/90') }, d.title));
      list.push(h('div', { class: 'relative my-3', style: 'padding-left:calc(' + offsets[i % 4] + '% - 56px)' }, node));
    });

    var finale = done === 30 ? h('div', { class: 'mx-6 mt-6 border-4 border-gold bg-olived p-4' },
      h('p', { class: 'font-display text-3xl uppercase' }, 'You made it, ', h('span', { class: 'text-gold' }, 'sis')),
      h('p', { class: 'mt-2 font-semibold' }, '30 days. Behold, He makes all things new. Go back to your Vault and read Day 1. See how far you\'ve come.')) : null;

    return shell('map', h('div', null,
      h('div', { class: 'px-6 pt-6' },
        label('Your journey'),
        h('h1', { class: 'font-display text-5xl uppercase leading-none mt-1' }, done + ' of 30 ', h('span', { class: 'text-sun' }, 'days')),
        h('div', { class: 'mt-3 h-4 border-4 border-cream bg-night', role: 'progressbar', 'aria-valuemin': '0', 'aria-valuemax': '100', 'aria-valuenow': String(pct) },
          h('div', { class: 'h-full bg-sun', style: 'width:' + pct + '%' })),
        cur <= 30 ? h('div', { class: 'mt-4' }, btnPrimary(done === 0 ? 'Start Day 1' : 'Continue Day ' + cur, function () { location.hash = '#/day/' + cur; })) : null),
      finale,
      h('div', { class: 'px-2 mt-2' }, list)));
  }

  function lockedBox(title, text, cta) {
    return h('div', { class: 'border-4 border-dashed border-cream/40 p-4 mt-2 text-center' },
      h('p', { class: 'font-display text-2xl uppercase' }, '🔒 ' + title),
      h('p', { class: 'mt-1 text-sm font-semibold text-cream/70' }, text),
      h('button', { type: 'button', class: 'mt-3 underline font-bold text-gold', onclick: function () { location.hash = '#/account'; } }, cta || 'Upgrade in Account'));
  }

  function viewDay(n) {
    var d = S.days[n - 1];
    if (!d) return shell('map', h('div', { class: 'p-6' }, h('p', { class: 'font-bold' }, 'Day not found.')));
    var cur = currentDay();
    if (n > cur) { location.hash = '#/day/' + cur; return viewLoading(); }
    var p = progressRow(n);
    var saved = h('span', { class: 'text-xs font-bold text-cream/60' }, '');

    // Tracker
    var habits = d.habits.map(function (text, i) {
      var cb = h('input', { type: 'checkbox', id: 'habit-' + i, checked: !!p.habits[i], class: 'mt-1 w-6 h-6 accent-[#FF6B1A] shrink-0',
        onchange: function (ev) { var hb = progressRow(n).habits.slice(); hb[i] = ev.target.checked; saveProgress(n, { habits: hb }); refreshComplete(); } });
      return h('label', { for: 'habit-' + i, class: 'flex gap-3 items-start font-semibold' }, cb, h('span', null, text));
    });
    var minBtns = [];
    function styleMin(btn, on) {
      btn.className = 'flex-1 py-2 border-4 font-extrabold text-sm ' + (on ? 'bg-sun text-night border-cream' : 'border-cream/50 text-cream');
      btn.setAttribute('aria-pressed', String(on));
    }
    var mins = h('div', { class: 'flex gap-2 mt-2' }, [0, 5, 10, 15, 20].map(function (m) {
      var b = h('button', { type: 'button', 'data-min': String(m),
        onclick: function () { saveProgress(n, { prayer_minutes: m }); minBtns.forEach(function (x) { styleMin(x.b, x.m === m); }); } }, m === 20 ? '20+' : String(m));
      styleMin(b, progressRow(n).prayer_minutes === m);
      minBtns.push({ b: b, m: m });
      return b;
    }));
    function scale(field, lab) {
      var sel = h('select', { class: 'w-full border-4 border-cream bg-night px-3 py-3 font-bold', 'aria-label': lab,
        onchange: function (ev) { var v = ev.target.value; var patch = {}; patch[field] = v ? Number(v) : null; saveProgress(n, patch); } },
        h('option', { value: '' }, '-'),
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(function (x) { return h('option', { value: String(x), selected: p[field] === x ? true : null }, String(x)); }));
      return h('div', { class: 'flex-1' }, h('p', { class: 'text-xs font-extrabold tracking-widest text-gold mb-1' }, lab.toUpperCase()), sel);
    }

    // Vault prompt
    var vaultPart;
    if (S.rank >= 2) {
      var existing = S.vault.filter(function (e) { return e.kind === 'journal' && e.day === n; })[0];
      var ta = h('textarea', { rows: '5', maxlength: '8000', placeholder: 'Write it out. Only you can see this.',
        class: 'w-full border-4 border-cream bg-night px-3 py-3 font-semibold text-cream placeholder-cream/40' });
      ta.value = existing ? existing.body : '';
      vaultPart = h('div', null,
        ta,
        h('div', { class: 'mt-2 flex items-center gap-3' },
          h('button', { type: 'button', class: 'px-5 py-3 bg-gold text-night font-display text-xl uppercase border-4 border-cream', onclick: function () {
            var body = ta.value.trim();
            if (!body) { showToast('Write something first.'); return; }
            var q = existing
              ? S.sb.from('vault_entries').update({ body: body }).eq('id', existing.id)
              : S.sb.from('vault_entries').insert({ user_id: S.session.user.id, day: n, kind: 'journal', body: body });
            q.then(function (res) { if (res.error) { showToast('Could not save.'); return; } return loadVault().then(function () { showToast('Saved to your Vault.'); }); });
          } }, 'Save to Vault'),
          saved));
    } else {
      vaultPart = lockedBox('Private Vault', 'Journal every prompt privately. Available on Vault and Full Access plans.');
    }

    // Audio
    var audioPart;
    if (S.rank >= 3) {
      var ab = h('button', { type: 'button', class: BTN + 'bg-gold text-night' }, audio.playing === n ? 'STOP' : 'PLAY DEVOTIONAL');
      ab.addEventListener('click', function () { toggleAudio(n, ab); });
      audioPart = ab;
    } else {
      audioPart = lockedBox('Audio Devotional', 'Listen to today\'s breakdown and prayer hands-free. Included in Full Access.');
    }

    // Complete
    var completeBtn = h('button', { type: 'button', class: BTN + 'bg-sun text-night' }, p.completed ? 'Day complete ✓' : 'Complete Day ' + n);
    function allChecked() { var pr = progressRow(n); return pr.habits.length > 0 && pr.habits.every(Boolean); }
    function refreshComplete() {
      var ok = allChecked() || progressRow(n).completed;
      completeBtn.disabled = !ok;
      completeBtn.setAttribute('aria-disabled', ok ? 'false' : 'true');
    }
    completeBtn.addEventListener('click', function () {
      if (progressRow(n).completed) { location.hash = '#/map'; return; }
      if (!allChecked()) return;
      completeBtn.disabled = true;
      saveProgress(n, { completed: true, completed_at: new Date().toISOString() }, true).then(function (ok) {
        if (!ok) { completeBtn.disabled = false; return; }
        showToast(n === 30 ? 'Day 30 complete. He makes all things new.' : 'Day ' + n + ' complete. Keep going, sis.');
        location.hash = '#/map';
      });
    });
    refreshComplete();

    var prev = n > 1 ? h('a', { href: '#/day/' + (n - 1), class: 'font-bold underline' }, '← Day ' + (n - 1)) : h('span');
    var next = (n < 30 && isDone(n)) ? h('a', { href: '#/day/' + (n + 1), class: 'font-bold underline' }, 'Day ' + (n + 1) + ' →') : h('span');

    return shell('map', h('article', null,
      h('header', { class: 'camo px-6 pt-6 pb-5 border-b-4 border-sun' },
        h('a', { href: '#/map', class: 'text-xs font-extrabold tracking-widest text-gold' }, '← BACK TO MAP'),
        h('p', { class: 'mt-3 text-xs font-extrabold tracking-[.3em] text-gold' }, 'DAY ' + n + ' OF 30'),
        h('h1', { class: 'font-display text-4xl uppercase leading-none mt-1' }, d.title)),
      h('div', { class: 'px-6 pt-6 space-y-6' },
        h('section', null, label('Core Scripture', 'text-sun'),
          h('blockquote', { class: 'mt-2 bg-cream text-night border-l-8 border-sun p-4 font-bold italic' }, '“' + d.verse + '”',
            h('footer', { class: 'mt-2 not-italic text-sm text-sun font-extrabold' }, '- ' + d.ref.toUpperCase() + ' (KJV)'))),
        h('section', null, label('The Breakdown', 'text-sun'), h('p', { class: 'mt-2 font-semibold leading-relaxed' }, d.breakdown)),
        h('section', null, label('Audio Devotional', 'text-sun'), h('div', { class: 'mt-2' }, audioPart)),
        h('section', null, label('Action Tracker', 'text-sun'),
          h('div', { class: 'mt-3 space-y-3' }, habits),
          h('p', { class: 'mt-5 text-xs font-extrabold tracking-widest text-gold' }, 'PRAYER MINUTES'), mins,
          h('div', { class: 'mt-4 flex gap-3' }, scale('chain_before', 'Chain weight before'), scale('chain_after', 'Chain weight after'))),
        h('section', null, label('The Vault Prompt', 'text-sun'), h('p', { class: 'mt-2 font-semibold italic' }, d.vault), h('div', { class: 'mt-3' }, vaultPart)),
        h('section', { class: 'bg-olived border-4 border-gold p-4' }, label('Daily Prayer'), h('p', { class: 'mt-2 font-bold leading-relaxed' }, d.prayer)),
        completeBtn,
        h('div', { class: 'flex justify-between pb-4' }, prev, next))));
  }

  function viewVault() {
    if (S.rank < 2) {
      return shell('vault', h('div', { class: 'px-6 pt-8' }, label('Private Prayer Vault'),
        h('h1', { class: 'font-display text-5xl uppercase leading-none mt-1' }, 'Your ', h('span', { class: 'text-sun' }, 'vault')),
        h('p', { class: 'mt-3 font-semibold text-cream/80' }, 'A private place for your prayers, journal entries and breakthroughs. Only you can read it.'),
        lockedBox('Vault plan required', 'Upgrade to Vault ($' + S.cfg.tiers.vault.price + '/mo) or Full Access ($' + S.cfg.tiers.full.price + '/mo).')));
    }
    var kind = h('select', { 'aria-label': 'Entry type', class: 'border-4 border-cream bg-night px-3 py-3 font-bold' },
      h('option', { value: 'prayer' }, 'Prayer'), h('option', { value: 'journal' }, 'Journal'));
    var ta = h('textarea', { rows: '4', maxlength: '8000', 'aria-label': 'New entry', placeholder: 'Write a prayer or a breakthrough. Private to you.',
      class: 'w-full border-4 border-cream bg-night px-3 py-3 font-semibold text-cream placeholder-cream/40' });
    var add = h('button', { type: 'button', class: BTN + 'bg-sun text-night mt-3', onclick: function () {
      var body = ta.value.trim();
      if (!body) { showToast('Write something first.'); return; }
      add.disabled = true;
      S.sb.from('vault_entries').insert({ user_id: S.session.user.id, kind: kind.value, body: body, day: null }).then(function (res) {
        add.disabled = false;
        if (res.error) { showToast('Could not save.'); return; }
        return loadVault().then(function () { render(); showToast('Saved.'); });
      });
    } }, 'Add to Vault');
    var entries = S.vault.length === 0
      ? h('p', { class: 'mt-6 font-semibold text-cream/60' }, 'Nothing here yet. Your first prayer goes above.')
      : S.vault.map(function (e) {
        return h('article', { class: 'mt-4 border-4 border-cream/40 p-4' },
          h('div', { class: 'flex justify-between items-center' },
            h('p', { class: 'text-xs font-extrabold tracking-widest text-gold' }, (e.kind === 'prayer' ? 'PRAYER' : 'JOURNAL') + (e.day ? ' - DAY ' + e.day : '') + ' - ' + new Date(e.created_at).toLocaleDateString()),
            h('button', { type: 'button', 'aria-label': 'Delete entry', class: 'text-xs font-bold underline text-cream/70', onclick: function () {
              if (!window.confirm('Delete this entry? This cannot be undone.')) return;
              S.sb.from('vault_entries').delete().eq('id', e.id).then(function (res) {
                if (res.error) { showToast('Could not delete.'); return; }
                return loadVault().then(render);
              });
            } }, 'Delete')),
          h('p', { class: 'mt-2 font-semibold whitespace-pre-wrap break-words' }, e.body));
      });
    return shell('vault', h('div', { class: 'px-6 pt-8 pb-8' }, label('Private Prayer Vault'),
      h('h1', { class: 'font-display text-5xl uppercase leading-none mt-1' }, 'Your ', h('span', { class: 'text-sun' }, 'vault')),
      h('p', { class: 'mt-2 text-sm font-semibold text-cream/70' }, 'Only you can read what\'s written here.'),
      h('div', { class: 'mt-5' }, kind, h('div', { class: 'mt-3' }, ta), add), chevrons(), entries));
  }

  function viewAccount() {
    var planName = S.rank ? S.cfg.tiers[S.sub.tier].label : 'No plan';
    var renew = S.sub && S.sub.current_period_end ? new Date(S.sub.current_period_end).toLocaleDateString() : null;
    var canBill = !!S.sub;
    return shell('account', h('div', { class: 'px-6 pt-8 pb-8' }, label('Account'),
      h('h1', { class: 'font-display text-5xl uppercase leading-none mt-1' }, 'Your ', h('span', { class: 'text-sun' }, 'plan')),
      h('div', { class: 'mt-5 border-4 border-cream p-4' },
        h('p', { class: 'text-xs font-extrabold tracking-widest text-gold' }, 'SIGNED IN AS'), h('p', { class: 'font-bold break-all' }, S.session.user.email),
        h('p', { class: 'mt-3 text-xs font-extrabold tracking-widest text-gold' }, 'PLAN'),
        h('p', { class: 'font-bold' }, planName + (S.sub ? ' (' + S.sub.status + ')' : '')),
        renew ? h('p', { class: 'mt-3 text-xs font-extrabold tracking-widest text-gold' }, S.sub.cancel_at_period_end ? 'ENDS ON' : 'RENEWS ON') : null,
        renew ? h('p', { class: 'font-bold' }, renew) : null),
      h('div', { class: 'mt-5 space-y-3' },
        canBill ? btnPrimary('Manage billing / change plan', function (ev) {
          var b = ev.currentTarget; b.disabled = true;
          api('/api/stripe-portal').then(function (d) { location.href = d.url; }).catch(function (e) { b.disabled = false; showToast(e.message); });
        }) : null,
        !S.rank ? btnPrimary('Choose a plan', function () { S.forcePaywall = true; render(); }) : null,
        btnGhost('Sign out', function () { stopAudio(); S.sb.auth.signOut(); })),
      h('p', { class: 'mt-6 text-xs text-cream/50 font-semibold' }, 'Scripture: King James Version. Billing is handled securely by Stripe.')));
  }

  // ---------- routing ----------
  function route() {
    var hash = location.hash || '#/map';
    var m = /^#\/day\/(\d+)$/.exec(hash);
    if (m) return { name: 'day', n: Math.max(1, Math.min(30, parseInt(m[1], 10))) };
    if (hash === '#/vault') return { name: 'vault' };
    if (hash === '#/account') return { name: 'account' };
    return { name: 'map' };
  }

  function render() {
    if (S.booting) return mount(viewLoading());
    if (S.error) return mount(viewError(S.error));
    if (!S.session) { S.forcePaywall = false; return mount(viewAuth()); }
    var r = route();
    if (S.rank < 1) {
      if (r.name === 'account' && !S.forcePaywall) return mount(viewAccount());
      return mount(viewPaywall());
    }
    var view = r.name === 'day' ? viewDay(r.n) : r.name === 'vault' ? viewVault() : r.name === 'account' ? viewAccount() : viewMap();
    mount(view);
    if (r.name !== 'day') window.scrollTo(0, 0);
    if (S.toast) showToast(S.toast);
  }

  window.addEventListener('hashchange', function () { stopAudio(); render(); if (route().name === 'day') window.scrollTo(0, 0); });

  // After Stripe redirects back, the webhook may lag a few seconds: poll for the subscription.
  function pollForSubscription() {
    var params = new URLSearchParams(location.search);
    if (params.get('checkout') !== 'success' || S.rank >= 1) return;
    S.polling = true; render();
    var tries = 0;
    (function tick() {
      tries++;
      loadAll().then(function () {
        if (S.rank >= 1) { S.polling = false; history.replaceState(null, '', '/app/#/map'); render(); showToast('You\'re in. Welcome to the journey.'); return; }
        if (tries >= 20) { S.polling = false; render(); showToast('Still confirming. Refresh in a minute or contact support.'); return; }
        setTimeout(tick, 2000);
      }).catch(function () { S.polling = false; render(); });
    })();
  }

  // ---------- boot ----------
  function boot() {
    Promise.all([
      fetch('/api/config').then(function (r) { if (!r.ok) throw new Error('The app is not configured yet.'); return r.json(); }),
      fetch('/app/days.json').then(function (r) { if (!r.ok) throw new Error('Could not load the journey content.'); return r.json(); })
    ]).then(function (res) {
      S.cfg = res[0];
      S.days = res[1];
      if (!window.supabase || !window.supabase.createClient) throw new Error('Could not load the sign-in library. Check your connection and reload.');
      S.sb = window.supabase.createClient(S.cfg.supabaseUrl, S.cfg.supabaseAnonKey, { auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true } });
      return S.sb.auth.getSession();
    }).then(function (res) {
      S.session = res.data && res.data.session;
      S.sb.auth.onAuthStateChange(function (event, session) {
        var was = S.session && S.session.user.id;
        S.session = session;
        if (event === 'SIGNED_OUT') { S.sub = null; S.rank = 0; S.progress = {}; S.vault = []; S.authSent = null; render(); return; }
        if (session && session.user.id !== was) { loadAll().then(function () { render(); pollForSubscription(); }).catch(function () { render(); }); }
      });
      if (!S.session) return;
      return loadAll();
    }).then(function () {
      S.booting = false;
      render();
      pollForSubscription();
    }).catch(function (e) {
      S.booting = false;
      S.error = (e && e.message) || 'Something went wrong.';
      render();
    });
    if ('serviceWorker' in navigator) navigator.serviceWorker.register('/app/sw.js', { scope: '/app/' }).catch(function () {});
  }

  render();
  boot();
})();
