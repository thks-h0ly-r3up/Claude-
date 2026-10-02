"""Extend the three AI-generated landscape art plates into full portrait art pages for the covers/dividers,
and cut the turquoise-leather corners for the certificate. Run once after the plates are in art/."""
import os
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "art")
W, H = 1700, 2200                       # 8.5 x 11 in at 200 dpi

def mirror_tile(region, w, h):
    rw, rh = region.size
    big = Image.new("RGB", (rw * 2, rh * 2))
    big.paste(region, (0, 0)); big.paste(region.transpose(Image.FLIP_LEFT_RIGHT), (rw, 0))
    big.paste(region.transpose(Image.FLIP_TOP_BOTTOM), (0, rh)); big.paste(region.transpose(Image.ROTATE_180), (rw, rh))
    out = Image.new("RGB", (w, h))
    for x in range(0, w, big.width):
        for y in range(0, h, big.height):
            out.paste(big, (x, y))
    return out

def paper(w, h, mean, seed=7):
    """Seamless-looking cream paper: smooth mottling + fine grain + soft edge darkening (no tiling)."""
    rng = np.random.default_rng(seed)
    def layer(scale, amp):
        small = rng.normal(0, 1, (max(2, h // scale), max(2, w // scale))).astype(np.float32)
        im = Image.fromarray(((small - small.min()) / (np.ptp(small) + 1e-6) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        return (np.asarray(im, dtype=np.float32) / 255 - 0.5) * amp
    n = layer(260, 14) + layer(60, 8) + layer(6, 5)
    yy, xx = np.mgrid[0:h, 0:w]
    vig = 1.03 - 0.03 * (((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    base = np.array(mean, dtype=np.float32)[None, None, :] * vig[..., None] + n[..., None]
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))

def compose(name, strip_src="el1", scale=1.55):
    plate = Image.open(os.path.join(ART, name + ".png")).convert("RGB")
    reg = np.array(plate.crop((340, 535, 1180, 700)))
    mean = tuple(int(v) for v in reg.reshape(-1, 3).mean(axis=0))
    base = paper(W, H, tuple(min(255, int(v * 1.03)) for v in mean))
    # denim strip down the left edge, always cut from the clean denim in plate 1
    sp = Image.open(os.path.join(ART, strip_src + ".png")).convert("RGB")
    sw = int(235 * scale)
    strip = sp.crop((0, 548, 235, 718)).resize((sw, int(170 * scale)), Image.LANCZOS)
    base.paste(mirror_tile(strip, sw, H), (0, 0))
    # plate scaled up, left-anchored, cropped to page width
    pw, ph = int(plate.width * scale), int(plate.height * scale)
    p = plate.resize((pw, ph), Image.LANCZOS).crop((0, 0, W, ph))
    arr = np.full((ph, W), 255, dtype=np.uint8)
    f = 80
    for i in range(f):
        arr[ph - f + i, :] = int(255 * (1 - i / f))
    base.paste(p, (0, 0), Image.fromarray(arr))
    out = os.path.join(ART, name + "_page.jpg")
    base.save(out, quality=90)
    return out

def leather_corner(name):
    """Alpha-cut the turquoise leather wedge from the plate's top-right."""
    im = Image.open(os.path.join(ART, name + ".png")).convert("RGB")
    crop = im.crop((820, 0, 1280, 360))
    hsv = np.array(crop.convert("HSV")).astype(int)
    hue, sat, val = hsv[..., 0] * 360 / 255, hsv[..., 1], hsv[..., 2]
    m = ((hue > 150) & (hue < 215) & (sat > 60) & (val > 40)).astype(np.uint8) * 255
    mask = Image.fromarray(m).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(9)).filter(ImageFilter.GaussianBlur(1.5))
    rgba = crop.convert("RGBA"); rgba.putalpha(mask)
    out = os.path.join(ART, name + "_leather.png")
    rgba.save(out)
    return out

def cert_page():
    """Parchment page framed by stitched denim bands (cut from plate 1)."""
    base = paper(W, H, (238, 226, 198), seed=11)
    sp = Image.open(os.path.join(ART, "el1.png")).convert("RGB")
    sw = 170
    strip = sp.crop((0, 548, 235, 718)).resize((sw, int(170 * sw / 235)), Image.LANCZOS)
    col = mirror_tile(strip, sw, H)
    base.paste(col, (0, 0))
    base.paste(col.transpose(Image.FLIP_LEFT_RIGHT), (W - sw, 0))
    out = os.path.join(ART, "cert_page.jpg")
    base.save(out, quality=90)
    return out

if __name__ == "__main__":
    for n in ("el1", "el2", "el3"):
        print(compose(n), leather_corner(n))
    print(cert_page())

