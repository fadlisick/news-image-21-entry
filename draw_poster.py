#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news poster (code-drawn, PIL only).

One image, 1024x1024, deterministic: no randomness, no clock, no network.
Stories were verified against live sources on 21 Nov 2026 (AP, Reuters,
KyivPost, IMD, ECDC, FT, NYT, BCCI, FIA). Every story is either an event of
Saturday 21 November 2026, first reported that day, or is labelled with the
day it broke (see DATE CHECK on the poster).

Story count: 3 leads + 8 cards + 28 ALSO + 6 ticker + 6 numbers = 51.
"""
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
RULE = (26, 26, 26)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 42)
F_DATE = font("DejaVuSans-Bold.ttf", 16)
F_SUB = font("DejaVuSans.ttf", 11)
F_SEC = font("DejaVuSans-Bold.ttf", 12)
F_LEAD = font("DejaVuSerif-Bold.ttf", 17)
F_LEADSUB = font("DejaVuSans.ttf", 11)
F_CARD = font("DejaVuSans-Bold.ttf", 11)
F_CARDSUB = font("DejaVuSans.ttf", 9)
F_ALSO = font("DejaVuSans.ttf", 10)
F_ALSONUM = font("DejaVuSans-Bold.ttf", 10)
F_NUM = font("DejaVuSans-Bold.ttf", 17)
F_NUMLAB = font("DejaVuSans.ttf", 9)
F_TL = font("DejaVuSans.ttf", 10)
F_TLB = font("DejaVuSans-Bold.ttf", 10)
F_DC = font("DejaVuSans.ttf", 9)
F_DCB = font("DejaVuSans-Bold.ttf", 9)
F_FOOT = font("DejaVuSans.ttf", 8)
F_TICK = font("DejaVuSans-Bold.ttf", 9)
F_BAND = font("DejaVuSans-Bold.ttf", 10)
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
LEADS = [
    {
        "kicker": "CLIMATE  •  ANTALYA",
        "head": "COP31 SPILLS INTO SATURDAY",
        "sub": "Talks pass the Friday deadline with no deal: fossil fuels are still "
               "absent from the draft, a third text is due Saturday morning, and "
               "delegates held a \"failure\" banner protest overnight.",
        "art": "cop31",
        "region": "EUROPE",
    },
    {
        "kicker": "MARKETS  •  FRIDAY CLOSE",
        "head": "WALL ST ROUT: WORST WEEK SINCE COVID",
        "sub": "Nasdaq -5.28% to 22,617.73, S&P -3.70% to 6,910.39 and in correction, "
               "Dow -949.73; the AI sell-off wiped out the Nasdaq's gains for the year.",
        "art": "markets",
        "region": "N AMERICA",
    },
    {
        "kicker": "UKRAINE  •  TOLL CONFIRMED SATURDAY",
        "head": "DOUBLE-TAP KILLS BOY, 7, AND MEDIC, 20",
        "sub": "2 dead, 42 hurt, 27 in serious condition, as Russian missiles hit a "
               "Kryvyi Rih restaurant, then jet drones struck the rescuers at work.",
        "art": "kryvyi",
        "region": "EUROPE",
    },
]

CARDS = [
    ("TRUMP HOME", "Back from Shenzhen, he calls the China trip successful; the "
     "4-point declaration settles neither Ukraine nor Iran.", "plane", "N AMERICA"),
    ("PEACE CLOCK", "FT: Trump team tells Kyiv and Europe it wants a Ukraine-Russia "
     "peace deal by early January.", "clock", "EUROPE"),
    ("NVIDIA", "Trump urges the board to bring back Jensen Huang; it says no, and "
     "the SEC is probing Nvidia's accounting.", "chip", "N AMERICA"),
    ("BOLSONARO", "Jailed ex-president, 71, in a Brasilia hospital with a "
     "near-complete intestinal obstruction.", "cross", "S AMERICA"),
    ("HORMUZ", "UKMTO: a tanker is struck and on fire 8 miles north of Khasab "
     "in the Strait of Hormuz.", "ship", "ASIA"),
    ("EU AID", "EU Council adopts two decisions for 1bn euros in military aid "
     "to Ukraine.", "stars", "EUROPE"),
    ("N. KOREA", "Satellite images show an expansion of North Korea's "
     "uranium-enrichment plant.", "atom", "ASIA"),
    ("LA AUTO SHOW", "Hyundai unveils the 2027 Elantra, eighth generation, with "
     "hybrid options.", "car", "N AMERICA"),
]

# (number, text, region) -- ALSO list, 28 items
ALSO = [
    ("Panama vows to block any COP31 deal without an oil cap and methane steps.",
     "N AMERICA"),
    ("Ebola still not under control: 11,376 cases, 5,568 deaths (15 Nov).",
     "AFRICA"),
    ("Trump weighs new Iran strikes as the military warns of strain (FT).",
     "ASIA"),
    ("US approves ~880,000 AI chip sales to China, buyers linked to military.",
     "ASIA"),
    ("SpaceX unit plans to drop Chinese AI models from its stack.", "N AMERICA"),
    ("JPMorgan, Visa, Mastercard confirm vendor breach; 16,000+ Chase emails leaked.",
     "N AMERICA"),
    ("Trump gives a posthumous pardon to baseball star Pete Rose.", "N AMERICA"),
    ("UK pledges 1,000+ drones in a 260m-pound package for Ukraine.", "EUROPE"),
    ("US sanctions the Comancheros and the 'Ndrangheta.", "OCEANIA"),
    ("US adds four Iranians to the OFAC sanctions list.", "ASIA"),
    ("ECB: Boone and Brunnermeier seek Executive Board seats.", "EUROPE"),
    ("Sensex rallies ~898 points on Saturday.", "ASIA"),
    ("Wellington Test, Day 3: India resume 159/1, trail NZ by 209.", "OCEANIA"),
    ("Cyclone Xavier: gale warning narrows over the Cook Islands.", "OCEANIA"),
    ("Gold at a 14-month low after a 9.4% weekly loss.", "N AMERICA"),
    ("Anthropic's second trading day fails to calm AI fears.", "N AMERICA"),
    ("Las Vegas GP tonight; Russell topped the rain-hit practice.", "N AMERICA"),
    ("Gaza: 22,000+ Palestinian children dead, the ministry says.", "ASIA"),
    ("Russia mass strike: 84 cruise missiles, 404 drones, 9 killed.", "EUROPE"),
    ("Kyiv bridges hit; the Southern Bridge is struck again.", "EUROPE"),
    ("Akvan's remnant rain eases; 300,000+ sheltered, no deaths.", "ASIA"),
    ("Zelensky: the Crimean Bridge \"will not stay\".", "EUROPE"),
    ("Third US carrier, USS Theodore Roosevelt, joins the Gulf build-up.", "ASIA"),
    ("COP31 co-hosts Turkey and Australia under fire over the draft.", "OCEANIA"),
    ("Flavio Bolsonaro loses his vote and moves his family to the US.", "S AMERICA"),
    ("Potatoes grow a full cycle in simulated Moon soil (Oregon State).",
     "N AMERICA"),
    ("First black-hole image validated by an independent team.", "WORLD"),
    ("Next climate summit set for Addis Ababa, November 2027.", "AFRICA"),
]

TICKER = [
    ("Youth cost-of-living protests across Europe, 21-22 Nov.", "EUROPE"),
    ("Saudi Arabia warns of storms through Tuesday 24 Nov.", "ASIA"),
    ("F1: Verstappen to face an FIA probe after a Colapinto clash.", "N AMERICA"),
    ("Ebola: 400-500 new cases a week, mostly in rural areas.", "AFRICA"),
    ("Nasdaq now down on the year after Friday's rout.", "N AMERICA"),
    ("COP31: electrify to 35% by 2035, but not necessarily clean.", "EUROPE"),
]

NUMBERS = [
    ("-5.28%", "NASDAQ, FRIDAY"),
    ("-949.73", "DOW POINTS, FRIDAY"),
    ("2 / 42", "DEAD / HURT, KRYVYI RIH"),
    ("300,000+", "EVACUATED FOR AKVAN"),
    ("16,000+", "CHASE EMAILS LEAKED"),
    ("880,000", "AI CHIPS CLEARED FOR CHINA"),
]

PINS = [
    (1, "ANTALYA", 30.7, 36.9),
    (2, "KRYVYI RIH", 33.4, 47.9),
    (3, "HORMUZ", 56.3, 26.5),
    (4, "BRASILIA", -47.9, -15.8),
    (5, "WELLINGTON", 174.8, -41.3),
    (6, "GOPALPUR", 84.9, 19.3),
    (7, "PYONGYANG", 125.8, 39.0),
    (8, "NEW YORK", -74.0, 40.7),
]

TIMELINE = [
    ("02:26 UTC", "Kryvyi Rih toll confirmed: 2 dead, 42 hurt"),
    ("03:34 UTC", "Xavier gale warning narrows"),
    ("SAT MORNING", "COP31 third draft due in Antalya"),
    ("SAT 20:00 PST", "Las Vegas GP race under the lights"),
    ("FRI 21:00 UTC", "Wall St closes: Nasdaq -5.28%"),
]

DATE_CHECK_LEFT = ("Left out - broke earlier: Shenzhen summit (Thu 19); ICJ Myanmar "
                   "genocide ruling (Thu 19); Akvan landfall (Fri 20); n0n breach "
                   "disclosures (Thu 19); Senate Iran vote (Thu 19); Voyager 1 "
                   "one light-day (Wed 18).")
DATE_CHECK_RIGHT = ("Not yet: COP31 final deal; Las Vegas GP result; Wellington Day 3 "
                    "result; Fed December hike decision; Ukraine peace deal.")

MARKETS = ("FRIDAY CLOSE  •  Dow 48,147.33 -1.93%  •  S&P 500 6,910.39 -3.70%  •  "
           "Nasdaq 22,617.73 -5.28%  •  Nasdaq 100 25,028.98 -5.61%  •  Russell 2,581.79 -2.76%")

SOURCES = ("Sources: AP, Reuters, KyivPost, IMD, ECDC, FT, NYT, BCCI, FIA. "
           "Drawn in code; no photos. Times UTC unless noted.")

STORY_TOTAL = 3 + 8 + len(ALSO) + len(TICKER) + len(NUMBERS)


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


def art_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for gy in range(y + 14, y + h - 8, 16):
        d.line([(x + 6, gy), (x + w - 6, gy)], fill=(70, 90, 130), width=1)
    pts = [(x + 8, y + 18), (x + w * 0.3, y + 26), (x + w * 0.5, y + 22),
           (x + w * 0.68, y + 48), (x + w * 0.85, y + 62), (x + w - 10, y + h - 12)]
    d.line(pts, fill=(235, 64, 52), width=4, joint="curve")
    d.polygon([(x + w - 10, y + h - 12), (x + w - 22, y + h - 16), (x + w - 20, y + h - 4)],
              fill=(235, 64, 52))
    text(d, (x + 10, y + h - 24), "-5.28%", font("DejaVuSans-Bold.ttf", 20),
         fill=(255, 255, 255), anchor="ls")


def art_kryvyi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 38, 28))
    d.ellipse([x + w - 46, y + 10, x + w - 14, y + 42], fill=(232, 150, 60))
    for bx, bw, bh in ((x + 8, 52, 46), (x + 66, 44, 62), (x + 116, 56, 38),
                       (x + 178, 48, 54), (x + 232, 44, 66)):
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(20, 20, 22))
        for wy in range(y + h - bh + 8, y + h - 6, 12):
            for wx in range(bx + 6, bx + bw - 6, 12):
                d.rectangle([wx, wy, wx + 5, wy + 6], fill=(232, 190, 90))
    d.ellipse([x + w // 2 - 8, y + 14, x + w // 2 + 26, y + 40], fill=(120, 120, 120))
    d.ellipse([x + w // 2 + 6, y + 6, x + w // 2 + 34, y + 28], fill=(150, 150, 150))
    d.rectangle([x + w - 58, y + h - 26, x + w - 10, y + h - 8], fill=(255, 255, 255))
    d.rectangle([x + w - 42, y + h - 23, x + w - 36, y + h - 11], fill=RED)
    d.rectangle([x + w - 48, y + h - 20, x + w - 30, y + h - 14], fill=RED)


def draw_art(d, kind, x, y, w, h):
    if kind == "cop31":
        art_cop31(d, x, y, w, h)
    elif kind == "markets":
        art_markets(d, x, y, w, h)
    else:
        art_kryvyi(d, x, y, w, h)


# ---------------------------------------------------------------- icons
def icon(d, kind, x, y, s=30):
    d.rectangle([x, y, x + s, y + s], outline=INK, width=1, fill=LIGHT)
    c = (x + s // 2, y + s // 2)
    if kind == "plane":
        d.polygon([(x + 4, c[1] + 2), (x + s - 4, c[1] - 6), (x + s - 8, c[1] + 2),
                   (x + s - 12, c[1] + 8), (x + 8, c[1] + 8)], fill=NAVY)
        d.polygon([(x + s // 2, c[1] - 2), (x + s // 2 + 8, c[1] - 12),
                   (x + s // 2 + 12, c[1] - 2)], fill=NAVY)
    elif kind == "clock":
        d.ellipse([x + 6, y + 6, x + s - 6, y + s - 6], outline=INK, width=2)
        d.line([(c[0], c[1]), (c[0], y + 9)], fill=INK, width=2)
        d.line([(c[0], c[1]), (x + s - 10, c[1] + 4)], fill=INK, width=2)
    elif kind == "chip":
        d.rectangle([x + 8, y + 8, x + s - 8, y + s - 8], fill=INK)
        d.rectangle([x + 12, y + 12, x + s - 12, y + s - 12], fill=(247, 243, 232))
        for px in (x + 11, x + s // 2 - 1, x + s - 13):
            d.line([(px, y + 2), (px, y + 8)], fill=INK, width=2)
            d.line([(px, y + s - 8), (px, y + s - 2)], fill=INK, width=2)
    elif kind == "cross":
        d.rectangle([x + 4, y + 4, x + s - 4, y + s - 4], fill=RED)
        d.rectangle([x + s // 2 - 3, y + 8, x + s // 2 + 3, y + s - 8], fill=(255, 255, 255))
        d.rectangle([x + 8, y + s // 2 - 3, x + s - 8, y + s // 2 + 3], fill=(255, 255, 255))
    elif kind == "ship":
        d.polygon([(x + 4, y + s - 10), (x + s - 4, y + s - 10), (x + s - 9, y + s - 4),
                   (x + 9, y + s - 4)], fill=NAVY)
        d.rectangle([x + s // 2 - 2, y + 7, x + s // 2 + 2, y + s - 12], fill=INK)
        d.polygon([(x + s // 2 + 2, y + 7), (x + s // 2 + 12, y + 15),
                   (x + s // 2 + 2, y + 15)], fill=RED)
        d.line([(x + 4, y + s - 1), (x + s - 4, y + s - 1)], fill=TEAL, width=2)
    elif kind == "stars":
        d.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], fill=(0, 51, 153))
        for k in range(8):
            import math
            a = math.pi * 2 * k / 8 - math.pi / 2
            px = c[0] + int(9 * math.cos(a))
            py = c[1] + int(9 * math.sin(a))
            d.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255, 204, 0))
    elif kind == "atom":
        d.ellipse([c[0] - 2, c[1] - 2, c[0] + 2, c[1] + 2], fill=RED)
        for ang in (0, 60, 120):
            import math
            a = math.radians(ang)
            d.ellipse([x + 4, y + 7, x + s - 4, y + s - 7], outline=INK, width=1)
            break
        d.ellipse([x + 5, y + 10, x + s - 5, y + s - 10], outline=INK, width=1)
        d.ellipse([x + 10, y + 5, x + s - 10, y + s - 5], outline=INK, width=1)
    elif kind == "car":
        d.rounded_rectangle([x + 4, y + 12, x + s - 4, y + 21], radius=4, fill=TEAL)
        d.polygon([(x + 9, y + 12), (x + 12, y + 6), (x + s - 12, y + 6),
                   (x + s - 9, y + 12)], fill=TEAL)
        d.ellipse([x + 8, y + 20, x + 14, y + 26], fill=INK)
        d.ellipse([x + s - 14, y + 20, x + s - 8, y + 26], fill=INK)


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
    offsets = {1: (-16, 10), 2: (16, -8)}
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
    text(d, (x0 + w // 2, y0 + h - 11), labels, F_TL, fill=GREY, anchor="ma")


# ---------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([4, 4, W - 5, H - 5], outline=INK, width=2)

    # masthead
    y = 14
    text(d, (M, y), "THE WORLD IN ONE DAY", F_MAST, anchor="la")
    text(d, (W - M, y + 6), "SATURDAY", F_DATE, anchor="ra")
    text(d, (W - M, y + 26), "21 NOVEMBER 2026", F_DATE, anchor="ra")
    y = 62
    hline(d, y, width=2)
    text(d, (M, y + 5), f"{STORY_TOTAL} STORIES  •  6 CONTINENTS  •  ONE DAY",
         F_SUB, anchor="la")
    text(d, (W - M, y + 5), "CODE-DRAWN  •  NO PHOTOS", F_SUB, fill=GREY, anchor="ra")
    y = 86
    hline(d, y, width=1)

    # region band (computed from the story lists)
    regions = ["N AMERICA", "S AMERICA", "EUROPE", "AFRICA", "ASIA", "OCEANIA", "WORLD"]
    counts = {r: 0 for r in regions}
    for s in LEADS:
        counts[s["region"]] += 1
    for _, _, _, r in CARDS:
        counts[r] += 1
    for _, r in ALSO:
        counts[r] += 1
    for _, r in TICKER:
        counts[r] += 1
    band = "   ".join(f"{r} {counts[r]}" for r in regions)
    text(d, (W // 2, 96), band, F_BAND, fill=NAVY, anchor="ma")
    hline(d, 106, width=1)

    # leads: 3 columns
    colw = (CW - 2 * 8) // 3
    ly = 112
    for i, lead in enumerate(LEADS):
        x = M + i * (colw + 8)
        draw_art(d, lead["art"], x, ly, colw, 88)
        text(d, (x, ly + 94), lead["kicker"], F_TLB, fill=RED, anchor="la")
        yy = ly + 112
        for ln in wrap(d, lead["head"], F_LEAD, colw):
            text(d, (x, yy), ln, F_LEAD, anchor="la")
            yy += 20
        yy += 2
        for ln in wrap(d, lead["sub"], F_LEADSUB, colw):
            text(d, (x, yy), ln, F_LEADSUB, anchor="la")
            yy += 13
        if i < 2:
            d.line([(x + colw + 4, ly), (x + colw + 4, ly + 200)], fill=GREY, width=1)
    hline(d, 316, width=1)

    # cards: 4 cols x 2 rows
    cardw = (CW - 3 * 6) // 4
    cardh = 88
    for i, (head, sub, kind, _r) in enumerate(CARDS):
        row, col = divmod(i, 4)
        x = M + col * (cardw + 6)
        yy = 322 + row * (cardh + 6)
        icon(d, kind, x, yy + 2)
        tx = x + 36
        tw = cardw - 36
        lines = wrap(d, head, F_CARD, tw)
        hy = yy + 2
        for ln in lines[:1]:
            text(d, (tx, hy), ln, F_CARD, anchor="la")
        sy = yy + 16
        for ln in wrap(d, sub, F_CARDSUB, tw)[:4]:
            text(d, (tx, sy), ln, F_CARDSUB, anchor="la")
            sy += 11
    hline(d, 500, width=1)

    # map
    text(d, (M, 506), "WHERE IT HAPPENED", F_SEC, anchor="la")
    text(d, (W - M, 506), "NUMBERED PINS = LEADS, CARDS & ALSO LIST", F_TL, fill=GREY, anchor="ra")
    draw_map(d, M, 522, CW, 92)
    hline(d, 616, width=1)

    # ALSO list: 28 items, 2 columns x 14
    text(d, (M, 622), f"ALSO TODAY  —  {len(ALSO)} MORE STORIES", F_SEC, anchor="la")
    colw2 = (CW - 16) // 2
    row_h = 11
    for i, (txt, _r) in enumerate(ALSO):
        col = 0 if i < 14 else 1
        row = i if i < 14 else i - 14
        x = M + col * (colw2 + 16)
        yy = 638 + row * row_h
        num = 12 + i
        text(d, (x, yy), f"{num}.", F_ALSONUM, fill=RED, anchor="la")
        lines = wrap(d, txt, F_ALSO, colw2 - 24)
        text(d, (x + 24, yy), lines[0], F_ALSO, anchor="la")
    hline(d, 802, width=1)

    # by the numbers
    text(d, (M, 808), "BY THE NUMBERS", F_SEC, anchor="la")
    numw = CW // len(NUMBERS)
    for i, (val, lab) in enumerate(NUMBERS):
        x = M + i * numw
        text(d, (x + numw // 2, 826), val, F_NUM, fill=DARKRED, anchor="ma")
        text(d, (x + numw // 2, 846), lab, F_NUMLAB, fill=GREY, anchor="ma")
    hline(d, 860, width=1)

    # timeline
    text(d, (M, 866), "SATURDAY, IN UTC", F_TLB, fill=RED, anchor="la")
    tl = "   •   ".join(f"{t} {s}" for t, s in TIMELINE)
    lines = wrap(d, tl, F_TL, CW - 150)
    yy = 866
    for ln in lines:
        text(d, (M + 150, yy), ln, F_TL, anchor="la")
        yy += 12
    hline(d, 892, width=1)

    # markets band
    text(d, (W // 2, 898), MARKETS, F_TLB, anchor="ma")
    hline(d, 916, width=2)

    # date check + how sure
    dc_y = 922
    half = (CW - 8) // 2
    d.rectangle([M, dc_y, M + half, dc_y + 62], outline=INK, width=1)
    text(d, (M + 6, dc_y + 4), "DATE CHECK", F_DCB, fill=RED, anchor="la")
    yy = dc_y + 18
    for ln in wrap(d, DATE_CHECK_LEFT, F_DC, half - 12):
        text(d, (M + 6, yy), ln, F_DC, anchor="la")
        yy += 11
    x2 = M + half + 8
    d.rectangle([x2, dc_y, x2 + half, dc_y + 62], outline=INK, width=1)
    text(d, (x2 + 6, dc_y + 4), "NOT YET  •  HOW SURE", F_DCB, fill=RED, anchor="la")
    yy = dc_y + 18
    for ln in wrap(d, DATE_CHECK_RIGHT, F_DC, half - 12):
        text(d, (x2 + 6, yy), ln, F_DC, anchor="la")
        yy += 11
    yy += 1
    text(d, (x2 + 6, yy), "SOLID = 2+ sources  •  DEVELOPING = still moving",
         F_DC, fill=GREY, anchor="la")

    # footer: ticker + sources
    hline(d, 992, width=1)
    tick = ("TICKER  •  Europe youth cost-of-living protests  •  Saudi storm warning to Tue  "
            "•  Verstappen FIA probe  •  Ebola 400-500 cases/week  •  Nasdaq down on year  "
            "•  COP31: 35% electrify by 2035")
    text(d, (M, 997), tick, F_TICK, anchor="la")
    text(d, (M, 1010), SOURCES, F_FOOT, fill=GREY, anchor="la")
    return img


def main():
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
