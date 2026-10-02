"""Page backgrounds for the day pages: cream parchment with a stitched denim band on the binding edge."""
import os
from PIL import Image
import compose_art as c

def make():
    w, h = 1275, 1650
    base = c.paper(w, h, (243, 233, 208), seed=21)
    sp = Image.open(os.path.join(c.ART, "el1.png")).convert("RGB")
    sw = 96
    strip = sp.crop((0, 548, 235, 718)).resize((sw, int(170 * sw / 235)), Image.LANCZOS)
    col = c.mirror_tile(strip, sw, h)
    right = base.copy(); right.paste(col, (0, 0))
    left = base.copy(); left.paste(col.transpose(Image.FLIP_LEFT_RIGHT), (w - sw, 0))
    for n, im in (("bg_right.jpg", right), ("bg_left.jpg", left)):
        im.save(os.path.join(c.ART, n), quality=78)
    print("bg ok")
if __name__ == "__main__":
    make()
