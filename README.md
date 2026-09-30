# SHATTERING CHAINS - Automated Lead Gen & Digital Sales Funnel

```
Reel/TikTok -> comment "SHATTER" -> ManyChat DM -> Landing page (Vercel)
                                                      |  POST /api/lead
                                                      v
                             Supabase (leads_funnel)  +  Google Sheet (live)
                                                      |
                     instant PDF download  ->  /api/track (pdf_downloaded)
                     Premium App card      ->  /api/app  (app_clicked) -> APP_DOWNLOAD_URL
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

## Live auditing

- **Google Sheet > Metrics tab:** total leads, today, last 7 days, PDF download rate, app click rate, leads by source.
- **Supabase SQL:** `select * from leads_funnel_metrics;` for per-platform conversion.

## Security notes

- The service-role key and the Sheets secret live only in Vercel env vars.
- The browser never talks to Supabase or Sheets directly; it only calls `/api/lead`, `/api/track` and `/api/app`.
- The opt-in form has a honeypot field. For heavier traffic, add Vercel's WAF rate limiting on `/api/lead`.
- You are collecting emails: keep the unsubscribe promise, and add your privacy policy link if you send marketing email.

## Local development

```bash
npm i -g vercel
cp .env.example .env      # fill in real values
vercel dev
```
