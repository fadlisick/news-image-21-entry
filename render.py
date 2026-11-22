"""Fourth-edition poster: Saturday 21 November 2026 in one image.

Draws a 1024x1024 news poster with Pillow: masthead, UTC ticker,
six-number band, four scenic leads, twelve scene cards, a filled
continent map with labelled pins, an explicit DATE CHECK, a 22-item
ALSO list and a footer dating claim. Deterministic: no randomness,
no timestamps, fixed palette and fonts.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (247, 242, 231)
PAPER2 = (241, 235, 220)
INK = (26, 26, 26)
MUTED = (90, 84, 74)
NAVY = (31, 58, 95)
NAVY_D = (22, 42, 70)
RED = (179, 39, 30)
TEAL = (14, 107, 107)
GOLD = (192, 138, 43)
CREAM = (250, 246, 236)
LINE = (200, 190, 170)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(size, bold=False, serif=False):
    name = "DejaVuSerif-Bold.ttf" if serif else (
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(FD + name, size)


def tw(d, text, f):
    return d.textlength(text, font=f)


def wrap(d, text, f, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(d, trial, f) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def vgrad(d, box, top, bottom):
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    for yy in range(y0, y1):
        t = (yy - y0) / span
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(x0, yy), (x1, yy)], fill=c)


def sky(d, box, day="day"):
    if day == "night":
        vgrad(d, box, (16, 24, 48), (52, 68, 110))
    elif day == "dusk":
        vgrad(d, box, (232, 148, 88), (94, 70, 110))
    elif day == "dawn":
        vgrad(d, box, (250, 214, 150), (150, 178, 205))
    else:
        vgrad(d, box, (168, 205, 232), (226, 238, 244))


def stars(d, box, pts):
    x0, y0, x1, y1 = box
    for fx, fy, r in pts:
        cx, cy = x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 220))


def clouds(d, box, spots, col=(255, 255, 255)):
    x0, y0, x1, y1 = box
    for fx, fy, rw, rh in spots:
        cx, cy = x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)
        d.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=col)


def sun(d, box, fx, fy, r, col=(250, 200, 80)):
    x0, y0, x1, y1 = box
    cx, cy = x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.ellipse([cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3],
              outline=(250, 220, 130), width=2)


def skyline(d, box, base_y, heights, col, win=(250, 220, 130)):
    x0, y0, x1, y1 = box
    n = len(heights)
    bw = (x1 - x0) / n
    gy = y0 + base_y * (y1 - y0)
    for i, hh in enumerate(heights):
        bx0 = x0 + i * bw + 1
        bx1 = x0 + (i + 1) * bw - 1
        top = gy - hh * (y1 - y0)
        d.rectangle([bx0, top, bx1, gy], fill=col)
        for wy in range(int(top) + 4, int(gy) - 3, 9):
            for wx in range(int(bx0) + 3, int(bx1) - 3, 8):
                if (wx + wy) % 17 < 6:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=win)


def sea(d, box, fy, col=(28, 90, 120)):
    x0, y0, x1, y1 = box
    gy = y0 + fy * (y1 - y0)
    d.rectangle([x0, gy, x1, y1], fill=col)
    for k in range(4):
        yy = gy + 5 + k * 6
        d.line([(x0 + 4, yy), (x1 - 4, yy)], fill=(120, 180, 200), width=1)


def mountains(d, box, fy, peaks, col, snow=(245, 245, 240)):
    x0, y0, x1, y1 = box
    gy = y0 + fy * (y1 - y0)
    pts = [(x0, gy)]
    for fx, fh in peaks:
        pts.append((x0 + fx * (x1 - x0), gy - fh * (y1 - y0)))
    pts.append((x1, gy))
    d.polygon(pts, fill=col)
    for fx, fh in peaks:
        px, py = x0 + fx * (x1 - x0), gy - fh * (y1 - y0)
        d.polygon([(px - 8, py + 10), (px, py), (px + 8, py + 10)],
                  fill=snow)


# ---------------------------------------------------------------- scenes
def scene_cop31(d, box):
    sky(d, box, "day")
    sun(d, box, 0.82, 0.22, 11)
    clouds(d, box, [(0.25, 0.18, 16, 6), (0.55, 0.10, 12, 5)])
    x0, y0, x1, y1 = box
    gy = y0 + 0.72 * (y1 - y0)
    d.rectangle([x0, gy, x1, y1], fill=(52, 110, 80))
    d.pieslice([x0 + 0.24 * (x1 - x0), gy - 0.20 * (y1 - y0),
                x0 + 0.76 * (x1 - x0), gy + 0.06 * (y1 - y0)],
               180, 360, fill=(70, 110, 150))
    for i, c in enumerate([(179, 39, 30), (192, 138, 43), (14, 107, 107),
                           (31, 58, 95), (120, 60, 120)]):
        fx = 0.14 + i * 0.18
        px = x0 + fx * (x1 - x0)
        d.line([(px, gy - 26), (px, gy - 8)], fill=INK, width=2)
        d.polygon([(px, gy - 26), (px + 12, gy - 21), (px, gy - 16)],
                  fill=c)
    d.ellipse([x0 + 0.44 * (x1 - x0), gy - 0.34 * (y1 - y0),
               x0 + 0.56 * (x1 - x0), gy - 0.22 * (y1 - y0)],
              fill=(120, 200, 140), outline=(30, 90, 60), width=2)


def scene_denmark(d, box):
    sky(d, box, "dusk")
    sun(d, box, 0.78, 0.30, 10, col=(250, 180, 110))
    x0, y0, x1, y1 = box
    gy = y0 + 0.78 * (y1 - y0)
    d.rectangle([x0, gy, x1, y1], fill=(60, 58, 66))
    for i, (fx, fw, fh) in enumerate([(0.05, 0.20, 0.30), (0.28, 0.22, 0.42),
                                      (0.53, 0.20, 0.34), (0.76, 0.20, 0.46)]):
        bx0 = x0 + fx * (x1 - x0)
        bw = fw * (x1 - x0)
        d.rectangle([bx0, gy - fh * (y1 - y0), bx0 + bw, gy],
                    fill=(48, 40, 52) if i % 2 else (66, 52, 58))
        d.polygon([(bx0, gy - fh * (y1 - y0)),
                   (bx0 + bw / 2, gy - (fh + 0.16) * (y1 - y0)),
                   (bx0 + bw, gy - fh * (y1 - y0))], fill=(30, 26, 34))
    d.rectangle([x0 + 0.60 * (x1 - x0), gy - 0.62 * (y1 - y0),
                 x0 + 0.64 * (x1 - x0), gy], fill=(30, 26, 34))
    d.polygon([(x0 + 0.58 * (x1 - x0), gy - 0.62 * (y1 - y0)),
               (x0 + 0.62 * (x1 - x0), gy - 0.78 * (y1 - y0)),
               (x0 + 0.66 * (x1 - x0), gy - 0.62 * (y1 - y0))],
              fill=(30, 26, 34))
    for fx in (0.18, 0.45, 0.72, 0.92):
        px = x0 + fx * (x1 - x0)
        d.line([(px, gy - 12), (px, gy)], fill=(250, 220, 130), width=2)
        d.ellipse([px - 3, gy - 16, px + 3, gy - 10], fill=(250, 220, 130))


def scene_warsaw(d, box):
    sky(d, box, "dawn")
    clouds(d, box, [(0.30, 0.16, 18, 6), (0.70, 0.26, 14, 5)])
    skyline(d, box, 0.82, [0.30, 0.48, 0.38, 0.62, 0.44, 0.34],
            (52, 60, 78))
    x0, y0, x1, y1 = box
    gy = y0 + 0.82 * (y1 - y0)
    d.rectangle([x0, gy, x1, y1], fill=(70, 76, 88))
    for fx, fy, ang in [(0.30, 0.22, -1), (0.62, 0.34, 1)]:
        cx, cy = x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)
        d.line([(cx - 26 * ang, cy + 8), (cx, cy)], fill=(255, 255, 255),
               width=2)
        d.polygon([(cx, cy - 5), (cx + 16 * ang, cy + 2), (cx, cy + 5)],
                  fill=(40, 40, 48))
        d.polygon([(cx - 2, cy), (cx - 10 * ang, cy - 7),
                   (cx - 10 * ang, cy + 7)], fill=(90, 90, 100))


def scene_riyadh(d, box):
    sky(d, box, "night")
    stars(d, box, [(0.12, 0.12, 2), (0.30, 0.08, 1), (0.55, 0.14, 2),
                   (0.78, 0.10, 1), (0.90, 0.22, 2), (0.45, 0.06, 1)])
    x0, y0, x1, y1 = box
    gy = y0 + 0.80 * (y1 - y0)
    d.rectangle([x0, gy, x1, y1], fill=(24, 22, 30))
    d.rectangle([x0 + 0.42 * (x1 - x0), gy - 0.55 * (y1 - y0),
                 x0 + 0.58 * (x1 - x0), gy], fill=(48, 44, 66))
    d.ellipse([x0 + 0.42 * (x1 - x0), gy - 0.62 * (y1 - y0),
               x0 + 0.58 * (x1 - x0), gy - 0.42 * (y1 - y0)],
              outline=(250, 220, 130), width=3)
    for fx, fh in [(0.10, 0.28), (0.24, 0.38), (0.70, 0.34), (0.86, 0.26)]:
        bx = x0 + fx * (x1 - x0)
        d.rectangle([bx, gy - fh * (y1 - y0), bx + 0.08 * (x1 - x0), gy],
                    fill=(44, 40, 60))
    for fx, fy in [(0.18, 0.30), (0.55, 0.18), (0.82, 0.38)]:
        sx, sy = x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)
        d.line([(sx - 26, sy + 22), (sx + 26, sy - 22)],
               fill=(255, 190, 90), width=3)
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 240, 180))
        d.ellipse([sx + 18, sy - 16, sx + 24, sy - 10],
                  fill=(255, 160, 60))


def scene_mercury(d, box):
    vgrad(d, box, (8, 8, 18), (30, 26, 52))
    stars(d, box, [(0.10, 0.15, 2), (0.22, 0.08, 1), (0.15, 0.45, 1),
                   (0.88, 0.12, 2), (0.80, 0.55, 1), (0.55, 0.08, 1)])
    x0, y0, x1, y1 = box
    cx, cy = x0 + 0.62 * (x1 - x0), y0 + 0.55 * (y1 - y0)
    r = 0.34 * min(x1 - x0, y1 - y0)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 158, 148))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 112, 104),
              width=2)
    for fx, fy, cr in [(0.55, 0.45, 0.10), (0.70, 0.62, 0.08),
                       (0.60, 0.68, 0.06), (0.72, 0.42, 0.05)]:
        px, py = x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)
        rr = cr * min(x1 - x0, y1 - y0)
        d.ellipse([px - rr, py - rr, px + rr, py + rr],
                  fill=(140, 130, 120))
    sx, sy = x0 + 0.30 * (x1 - x0), y0 + 0.30 * (y1 - y0)
    d.rectangle([sx - 8, sy - 5, sx + 8, sy + 5], fill=(220, 220, 230))
    d.rectangle([sx - 20, sy - 2, sx - 8, sy + 2], fill=(90, 110, 180))
    d.rectangle([sx + 8, sy - 2, sx + 20, sy + 2], fill=(90, 110, 180))
    d.line([(sx - 14, sy + 12), (sx, sy + 5)], fill=(250, 200, 90), width=2)


def scene_cyclone(d, box):
    sky(d, box, "day")
    clouds(d, box, [(0.20, 0.14, 14, 5), (0.75, 0.10, 12, 4)],
           col=(235, 235, 240))
    sea(d, box, 0.72)
    x0, y0, x1, y1 = box
    cx, cy = x0 + 0.50 * (x1 - x0), y0 + 0.42 * (y1 - y0)
    for k, rr in enumerate([34, 26, 18, 10]):
        d.arc([cx - rr, cy - rr * 0.8, cx + rr, cy + rr * 0.8],
              200 + k * 40, 200 + k * 40 + 220, fill=(255, 255, 255),
              width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))
    for fx in (0.15, 0.35, 0.65, 0.85):
        px = x0 + fx * (x1 - x0)
        d.line([(px, y0 + 0.55 * (y1 - y0)), (px - 3, y0 + 0.68 * (y1 - y0))],
               fill=(200, 220, 235), width=1)


def scene_quake(d, box):
    sky(d, box, "dawn")
    mountains(d, box, 0.80, [(0.20, 0.42), (0.48, 0.58), (0.78, 0.40)],
              (96, 84, 96))
    x0, y0, x1, y1 = box
    gy = y0 + 0.80 * (y1 - y0)
    d.rectangle([x0, gy, x1, y1], fill=(120, 100, 78))
    cx = x0 + 0.50 * (x1 - x0)
    d.line([(cx, gy), (cx + 8, gy + 8), (cx - 4, gy + 14), (cx + 6, gy + 20)],
           fill=(60, 48, 36), width=3)
    for fx, fh in [(0.15, 0.18), (0.32, 0.24), (0.68, 0.20), (0.85, 0.15)]:
        bx = x0 + fx * (x1 - x0)
        d.rectangle([bx, gy - fh * (y1 - y0), bx + 0.09 * (x1 - x0), gy],
                    fill=(70, 60, 52))
        d.polygon([(bx, gy - fh * (y1 - y0)),
                   (bx + 0.045 * (x1 - x0), gy - (fh + 0.08) * (y1 - y0)),
                   (bx + 0.09 * (x1 - x0), gy - fh * (y1 - y0))],
                  fill=(52, 44, 40))


def scene_ufo(d, box):
    sky(d, box, "night")
    stars(d, box, [(0.10, 0.12, 2), (0.28, 0.20, 1), (0.70, 0.10, 2),
                   (0.88, 0.28, 1), (0.45, 0.08, 1), (0.60, 0.30, 1)])
    x0, y0, x1, y1 = box
    cx, cy = x0 + 0.50 * (x1 - x0), y0 + 0.38 * (y1 - y0)
    d.polygon([(cx - 34, cy + 26), (cx - 8, cy), (cx + 8, cy),
               (cx + 34, cy + 26)], fill=(250, 230, 140))
    d.ellipse([cx - 34, cy - 8, cx + 34, cy + 8], fill=(200, 205, 215))
    d.ellipse([cx - 16, cy - 14, cx + 16, cy - 2], fill=(120, 130, 150))
    for fx in (0.30, 0.50, 0.70):
        px = x0 + fx * (x1 - x0)
        d.ellipse([px - 3, cy - 4, px + 3, cy + 2], fill=(255, 200, 80))
    d.polygon([(x0 + 0.15 * (x1 - x0), y1), (x0 + 0.35 * (x1 - x0), y1),
               (cx, cy + 26)], fill=(60, 70, 90))
    d.rectangle([x0, y0 + 0.88 * (y1 - y0), x1, y1], fill=(20, 26, 34))


def scene_scales(d, box):
    vgrad(d, box, (226, 220, 205), (200, 190, 170))
    x0, y0, x1, y1 = box
    cx = x0 + 0.50 * (x1 - x0)
    top = y0 + 0.18 * (y1 - y0)
    base = y0 + 0.82 * (y1 - y0)
    d.rectangle([cx - 3, top, cx + 3, base], fill=(60, 52, 44))
    d.polygon([(cx - 12, top), (cx + 12, top), (cx, top - 10)],
              fill=(192, 138, 43))
    d.rectangle([cx - 22, base, cx + 22, base + 5], fill=(60, 52, 44))
    for sgn in (-1, 1):
        ax = cx + sgn * 0.28 * (x1 - x0)
        ay = top + 0.22 * (y1 - y0)
        d.line([(cx, top + 6), (ax, ay)], fill=(60, 52, 44), width=2)
        d.line([(ax, ay), (ax, ay + 12)], fill=(60, 52, 44), width=2)
        d.pieslice([ax - 14, ay + 10, ax + 14, ay + 22], 0, 180,
                   fill=(192, 138, 43))
    for fx in (0.08, 0.92):
        px = x0 + fx * (x1 - x0)
        d.rectangle([px, base - 0.34 * (y1 - y0), px + 6, base],
                    fill=(90, 84, 74))


def scene_nepal(d, box):
    sky(d, box, "day")
    sun(d, box, 0.80, 0.20, 10)
    mountains(d, box, 0.82, [(0.18, 0.50), (0.45, 0.68), (0.72, 0.46),
                             (0.92, 0.34)], (88, 96, 118))
    x0, y0, x1, y1 = box
    gy = y0 + 0.82 * (y1 - y0)
    d.rectangle([x0, gy, x1, y1], fill=(52, 96, 62))
    d.line([(x0 + 6, y0 + 0.30 * (y1 - y0)),
            (x1 - 6, y0 + 0.22 * (y1 - y0))], fill=(60, 52, 44), width=1)
    for i, c in enumerate([(179, 39, 30), (250, 200, 80), (14, 107, 107),
                           (192, 138, 43), (120, 60, 120)]):
        fx = 0.12 + i * 0.17
        px = x0 + fx * (x1 - x0)
        py = y0 + (0.30 - i * 0.016) * (y1 - y0)
        d.polygon([(px, py), (px + 9, py - 1), (px + 4, py + 10)], fill=c)


def scene_anc(d, box):
    vgrad(d, box, (250, 230, 150), (232, 196, 110))
    x0, y0, x1, y1 = box
    cx, cy = x0 + 0.50 * (x1 - x0), y0 + 0.52 * (y1 - y0)
    d.rectangle([cx - 26, cy - 14, cx + 26, cy + 20], fill=(31, 58, 95))
    d.rectangle([cx - 30, cy - 20, cx + 30, cy - 12], fill=(22, 42, 70))
    d.rectangle([cx - 12, cy - 20, cx + 12, cy - 12], fill=(26, 26, 26))
    d.rectangle([cx - 8, cy - 34, cx + 12, cy - 18], fill=(250, 246, 236),
                outline=(26, 26, 26), width=1)
    d.line([(cx - 5, cy - 26), (cx, cy - 21), (cx + 9, cy - 31)],
           fill=(179, 39, 30), width=3)
    for fx, fy in [(0.18, 0.72), (0.34, 0.78), (0.68, 0.76), (0.84, 0.70)]:
        px, py = x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(120, 80, 40))
        d.ellipse([px - 5, py - 12, px + 5, py - 2], fill=(200, 160, 110))


def scene_mongolia(d, box):
    sky(d, box, "dawn")
    sun(d, box, 0.78, 0.24, 11)
    x0, y0, x1, y1 = box
    gy = y0 + 0.66 * (y1 - y0)
    d.polygon([(x0, gy), (x1, gy), (x1, y1), (x0, y1)], fill=(96, 140, 70))
    d.polygon([(x0, gy), (x0 + 0.5 * (x1 - x0), gy - 0.10 * (y1 - y0)),
               (x1, gy)], fill=(120, 160, 84))
    cx, cy = x0 + 0.50 * (x1 - x0), gy + 0.10 * (y1 - y0)
    d.pieslice([cx - 26, cy - 16, cx + 26, cy + 16], 180, 360,
               fill=(232, 220, 190), outline=(120, 90, 50), width=2)
    d.rectangle([cx - 26, cy - 2, cx + 26, cy + 16], fill=(240, 230, 200),
                outline=(120, 90, 50), width=2)
    d.line([(cx, cy - 16), (cx, cy - 2)], fill=(120, 90, 50), width=2)
    d.rectangle([cx - 4, cy + 2, cx + 4, cy + 16], fill=(120, 90, 50))


def scene_vaccine(d, box):
    vgrad(d, box, (226, 240, 240), (190, 215, 220))
    x0, y0, x1, y1 = box
    cx, cy = x0 + 0.42 * (x1 - x0), y0 + 0.55 * (y1 - y0)
    d.rectangle([cx - 14, cy - 22, cx + 14, cy + 18], fill=(250, 250, 250),
                outline=(90, 110, 120), width=2)
    d.rectangle([cx - 8, cy - 30, cx + 8, cy - 22], fill=(120, 140, 150))
    d.rectangle([cx - 14, cy - 6, cx + 14, cy + 18], fill=(90, 170, 200))
    d.line([(cx - 14, cy + 2), (cx + 14, cy + 2)], fill=(255, 255, 255),
           width=1)
    d.line([(cx + 26, cy - 28), (cx + 40, cy - 14)], fill=(150, 150, 150),
           width=4)
    d.polygon([(cx + 40, cy - 14), (cx + 52, cy - 2), (cx + 44, cy + 4),
               (cx + 34, cy - 6)], fill=(220, 220, 225))
    d.line([(cx + 52, cy - 2), (cx + 60, cy + 6)], fill=(150, 150, 150),
           width=2)
    d.rectangle([cx - 30, cy - 34, cx - 18, cy - 22], fill=(179, 39, 30))
    d.rectangle([cx - 26, cy - 38, cx - 22, cy - 18], fill=(179, 39, 30))


def scene_iran_cost(d, box):
    vgrad(d, box, (250, 238, 200), (232, 205, 140))
    x0, y0, x1, y1 = box
    gy = y0 + 0.82 * (y1 - y0)
    d.rectangle([x0, gy, x1, y1], fill=(120, 90, 40))
    for i, h in enumerate([0.18, 0.30, 0.24, 0.44, 0.36]):
        bx = x0 + (0.10 + i * 0.17) * (x1 - x0)
        bw = 0.11 * (x1 - x0)
        d.rectangle([bx, gy - h * (y1 - y0), bx + bw, gy],
                    fill=(31, 58, 95) if i % 2 else (179, 39, 30))
    for i in range(3):
        cx = x0 + (0.72 + i * 0.02) * (x1 - x0)
        cy = gy - 0.52 * (y1 - y0) - i * 4
        d.ellipse([cx - 14, cy - 4, cx + 14, cy + 4], fill=(250, 200, 80),
                  outline=(160, 120, 40), width=1)
    d.text((x0 + 0.10 * (x1 - x0), y0 + 0.10 * (y1 - y0)), "$",
           font=font(20, bold=True), fill=(120, 90, 20))


def scene_oil(d, box):
    sky(d, box, "dusk")
    sun(d, box, 0.80, 0.26, 10, col=(250, 180, 110))
    sea(d, box, 0.68, col=(40, 70, 100))
    x0, y0, x1, y1 = box
    gy = y0 + 0.68 * (y1 - y0)
    d.polygon([(x0 + 0.12 * (x1 - x0), gy),
               (x0 + 0.20 * (x1 - x0), gy - 0.22 * (y1 - y0)),
               (x0 + 0.82 * (x1 - x0), gy - 0.22 * (y1 - y0)),
               (x0 + 0.88 * (x1 - x0), gy)], fill=(30, 32, 40))
    d.rectangle([x0 + 0.68 * (x1 - x0), gy - 0.34 * (y1 - y0),
                 x0 + 0.80 * (x1 - x0), gy - 0.22 * (y1 - y0)],
                fill=(200, 200, 205))
    for fx in (0.30, 0.45, 0.60):
        px = x0 + fx * (x1 - x0)
        d.ellipse([px - 7, gy - 0.16 * (y1 - y0), px + 7,
                   gy - 0.02 * (y1 - y0)], fill=(250, 200, 80),
                  outline=(160, 120, 40), width=1)


def scene_kenya(d, box):
    vgrad(d, box, (232, 224, 205), (205, 192, 165))
    x0, y0, x1, y1 = box
    cx, cy = x0 + 0.50 * (x1 - x0), y0 + 0.46 * (y1 - y0)
    d.rectangle([cx - 30, cy - 12, cx + 30, cy + 2], fill=(120, 82, 40),
                outline=(70, 48, 22), width=2)
    d.line([(cx - 26, cy + 18), (cx + 34, cy - 30)], fill=(90, 64, 32),
           width=6)
    d.rectangle([cx + 22, cy - 40, cx + 46, cy - 18], fill=(140, 98, 48),
                outline=(70, 48, 22), width=2)
    d.ellipse([cx - 22, cy + 14, cx + 22, cy + 24], fill=(90, 64, 32))
    for fx in (0.10, 0.90):
        px = x0 + fx * (x1 - x0)
        d.rectangle([px, y0 + 0.86 * (y1 - y0), px + 5,
                     y0 + 0.92 * (y1 - y0)], fill=(90, 84, 74))


SCENES = {
    "cop31": scene_cop31, "denmark": scene_denmark,
    "warsaw": scene_warsaw, "riyadh": scene_riyadh,
    "mercury": scene_mercury, "cyclone": scene_cyclone,
    "quake": scene_quake, "ufo": scene_ufo,
    "scales": scene_scales, "nepal": scene_nepal,
    "anc": scene_anc, "mongolia": scene_mongolia,
    "vaccine": scene_vaccine, "iran_cost": scene_iran_cost,
    "oil": scene_oil, "kenya": scene_kenya,
}


# ---------------------------------------------------------------- content
LEADS = [
    {"kicker": "CLIMATE  |  ANTALYA", "scene": "cop31", "src": "Reuters",
     "head": "COP31 deadlocks on fossil fuels as talks run over",
     "sub": "Negotiators extend the conference past its deadline "
            "with the phase-out text still bracketed."},
    {"kicker": "SECURITY  |  COPENHAGEN", "scene": "denmark", "src": "AP",
     "head": "Denmark police foil terror plot, arrests at dawn",
     "sub": "Raids across the capital break up a planned attack; "
            "officers say the threat was imminent."},
    {"kicker": "EUROPE  |  WARSAW", "scene": "warsaw", "src": "Reuters",
     "head": "Rutte flies to Warsaw as NATO jets watch Poland's skies",
     "sub": "A day after Russian missiles fell in Poland, the NATO "
            "chief lands to stand with Warsaw."},
    {"kicker": "MIDDLE EAST  |  RIYADH", "scene": "riyadh", "src": "Reuters",
     "head": "Riyadh's skies light up as three Houthi missiles fall",
     "sub": "Saudi air defences destroy three ballistic missiles aimed "
            "at the capital on the third night of alerts."},
]

CARDS = [
    ("BepiColombo reaches Mercury",
     "Eight-year odyssey ends as the burn begins 18:24 GMT", "ESA",
     "mercury"),
    ("Cyclone Akvan drives 372,000 to shelter",
     "Coastal districts empty as the storm makes landfall", "AP",
     "cyclone"),
    ("Peru shakes at 6.9",
     "Andean quake felt in Lima; no casualties at first", "IGP Peru",
     "quake"),
    ("US releases UFO footage",
     "Newly declassified video fuels a day of debate", "AP", "ufo"),
    ("Sikh murder-plot sentence: 19 years",
     "Court jails the plotters behind the case", "BBC", "scales"),
    ("Nepal turns to Balendra Shah",
     "The new leader takes charge after weeks of upheaval", "Reuters",
     "nepal"),
    ("ANC falls to 31%",
     "Worst result since 1994 shakes South Africa", "Reuters", "anc"),
    ("Mongolia's president resigns",
     "Steppe politics in turmoil as the leader steps down", "AP",
     "mongolia"),
    ("India clears H3N1 vaccine",
     "First shots against the new flu strain get the go-ahead", "Reuters",
     "vaccine"),
    ("America's Iran war bill: $48.3bn",
     "The cost of the campaign, counted in full", "AP", "iran_cost"),
    ("8m barrels of Saudi oil for Japan",
     "Tokyo locks in supply as Gulf tensions climb", "Reuters", "oil"),
    ("Kenya cult leader jailed 200 years",
     "The doomsday preacher's sentence closes a grim trial", "BBC",
     "kenya"),
]

ALSO = [
    "South Africa holds its rate at 7.25% (Reuters)",
    "Two tankers struck near Oman in the Hormuz Strait (AP)",
    "Iran downs a US MQ-9 drone over Hormuz (Reuters)",
    "Hartha power-plant fire kills four, hurts 30 in Iraq (AP)",
    "Brazil supercell storm kills three, wrecks 5,000 homes (Reuters)",
    "Indonesia quake 7.2; no tsunami warning issued (Reuters)",
    "Australia and Philippines sign defence pact (AP)",
    "London and Brussels strike biggest deal since Brexit (Reuters)",
    "FBI and US agriculture dept hacked (AP)",
    "Gaza aid-vehicle strike kills three (Reuters)",
    "Russian strikes on Kryvyi Rih kill two, injure 83 (AP)",
    "Sudan rebels seize Bau district in Blue Nile (Reuters)",
    "Salvadoran troops retake Port-au-Prince stadium (AP)",
    "Bahrain warns residents of a potential threat (Reuters)",
    "French cost-of-living protests enter a sixth Saturday (AP)",
    "Blasts reported near Russia's Baltic Fleet base (Reuters)",
    "UN: Saudi strikes on Hodeidah threaten aid lifeline (UN)",
    "Houthis claim 71 Saudi raids across eight provinces (AP)",
    "Iraq opens Jurf al-Nasr-Karbala road (Reuters)",
    "Three militants killed in Pakistan operation (AP)",
    "Seven killed in Gaza strikes despite ceasefire (Reuters)",
    "Russian drone hits Kharkiv region, 11 hurt (AP)",
]

NUMBERS = [
    ("3", "Houthi missiles intercepted over Riyadh"),
    ("372,000", "people moved to shelter from Cyclone Akvan"),
    ("6.9", "magnitude of the Peru quake"),
    ("$48.3bn", "counted cost of the US Iran war"),
    ("8m", "barrels of Saudi oil bound for Japan"),
    ("31%", "ANC vote share, worst since 1994"),
]

TICKER = ("02:30 UTC  Riyadh intercepts  •  10:15 UTC  Peru quake 6.9  •  "
          "18:24 GMT  BepiColombo burn begins  •  19:24 CET  Mercury capture")

DATE_CHECK = [
    "DATE CHECK  —  Friday is not Saturday.",
    "FRIDAY 20 NOV:  Russian missiles fell in Poland  •  Anthropic filed "
    "an $81.3bn IPO  •  Saudi jets hit Hodeidah port.",
    "SATURDAY 21 NOV:  Rutte flies to Warsaw  •  Riyadh intercepts three "
    "missiles  •  BepiColombo burns for Mercury at 18:24 GMT.",
]

FOOTER = ("Every story here happened, or was first reported, on Saturday "
          "21 November 2026 in at least one time zone.  Sources: Reuters, "
          "AP, BBC, ESA, Nature, IGP Peru.  Fourth edition — 38 stories.")

CONTINENTS = [
    [(0.03, 0.34), (0.08, 0.26), (0.16, 0.28), (0.22, 0.34), (0.20, 0.48),
     (0.12, 0.56), (0.05, 0.48)],
    [(0.24, 0.24), (0.27, 0.22), (0.29, 0.28), (0.25, 0.32)],
    [(0.24, 0.60), (0.28, 0.58), (0.31, 0.68), (0.29, 0.88), (0.26, 0.82)],
    [(0.46, 0.46), (0.53, 0.42), (0.58, 0.50), (0.56, 0.74), (0.51, 0.84),
     (0.47, 0.64)],
    [(0.54, 0.30), (0.72, 0.24), (0.90, 0.28), (0.94, 0.44), (0.86, 0.54),
     (0.72, 0.52), (0.60, 0.46), (0.54, 0.40)],
    [(0.82, 0.72), (0.89, 0.70), (0.93, 0.78), (0.88, 0.86), (0.82, 0.80)],
]

# name, fx, fy, label dx, label dy (px from the dot)
PINS = [
    ("WARSAW", 0.550, 0.28, -56, -14),
    ("KYIV", 0.615, 0.30, 8, -14),
    ("ANTALYA", 0.575, 0.40, -60, 4),
    ("RIYADH", 0.630, 0.52, 8, 2),
    ("LIMA", 0.265, 0.74, -10, 8),
    ("KATHMANDU", 0.740, 0.44, 8, -14),
]


# ---------------------------------------------------------------- layout
def draw_masthead(d):
    d.rectangle([0, 0, W, 68], fill=NAVY)
    d.rectangle([0, 68, W, 70], fill=RED)
    d.text((14, 8), "THE WORLD IN ONE IMAGE",
           font=font(29, serif=True), fill=CREAM)
    d.text((14, 44), "Thirty-eight stories from one Saturday, drawn in "
                     "a single frame",
           font=font(11), fill=(200, 210, 225))
    r1 = "SATURDAY  21  NOVEMBER  2026"
    d.text((W - 14 - tw(d, r1, font(13, bold=True)), 10), r1,
           font=font(13, bold=True), fill=(250, 200, 90))
    r2 = "FOURTH EDITION  •  38 STORIES"
    d.text((W - 14 - tw(d, r2, font(10, bold=True)), 34), r2,
           font=font(10, bold=True), fill=(200, 210, 225))


def draw_ticker(d, y):
    d.rectangle([0, y, W, y + 20], fill=INK)
    f = font(11, bold=True)
    t = tw(d, TICKER, f)
    d.text(((W - t) / 2, y + 4), TICKER, font=f, fill=(250, 240, 210))


def draw_numbers(d, y):
    cell = 1000 / 6
    for i, (val, lab) in enumerate(NUMBERS):
        cx = 12 + i * cell
        d.text((cx + 8, y + 4), val, font=font(20, bold=True),
               fill=RED if i % 2 == 0 else NAVY)
        for j, ln in enumerate(wrap(d, lab, font(9), cell - 16)):
            d.text((cx + 8, y + 28 + j * 10), ln, font=font(9), fill=MUTED)
        if i:
            d.line([(cx, y + 4), (cx, y + 46)], fill=LINE, width=1)


def draw_leads(d, y):
    cw, ch, gap = 496, 158, 8
    for idx, lead in enumerate(LEADS):
        row, col = divmod(idx, 2)
        x = 12 + col * (cw + gap)
        yy = y + row * (ch + 6)
        d.rectangle([x, yy, x + cw, yy + ch], fill=CREAM,
                    outline=LINE, width=1)
        SCENES[lead["scene"]](d, (x + 1, yy + 1, x + 201, yy + ch - 1))
        tx = x + 212
        d.text((tx, yy + 8), lead["kicker"], font=font(10, bold=True),
               fill=RED)
        hl = wrap(d, lead["head"], font(16, bold=True), cw - 224)
        for j, ln in enumerate(hl[:3]):
            d.text((tx, yy + 26 + j * 19), ln, font=font(16, bold=True),
                   fill=INK)
        sub = wrap(d, lead["sub"], font(11), cw - 224)
        for j, ln in enumerate(sub[:3]):
            d.text((tx, yy + 26 + len(hl[:3]) * 19 + j * 14), ln,
                   font=font(11), fill=MUTED)
        tag = "(" + lead["src"] + ")"
        d.text((x + cw - 8 - tw(d, tag, font(9, bold=True)), yy + ch - 18),
               tag, font=font(9, bold=True), fill=NAVY)


def draw_field_band(d, y):
    d.rectangle([0, y, W, y + 18], fill=PAPER2)
    d.line([(0, y), (W, y)], fill=LINE, width=1)
    d.line([(0, y + 18), (W, y + 18)], fill=LINE, width=1)
    txt = ("CONFLICT   •   CLIMATE   •   SPACE   •   POLITICS   •   "
           "SCIENCE   •   MARKETS   •   DISASTERS   •   JUSTICE")
    f = font(10, bold=True)
    d.text(((W - tw(d, txt, f)) / 2, y + 3), txt, font=f, fill=NAVY)


def draw_cards(d, y):
    cw, ch, gap = 244, 80, 8
    for idx, (head, sub, src, scene) in enumerate(CARDS):
        row, col = divmod(idx, 4)
        x = 12 + col * (cw + gap)
        yy = y + row * (ch + 6)
        d.rectangle([x, yy, x + cw, yy + ch], fill=CREAM,
                    outline=LINE, width=1)
        SCENES[scene](d, (x + 1, yy + 1, x + 77, yy + ch - 1))
        tx = x + 84
        hl = wrap(d, head, font(11, bold=True), cw - 92)
        for j, ln in enumerate(hl[:2]):
            d.text((tx, yy + 6 + j * 13), ln, font=font(11, bold=True),
                   fill=INK)
        sb = wrap(d, sub, font(9), cw - 92)
        for j, ln in enumerate(sb[:2]):
            d.text((tx, yy + 6 + len(hl[:2]) * 13 + j * 11), ln,
                   font=font(9), fill=MUTED)
        tag = "(" + src + ")"
        d.text((x + cw - 6 - tw(d, tag, font(8, bold=True)), yy + ch - 13),
               tag, font=font(8, bold=True), fill=NAVY)


def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(208, 224, 232), outline=LINE,
                width=1)
    d.text((x0 + 8, y0 + 5), "WHERE IT HAPPENED", font=font(10, bold=True),
           fill=NAVY)
    for poly in CONTINENTS:
        pts = [(x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)) for fx, fy in poly]
        d.polygon(pts, fill=(44, 110, 90), outline=(30, 80, 64))
    f = font(9, bold=True)
    for name, fx, fy, dx, dy in PINS:
        px, py = x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED,
                  outline=(255, 255, 255), width=1)
        lx = min(max(px + dx, x0 + 4), x1 - tw(d, name, f) - 4)
        ly = min(max(py + dy, y0 + 14), y1 - 12)
        d.text((lx + 1, ly + 1), name, font=f, fill=(255, 255, 255))
        d.text((lx, ly), name, font=f, fill=INK)


def draw_datecheck(d, box):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=PAPER2, outline=LINE, width=1)
    d.rectangle([x0, y0, x0 + 5, y1], fill=RED)
    d.text((x0 + 12, y0 + 6), DATE_CHECK[0], font=font(11, bold=True),
           fill=RED)
    yy = y0 + 24
    for ln in DATE_CHECK[1:]:
        for j, wln in enumerate(wrap(d, ln, font(10), (x1 - x0) - 22)):
            d.text((x0 + 12, yy + j * 13), wln, font=font(10), fill=INK)
        yy += len(wrap(d, ln, font(10), (x1 - x0) - 22)) * 13 + 4


def draw_also(d, y, height):
    d.text((12, y), "ALSO TODAY  —  22 MORE STORIES",
           font=font(11, bold=True), fill=NAVY)
    d.line([(12, y + 16), (W - 12, y + 16)], fill=LINE, width=1)
    rows = 11
    rh = (height - 20) / rows
    f = font(10)
    for i, item in enumerate(ALSO):
        col, row = divmod(i, rows)
        x = 12 + col * 500
        yy = y + 20 + row * rh
        d.text((x, yy), "•  " + item, font=f, fill=INK)


def draw_footer(d, y):
    f = font(9)
    t = tw(d, FOOTER, f)
    if t > W - 24:
        f = font(8)
        t = tw(d, FOOTER, f)
    d.text(((W - t) / 2, y + 3), FOOTER, font=f, fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_ticker(d, 70)
    draw_numbers(d, 94)
    draw_leads(d, 148)
    draw_field_band(d, 474)
    draw_cards(d, 496)
    draw_map(d, (12, 754, 636, 850))
    draw_datecheck(d, (644, 754, 1012, 850))
    draw_also(d, 856, 1024 - 16 - 856)
    draw_footer(d, 1008)
    img.save(OUT, format="PNG")


if __name__ == "__main__":
    main()
