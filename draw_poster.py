#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news poster, round 3 (code-drawn, PIL only).

One image, 1024x1024, deterministic: no randomness, no clock, no network.
35 stories: 4 illustrated leads + 12 illustrated cards + 19 ALSO items.
Every story is an event of Saturday 21 November 2026, first reported that
day, or a late-Friday story dominating Saturday's coverage (see DATE CHECK).
Stories verified against live sources on 21 Nov 2026 (AP, Reuters, KyivPost,
UKMTO, DR, FT, NYT). Layout follows the dev board's winning pattern: big
masthead, region + field bands, UTC timeline, numbers band, large leads,
illustrated card grid, dot map, date check.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 12
CW = W - 2 * M  # 1000

PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (178, 34, 34)
DARKRED = (139, 0, 0)
NAVY = (23, 42, 74)
TEAL = (14, 92, 84)
GOLD = (176, 141, 45)
GREY = (90, 90, 90)
LIGHT = (232, 226, 210)
SKY = (135, 206, 235)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 38)
F_DATEB = font("DejaVuSans-Bold.ttf", 22)
F_DATES = font("DejaVuSans-Bold.ttf", 11)
F_SUB = font("DejaVuSans.ttf", 11)
F_BAND = font("DejaVuSans-Bold.ttf", 10)
F_FIELDB = font("DejaVuSans-Bold.ttf", 10)
F_TL = font("DejaVuSans.ttf", 9)
F_TLB = font("DejaVuSans-Bold.ttf", 9)
F_NUM = font("DejaVuSans-Bold.ttf", 20)
F_NUMLAB = font("DejaVuSans.ttf", 8)
F_SEC = font("DejaVuSans-Bold.ttf", 12)
F_LEAD = font("DejaVuSerif-Bold.ttf", 16)
F_LEADSUB = font("DejaVuSans.ttf", 10)
F_KICK = font("DejaVuSans-Bold.ttf", 9)
F_CARD = font("DejaVuSans-Bold.ttf", 11)
F_CARDSUB = font("DejaVuSans.ttf", 9)
F_ALSO = font("DejaVuSans.ttf", 10)
F_ALSONUM = font("DejaVuSans-Bold.ttf", 10)
F_DC = font("DejaVuSans.ttf", 9)
F_DCB = font("DejaVuSans-Bold.ttf", 9)
F_FOOT = font("DejaVuSans.ttf", 8)
F_TICK = font("DejaVuSans-Bold.ttf", 9)
F_PIN = font("DejaVuSans-Bold.ttf", 9)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def hline(draw, y, x0=M, x1=W - M, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
# fields: WAR, POL, ECON, TECH, SPORT, SCI, CLIM, COURT
LEADS = [
    {
        "num": 1, "kicker": "ANTALYA  •  CLIMATE", "field": "CLIM",
        "head": "COP31 runs into overtime over fossil fuels",
        "sub": "Talks pass the Friday deadline with no deal: the draft still omits "
               "coal, oil and gas, a third text is due Saturday morning, and "
               "France and Panama demand a phase-out. (AP)",
        "art": "cop31", "region": "EUROPE",
    },
    {
        "num": 2, "kicker": "COPENHAGEN  •  SECURITY", "field": "WAR",
        "head": "Denmark foils 'Russian plot to kill Ukrainian rapper'",
        "sub": "PET: three men were arrested on 25 Sept, five minutes before "
               "Kyivstoner was due on stage; Denmark expels Russia's defence "
               "attache. (Reuters)",
        "art": "target", "region": "EUROPE",
    },
    {
        "num": 3, "kicker": "WARSAW  •  WAR", "field": "WAR",
        "head": "Russian missile lands in Poland; Warsaw cries provocation",
        "sub": "A Kh-101 came down at Nowy Lipowiec, a second missile and a drone "
               "fell nearby; no one was hurt. NATO chief Rutte visits Warsaw "
               "today. (Reuters, AP)",
        "art": "missile", "region": "EUROPE",
    },
    {
        "num": 4, "kicker": "STRAIT OF HORMUZ  •  SHIPPING", "field": "WAR",
        "head": "Tanker on fire near Oman after projectile strike",
        "sub": "UKMTO: the outbound tanker was hit 8 nautical miles north of "
               "Khasab, with a fire on board and no casualties; Iran's Guards "
               "blame a mine. (Reuters)",
        "art": "tanker", "region": "ASIA",
    },
]

CARDS = [
    # (num, kicker, head, sub, art, region, field)
    (5, "KRYVYI RIH  •  WAR", "Double-tap kills boy, 7, and medic, 20",
     "2 dead, 42 hurt, 27 serious, as missiles hit a restaurant, then drones "
     "hit the rescuers. (KyivPost)", "night", "EUROPE", "WAR"),
    (6, "WALL ST  •  MARKETS", "Rout: worst week since Covid",
     "Nasdaq -5.28% to 22,617.73, S&P -3.70%, Dow -949.73; worst week since "
     "Covid. (AP)", "chart", "N AMERICA", "ECON"),
    (7, "WASHINGTON  •  TECH", "US cleared ~900K AI chips for China",
     "House panel: 879,000 Nvidia/AMD chips approved Dec-May; 150,000 for "
     "Tencent. (Reuters)", "chip", "ASIA", "TECH"),
    (8, "MISSOURI  •  COURTS", "Bayer Roundup deal: $7.25B approved",
     "A judge approves up to $7.25B over 21 years for current and future "
     "Roundup cancer claims. (AP)", "gavel", "N AMERICA", "COURT"),
    (9, "BRUSSELS  •  WAR", "EU adopts €1bn military aid for Kyiv",
     "The Council adopts two decisions for 1 billion euros in military aid "
     "to Ukraine. (EU)", "stars", "EUROPE", "WAR"),
    (10, "BRASILIA  •  POLITICS", "Jailed Bolsonaro in hospital",
     "The ex-president, 71, is in a Brasilia hospital with a near-complete "
     "intestinal obstruction. (Reports)", "cross", "S AMERICA", "POL"),
    (11, "PYONGYANG  •  WAR", "N. Korea expands enrichment plant",
     "Satellite images show an expansion of North Korea's uranium-"
     "enrichment plant. (Reports)", "atom", "ASIA", "WAR"),
    (12, "UKRAINE  •  WAR", "Mass strike: 84 missiles, 404 drones",
     "Russia's overnight barrage kills 9; Kyiv's bridges are hit again. "
     "(Reports)", "burst", "EUROPE", "WAR"),
    (13, "WASHINGTON  •  POLITICS", "Trump home, calls China trip a win",
     "Back from Shenzhen, he calls the trip successful; the 4-point "
     "declaration settles neither Ukraine nor Iran. (Reports)", "plane", "N AMERICA", "POL"),
    (14, "KYIV  •  POLITICS", "Peace deal wanted by early January",
     "FT: the Trump team tells Kyiv and Europe it wants a Ukraine-Russia "
     "peace deal by early January. (FT)", "clock", "EUROPE", "POL"),
    (15, "CALIFORNIA  •  TECH", "Nvidia: bring back Huang, board says no",
     "Trump urges the board to restore Jensen Huang; it refuses, and the "
     "SEC is probing Nvidia's accounting. (Reports)", "chip2", "N AMERICA", "TECH"),
    (16, "LAS VEGAS  •  SPORT", "GP tonight under the lights",
     "Russell topped a rain-hit practice for tonight's Las Vegas Grand "
     "Prix. (FIA)", "flag", "N AMERICA", "SPORT"),
]

# (text, region, field) -- ALSO list, 19 items
ALSO = [
    ("Panama vows to block any COP31 deal without an oil cap and methane steps.",
     "N AMERICA", "POL"),
    ("Ebola still not under control: 11,376 cases, 5,568 deaths (15 Nov).",
     "AFRICA", "SCI"),
    ("Trump weighs new Iran strikes as the military warns of strain (FT).",
     "ASIA", "WAR"),
    ("SpaceX unit plans to drop Chinese AI models from its stack.", "N AMERICA", "TECH"),
    ("JPMorgan, Visa, Mastercard confirm vendor breach; 16,000+ Chase emails leaked.",
     "N AMERICA", "TECH"),
    ("Trump gives a posthumous pardon to baseball star Pete Rose.", "N AMERICA", "SPORT"),
    ("UK pledges 1,000+ drones in a 260m-pound package for Ukraine.", "EUROPE", "WAR"),
    ("US sanctions the Comancheros and the 'Ndrangheta.", "OCEANIA", "POL"),
    ("US adds four Iranians to the OFAC sanctions list.", "ASIA", "POL"),
    ("ECB: Boone and Brunnermeier seek Executive Board seats.", "EUROPE", "ECON"),
    ("Sensex rallies ~898 points on Saturday.", "ASIA", "ECON"),
    ("Wellington Test, Day 3: India resume 159/1, trail NZ by 209.", "OCEANIA", "SPORT"),
    ("Cyclone Xavier: gale warning narrows over the Cook Islands.", "OCEANIA", "CLIM"),
    ("Gold at a 14-month low after a 9.4% weekly loss.", "N AMERICA", "ECON"),
    ("Anthropic's second trading day fails to calm AI fears.", "N AMERICA", "TECH"),
    ("Gaza: 22,000+ Palestinian children dead, the ministry says.", "ASIA", "WAR"),
    ("Kyiv bridges hit; the Southern Bridge is struck again.", "EUROPE", "WAR"),
    ("Zelensky: the Crimean Bridge \"will not stay\".", "EUROPE", "WAR"),
    ("Third US carrier, USS Theodore Roosevelt, joins the Gulf build-up.", "ASIA", "WAR"),
]

NUMBERS = [
    ("0", "FOSSIL-FUEL MENTIONS IN COP31 DRAFT"),
    ("2", "DEAD, KRYVYI RIH"),
    ("42", "HURT, KRYVYI RIH"),
    ("900K", "AI CHIPS CLEARED FOR CHINA"),
    ("$7.25B", "BAYER ROUNDUP DEAL"),
    ("3", "RUSSIAN WEAPONS DOWN IN POLAND"),
]

TIMELINE = [
    ("OVERNIGHT", "Denmark plot revealed"),
    ("02:26 UTC", "Kryvyi Rih toll confirmed"),
    ("MORNING", "COP31 third draft due"),
    ("15:00 UTC", "Tanker struck off Khasab (Fri)"),
    ("21:00 UTC", "Wall St: Nasdaq -5.28% (Fri)"),
    ("EVENING", "Las Vegas GP"),
]

PINS = [
    (1, "ANTALYA", 30.7, 36.9),
    (2, "COPENHAGEN", 12.6, 55.7),
    (3, "NOWY LIPOWIEC", 22.9, 50.4),
    (4, "KHASAB", 56.3, 26.5),
    (5, "KRYVYI RIH", 33.4, 47.9),
    (6, "NEW YORK", -74.0, 40.7),
    (7, "BRASILIA", -47.9, -15.8),
    (8, "PYONGYANG", 125.8, 39.0),
]

DATE_CHECK_LEFT = ("Left out - broke earlier: Shenzhen summit (Thu 19); ICJ Myanmar "
                   "genocide ruling (Thu 19); Akvan landfall (Fri 20); n0n breach "
                   "disclosures (Thu 19); Senate Iran vote (Thu 19); Voyager 1 "
                   "one light-day (Wed 18).")
DATE_CHECK_RIGHT = ("Not yet: COP31 final deal; Las Vegas GP result; Wellington Day 3 "
                    "result; Fed December decision; Ukraine peace deal. "
                    "Solid = 2+ sources; developing = still moving.")

MARKETS = ("FRIDAY CLOSE  •  Dow 48,147.33 -1.93%  •  S&P 500 6,910.39 -3.70%  •  "
           "Nasdaq 22,617.73 -5.28%  •  Nasdaq 100 25,028.98 -5.61%  •  Russell 2,581.79 -2.76%")

SOURCES = ("Sources: AP, Reuters, KyivPost, UKMTO, DR, FT, NYT, EU, FIA. "
           "Drawn in code; no photos. Times UTC unless noted.")

STORY_TOTAL = len(LEADS) + len(CARDS) + len(ALSO)


# ---------------------------------------------------------------- art
def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 77, 66))
    d.ellipse([x + w // 2 - 34, y + 8, x + w // 2 + 34, y + 76], fill=(247, 243, 232))
    d.ellipse([x + w // 2 - 22, y + 20, x + w // 2 - 2, y + 40], fill=(46, 139, 87))
    d.ellipse([x + w // 2 + 4, y + 44, x + w // 2 + 24, y + 64], fill=(46, 139, 87))
    d.ellipse([x + w // 2 - 34, y + 8, x + w // 2 + 34, y + 76], outline=(18, 77, 66), width=2)
    for fx in (x + 14, x + w - 26):
        d.line([(fx + 5, y + 12), (fx + 5, y + 58)], fill=(247, 243, 232), width=2)
        d.polygon([(fx + 5, y + 12), (fx + 22, y + 18), (fx + 5, y + 24)],
                  fill=(178, 34, 34))
    text(d, (x + w // 2, y + h - 6), "COP31", F_TICK, fill=(247, 243, 232), anchor="ms")


def art_target(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 24, 40))
    cx, cy = x + w // 2, y + h // 2 - 4
    for r, col in ((42, (247, 243, 232)), (30, (178, 34, 34)), (18, (247, 243, 232))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(178, 34, 34))
    d.line([(cx, y + 6), (cx, cy - 48)], fill=(247, 243, 232), width=2)
    d.line([(cx, cy + 48), (cx, y + h - 6)], fill=(247, 243, 232), width=2)
    d.line([(x + 8, cy), (cx - 48, cy)], fill=(247, 243, 232), width=2)
    d.line([(cx + 48, cy), (x + w - 8, cy)], fill=(247, 243, 232), width=2)
    for sx in (x + 20, x + w - 60):
        d.ellipse([sx, y + h - 22, sx + 14, y + h - 8], fill=(232, 190, 90))


def art_missile(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 42, 66))
    for sx in (x + 16, x + 66, x + 116, x + 166):
        d.rectangle([sx, y + h - 34, sx + 26, y + h - 10], fill=(20, 20, 22))
        for wy in range(y + h - 30, y + h - 12, 8):
            d.rectangle([sx + 5, wy, sx + 10, wy + 3], fill=(232, 190, 90))
    d.line([(x + 12, y + 22), (x + w - 30, y + h - 44)], fill=(255, 220, 120), width=3)
    d.polygon([(x + w - 30, y + h - 44), (x + w - 52, y + h - 40),
               (x + w - 44, y + h - 62)], fill=(220, 220, 220))
    d.polygon([(x + 12, y + 22), (x + 30, y + 30), (x + 22, y + 38)], fill=(255, 120, 60))
    d.ellipse([x + w - 40, y + 10, x + w - 12, y + 38], outline=(247, 243, 232), width=2)
    d.line([(x + w - 26, y + 10), (x + w - 26, y + 38)], fill=(247, 243, 232), width=1)
    d.line([(x + w - 40, y + 24), (x + w - 12, y + 24)], fill=(247, 243, 232), width=1)


def art_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 60, 80))
    d.ellipse([x + w - 52, y + 8, x + w - 20, y + 40], fill=(232, 190, 90))
    d.rectangle([x + 14, y + h - 52, x + w - 14, y + h - 30], fill=(120, 40, 30))
    d.rectangle([x + 14, y + h - 30, x + w - 14, y + h - 22], fill=(60, 20, 16))
    d.rectangle([x + w - 70, y + h - 78, x + w - 40, y + h - 52], fill=(200, 200, 200))
    for fy in range(y + h - 84, y + h - 30, 8):
        d.line([(x + 30, fy), (x + 44, fy)], fill=(255, 120, 40), width=2)
    d.polygon([(x + 34, y + 18), (x + 46, y + 44), (x + 22, y + 44)], fill=(255, 140, 40))
    d.polygon([(x + 52, y + 30), (x + 62, y + 50), (x + 42, y + 50)], fill=(255, 200, 60))
    for wx in range(x + 8, x + w - 8, 14):
        d.line([(wx, y + h - 12), (wx + 8, y + h - 12)], fill=(135, 206, 235), width=2)


def art_night(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 38, 28))
    d.ellipse([x + w - 40, y + 6, x + w - 14, y + 32], fill=(232, 150, 60))
    for bx, bw, bh in ((x + 6, 40, 34), (x + 50, 34, 46), (x + 88, 44, 28),
                       (x + 136, 38, 40), (x + 178, 34, 48)):
        bh = min(bh, h - 6)
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(20, 20, 22))
        for wy in range(y + h - bh + 6, y + h - 4, 10):
            for wx in range(bx + 5, bx + bw - 5, 10):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(232, 190, 90))
    d.ellipse([x + w // 2 - 6, y + 10, x + w // 2 + 20, y + 30], fill=(120, 120, 120))
    d.ellipse([x + w // 2 + 4, y + 4, x + w // 2 + 26, y + 20], fill=(150, 150, 150))


def art_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for gy in range(y + 10, y + h - 6, 12):
        d.line([(x + 5, gy), (x + w - 5, gy)], fill=(70, 90, 130), width=1)
    pts = [(x + 6, y + 14), (x + w * 0.3, y + 20), (x + w * 0.5, y + 18),
           (x + w * 0.68, y + 38), (x + w * 0.85, y + 48), (x + w - 8, y + h - 10)]
    d.line(pts, fill=(235, 64, 52), width=3, joint="curve")
    fs = 16 if h > 50 else 11
    text(d, (x + 8, y + h - 8), "-5.28%", font("DejaVuSans-Bold.ttf", fs),
         fill=(255, 255, 255), anchor="ls")


def art_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 34))
    d.rectangle([x + w // 2 - 26, y + 5, x + w // 2 + 26, y + h - 5], fill=INK)
    d.rectangle([x + w // 2 - 18, y + 9, x + w // 2 + 18, y + h - 9], fill=(247, 243, 232))
    for px in range(x + w // 2 - 22, x + w // 2 + 23, 10):
        d.line([(px, y + 1), (px, y + 5)], fill=(247, 243, 232), width=2)
        d.line([(px, y + h - 5), (px, y + h - 1)], fill=(247, 243, 232), width=2)
    if h > 50:
        text(d, (x + w // 2, y + h - 6), "900K", F_TICK, fill=(247, 243, 232), anchor="ms")


def art_gavel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    d.rectangle([x + 30, y + h - 6, x + w - 30, y + h - 2], fill=(120, 80, 40))
    d.line([(x + w // 2 - 40, y + 8), (x + w // 2 + 40, y + h - 8)], fill=(90, 60, 30), width=5)
    d.rectangle([x + w // 2 - 52, y + 2, x + w // 2 - 28, y + 14], fill=(60, 40, 20))
    d.rectangle([x + w // 2 + 28, y + h - 14, x + w // 2 + 52, y + h - 2], fill=(60, 40, 20))
    d.ellipse([x + 16, y + 6, x + 28, y + 18], fill=GOLD)
    d.ellipse([x + w - 28, y + h - 18, x + w - 16, y + h - 6], fill=GOLD)


def art_stars(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    cx, cy = x + w // 2, y + h // 2
    rx, ry = min(30, w // 2 - 8), min(22, h // 2 - 4)
    for k in range(12):
        a = math.pi * 2 * k / 12 - math.pi / 2
        px = cx + int(rx * math.cos(a))
        py = cy + int(ry * math.sin(a))
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 204, 0))
    if h > 50:
        text(d, (cx, y + h - 6), "€1bn", F_TICK, fill=(255, 255, 255), anchor="ms")


def art_cross(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(247, 243, 232))
    d.rectangle([x + w // 2 - 26, y + 8, x + w // 2 + 26, y + h - 8], fill=RED)
    d.rectangle([x + 16, y + h // 2 - 8, x + w - 16, y + h // 2 + 8], fill=(255, 255, 255))
    d.rectangle([x + w // 2 - 7, y + 12, x + w // 2 + 7, y + h - 12], fill=(255, 255, 255))


def art_atom(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 30, 50))
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    rx, ry = min(42, w // 2 - 6), min(14, h // 2 - 3)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=(247, 243, 232), width=2)
    d.ellipse([cx - ry, cy - rx, cx + ry, cy + rx], outline=(247, 243, 232), width=2)


def art_burst(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 20, 20))
    cx, cy = x + w // 2, y + h // 2
    rx, ry = min(34, w // 2 - 4), min(24, h // 2 - 4)
    for k in range(8):
        a = math.pi * 2 * k / 8
        ex = cx + int(rx * math.cos(a))
        ey = cy + int(ry * math.sin(a))
        d.line([(cx, cy), (ex, ey)], fill=(255, 180, 60), width=3)
    r = min(12, h // 2 - 3)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 120, 40))
    r2 = max(2, r - 7)
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=(255, 220, 120))


def art_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(135, 206, 235))
    d.polygon([(x + 14, y + h // 2 + 6), (x + w - 14, y + h // 2 - 14),
               (x + w - 30, y + h // 2 + 2), (x + w - 44, y + h // 2 + 14),
               (x + 30, y + h // 2 + 14)], fill=(255, 255, 255))
    d.polygon([(x + w // 2, y + h // 2 + 2), (x + w // 2 + 18, y + h // 2 - 18),
               (x + w // 2 + 26, y + h // 2 + 2)], fill=(255, 255, 255))
    d.ellipse([x + 20, y + 12, x + 34, y + 26], fill=(255, 255, 255))
    d.ellipse([x + 44, y + 8, x + 62, y + 22], fill=(255, 255, 255))


def art_clock(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(247, 243, 232))
    cx, cy = x + w // 2, y + h // 2
    r = min(26, h // 2 - 2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    d.line([(cx, cy), (cx, cy - r + 8)], fill=INK, width=3)
    d.line([(cx, cy), (cx + r - 10, cy + 6)], fill=INK, width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    for k in range(12):
        a = math.pi * 2 * k / 12
        px = cx + int((r - 4) * math.cos(a))
        py = cy + int((r - 4) * math.sin(a))
        d.ellipse([px - 1, py - 1, px + 1, py + 1], fill=INK)


def art_flag(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 20, 22))
    rows = max(2, h // 12)
    for row in range(rows):
        for col in range(8):
            if (row + col) % 2 == 0:
                d.rectangle([x + 10 + col * 22, y + 6 + row * 12,
                             x + 10 + col * 22 + 22, y + 6 + row * 12 + 12],
                            fill=(255, 255, 255))
    if h > 60:
        d.rectangle([x + 10, y + 58, x + w - 10, y + 62], fill=GOLD)
        text(d, (x + w // 2, y + h - 6), "LAS VEGAS", F_TICK, fill=(255, 255, 255), anchor="ms")


def draw_art(d, kind, x, y, w, h):
    {"cop31": art_cop31, "target": art_target, "missile": art_missile,
     "tanker": art_tanker, "night": art_night, "chart": art_chart,
     "chip": art_chip, "chip2": art_chip, "gavel": art_gavel,
     "stars": art_stars, "cross": art_cross, "atom": art_atom,
     "burst": art_burst, "plane": art_plane, "clock": art_clock,
     "flag": art_flag}[kind](d, x, y, w, h)


# ---------------------------------------------------------------- map
LAND = [
    (-168, -52, 15, 72), (-105, -77, 7, 16), (-80, -34, -56, 12),
    (-11, 42, 36, 71), (-18, 52, -35, 36), (42, 180, 5, 77),
    (35, 60, 12, 42), (95, 141, -11, 7), (113, 154, -40, -11),
    (166, 179, -48, -34), (129, 146, 31, 46), (-6, 2, 50, 59),
    (43, 51, -26, -12), (-58, -20, 60, 84),
]


def is_land(lon, lat):
    return any(a <= lon <= b and c <= lat <= dd for a, b, c, dd in LAND)


def map_xy(lon, lat, x0, y0, w, h):
    return (x0 + (lon + 170) / 350.0 * w, y0 + (78 - lat) / 136.0 * h)


def draw_map(d, x0, y0, w, h):
    lon = -168
    while lon <= 180:
        lat = -54
        while lat <= 78:
            if is_land(lon, lat):
                px, py = map_xy(lon, lat, x0, y0, w, h - 14)
                d.ellipse([px - 1.4, py - 1.4, px + 1.4, py + 1.4], fill=(70, 70, 70))
            lat += 12
        lon += 6
    offsets = {2: (-14, 10), 3: (14, -8), 5: (14, 8)}
    for num, name, lon, lat in PINS:
        px, py = map_xy(lon, lat, x0, y0, w, h - 14)
        dx, dy = offsets.get(num, (0, 0))
        if (dx, dy) != (0, 0):
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=INK)
            d.line([(px, py), (px + dx, py + dy)], fill=INK, width=1)
            px, py = px + dx, py + dy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        text(d, (px, py), str(num), F_PIN, fill=(255, 255, 255), anchor="mm")
    labels = "  •  ".join(f"{n} {name}" for n, name, _, _ in PINS)
    labels = labels.replace("NOWY LIPOWIEC", "LIPOWIEC")
    text(d, (x0 + w // 2, y0 + h - 11), labels, F_FOOT, fill=GREY, anchor="ma")


# ---------------------------------------------------------------- layout
REGION_COLORS = [
    ("EUROPE", (0, 51, 153)),
    ("AMERICAS", (178, 34, 34)),
    ("ASIA", (176, 141, 45)),
    ("AFRICA", (14, 92, 84)),
    ("OCEANIA", (90, 90, 160)),
]
FIELD_LABELS = [
    ("WAR", "War & security"),
    ("POL", "Politics & diplomacy"),
    ("TECH", "Tech"),
    ("ECON", "Economy & markets"),
    ("SPORT", "Sport"),
    ("CLIM", "Climate"),
    ("COURT", "Courts & justice"),
    ("SCI", "Science & health"),
]


def region_counts():
    counts = {"EUROPE": 0, "AMERICAS": 0, "ASIA": 0, "AFRICA": 0, "OCEANIA": 0}
    for s in LEADS:
        r = s["region"]
        counts["AMERICAS" if r in ("N AMERICA", "S AMERICA") else r] += 1
    for c in CARDS:
        r = c[5]
        counts["AMERICAS" if r in ("N AMERICA", "S AMERICA") else r] += 1
    for _t, r, _f in ALSO:
        counts["AMERICAS" if r in ("N AMERICA", "S AMERICA") else r] += 1
    return counts


def field_counts():
    counts = {k: 0 for k, _ in FIELD_LABELS}
    for s in LEADS:
        counts[s["field"]] += 1
    for c in CARDS:
        counts[c[6]] += 1
    for _t, _r, f in ALSO:
        counts[f] += 1
    return counts


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([4, 4, W - 5, H - 5], outline=INK, width=2)

    # masthead: red date block + giant title
    d.rectangle([M, 14, 108, 82], fill=RED)
    text(d, (60, 20), "NOV 21", F_DATEB, fill=(255, 255, 255), anchor="ma")
    text(d, (60, 48), "SAT  •  2026", F_DATES, fill=(255, 255, 255), anchor="ma")
    text(d, (60, 64), "35 STORIES", F_DATES, fill=(255, 220, 120), anchor="ma")
    text(d, (120, 18), "Saturday 21 November 2026", F_MAST, anchor="la")
    text(d, (120, 64), "The day's news from Antalya to Wellington, in one page.",
         F_SUB, anchor="la")
    text(d, (W - M, 22), "35 STORIES  •  7 REGIONS  •  16 DRAWN", F_BAND, fill=NAVY, anchor="ra")
    text(d, (W - M, 42), "CODE-DRAWN  •  NO PHOTOS", F_SUB, fill=GREY, anchor="ra")
    hline(d, 88, width=2)

    # region band: coloured segments
    rc = region_counts()
    widths = {"EUROPE": 300, "AMERICAS": 320, "ASIA": 200, "AFRICA": 80, "OCEANIA": 100}
    x = M
    for name, col in REGION_COLORS:
        wseg = widths[name]
        d.rectangle([x, 94, x + wseg - 2, 112], fill=col)
        text(d, (x + wseg // 2, 97), f"{name} {rc[name]}", F_BAND,
             fill=(255, 255, 255), anchor="ma")
        x += wseg
    hline(d, 116, width=1)

    # field band
    fc = field_counts()
    fband = "   •   ".join(f"{lab} {fc[k]}" for k, lab in FIELD_LABELS)
    text(d, (W // 2, 120), "BY FIELD:  " + fband, F_FIELDB, fill=NAVY, anchor="ma")
    hline(d, 132, width=1)

    # UTC timeline strip
    text(d, (M, 136), "THE DAY IN UTC", F_TLB, fill=RED, anchor="la")
    cellw = (CW - 130) // len(TIMELINE)
    for i, (t, s) in enumerate(TIMELINE):
        cx = M + 130 + i * cellw
        if i:
            d.line([(cx - 3, 136), (cx - 3, 158)], fill=GREY, width=1)
        text(d, (cx + 4, 136), t, F_TLB, anchor="la")
        for j, ln in enumerate(wrap(d, s, F_TL, cellw - 10)[:2]):
            text(d, (cx + 4, 148 + j * 10), ln, F_TL, fill=GREY, anchor="la")
    hline(d, 162, width=1)

    # numbers band
    text(d, (M, 166), "THE DAY IN NUMBERS", F_SEC, anchor="la")
    numw = CW // len(NUMBERS)
    for i, (val, lab) in enumerate(NUMBERS):
        cx = M + i * numw
        text(d, (cx + numw // 2, 182), val, F_NUM, fill=DARKRED, anchor="ma")
        text(d, (cx + numw // 2, 202), lab, F_NUMLAB, fill=GREY, anchor="ma")
    hline(d, 214, width=1)

    # leads: 4 columns
    colw = (CW - 3 * 8) // 4
    ly = 220
    for i, lead in enumerate(LEADS):
        x = M + i * (colw + 8)
        draw_art(d, lead["art"], x, ly, colw, 104)
        text(d, (x, ly + 108), f"{lead['num']}  {lead['kicker']}", F_KICK, fill=RED, anchor="la")
        yy = ly + 122
        for ln in wrap(d, lead["head"], F_LEAD, colw)[:2]:
            text(d, (x, yy), ln, F_LEAD, anchor="la")
            yy += 19
        yy += 2
        for ln in wrap(d, lead["sub"], F_LEADSUB, colw)[:4]:
            text(d, (x, yy), ln, F_LEADSUB, anchor="la")
            yy += 12
        if i < 3:
            d.line([(x + colw + 4, ly), (x + colw + 4, ly + 216)], fill=GREY, width=1)
    hline(d, 444, width=1)

    # cards: 4 cols x 3 rows, scene strip on top
    cardw = (CW - 3 * 8) // 4
    cardh = 96
    for i, (num, kick, head, sub, art, _r, _f) in enumerate(CARDS):
        row, col = divmod(i, 4)
        x = M + col * (cardw + 8)
        yy = 450 + row * (cardh + 4)
        draw_art(d, art, x, yy, cardw, 32)
        text(d, (x, yy + 36), f"{num}  {kick}", F_KICK, fill=RED, anchor="la")
        hy = yy + 48
        for ln in wrap(d, head, F_CARD, cardw)[:2]:
            text(d, (x, hy), ln, F_CARD, anchor="la")
            hy += 13
        sy = hy + 1
        for ln in wrap(d, sub, F_CARDSUB, cardw)[:2]:
            text(d, (x, sy), ln, F_CARDSUB, anchor="la")
            sy += 11
    hline(d, 744, width=1)

    # ALSO list: 19 items, 2 columns
    text(d, (M, 750), f"ALSO TODAY  —  {len(ALSO)} MORE STORIES", F_SEC, anchor="la")
    colw2 = (CW - 16) // 2
    for i, (txt, _r, _f) in enumerate(ALSO):
        col = 0 if i < 10 else 1
        row = i if i < 10 else i - 10
        x = M + col * (colw2 + 16)
        yy = 766 + row * 11
        num = 17 + i
        text(d, (x, yy), f"{num}.", F_ALSONUM, fill=RED, anchor="la")
        lines = wrap(d, txt, F_ALSO, colw2 - 24)
        text(d, (x + 24, yy), lines[0], F_ALSO, anchor="la")
    hline(d, 882, width=1)

    # bottom: map left, date check right
    text(d, (M, 888), "WHERE IT HAPPENED", F_SEC, anchor="la")
    draw_map(d, M, 904, 484, 84)
    x2 = M + 496
    d.rectangle([x2, 888, x2 + 504, 988], outline=INK, width=1)
    text(d, (x2 + 8, 892), "DATE CHECK", F_DCB, fill=RED, anchor="la")
    yy = 906
    for ln in wrap(d, DATE_CHECK_LEFT, F_DC, 504 - 16):
        text(d, (x2 + 8, yy), ln, F_DC, anchor="la")
        yy += 11
    yy += 4
    text(d, (x2 + 8, yy), "NOT YET  •  HOW SURE", F_DCB, fill=RED, anchor="la")
    yy += 14
    for ln in wrap(d, DATE_CHECK_RIGHT, F_DC, 504 - 16):
        text(d, (x2 + 8, yy), ln, F_DC, anchor="la")
        yy += 11

    # footer: markets + ticker + sources
    hline(d, 994, width=1)
    text(d, (W // 2, 998), MARKETS, F_TLB, anchor="ma")
    text(d, (M, 1010), SOURCES, F_FOOT, fill=GREY, anchor="la")
    return img


def main():
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
