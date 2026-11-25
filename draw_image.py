#!/usr/bin/env python3
"""Revised build: one-page visual newspaper for Tuesday 24 November 2026.

Round-2 revision. Every story is anchored to 24 November 2026 itself:
the ICJ Rohingya ruling was 19 November (five days stale as a lead),
so the hero is now the Houthi strike on Riyadh's PIF Tower on
24 November (11 injured). The four panels are all 24 November news
too: Zelensky confirms the Sparta II drone strike, a Brooklyn jury
convicts Huawei, China names the Shenzhou-24 crew, and the Solomon
Islands drops its China security pact for Australia.

Draws entry.png with Pillow at 2x supersampling, then downscales with
Lanczos to 1024x1024. Fully deterministic: fixed coordinates, fixed
colours, no randomness, no timestamps, no network.

Layout (final 1024 px): navy banner with day + date only; one hero
panel (image left 60%, text right); four panels in a 2x2 grid, each
with its picture on top (50% of the panel) and kicker + headline +
one concrete fact line below. Kicker >= 16 px final, sub-lines
>= 19 px final, so both stay legible at ~300 px wide.
"""
import os
from PIL import Image, ImageDraw, ImageFont

SS = 2                      # supersampling factor
W, H = 1024 * SS, 1024 * SS
MARGIN = 12 * SS            # outer margin (final 12 px)

PAPER = (246, 241, 231)     # newsprint cream
INK = (17, 24, 39)          # near-black text
NAVY = (10, 30, 60)         # banner navy
GOLD = (201, 162, 39)
GOLD_LIGHT = (212, 160, 23)
RED = (185, 28, 28)
SUB = (51, 51, 51)          # dark grey sub-lines (never light grey)

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FALLBACK_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FALLBACK_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, fallback, size):
    for p in (path, fallback):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def bold(size):
    return font(FONT_BOLD, FALLBACK_BOLD, size)


def reg(size):
    return font(FONT_REG, FALLBACK_REG, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, line_h, color):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += line_h
    return y


def fit_bold(draw, text, max_w, max_h, start_size, min_size=20):
    """Largest bold font (step 2) whose wrap fits max_w x max_h."""
    size = start_size
    while size > min_size:
        fnt = bold(size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) * int(size * 1.12) <= max_h:
            return fnt, lines
        size -= 2
    fnt = bold(min_size)
    return fnt, wrap(draw, text, fnt, max_w)


def fx(box, u):
    """Fraction helpers: map (u, v) in 0..1 across a box to pixels."""
    x0, y0, x1, y1 = box
    return x0 + u * (x1 - x0)


def fy(box, v):
    x0, y0, x1, y1 = box
    return y0 + v * (y1 - y0)


# ---------------------------------------------------------------- scenes
def scene_tower(d, box):
    """Hero art: Riyadh's PIF Tower at night, upper floors on fire
    after the Houthi projectile strike, black smoke, glowing skyline.
    One tall tower fills the frame; nothing near the text edge."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=(11, 19, 36))
    for u, v in [(0.06, 0.08), (0.16, 0.16), (0.28, 0.06), (0.70, 0.10),
                 (0.82, 0.05), (0.92, 0.16), (0.60, 0.04), (0.38, 0.14)]:
        sx, sy = fx(box, u), fy(box, v)
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 255, 255))
    # distant skyline silhouettes along the bottom
    for u, vw, vh in [(0.00, 0.09, 0.16), (0.10, 0.07, 0.24), (0.62, 0.08, 0.20),
                      (0.71, 0.06, 0.28), (0.78, 0.09, 0.15), (0.88, 0.12, 0.22)]:
        bx = fx(box, u)
        bw = vw * w
        d.rectangle([bx, y1 - vh * h, bx + bw, y1], fill=(24, 38, 66))
        for k in range(3):
            wx = bx + bw * (0.25 + 0.25 * k)
            d.rectangle([wx, y1 - vh * h + 12, wx + 8, y1 - vh * h + 26],
                        fill=(255, 210, 110))
    # PIF Tower: tall tapered tower, centre-left
    cx = fx(box, 0.40)
    top = fy(box, 0.05)
    base = y1
    bw_top = 0.075 * w
    bw_base = 0.115 * w
    d.polygon([(cx - bw_top, top), (cx + bw_top, top),
               (cx + bw_base, base), (cx - bw_base, base)],
              fill=(52, 78, 122))
    # lit windows, lower two-thirds only (fire owns the top)
    for r in range(9):
        wy = fy(box, 0.42 + r * 0.06)
        half = bw_top + (bw_base - bw_top) * ((wy - top) / (base - top))
        for k in (-1, 0, 1):
            wx = cx + k * half * 0.55
            d.rectangle([wx - 9, wy, wx + 9, wy + 12], fill=(170, 215, 240))
    # diagonal twist bands on the tower (kept clear of the PIF plaque
    # at 0.46-0.62): one above it, one below it
    for yy in (fy(box, 0.30), fy(box, 0.70)):
        d.polygon([(cx - bw_base * 0.92, yy), (cx + bw_base * 0.92, yy - 34),
                   (cx + bw_base * 0.92, yy - 14), (cx - bw_base * 0.92, yy + 20)],
                  fill=(255, 210, 110))
    # fire: orange glow + flames bursting from the upper floors
    fx0 = fy(box, 0.12)
    d.ellipse([cx - 130, fx0 - 50, cx + 130, fx0 + 110], fill=(255, 90, 0))
    d.polygon([(cx - 150, fy(box, 0.30)), (cx - 90, fy(box, 0.08)),
               (cx - 30, fy(box, 0.24)), (cx + 30, fy(box, 0.06)),
               (cx + 95, fy(box, 0.26)), (cx + 150, fy(box, 0.10)),
               (cx + 130, fy(box, 0.32)), (cx - 130, fy(box, 0.32))],
              fill=(255, 140, 0))
    d.polygon([(cx - 90, fy(box, 0.30)), (cx - 40, fy(box, 0.14)),
               (cx + 10, fy(box, 0.27)), (cx + 60, fy(box, 0.13)),
               (cx + 95, fy(box, 0.30))], fill=(255, 220, 80))
    # black smoke column drifting up-left from the fire
    for u, v, r in [(0.34, 0.10, 52), (0.28, 0.04, 62), (0.20, 0.08, 46),
                    (0.30, 0.16, 40)]:
        sx, sy = fx(box, u), fy(box, v)
        d.ellipse([sx - r, sy - r * 0.7, sx + r, sy + r * 0.7],
                  fill=(35, 35, 40))
    # incoming projectile trail, top right
    d.line([(fx(box, 0.97), fy(box, 0.02)), (fx(box, 0.62), fy(box, 0.13))],
           fill=(255, 255, 255), width=6)
    d.ellipse([fx(box, 0.60) - 14, fy(box, 0.12) - 14,
               fx(box, 0.60) + 14, fy(box, 0.12) + 14], fill=(255, 160, 40))
    # PIF plaque: dark band across the tower so the letters sit on a
    # clean background, clear of windows and twist bands
    pw = bw_top + (bw_base - bw_top) * 0.55
    d.rectangle([cx - pw, fy(box, 0.46), cx + pw, fy(box, 0.62)],
                fill=(10, 22, 44))
    label = "PIF"
    lf = bold(int(0.085 * h))
    lw = d.textlength(label, font=lf)
    d.text((cx - lw / 2, fy(box, 0.49)), label, font=lf, fill=(255, 255, 255))
    # orange ground glow at the tower base
    d.ellipse([cx - 260, y1 - 46, cx + 260, y1 + 30], fill=(255, 110, 20))


def scene_rocket(d, box):
    """Shenzhou-24: big rocket lifting off over Earth, starry sky. All
    coords are fractions of the panel's picture box, so nothing can
    overflow. The rocket is wide and central so it reads at 300 px."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(11, 27, 51))
    for u, v in [(0.07, 0.10), (0.20, 0.22), (0.34, 0.08), (0.48, 0.18),
                 (0.62, 0.10), (0.76, 0.24), (0.88, 0.11), (0.12, 0.42),
                 (0.30, 0.48), (0.70, 0.42), (0.90, 0.48), (0.56, 0.32),
                 (0.04, 0.68), (0.94, 0.68), (0.42, 0.06), (0.82, 0.34)]:
        sx, sy = fx(box, u), fy(box, v)
        d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 255, 255))
    # Earth curve at the bottom of the box
    d.ellipse([fx(box, -0.35), fy(box, 0.72), fx(box, 1.35), fy(box, 2.40)],
              fill=(38, 110, 160))
    d.ellipse([fx(box, 0.12), fy(box, 0.80), fx(box, 0.42), fy(box, 0.95)],
              fill=(70, 160, 110))
    d.ellipse([fx(box, 0.62), fy(box, 0.78), fx(box, 0.90), fy(box, 0.92)],
              fill=(70, 160, 110))
    cx = fx(box, 0.50)
    top = fy(box, 0.06)
    body_b = fy(box, 0.62)
    bw = (x1 - x0) * 0.11
    d.polygon([(cx - bw, fy(box, 0.26)), (cx, top), (cx + bw, fy(box, 0.26))],
              fill=(200, 30, 30))
    d.rectangle([cx - bw, fy(box, 0.26), cx + bw, body_b], fill=(245, 245, 245))
    d.rectangle([cx - bw, fy(box, 0.46), cx + bw, fy(box, 0.54)], fill=(200, 30, 30))
    d.ellipse([cx - bw * 0.45, fy(box, 0.31), cx + bw * 0.45, fy(box, 0.42)],
              fill=(120, 200, 235), outline=(10, 30, 60), width=4)
    d.polygon([(cx - bw, body_b - 14), (cx - bw * 1.9, body_b + 12), (cx - bw, body_b)],
              fill=(200, 30, 30))
    d.polygon([(cx + bw, body_b - 14), (cx + bw * 1.9, body_b + 12), (cx + bw, body_b)],
              fill=(200, 30, 30))
    d.polygon([(cx - bw * 0.75, body_b), (cx + bw * 0.75, body_b), (cx, fy(box, 0.96))],
              fill=(255, 140, 0))
    d.polygon([(cx - bw * 0.4, body_b), (cx + bw * 0.4, body_b), (cx, fy(box, 0.84))],
              fill=(255, 220, 80))
    for u, v, r in [(0.24, 0.82, 0.055), (0.76, 0.82, 0.055),
                    (0.17, 0.90, 0.045), (0.83, 0.90, 0.045)]:
        sx, sy = fx(box, u), fy(box, v)
        rr = r * (x1 - x0)
        d.ellipse([sx - rr, sy - rr, sx + rr, sy + rr], fill=(230, 230, 230))


def scene_sea_burning(d, box):
    """Ukraine / Gulf of Finland: the Russian cargo ship Sparta II
    ablaze after the Ukrainian drone strike, black smoke, a small sea
    drone closing in at lower right. The burning ship fills the frame;
    no flag of the wrong side anywhere on it."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # smoke-grey sky, top strip
    d.rectangle([x0, y0, x1, fy(box, 0.30)], fill=(120, 125, 135))
    d.rectangle([x0, fy(box, 0.30), x1, y1], fill=(28, 78, 128))
    # sea waves
    for v in (0.78, 0.92):
        for u in (0.04, 0.22, 0.40, 0.58, 0.76):
            wx, wy = fx(box, u), fy(box, v)
            d.arc([wx, wy, wx + 0.11 * w, wy + 0.12 * h],
                  180, 360, fill=(255, 255, 255), width=6)
    # hull: wide, dark, red waterline, bow right
    hx0, hx1 = fx(box, 0.06), fx(box, 0.88)
    hull_y = fy(box, 0.52)
    hull_h = 0.20 * h
    d.polygon([(hx0, hull_y), (hx1, hull_y), (hx1 - 0.04 * w, hull_y + hull_h),
               (hx0 + 0.02 * w, hull_y + hull_h)], fill=(18, 28, 44))
    d.rectangle([hx0, hull_y + hull_h - 10, hx1 - 0.02 * w, hull_y + hull_h],
                fill=(185, 28, 28))
    # containers on deck
    cy = hull_y - 0.16 * h
    for u, cw, col in [(0.10, 0.16, (200, 60, 40)), (0.27, 0.15, (40, 110, 180)),
                       (0.43, 0.16, (60, 140, 90))]:
        d.rectangle([fx(box, u), cy, fx(box, u + cw), hull_y], fill=col)
    # bridge tower, starboard side, on fire
    bx0, bx1 = fx(box, 0.62), fx(box, 0.80)
    by0 = fy(box, 0.22)
    d.rectangle([bx0, by0, bx1, hull_y], fill=(235, 235, 230))
    for r in range(3):
        wy = by0 + 14 + r * 0.10 * h
        d.rectangle([bx0 + 12, wy, bx1 - 12, wy + 12], fill=(120, 200, 235))
    # flames bursting from the bridge top
    d.polygon([(bx0 - 30, by0 + 8), (bx0 + 30, by0 - 0.16 * h),
               (bx0 + 80, by0 + 2), (bx0 + 130, by0 - 0.14 * h),
               (bx1 + 40, by0 + 6), (bx1 - 10, by0 + 16), (bx0 - 10, by0 + 16)],
              fill=(255, 140, 0))
    d.polygon([(bx0 + 10, by0 + 6), (bx0 + 50, by0 - 0.09 * h),
               (bx0 + 95, by0 + 4), (bx0 + 60, by0 + 14)],
              fill=(255, 220, 80))
    # thick black smoke above the flames
    for u, v, r in [(0.66, 0.10, 34), (0.72, 0.03, 40), (0.78, 0.09, 30)]:
        sx, sy = fx(box, u), fy(box, v)
        d.ellipse([sx - r, sy - r * 0.6, sx + r, sy + r * 0.6],
                  fill=(30, 30, 35))
    # Russian flag (white-blue-red) on the stern mast, left end
    mx = fx(box, 0.08)
    d.line([(mx, hull_y - 0.16 * h), (mx, hull_y - 0.34 * h)],
           fill=(18, 28, 44), width=5)
    fw = 0.07 * w
    d.rectangle([mx, hull_y - 0.34 * h, mx + fw, hull_y - 0.295 * h],
                fill=(255, 255, 255))
    d.rectangle([mx, hull_y - 0.295 * h, mx + fw, hull_y - 0.25 * h],
                fill=(0, 57, 166))
    d.rectangle([mx, hull_y - 0.25 * h, mx + fw, hull_y - 0.205 * h],
                fill=(213, 0, 50))
    # sea drone: low grey hull + mast, lower right, with wake
    dx0 = fx(box, 0.86)
    dy = fy(box, 0.86)
    d.polygon([(dx0 - 70, dy), (dx0 + 46, dy), (dx0 + 30, dy + 18),
               (dx0 - 56, dy + 18)], fill=(60, 65, 72))
    d.line([(dx0 - 10, dy), (dx0 - 10, dy - 34)], fill=(60, 65, 72), width=5)
    d.ellipse([dx0 - 16, dy - 42, dx0 - 4, dy - 30], fill=(255, 60, 60))
    d.arc([dx0 - 96, dy - 6, dx0 - 40, dy + 22], 180, 360,
          fill=(255, 255, 255), width=5)


def scene_huawei(d, box):
    """US jury convicts Huawei: a courtroom verdict scene — two
    columns, one oversized gold scales of justice in the centre, and a
    red GUILTY band across the bottom. Reads as 'court verdict' at
    300 px."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=(16, 32, 64))
    # courthouse columns at both edges
    for cx in (fx(box, 0.05), fx(box, 0.88)):
        d.rectangle([cx, y0, cx + 0.07 * w, fy(box, 0.78)], fill=(232, 220, 195))
        d.rectangle([cx - 8, fy(box, 0.74), cx + 0.07 * w + 8, fy(box, 0.78)],
                    fill=(210, 196, 168))
    # judge's bench line
    d.rectangle([x0, fy(box, 0.78), x1, y1], fill=(92, 58, 32))
    # oversized scales of justice, centred
    sx = fx(box, 0.50)
    top = fy(box, 0.10)
    d.rectangle([sx - 10, top, sx + 10, fy(box, 0.70)], fill=GOLD_LIGHT)
    d.ellipse([sx - 26, top - 26, sx + 26, top + 26], fill=GOLD_LIGHT)
    d.rectangle([sx - 0.30 * w, top + 8, sx + 0.30 * w, top + 26],
                fill=GOLD_LIGHT)
    for sign in (-1, 1):
        px = sx + sign * 0.27 * w
        d.line([(sx + sign * 0.29 * w, top + 16), (px - 52, fy(box, 0.46))],
               fill=GOLD_LIGHT, width=6)
        d.line([(sx + sign * 0.29 * w, top + 16), (px + 52, fy(box, 0.46))],
               fill=GOLD_LIGHT, width=6)
        d.line([(sx + sign * 0.29 * w, top + 16), (px, fy(box, 0.46))],
               fill=GOLD_LIGHT, width=6)
        d.pieslice([px - 62, fy(box, 0.46), px + 62, fy(box, 0.64)], 0, 180,
                   fill=GOLD_LIGHT)
        d.rectangle([px - 62, fy(box, 0.46), px + 62, fy(box, 0.50)],
                    fill=GOLD_LIGHT)
    d.rectangle([sx - 80, fy(box, 0.70), sx + 80, fy(box, 0.76)],
                fill=GOLD_LIGHT)
    # red GUILTY band across the bottom of the picture
    d.rectangle([x0, fy(box, 0.80), x1, y1], fill=(255, 255, 255))
    word = "GUILTY"
    wf = bold(int(0.16 * h))
    ww = d.textlength(word, font=wf)
    d.text(((x0 + x1 - ww) / 2, fy(box, 0.815)), word, font=wf, fill=RED)


def scene_pacific(d, box):
    """Solomon Islands / Australia: big Pacific map. Australia fills
    the lower left, the Solomon chain sits upper right, a gold arrow
    runs between them. Labels sit clear of every island and the arrow;
    no dotted trail, no sun, nothing collides."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(158, 205, 225))
    # label first, top area, well clear of the islands below it
    d.text((fx(box, 0.50), fy(box, 0.02)), "SOLOMON ISLANDS",
           font=bold(30), fill=(20, 60, 40))
    # Solomon island chain, upper right, large green ellipses
    islands = [(0.56, 0.32), (0.65, 0.26), (0.74, 0.30), (0.83, 0.24),
               (0.90, 0.32), (0.68, 0.42), (0.78, 0.41)]
    for u, v in islands:
        ix, iy = fx(box, u), fy(box, v)
        d.ellipse([ix - 26, iy - 15, ix + 26, iy + 15], fill=(46, 125, 70),
                  outline=(255, 255, 255), width=3)
    # Australia, lower left, large
    aus = [(0.05, 0.56), (0.16, 0.48), (0.31, 0.49), (0.41, 0.60),
           (0.38, 0.76), (0.28, 0.88), (0.16, 0.84), (0.06, 0.70)]
    d.polygon([(fx(box, u), fy(box, v)) for u, v in aus],
              fill=(224, 179, 106), outline=(150, 100, 40), width=4)
    d.text((fx(box, 0.12), fy(box, 0.62)), "AUSTRALIA", font=bold(30),
           fill=(90, 55, 20))
    # gold partnership arrow: Australia -> Solomons, routed between them
    ax0, ay0 = fx(box, 0.42), fy(box, 0.58)
    ax1, ay1 = fx(box, 0.54), fy(box, 0.40)
    d.line([(ax0, ay0), (ax1, ay1)], fill=GOLD, width=14)
    d.polygon([(ax1, ay1 - 22), (ax1 + 26, ay1 + 6), (ax1 - 14, ay1 + 18)],
              fill=GOLD)
    # waves along the bottom
    for v in (0.92,):
        for u in (0.46, 0.64, 0.82):
            wx, wy = fx(box, u), fy(box, v)
            d.arc([wx, wy, wx + 0.11 * (x1 - x0), wy + 0.07 * (y1 - y0)],
                  180, 360, fill=(255, 255, 255), width=5)


def render_scene(img, scene, box):
    """Draw a scene onto its own layer clipped exactly to its box, then
    paste it. This guarantees no scene art can ever bleed into the text
    area or a neighbouring panel."""
    x0, y0, x1, y1 = box
    layer = Image.new("RGB", (x1 - x0, y1 - y0), PAPER)
    ld = ImageDraw.Draw(layer)
    scene(ld, (0, 0, x1 - x0, y1 - y0))
    img.paste(layer, (x0, y0))


# ---------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top banner: single navy band, day + full date only
    d.rectangle([0, 0, W, 208], fill=NAVY)
    d.rectangle([0, 200, W, 208], fill=GOLD)
    banner_font = bold(96)
    banner = "TUESDAY, 24 NOVEMBER 2026"
    bw = d.textlength(banner, font=banner_font)
    d.text(((W - bw) / 2, 52), banner, font=banner_font, fill=(255, 255, 255))

    # --- hero panel (full width): image left 60%, text right 40%
    hx0, hy0, hx1, hy1 = MARGIN, 232, W - MARGIN, 992
    d.rectangle([hx0, hy0, hx1, hy1], fill=(255, 255, 255), outline=INK, width=4)
    img_w = int((hx1 - hx0) * 0.60)
    render_scene(img, scene_tower, (hx0 + 4, hy0 + 4, hx0 + img_w, hy1 - 4))
    tx = hx0 + img_w + 36
    tw = hx1 - 36 - tx
    d.text((tx, hy0 + 44), "TOP STORY  •  RIYADH", font=bold(36), fill=RED)
    fnt, lines = fit_bold(d, "Houthi Missile Hits Riyadh's PIF Tower",
                          tw, 300, 78)
    y = hy0 + 110
    for ln in lines:
        d.text((tx, y), ln, font=fnt, fill=INK)
        y += int(fnt.size * 1.12)
    sub = ("A Houthi projectile strikes Riyadh's 80-storey PIF Tower, "
           "injuring 11 people in a second strike in a week.")
    draw_wrapped(d, sub, reg(40), tx, y + 22, tw, 52, SUB)
    d.text((tx, hy1 - 70), "RIYADH  •  11 INJURED  •  2ND IN A WEEK",
           font=bold(32), fill=NAVY)

    # --- four small panels, 2 x 2 grid; image top 50%, text below
    # kicker 32 (16 px final), sub 38 (19 px final): legible at 300 px.
    panels = [
        ("UKRAINE  •  GULF OF FINLAND", "Ukraine's Drones Set Russian Ship Ablaze",
         "Zelensky confirms Ukrainian drones set Russian ship Sparta II "
         "ablaze; all 16 crew got off.",
         scene_sea_burning),
        ("UNITED STATES  •  HUAWEI", "Huawei Guilty on 10 of 12 Counts",
         "Brooklyn jury convicts Huawei on 10 of 12 counts, including "
         "bank fraud; racketeering cleared.",
         scene_huawei),
        ("SHENZHOU-24  •  CHINA", "China Names First Foreign Astronaut",
         "China names Pakistani pilot Zeeshan Ali as the first foreign "
         "astronaut bound for Tiangong.",
         scene_rocket),
        ("PACIFIC  •  AUSTRALIA", "Solomon Islands Picks Australia",
         "Solomon Islands scraps its 2022 China pact and names Australia "
         "its primary security partner.",
         scene_pacific),
    ]
    gx0, gy0 = MARGIN, 1016
    gw = (W - 2 * MARGIN - 24) // 2
    gh = 504
    for i, (kicker, head, sub, scene) in enumerate(panels):
        px0 = gx0 + (i % 2) * (gw + 24)
        py0 = gy0 + (i // 2) * (gh + 24)
        px1, py1 = px0 + gw, py0 + gh
        d.rectangle([px0, py0, px1, py1], fill=(255, 255, 255), outline=INK, width=4)
        ih = int(gh * 0.50)
        render_scene(img, scene, (px0 + 4, py0 + 4, px1 - 4, py0 + ih))
        ty = py0 + ih + 12
        d.text((px0 + 28, ty), kicker, font=bold(32), fill=RED)
        fnt, lines = fit_bold(d, head, gw - 56, 104, 46)
        y = ty + 38
        for ln in lines:
            d.text((px0 + 28, y), ln, font=fnt, fill=INK)
            y += int(fnt.size * 1.12)
        draw_wrapped(d, sub, reg(38), px0 + 28, y + 4, gw - 56, 42, SUB)

    small = img.resize((1024, 1024), Image.LANCZOS)
    return small


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build().save(out, format="PNG", optimize=True)
    print("wrote", out)
