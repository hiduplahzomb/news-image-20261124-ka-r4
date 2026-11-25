#!/usr/bin/env python3
"""Fresh build: one-page visual newspaper for Tuesday 24 November 2026.

Draws entry.png with Pillow at 2x supersampling, then downscales with
Lanczos to 1024x1024. Fully deterministic: fixed coordinates, fixed
colours, no randomness, no timestamps, no network.

Layout (final 1024 px): navy banner with day + date only; one hero
panel (image left 60%, text right); four panels in a 2x2 grid, each
with its picture on top (~60% of the panel) and headline + one fact
line below. No market numbers anywhere.
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
def scene_court(d, box):
    """Hero art: courtroom columns, golden scales of justice, Myanmar map."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(22, 42, 74))
    d.rectangle([x0, y1 - 90, x1, y1], fill=(30, 55, 96))
    cx = (x0 + x1) // 2
    d.polygon([(x0 + 60, y0 + 150), (x1 - 60, y0 + 150), (cx, y0 + 40)],
              fill=(232, 220, 195))
    d.rectangle([x0 + 60, y0 + 150, x1 - 60, y0 + 178], fill=(232, 220, 195))
    for col_x in (x0 + 90, x1 - 150):
        d.rectangle([col_x, y0 + 190, col_x + 60, y1 - 90], fill=(232, 220, 195))
        d.rectangle([col_x - 12, y0 + 178, col_x + 72, y0 + 196], fill=(210, 196, 168))
        d.rectangle([col_x - 12, y1 - 108, col_x + 72, y1 - 90], fill=(210, 196, 168))
    # Myanmar map silhouette (stylised), kept clear of the right column
    myanmar = [(cx + 260, y0 + 210), (cx + 360, y0 + 250), (cx + 400, y0 + 360),
               (cx + 360, y0 + 480), (cx + 310, y0 + 560), (cx + 230, y0 + 520),
               (cx + 190, y0 + 400), (cx + 210, y0 + 290)]
    d.polygon(myanmar, fill=(46, 90, 136), outline=GOLD, width=6)
    label = "MYANMAR"
    lw = d.textlength(label, font=bold(34))
    d.text((cx + 295 - lw / 2, y0 + 600), label, font=bold(34), fill=(240, 220, 160))
    # scales of justice, gold, centre-left
    sx = cx - 180
    top = y0 + 230
    d.rectangle([sx - 8, top, sx + 8, y1 - 130], fill=GOLD_LIGHT)
    d.ellipse([sx - 22, top - 22, sx + 22, top + 22], fill=GOLD_LIGHT)
    d.rectangle([sx - 260, top + 8, sx + 260, top + 24], fill=GOLD_LIGHT)
    for sign in (-1, 1):
        px = sx + sign * 240
        d.line([(sx + sign * 250, top + 16), (px - 70, y1 - 330)], fill=GOLD_LIGHT, width=5)
        d.line([(sx + sign * 250, top + 16), (px + 70, y1 - 330)], fill=GOLD_LIGHT, width=5)
        d.line([(sx + sign * 250, top + 16), (px, y1 - 330)], fill=GOLD_LIGHT, width=5)
        d.pieslice([px - 85, y1 - 330, px + 85, y1 - 190], 0, 180, fill=GOLD_LIGHT)
        d.rectangle([px - 85, y1 - 330, px + 85, y1 - 318], fill=GOLD_LIGHT)
    d.rectangle([sx - 90, y1 - 150, sx + 90, y1 - 130], fill=GOLD_LIGHT)


def scene_rocket(d, box):
    """Shenzhou-24: rocket lifting off over Earth, starry sky. All coords
    are fractions of the panel's picture box, so nothing can overflow."""
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
    top = fy(box, 0.10)
    body_b = fy(box, 0.66)
    bw = (x1 - x0) * 0.09
    d.polygon([(cx - bw, fy(box, 0.28)), (cx, top), (cx + bw, fy(box, 0.28))],
              fill=(200, 30, 30))
    d.rectangle([cx - bw, fy(box, 0.28), cx + bw, body_b], fill=(245, 245, 245))
    d.rectangle([cx - bw, fy(box, 0.48), cx + bw, fy(box, 0.55)], fill=(200, 30, 30))
    d.ellipse([cx - bw * 0.45, fy(box, 0.33), cx + bw * 0.45, fy(box, 0.44)],
              fill=(120, 200, 235), outline=(10, 30, 60), width=4)
    d.polygon([(cx - bw, body_b - 14), (cx - bw * 1.9, body_b + 12), (cx - bw, body_b)],
              fill=(200, 30, 30))
    d.polygon([(cx + bw, body_b - 14), (cx + bw * 1.9, body_b + 12), (cx + bw, body_b)],
              fill=(200, 30, 30))
    d.polygon([(cx - bw * 0.75, body_b), (cx + bw * 0.75, body_b), (cx, fy(box, 0.94))],
              fill=(255, 140, 0))
    d.polygon([(cx - bw * 0.4, body_b), (cx + bw * 0.4, body_b), (cx, fy(box, 0.82))],
              fill=(255, 220, 80))
    for u, v, r in [(0.24, 0.82, 0.055), (0.76, 0.82, 0.055),
                    (0.17, 0.90, 0.045), (0.83, 0.90, 0.045)]:
        sx, sy = fx(box, u), fy(box, v)
        rr = r * (x1 - x0)
        d.ellipse([sx - rr, sy - rr, sx + rr, sy + rr], fill=(230, 230, 230))


def scene_sea(d, box):
    """Ukraine / Gulf of Finland: ship on a grey-blue Baltic sea."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(176, 205, 225))
    d.polygon([(x0, y0), (fx(box, 0.26), y0), (fx(box, 0.18), fy(box, 0.30)), (x0, fy(box, 0.34))],
              fill=(96, 140, 90))
    d.polygon([(x1, y0), (fx(box, 0.76), y0), (fx(box, 0.83), fy(box, 0.28)), (x1, fy(box, 0.32))],
              fill=(96, 140, 90))
    d.rectangle([x0, fy(box, 0.32), x1, y1], fill=(36, 90, 140))
    for v in (0.48, 0.72, 0.92):
        for u in (0.04, 0.22, 0.40, 0.58, 0.76):
            wx, wy = fx(box, u), fy(box, v)
            d.arc([wx, wy, wx + 0.13 * (x1 - x0), wy + 0.10 * (y1 - y0)],
                  180, 360, fill=(255, 255, 255), width=6)
    cx = fx(box, 0.50)
    hull_y = fy(box, 0.44)
    hull_h = 0.16 * (y1 - y0)
    hw = 0.33 * (x1 - x0)
    d.polygon([(cx - hw, hull_y), (cx + hw, hull_y), (cx + hw * 0.82, hull_y + hull_h),
               (cx - hw * 0.82, hull_y + hull_h)], fill=(20, 30, 46))
    ch = 0.13 * (y1 - y0)
    d.rectangle([cx - hw * 0.78, hull_y - ch, cx - hw * 0.18, hull_y], fill=(255, 213, 0))
    d.rectangle([cx - hw * 0.12, hull_y - ch, cx + hw * 0.48, hull_y], fill=(0, 91, 187))
    d.rectangle([cx + hw * 0.54, hull_y - ch, cx + hw * 0.90, hull_y], fill=(255, 213, 0))
    d.rectangle([cx + hw * 0.60, hull_y - ch * 2.1, cx + hw * 0.90, hull_y - ch],
                fill=(245, 245, 245))
    d.rectangle([cx + hw * 0.65, hull_y - ch * 1.95, cx + hw * 0.85, hull_y - ch * 1.35],
                fill=(120, 200, 235))
    # Ukrainian flag on the mast
    mx = cx - hw * 0.90
    d.line([(mx, hull_y - ch), (mx, hull_y - ch * 2.4)], fill=(20, 30, 46), width=6)
    d.rectangle([mx, hull_y - ch * 2.4, mx + hw * 0.32, hull_y - ch * 1.95], fill=(0, 91, 187))
    d.rectangle([mx, hull_y - ch * 1.95, mx + hw * 0.32, hull_y - ch * 1.5], fill=(255, 213, 0))
    for u, v in [(0.12, 0.10), (0.20, 0.16), (0.84, 0.11)]:
        gx, gy = fx(box, u), fy(box, v)
        d.arc([gx, gy, gx + 34, gy + 20], 180, 360, fill=(40, 40, 40), width=4)
        d.arc([gx + 34, gy, gx + 68, gy + 20], 180, 360, fill=(40, 40, 40), width=4)


def scene_un_ai(d, box):
    """Guterres / AI: UN-blue globe with olive branches beside an AI chip."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 234, 248))
    h = y1 - y0
    cx, cy = fx(box, 0.32), fy(box, 0.52)
    r = 0.30 * h
    for side in (-1, 1):
        bx = cx + side * r * 1.25
        d.arc([bx - 0.09 * h, cy - 0.62 * r, bx + 0.09 * h, cy + 0.62 * r],
              90 if side < 0 else 270, 270 if side < 0 else 90,
              fill=(60, 120, 60), width=7)
        for k in range(4):
            ly = cy - 0.45 * r + k * 0.30 * r
            d.ellipse([bx - 16, ly - 9, bx + 16, ly + 9], fill=(60, 120, 60))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 158, 219))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=5)
    d.ellipse([cx - 0.33 * r, cy - r, cx + 0.33 * r, cy + r],
              outline=(255, 255, 255), width=4)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=4)
    d.line([(cx, cy - r), (cx, cy + r)], fill=(255, 255, 255), width=4)
    d.arc([cx - 0.9 * r, cy - 0.5 * r, cx + 0.9 * r, cy + 0.5 * r],
          200, 340, fill=(255, 255, 255), width=4)
    d.arc([cx - 0.9 * r, cy - 0.5 * r, cx + 0.9 * r, cy + 0.5 * r],
          20, 160, fill=(255, 255, 255), width=4)
    # AI chip, lower right
    c0, c1 = fx(box, 0.60), fx(box, 0.93)
    ct, cb = fy(box, 0.42), fy(box, 0.94)
    d.rectangle([c0, ct, c1, cb], fill=(20, 30, 46))
    for k in range(4):
        px = c0 + (k + 0.5) * (c1 - c0) / 4
        d.line([(px, ct - 16), (px, ct)], fill=(20, 30, 46), width=8)
        d.line([(px, cb), (px, cb + 16)], fill=(20, 30, 46), width=8)
    ai = "AI"
    af = bold(int(0.24 * h))
    aw = d.textlength(ai, font=af)
    d.text(( (c0 + c1 - aw) / 2, (ct + cb) / 2 - af.size * 0.62), ai,
           font=af, fill=(255, 255, 255))


def scene_pacific(d, box):
    """Solomon Islands / Australia: stylised Pacific map, sun, waves."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(158, 205, 225))
    sx, sy = fx(box, 0.88), fy(box, 0.10)
    d.ellipse([sx - 34, sy - 34, sx + 34, sy + 34], fill=(255, 200, 60))
    aus = [(0.06, 0.52), (0.18, 0.44), (0.33, 0.45), (0.43, 0.56),
           (0.40, 0.72), (0.30, 0.84), (0.18, 0.80), (0.08, 0.66)]
    d.polygon([(fx(box, u), fy(box, v)) for u, v in aus],
              fill=(224, 179, 106), outline=(150, 100, 40), width=4)
    d.text((fx(box, 0.13), fy(box, 0.58)), "AUSTRALIA", font=bold(30), fill=(90, 55, 20))
    islands = [(0.52, 0.26), (0.60, 0.19), (0.69, 0.22), (0.77, 0.15),
               (0.85, 0.20), (0.64, 0.34), (0.74, 0.32)]
    for u, v in islands:
        ix, iy = fx(box, u), fy(box, v)
        d.ellipse([ix - 18, iy - 11, ix + 18, iy + 11], fill=(46, 125, 70),
                  outline=(255, 255, 255), width=3)
    d.text((fx(box, 0.56), fy(box, 0.40)), "SOLOMON ISLANDS", font=bold(28),
           fill=(20, 60, 40))
    for k in range(5):
        lx, ly = fx(box, 0.56 - k * 0.03), fy(box, 0.44 + k * 0.045)
        d.ellipse([lx - 5, ly - 5, lx + 5, ly + 5], fill=(20, 60, 40))
    for v in (0.86, 0.94):
        for u in (0.03, 0.21, 0.39, 0.57, 0.75):
            wx, wy = fx(box, u), fy(box, v)
            d.arc([wx, wy, wx + 0.11 * (x1 - x0), wy + 0.09 * (y1 - y0)],
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
    render_scene(img, scene_court, (hx0 + 4, hy0 + 4, hx0 + img_w, hy1 - 4))
    tx = hx0 + img_w + 36
    tw = hx1 - 36 - tx
    d.text((tx, hy0 + 44), "TOP STORY  •  THE HAGUE", font=bold(36), fill=RED)
    fnt, lines = fit_bold(d, "World Court: Myanmar Guilty of Rohingya Genocide",
                          tw, 300, 78)
    y = hy0 + 110
    for ln in lines:
        d.text((tx, y), ln, font=fnt, fill=INK)
        y += int(fnt.size * 1.12)
    sub = ("The International Court of Justice rules Myanmar committed "
           "genocide against the Rohingya; 14 states backed the case.")
    draw_wrapped(d, sub, reg(40), tx, y + 22, tw, 52, SUB)
    d.text((tx, hy1 - 70), "ICJ  •  ROHINGYA  •  14 STATES", font=bold(30), fill=NAVY)

    # --- four small panels, 2 x 2 grid; image top 60%, text below
    panels = [
        ("SHENZHOU-24  •  CHINA", "China Launches Shenzhou-24 Crew to Space",
         "China sends its Shenzhou-24 crew to the Tiangong station.",
         scene_rocket),
        ("UKRAINE  •  GULF OF FINLAND", "Ukraine War Spills Into Gulf of Finland",
         "Finland and Baltic states watch the Gulf shipping lanes.",
         scene_sea),
        ("UNITED NATIONS  •  AI", "Guterres Warns World Must Govern AI",
         "UN chief Guterres urges global rules for artificial intelligence.",
         scene_un_ai),
        ("PACIFIC  •  AUSTRALIA", "Solomon Islands Turns to Australia for Help",
         "The Pacific island nation deepens its ties with Canberra.",
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
        ih = int(gh * 0.60)
        render_scene(img, scene, (px0 + 4, py0 + 4, px1 - 4, py0 + ih))
        ty = py0 + ih + 14
        d.text((px0 + 28, ty), kicker, font=bold(26), fill=RED)
        fnt, lines = fit_bold(d, head, gw - 56, 100, 48)
        y = ty + 42
        for ln in lines:
            d.text((px0 + 28, y), ln, font=fnt, fill=INK)
            y += int(fnt.size * 1.12)
        draw_wrapped(d, sub, reg(30), px0 + 28, y + 6, gw - 56, 38, SUB)

    small = img.resize((1024, 1024), Image.LANCZOS)
    return small


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build().save(out, format="PNG", optimize=True)
    print("wrote", out)
