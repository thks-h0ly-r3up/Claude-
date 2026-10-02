# 7HE H0LY R3UP FOR ALL — style guide (ultra-realistic western)

Applies to every product. See /CLAUDE.md for the standing rules; this is the design system.

**Never reuse art.** Each new product gets newly generated plates in this same style (no text in any plate; all lettering is live type).

## Palette
Navy #1f3b63 · Gold #a06f1c · Wine #7a2c4a · Turquoise #27857f · Purple #7a4c9e · Pink #d6598f · cream parchment (243,233,208).

## Type
Rye (titles) · Caveat (handwritten accents) · Libre Franklin (body). Fonts live in `fonts/`.

## Page
Cream parchment full page with a stitched denim band on the binding edge (right-hand pages: left edge; left-hand pages: right edge). Cards are translucent cream with thin tan or blue borders. Ink-saver variant: `python build_new.py --ink` (plain white).

## Day layout (6 pages)
Guide (goal, Bible in context, what research suggests, 5 numbered steps) → Standing left → Standing right → Coming Home → Write it (before/after 0–10 rating) → Pocket page (verse to carry, note of love + ESV verse, nugget, Today I choose, Future Me).

## Art recipe (photographic, no text)
Weathered wooden cross + crown of thorns at desert dusk · vineyard at sunrise · Bible, candle and broken chain on rugged wood · stitched blue denim · cracked turquoise leather with silver concho · mason jar with light and dried flowers · brass anchor · cowhide. Portrait 4:5 or taller; ≥2000 px wide for print. Big Boy: gray-and-white American Bully, muscular, NO EARS; use real supplied photos only.

## Build
`python compose_bg.py` (page backgrounds) · `python build_new.py` · `python build_covers.py` (binder covers).
Content: `rb_days_*.py` (research layer), `rb_love.py` (notes + verses), `rb_sources.py` (citations: verify before relying).
