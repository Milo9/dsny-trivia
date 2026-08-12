"""Generate PWA icon PNGs from scratch (no external art assets).

Draws the same gold Mickey-ears silhouette used inline in index.html's
.mickey-svg, on the app's dark navy-to-purple gradient background, at the
sizes a web app manifest / iOS home screen needs. Re-run after any theme
color change:

    python scripts/generate_icons.py

Writes into icons/ at the project root. Requires Pillow (`pip install pillow`).
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, 'icons')

BG_TOP = (6, 6, 20)       # #060614
BG_BOTTOM = (26, 14, 58)  # deep purple, echoes body's gradient
GOLD = (255, 215, 0)


def gradient_bg(size):
    img = Image.new('RGB', (size, size))
    px = img.load()
    for y in range(size):
        t = y / (size - 1)
        r = round(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t)
        g = round(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t)
        b = round(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t)
        for x in range(size):
            px[x, y] = (r, g, b)
    return img


def draw_mickey(draw, cx, cy, head_r, color=GOLD):
    ear_r = head_r * 0.62
    offset = head_r * 0.82
    draw.ellipse([cx - offset - ear_r, cy - offset - ear_r,
                  cx - offset + ear_r, cy - offset + ear_r], fill=color)
    draw.ellipse([cx + offset - ear_r, cy - offset - ear_r,
                  cx + offset + ear_r, cy - offset + ear_r], fill=color)
    draw.ellipse([cx - head_r, cy - head_r, cx + head_r, cy + head_r], fill=color)


def make_icon(size, out_name, maskable=False, rounded=True):
    img = gradient_bg(size)
    draw = ImageDraw.Draw(img)
    cx = size / 2
    cy = size * 0.53
    # Maskable icons need the glyph inside ~80% safe-zone circle; give it
    # more headroom than the "any" variant, which can bleed to the edge.
    head_r = size * (0.20 if maskable else 0.27)
    draw_mickey(draw, cx, cy, head_r)

    if rounded and not maskable:
        mask = Image.new('L', (size, size), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            [0, 0, size, size], radius=round(size * 0.22), fill=255)
        img.putalpha(mask)

    img.save(os.path.join(OUT_DIR, out_name))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    make_icon(16, 'favicon-16.png', rounded=False)
    make_icon(32, 'favicon-32.png', rounded=False)
    make_icon(180, 'apple-touch-icon.png', rounded=False)   # iOS rounds it itself
    make_icon(192, 'icon-192.png')
    make_icon(512, 'icon-512.png')
    make_icon(192, 'icon-192-maskable.png', maskable=True)
    make_icon(512, 'icon-512-maskable.png', maskable=True)
    print(f'Wrote 7 icons to {OUT_DIR}')


if __name__ == '__main__':
    main()
