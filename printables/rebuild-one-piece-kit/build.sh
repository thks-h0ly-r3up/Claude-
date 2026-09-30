#!/usr/bin/env bash
# Rebuild HTML + PDF for the Rebuild One Piece kit.
# Requires: python3, Chromium (set CHROME=/path/to/chrome), and fonts_embedded.css (optional).
set -euo pipefail
cd "$(dirname "$0")"
python3 build_kit.py
CHROME="${CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}"
"$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=20000 \
  --print-to-pdf="$PWD/rebuild-one-piece-at-a-time-kit.pdf" \
  "file://$PWD/rebuild-one-piece-at-a-time-kit.html"
echo "PDF written."
