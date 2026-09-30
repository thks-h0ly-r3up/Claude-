# Blank Product Template — Pre-Made Steps

Run `python3 new_product.py "your-slug" "Product Title" "Subtitle"`. It creates products/<slug>/ with:
- product.json  (unique design fingerprint: palette, border, ornament, footer rotation)
- body.html     (cover + step pages copied from template/page.blank.html)

Legal page, testimony page, photo gallery and rotating footer are added automatically by build.py to EVERY product. You cannot forget them.

## The 12 steps from idea to shelf
1. Pick ONE person on the other side of the screen and ONE next step you're giving them.
2. `new_product.py` (design + private creation-date record are stamped automatically).
3. Fill body.html: cover, 5–10 step pages (verse → truth → tool → prayer).
4. Edit only if needed: content/testimony.html and photos/team/ (your real photos).
5. `python3 build.py` → dist/<slug>.html and .pdf
6. Read the PDF start to finish out loud once.
7. `python3 build.py --release` (refuses if links/testimony/photos aren't finished).
8. Shopify: Add product → upload dist/<slug>.pdf as the digital file (Digital Downloads app).
9. Paste description + price from plan/monetization-plan.md.
10. Add 5 photos from photos/stages as product media.
11. Publish; add to the "Paid Tools" collection; post the social image.
12. Log it in private/ (done automatically) and set a 30-day check-in.
