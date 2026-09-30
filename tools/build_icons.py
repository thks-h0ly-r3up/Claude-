#!/usr/bin/env python3
"""Renders the app icons (sunrise + anchor on night) to public/app/icons/*.png using the kit's vector helpers."""
import io
import os

import pymupdf
from reportlab.pdfgen import canvas

import build_kit as k

OUT = os.path.join(k.ROOT, "public", "app", "icons")


def render(px, name, maskable=False):
    size = 512.0
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(size, size))
    c.setFillColor(k.NIGHT)
    c.rect(0, 0, size, size, stroke=0, fill=1)
    scale = 0.62 if maskable else 0.8  # maskable icons need a larger safe zone
    horizon = size * 0.36
    r = size * 0.24 * scale / 0.8
    k.sunrise(c, size / 2, horizon, r, rays=18, ray_len=size * 0.3 * scale / 0.8)
    c.setFillColor(k.OLIVE)
    c.rect(0, 0, size, horizon - 2, stroke=0, fill=1)
    c.setFillColor(k.ORANGE)
    c.rect(0, horizon - 4, size, 6, stroke=0, fill=1)
    k.anchor(c, size / 2, horizon + r * 0.44, r * 0.8, color=k.NIGHT, lw=size * 0.014)
    c.save()
    doc = pymupdf.open("pdf", buf.getvalue())
    pix = doc[0].get_pixmap(matrix=pymupdf.Matrix(px / size, px / size), alpha=False)
    pix.save(os.path.join(OUT, name))


def main():
    os.makedirs(OUT, exist_ok=True)
    render(192, "icon-192.png")
    render(512, "icon-512.png")
    render(512, "icon-maskable-512.png", maskable=True)
    render(180, "apple-touch-icon.png")
    print("icons written to", OUT)


if __name__ == "__main__":
    main()
