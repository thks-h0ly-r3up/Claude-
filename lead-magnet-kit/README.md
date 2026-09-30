# THKS Lead Magnet Kit — The Next Right Step
7HE H0LY KIL0 SYNDICATE (THKS) • 7HE H0LY R3UP by THKS & CO.

## What's here
| Folder / file | What it is |
|---|---|
| `dist/next-right-step.pdf` / `.html` | The finished free lead magnet (30 pages: cover, letter, how-to, safety check, 7 days × teaching+working page, 5 lies, boundaries, relapse plan, accountability partner, 30-day calendar + weekly check-in, prayers, scripture cards, resources, closing, testimony+photos, legal) |
| `dist/tracker.html` | Live progress tracker (7-day checklists, 30-day anchor grid, streak, craving log, wins, print/export). Data stays in the user's browser |
| `dist/emails/01…07` | 7-email welcome sequence in Nikki's voice, with send timing on line 1 |
| `photos/stages/stage-1…6.png` | Six separate "stages of completion" photos: seed in concrete → harvest |
| `social/thks-social-doa-1080x1350.png` | Social image: D.O.A. line + Ephesians 2:5 + big CTA |
| `plan/monetization-plan.md` | Ladder, Shopify setup (free guide stays off storefront), tracking, 30/60/90 |
| `template/` + `new_product.py` | Blank product template with pre-made steps; each new product gets a unique design |
| `content/legal.html`, `content/testimony.html` | Attached automatically to every product |
| `photos/team/` | **Drop your real photos here** (you + Big Boy). They're added to every product's testimony page |
| `private/` (git-ignored) | Your eyes only: `creation-log.csv` (date/time created, design fingerprint, file hash) and `funnel-tracker.csv` |

## 5 things only you can do (nothing was invented for you)
1. Fill `links.config.json` (Linktree, store, Gmail, Template Creator, Plugin Creator, tracker URL, guide URL, paid product URL, unsubscribe URL, mailing address — a postal address is legally required in commercial email).
2. Put real photos in `photos/team/` (jpg/png).
3. Open `content/testimony.html`, correct it in your own words, delete the `REVIEW_ME` comment.
4. Reconnect Shopify (it needs re-authorization), then follow `plan/monetization-plan.md`.
5. Have an attorney review `content/legal.html` and your store policies. It's solid boilerplate, not legal advice.

## Commands
```
python3 build.py              # draft build (shows what's missing)
python3 build.py --release    # refuses until links, testimony, photos are complete
python3 new_product.py my-slug "Title" "Subtitle"   # new blank product, unique design, logs creation date privately
```
Needs Python 3 and Chromium (for the PDF step).
