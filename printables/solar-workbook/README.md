# 7HE H0LY R3UP: The Solar Workbook (Original Lights)

A 91-day, one-page-per-day devotional workbook. Prelude starts Saturday, October 24, 2026; Day 1 is Wednesday, October 28, 2026.
Includes three monthly calendars (every day filled in), 13 week maps, 13 day-by-day step pages, and 91 daily pages.

- `solar-workbook.pdf`: print-ready, US Letter, 132 pages
- `solar-workbook.html`: the same book as HTML
- `data/`: all writing (`weeks.txt`, `days_m1.txt`, `days_m2.txt`, `days_m3.txt`), plain text, easy to edit
- `build.py`: regenerates the HTML and PDF from `data/`

Rebuild: `pip install playwright`, then `python3 build.py` (set `CHROMIUM_PATH` if your Chromium is elsewhere; add `--shots 10,11` to save page PNGs).

## Companion: Original Lights, The Deep Dive
- `original-lights-deep-dive.pdf` / `.html`: canon deep dive, computed sky data (moon, sun, bright star), and a "how to read it" word for each of the 91 days, three days per page, plus essays on trauma, addiction, spiritual warfare, and soul contracts and grief.
- `data/deepdive_days.txt`: the writing. `build_deepdive.py`: the builder (needs `pip install ephem playwright`).
- Optional: add `data/location.txt` (`City, ST | lat | lon | IANA time zone`) to include sunrise, sunset, day length, moonrise, and moonset on each day.
