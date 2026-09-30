# Monetization Plan — 7HE H0LY R3UP by THKS & CO.
*Prices and numbers below are planning estimates, not promises or income guarantees. Adjust to your real costs.*

## The ladder (honest, no fake scarcity, no countdowns)
| Step | Offer | Price | Purpose |
|---|---|---|---|
| 0 | **The Next Right Step** (7-day guide + tracker) — lead magnet, *not listed in the store*, delivered by email only | Free | Reach the person in the gap |
| 1 | **30-Day Vineyard Planner** (printable, built from `template/`) | $9–$12 | First small yes after Day 7 email |
| 2 | **Bando 2 Vineyard Workbook** (triggers, repair, boundaries, budget rebuild) | $19–$27 | Core product |
| 3 | **Recovery Toolkit Bundle** (planner + workbook + journal + checklists already in `/printables`) | $39–$47 | Bundle for higher order value |
| 4 | **Build-Your-Own Kit** (this template system for other faith/recovery creators; links: Template Creator / Plugin Creator) | $49–$97 | Second revenue stream, serves creators |
| — | **Scholarship codes** (100% off, no questions) | Free | Keeps the mission honest: nobody is priced out |

## Shopify setup (free guide stays OFF the storefront)
1. Products stay at the paid tiers only. Do **not** create a product for the free guide.
2. Host the guide PDF + `tracker.html` where only email subscribers get the link: Shopify Admin → Content → Files (copy link), or a hidden page (Online Store → Pages, "Hide from search engines", no menu link). Put those two URLs in `links.config.json` as `GUIDE_DOWNLOAD_URL` and `TRACKER_URL`.
3. Signup form: Online Store → Themes → Customize → add a Newsletter/"Subscribe" section (or Shopify Forms app). Button text: **Send me the free 7-day guide**. Tag new subscribers `lead-magnet`.
4. Automations: Shopify Email → Automations → build "Welcome series" using `dist/emails/01…07`. (Any email tool works; Klaviyo/MailerLite also fine.) Set each email's delay from the `SEND:` line at the top of each file.
5. Paid products: Digital Downloads app → upload `dist/<slug>.pdf`. Product media = photos from `photos/stages/`. Description includes the legal summary below.
6. Discount codes: `SCHOLAR` (100% off, limit 1 use, you approve manually) — never advertise a fake "sale ends."

## Product page copy rule
Lead with who it's for and exactly what's inside. State plainly: "Not medical advice. Personal-use license. Digital download, nothing ships." Link the full notices page. Refund policy: your call (write it in Shopify Settings → Policies); digital goods commonly are final-sale, but say so clearly and honor honest mistakes.

## Tracking (all yours, private)
| Metric | Where | Target (first 90 days) |
|---|---|---|
| Visitors → signups | Shopify Analytics / form | 8–15% |
| Signups → open Email 1 | email tool | 50%+ |
| Signups → Day-8 email click | email tool | 10–15% |
| Free → paid buyers | Shopify orders w/ tag | 2–5% |
| Average order value | Shopify | $20+ |
| Reply rate to Email 7 | Gmail | any — read them all |
Use `?utm_source=` on every social link (Instagram, TikTok, Facebook) so you can see what actually brings people in. Keep a weekly line in `private/funnel-tracker.csv`.

## Example math (illustrative only)
100 signups/month × 3% buy = 3 buyers × ~$25 = ~$75. It grows with signups, not pressure: 1,000 signups = ~$750. Fund the mission by the volume of *useful* things you put in front of people, not by squeezing anyone.

## Where the money goes (decide and publish it once)
Suggested split: hosting/tools 25% • free copies & scholarships 25% • the mission (recovery resources, Brandi Renee memorial work) 25% • Nikki's pay 25%. Change it, but put whatever you choose in writing and stick to it.

## 30/60/90
- **Days 1–30:** Fill `links.config.json`, add real photos, finish testimony, release build, sign up the form, load emails, post the social image 3×/week.
- **Days 31–60:** Ship the 30-Day Vineyard Planner via `new_product.py`. First paid emails. Ask 5 subscribers what they need next.
- **Days 61–90:** Workbook + bundle. Start the Build-Your-Own Kit outline. Review the numbers; cut what isn't serving anyone.

## Never
Fake testimonials • fake scarcity/countdowns • "God told me you need to buy this" • income claims • medical/cure claims • selling the same design twice (`new_product.py` prevents duplicates).
