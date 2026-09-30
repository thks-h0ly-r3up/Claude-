# SHATTERING CHAINS - Automated Lead Gen & Digital Sales Funnel

```
Reel/TikTok -> comment "SHATTER" -> ManyChat DM -> Landing page (Vercel)
                                                      |  POST /api/lead
                                                      v
                             Supabase (leads_funnel)  +  Google Sheet (live)
                                                      |
                     instant PDF download  ->  /api/track (pdf_downloaded)
                     Premium App card      ->  /api/app  (app_clicked) -> /app/  (the paid app)

/app/  (installable PWA)  --magic-link login-->  Supabase Auth
   |                                                  ^
   +-- Choose plan --> /api/stripe-checkout --> Stripe Checkout
                                   Stripe --webhook--> /api/stripe-webhook --> subscriptions table
   Row Level Security reads `subscriptions` to unlock: Starter $5 / Vault $8 / Full Access $12
```

## What's in this repo

| Path | What it is |
|---|---|
| `content/video-script.md` | Reel/TikTok script (Hook > Me Too > Truth > Tool > Outro > "SHATTER" trigger) |
| `content/manychat-dm-sequence.md` | ManyChat flow + the exact instant DM and tracked link |
| `content/kit-copy.md` | All 9 kit pages as copy + design commands (auto-generated, Canva-ready) |
| `tools/build_kit.py` | Builds the 9-page A5 PDF (sunrise + anchor + camo) and `kit-copy.md` |
| `public/index.html` | Mobile landing page: opt-in > instant PDF download > premium app card |
| `public/shattering-chains-7-day-kit.pdf` | The finished printable kit served by the page |
| `api/lead.js` `api/track.js` `api/app.js` | Vercel serverless functions (no dependencies) |
| `supabase/schema.sql` | `leads_funnel` table, RLS lockdown, metrics view |
| `google-apps-script/Code.gs` | Secure webhook that writes/updates the live Google Sheet |
| `.env.example` | Environment variable template |
| `content/days.json` | All 30 days (verse, breakdown, tracker, vault prompt, prayer). Source of truth for kit + app |
| `public/app/` | The paid app (PWA): auth, paywall, 30-day map, tracker, Prayer Vault, audio devotionals, account |
| `api/config.js` `api/stripe-*.js` | App runtime config, Stripe Checkout, billing portal, webhook |
| `supabase/app_schema.sql` | Subscriptions, progress, vault tables with tier-gated Row Level Security |
| `tools/build_icons.py` | Regenerates the app icons |

Scripture is the King James Version (public domain), so the kit is free of licensing issues.

---

# 30-Minute Deployment Blueprint

## Minute 0-5: Supabase

1. supabase.com > **New project** (any name, save the DB password, pick the closest region).
2. **SQL Editor > New query**, paste all of `supabase/schema.sql`, click **Run**.
3. **Project Settings > API**. Copy:
   - **Project URL** -> `SUPABASE_URL`
   - **service_role** secret -> `SUPABASE_SERVICE_ROLE_KEY` (server only; never in the browser)

The table is locked with Row Level Security and no public policies: only your Vercel functions (service role) can read or write it.

## Minute 5-12: Google Sheets

1. Create a new Google Sheet named `Shattering Chains Leads`.
2. **Extensions > Apps Script**. Delete the default code, paste all of `google-apps-script/Code.gs`, save.
3. **Project Settings (gear) > Script Properties > Add**: name `WEBHOOK_SECRET`, value = output of `openssl rand -hex 32` (or any 40+ random characters). Keep a copy -> `SHEETS_WEBHOOK_SECRET`.
4. Select the function `setup` in the toolbar > **Run**. Authorize when prompted (Advanced > Go to project). This builds the `Leads` sheet, checkboxes and a live `Metrics` tab.
5. **Deploy > New deployment > type: Web app**. Execute as **Me**, Who has access **Anyone**. **Deploy**, copy the **Web app URL** (ends in `/exec`) -> `SHEETS_WEBHOOK_URL`.
6. Open that URL in a browser: you should see `{"ok":true,"service":"shattering-chains-sheet-sync"}`.

The URL is public but useless without the secret; requests without it get `unauthorized` and write nothing.

## Minute 12-22: Vercel

1. Push this repo to GitHub (already done if you're reading this there).
2. vercel.com > **Add New > Project** > import the repo. Framework Preset: **Other**. Leave build settings empty. (`vercel.json` already points to `public/`.)
3. **Environment Variables** (Settings > Environment Variables, all environments), copy from `.env.example`:

```env
SUPABASE_URL=https://YOUR-PROJECT-REF.supabase.co
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY
SHEETS_WEBHOOK_URL=https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec
SHEETS_WEBHOOK_SECRET=YOUR_LONG_RANDOM_SECRET
APP_DOWNLOAD_URL=https://your-app-store-or-checkout-link
```

4. **Deploy**. Your site is at `https://<project>.vercel.app` (add a custom domain under Settings > Domains if you have one).

### Test the pipeline (2 minutes)

Open `https://<project>.vercel.app/?src=instagram&h=testhandle&n=Test`, submit a real email. You should see:
- the PDF download starts and the "Your kit is downloading" block appears,
- the Premium App card lights up,
- a new row in Supabase **Table Editor > leads_funnel** with `pdf_downloaded = true`,
- the same row in the Google Sheet `Leads` tab,
- clicking **Get The App** flips `app_clicked` to TRUE in both, then redirects to `APP_DOWNLOAD_URL`.

## Minute 22-28: ManyChat

1. In ManyChat connect your Instagram professional account (Settings > Instagram).
2. **Automation > New Automation > Instagram > "User comments on a Post or Reel"**.
3. Choose the Reel (or "Any post or reel"), keyword **contains** `SHATTER`.
4. Add a public reply (three variants listed in `content/manychat-dm-sequence.md`), then the DM message.
5. Paste the Message 1 text and set the button URL to
   `https://<project>.vercel.app/?src=instagram&h={{ig_username}}&n={{first_name}}&utm_campaign=shatter_reel`.
6. Publish (**Set Live**). Comment `SHATTER` from a second account to test.

## Minute 28-30: Publish & point the QR at your app

1. Post the Reel using `content/video-script.md`.
2. Re-brand the kit's Page 9 QR to your real app link and rebuild:

```bash
pip install reportlab
APP_URL="https://your-app-or-checkout-link" python3 tools/build_kit.py
git add public content && git commit -m "Rebuild kit with live QR" && git push
```

Vercel redeploys automatically. (Or replace Page 9's QR inside Canva using `content/kit-copy.md` as your text source.)

---

---

# The Paid App ($5 - $12 / month)

Live at `https://<project>.vercel.app/app/`. Installable to the phone home screen (Share > Add to Home Screen).

| Plan | Price | Unlocks |
|---|---|---|
| Starter | $5/mo | 30-day interactive map, daily tracker, scripture + breakdowns |
| Vault | $8/mo | + Private Prayer Vault and journaling every Vault Prompt |
| Full Access | $12/mo | + daily audio devotionals |

Access is enforced in the database (Row Level Security), not just the UI, so a hacked front end can't read the Vault without paying.

## App setup (extra ~15 minutes, after the funnel steps above)

### A. Supabase
1. SQL Editor: run `supabase/app_schema.sql` (after `schema.sql`).
2. **Authentication > URL Configuration**: Site URL `https://<project>.vercel.app`; add Redirect URL `https://<project>.vercel.app/app/`.
3. **Authentication > Providers > Email**: enable, keep "Confirm email" on (magic link).
4. **Authentication > SMTP Settings**: add a custom SMTP sender (Resend, Postmark, etc.). Supabase's built-in email is limited to a few messages per hour and will throttle real sign-ups.
5. **Project Settings > API**: copy the **anon public** key into `SUPABASE_ANON_KEY`.

### B. Stripe
1. Products: create 3 products with a **recurring monthly** price each: Starter $5, Vault $8, Full Access $12 (or pick any prices in $5-$12; the labels come from the code, the amounts from Stripe). Copy each `price_...` ID into `STRIPE_PRICE_STARTER`, `STRIPE_PRICE_VAULT`, `STRIPE_PRICE_FULL`.
2. **Developers > API keys**: copy the secret key into `STRIPE_SECRET_KEY` (use a test key first).
3. **Developers > Webhooks > Add endpoint**: URL `https://<project>.vercel.app/api/stripe-webhook`, events: `checkout.session.completed`, `customer.subscription.created`, `customer.subscription.updated`, `customer.subscription.deleted`. Copy the signing secret into `STRIPE_WEBHOOK_SECRET`.
4. **Settings > Billing > Customer portal**: turn on, allow cancel and plan switching between your 3 prices (this powers "Manage billing / change plan").
5. In Vercel add `SUPABASE_ANON_KEY`, the five `STRIPE_*` variables and `SITE_URL`, set `APP_DOWNLOAD_URL=https://<project>.vercel.app/app/`, then **Redeploy**.

### C. Test with Stripe test mode
Sign in at `/app/` with a real email > choose a plan > pay with card `4242 4242 4242 4242` (any future date/CVC) > you land back in the app with the plan unlocked. Cancel from Account > Manage billing and confirm access ends after the period. Then switch the Stripe keys/prices to live mode.

### D. Audio devotionals
Out of the box the Full plan reads each devotional aloud with the phone's built-in voice (prefers a female voice). To use your own recordings or ElevenLabs audio, host the MP3s and add `"audio_url": "https://..."` to a day in `content/days.json`, then run `python3 tools/build_kit.py` to sync it to the app.

### App notes
- Days unlock in order as you complete each one (tick every habit, then Complete Day).
- Subscribers' data: progress and Vault entries are per-user in Supabase; only that user (and you, via the Supabase dashboard) can read them.
- Business view: `select * from subscription_metrics;` in Supabase for active subscribers and estimated MRR.
- Refunds, taxes, invoices and dunning are handled in Stripe.

## Live auditing

- **Google Sheet > Metrics tab:** total leads, today, last 7 days, PDF download rate, app click rate, leads by source.
- **Supabase SQL:** `select * from leads_funnel_metrics;` for per-platform conversion.

## Security notes

- The service-role key and the Sheets secret live only in Vercel env vars.
- The landing page never talks to Supabase or Sheets directly; it only calls `/api/lead`, `/api/track` and `/api/app`. The paid app uses the public anon key with Row Level Security, so each user can only touch their own rows and only with an active plan. The `service_role` key, Stripe secret and webhook secret are server-only.
- Stripe webhooks are verified with the signing secret (HMAC, 5-minute tolerance) before any database write.
- The opt-in form has a honeypot field. For heavier traffic, add Vercel's WAF rate limiting on `/api/lead`.
- You are collecting emails: keep the unsubscribe promise, and add your privacy policy link if you send marketing email.

## Local development

```bash
npm i -g vercel
cp .env.example .env      # fill in real values
vercel dev
```
