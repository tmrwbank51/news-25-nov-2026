#!/usr/bin/env python3
"""Code-drawn newspaper front page for Wednesday 25 November 2026.

The image is rendered entirely with PIL primitives and text.  It uses no
network access and no photographs, and the same code always produces the
same PNG bytes.
"""

import os
from PIL import Image, ImageDraw, ImageFont


W = H = 1024
PAPER = (246, 238, 218)
PANEL = (255, 250, 238)
INK = (23, 19, 13)
MUTED = (92, 80, 64)
RULE = (124, 104, 74)
RED = (178, 35, 24)
BLUE = (31, 78, 120)
GREEN = (39, 103, 71)
GOLD = (150, 104, 24)
SEA = (190, 214, 224)
LAND = (222, 205, 164)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def text_w(draw, text, fnt):
    return draw.textbbox((0, 0), text, font=fnt)[2]


def wrap(draw, text, fnt, max_width, max_lines=None):
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and text_w(draw, last + "…", fnt) > max_width:
            last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
        lines[-1] = last + "…"
    return lines


def draw_lines(draw, x, y, lines, fnt, fill=INK, leading=None, align="left", width=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in lines:
        if align == "center" and width:
            xx = x + (width - text_w(draw, line, fnt)) / 2
        elif align == "right" and width:
            xx = x + width - text_w(draw, line, fnt)
        else:
            xx = x
        draw.text((xx, y), line, font=fnt, fill=fill)
        y += leading
    return y


def badge(draw, x, y, label):
    colors = {
        "CONFIRMED": GREEN,
        "OFFICIAL": BLUE,
        "REPORTED": GOLD,
        "CLAIM": RED,
    }
    fnt = font(SANS_B, 8)
    w = text_w(draw, label, fnt) + 10
    draw.rounded_rectangle((x, y, x + w, y + 13), radius=3, fill=colors[label])
    draw.text((x + 5, y + 2), label, font=fnt, fill=(255, 255, 255))
    return w


def number_badge(draw, x, y, n, r=11):
    draw.ellipse((x, y, x + 2 * r, y + 2 * r), fill=RED)
    fnt = font(SANS_B, 10 if n < 10 else 8)
    tw = text_w(draw, str(n), fnt)
    draw.text((x + r - tw / 2, y + r - fnt.size / 2 - 1), str(n), font=fnt, fill=(255, 255, 255))


def panel(draw, box, fill=PANEL):
    draw.rectangle(box, fill=fill, outline=RULE, width=1)


def meta_line(draw, x, y, label, source):
    w = badge(draw, x, y, label)
    draw.text((x + w + 6, y + 2), source, font=font(SANS_B, 8), fill=MUTED)


TOP3 = [
    {
        "n": 1,
        "region": "MIDDLE EAST · HORMUZ",
        "badge": "CLAIM",
        "source": "Reuters / Iran state media",
        "headline": "IRAN SAYS 2 TANKERS HIT MINES",
        "body": "Tehran said two tankers struck mines and caught fire. No independent confirmation; oil rose.",
        "art": "hormuz",
    },
    {
        "n": 2,
        "region": "OCEANIA · SECURITY",
        "badge": "CONFIRMED",
        "source": "AP / Reuters",
        "headline": "SOLOMONS PICK AUSTRALIA, BAR BASES",
        "body": "Albanese and Wale signed in Canberra: Australia is primary partner; no foreign base allowed.",
        "art": "treaty",
    },
    {
        "n": 3,
        "region": "SPACE · TIANGONG",
        "badge": "CONFIRMED",
        "source": "AP / CMSA",
        "headline": "PAKISTAN'S FIRST ASTRONAUT IN ORBIT",
        "body": "Shenzhou-24 docked at 03:56 UTC. Muhammad Zeeshan Ali became Tiangong's first foreign crew member.",
        "art": "space",
    },
]

GRID = [
    (4, "EUROPE · ENERGY", "CONFIRMED", "Reuters", "RUSSIAN STRIKES CUT POWER IN 5 REGIONS", "Zaporizhzhia plant lost external power for 17th time in 2026."),
    (5, "EUROPE · KYIV", "OFFICIAL", "Reuters", "MISSILES HIT KYIV LATE WEDNESDAY", "Two sites east of Dnipro struck; casualties possible."),
    (6, "EUROPE · AIR WAR", "CLAIM", "Reuters", "UKRAINE SAYS 5 JETS KNOCKED OUT", "Kyiv claimed 3 MiG-31s, 2 Su-34s at Savasleyka."),
    (7, "MIDDLE EAST · GAZA", "CONFIRMED", "Reuters / AFP", "STRIKE KILLS HAMAS CHIEF + FAMILY", "Abuelouf, wife and 2 daughters killed in Gaza City."),
    (8, "AMERICAS · TRADE", "OFFICIAL", "Reuters / AP", "US PROPOSES TARIFFS ON 14 PARTNERS", "Section 301 plan; China faces highest added rate."),
    (9, "AMERICAS · MARKETS", "CONFIRMED", "Reuters / AP", "NVIDIA SLIDES AGAIN -3.9%", "Closed $149.30 after Monday's +31.5% surge."),
    (10, "AMERICAS · COLOMBIA", "CONFIRMED", "AP / BBC", "HOSTAGES FREED IN CARTAGENA", "All rescued early Wednesday; one gunman killed."),
    (11, "ASIA-PACIFIC · INDONESIA", "OFFICIAL", "AP", "9 DEAD, 17 TRAPPED IN GOLD MINE", "325 searched 100 m Bogor shaft on Wednesday."),
    (12, "SOUTH ASIA · LABOUR", "CONFIRMED", "AP", "WAGE UP 36% TO 17,000 TAKA", "Garment board acted after weeks of protests."),
    (13, "AFRICA · EGYPT", "CONFIRMED", "AP / BBC", "CAIRO TANKER FIRE KILLS 30+", "Ring Road blaze toll rose during Wednesday."),
]

ALSO = [
    (14, "OFFICIAL", "Reuters", "ITALY REBUKES UKRAINE OVER LIBYA SHIPS"),
    (15, "OFFICIAL", "Reuters", "IRAN VOWS TO WITHSTAND US NAVAL BLOCKADE"),
    (16, "REPORTED", "FT / Reuters", "US SHELVES RUSSIA BUSINESS-DEAL PLAN"),
    (17, "OFFICIAL", "Reuters", "IS ATTACK KILLS 2 SYRIAN SECURITY STAFF"),
    (18, "OFFICIAL", "Reuters", "UN EVACUATES 10 EBOLA WORKERS IN CONGO"),
    (19, "REPORTED", "Reuters", "NIGERIA GOVERNOR VISITS BORGU AFTER TUE ATTACK"),
    (20, "OFFICIAL", "Reuters", "SENEGAL MPS VOTE 128-9 ON BUDGET ROW"),
    (21, "OFFICIAL", "Reuters", "KENYA CULT LEADER CONVICTED ON NEW CHARGES"),
    (22, "OFFICIAL", "Reuters", "FIRST GENERIC HIV DRUGS ARRIVE IN ZAMBIA"),
    (23, "OFFICIAL", "Reuters", "INDIA SAYS DAS TOLD NOT TO USE PASSPORT"),
    (24, "OFFICIAL", "Reuters", "THAILAND, MYANMAR AGREE RIVER MONITORS"),
    (25, "OFFICIAL", "Reuters / KCNA", "NORTH KOREA EXPELS SWISS DIPLOMAT"),
    (26, "OFFICIAL", "Reuters", "TAIWAN SAYS 15% US TARIFF SHOULD HOLD"),
    (27, "OFFICIAL", "Reuters", "CANARIES SEE RECORD 2,100+ MIGRANT ARRIVALS"),
    (28, "OFFICIAL", "Reuters / BTA", "BULGARIA INTERCEPTS BOAT WITH 35 MIGRANTS"),
    (29, "CONFIRMED", "Reuters", "GREEK WORKERS STRIKE OVER WAGES, SERVICES"),
    (30, "OFFICIAL", "Reuters", "EUROPE PROPOSES €50BN QUANTUM TECH FUND"),
    (31, "OFFICIAL", "Reuters", "BARCELONA BEAT SABAH 4-1 IN EUROPE"),
    (32, "OFFICIAL", "Reuters", "MERZ DEFENDS UKRAINE AID, WARNS RUSSIA"),
    (33, "OFFICIAL", "Reuters", "POLISH OFFICIAL CALLS FOR BORDER NO-FLY ZONE"),
    (34, "OFFICIAL", "Reuters / BEA", "US GDP REVISED TO 4.3%; CORE PCE 3.3%"),
    (35, "CONFIRMED", "AP", "KILMAR ÁBREGO GARCÍA ARRIVES IN SPAIN"),
    (36, "OFFICIAL", "AP", "US ARMY DETONATES LEAD-AZIDE STOCKPILE"),
    (37, "CONFIRMED", "AP / BBC", "MACY'S POSTPONES THANKSGIVING PARADE"),
    (38, "OFFICIAL", "Reuters", "JUDGES URGE DROPPING NETANYAHU BRIBERY CASE"),
    (39, "OFFICIAL", "Reuters", "FCC AUTHORISES 1M SPACEX DATA SATELLITES"),
]

TIMELINE = [
    ("00:18", "Shenzhou-24 lifts off"),
    ("03:56", "Docks with Tiangong"),
    ("06:35", "Crew enters station"),
    ("13:30", "US GDP/PCE data"),
    ("14:32", "India passport statement"),
    ("18:23", "UN Congo evacuation"),
    ("23:31", "Taiwan tariff pledge"),
]

REGION_COUNTS = [
    ("Europe", 11),
    ("Americas", 8),
    ("Africa", 6),
    ("Middle East", 5),
    ("Asia-Pacific", 4),
    ("South Asia", 2),
    ("Space", 2),
    ("Oceania", 1),
]


def draw_hormuz(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SEA)
    draw.polygon([(x0, y0), (x0 + 95, y0), (x0 + 70, y0 + 28), (x0 + 120, y0 + 38), (x0 + 92, y1), (x0, y1)], fill=LAND, outline=RULE)
    draw.polygon([(x1, y0), (x1 - 70, y0), (x1 - 105, y0 + 24), (x1 - 65, y0 + 42), (x1 - 95, y1), (x1, y1)], fill=LAND, outline=RULE)
    draw.arc((x0 + 82, y0 + 8, x1 - 62, y1 + 18), start=200, end=340, fill=BLUE, width=2)
    for cx, cy in [(x0 + 145, y0 + 34), (x0 + 205, y0 + 24)]:
        draw.polygon([(cx - 28, cy + 8), (cx + 28, cy + 8), (cx + 18, cy + 16), (cx - 18, cy + 16)], fill=INK)
        draw.rectangle((cx - 12, cy, cx + 8, cy + 8), fill=RED)
    for cx, cy in [(x0 + 122, y0 + 48), (x0 + 178, y0 + 44), (x0 + 238, y0 + 36)]:
        draw.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=RED)
        for dx, dy in [(-7, 0), (7, 0), (0, -7), (0, 7)]:
            draw.line((cx, cy, cx + dx, cy + dy), fill=RED, width=1)


def draw_treaty(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(238, 231, 205))
    # Australia flag, simplified.
    draw.rectangle((x0 + 18, y0 + 12, x0 + 92, y0 + 42), fill=BLUE, outline=INK)
    draw.line((x0 + 18, y0 + 12, x0 + 55, y0 + 27), fill=(255, 255, 255), width=3)
    draw.line((x0 + 55, y0 + 12, x0 + 18, y0 + 27), fill=(255, 255, 255), width=3)
    draw.line((x0 + 36, y0 + 12, x0 + 36, y0 + 27), fill=RED, width=3)
    for sx, sy in [(70, 18), (80, 28), (66, 34), (84, 16)]:
        draw.ellipse((x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3), fill=(255, 255, 255))
    # Solomon Islands flag, simplified diagonal.
    draw.rectangle((x1 - 92, y0 + 12, x1 - 18, y0 + 42), fill=(31, 105, 63), outline=INK)
    draw.polygon([(x1 - 92, y0 + 42), (x1 - 18, y0 + 12), (x1 - 18, y0 + 42)], fill=BLUE)
    draw.line((x1 - 92, y0 + 42, x1 - 18, y0 + 12), fill=(245, 197, 66), width=4)
    for sx, sy in [(-82, 17), (-72, 17), (-82, 25), (-72, 25), (-77, 21)]:
        draw.ellipse((x1 + sx, y0 + sy, x1 + sx + 3, y0 + sy + 3), fill=(255, 255, 255))
    # Treaty document.
    dx = (x0 + x1) // 2 - 34
    draw.rectangle((dx, y0 + 8, dx + 68, y1 - 6), fill=(255, 255, 255), outline=INK)
    for i in range(4):
        draw.line((dx + 10, y0 + 20 + i * 8, dx + 58, y0 + 20 + i * 8), fill=MUTED, width=1)
    draw.ellipse((dx + 44, y1 - 22, dx + 60, y1 - 6), fill=RED)


def draw_space(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(18, 28, 52))
    for sx, sy in [(30, 12), (70, 24), (120, 10), (180, 20), (250, 12), (285, 30), (210, 38)]:
        draw.ellipse((x0 + sx, y0 + sy, x0 + sx + 2, y0 + sy + 2), fill=(255, 255, 255))
    draw.arc((x0 + 24, y0 + 8, x1 - 24, y1 + 28), start=190, end=350, fill=(150, 190, 230), width=2)
    draw.ellipse((x0 + 132, y1 - 18, x0 + 196, y1 + 18), fill=(64, 116, 176))
    cx = x0 + 205
    cy = y0 + 24
    draw.rectangle((cx - 34, cy, cx + 34, cy + 8), fill=(220, 226, 232))
    draw.rectangle((cx - 8, cy - 8, cx + 8, cy + 16), fill=(220, 226, 232))
    draw.rectangle((cx - 58, cy - 3, cx - 38, cy + 11), fill=(92, 140, 200))
    draw.rectangle((cx + 38, cy - 3, cx + 58, cy + 11), fill=(92, 140, 200))
    rx = x0 + 78
    ry = y0 + 28
    draw.polygon([(rx, ry - 20), (rx + 9, ry + 8), (rx - 9, ry + 8)], fill=(240, 240, 240))
    draw.polygon([(rx - 4, ry + 8), (rx + 4, ry + 8), (rx, ry + 20)], fill=(245, 160, 60))


def draw_top3(draw):
    x = 22
    y = 172
    w = 322
    h = 170
    gap = 7
    for i, s in enumerate(TOP3):
        xx = x + i * (w + gap)
        panel(draw, (xx, y, xx + w, y + h))
        art_box = (xx + 8, y + 8, xx + w - 8, y + 52)
        if s["art"] == "hormuz":
            draw_hormuz(draw, art_box)
        elif s["art"] == "treaty":
            draw_treaty(draw, art_box)
        else:
            draw_space(draw, art_box)
        number_badge(draw, xx + 8, y + 58, s["n"], r=10)
        draw.text((xx + 34, y + 61), s["region"], font=font(SANS_B, 8), fill=RED)
        hy = draw_lines(draw, xx + 8, y + 82, wrap(draw, s["headline"], font(SERIF_B, 15), w - 16, 2), font(SERIF_B, 15), leading=16)
        draw_lines(draw, xx + 8, hy + 2, wrap(draw, s["body"], font(SANS, 10), w - 16, 3), font(SANS, 10), leading=11)
        meta_line(draw, xx + 8, y + h - 18, s["badge"], s["source"])


def draw_grid(draw):
    x0 = 22
    y0 = 350
    w = 192
    h = 104
    gapx = 5
    gapy = 6
    accents = [RED, BLUE, GOLD, GREEN]
    for idx, (n, region, label, source, headline, body) in enumerate(GRID):
        col = idx % 5
        row = idx // 5
        x = x0 + col * (w + gapx)
        y = y0 + row * (h + gapy)
        panel(draw, (x, y, x + w, y + h))
        draw.rectangle((x, y, x + w, y + 4), fill=accents[idx % len(accents)])
        number_badge(draw, x + 6, y + 8, n, r=9)
        draw.text((x + 29, y + 11), region, font=font(SANS_B, 7), fill=RED)
        hy = draw_lines(draw, x + 7, y + 30, wrap(draw, headline, font(SERIF_B, 12), w - 14, 2), font(SERIF_B, 12), leading=13)
        draw_lines(draw, x + 7, hy + 2, wrap(draw, body, font(SANS, 9.5), w - 14, 3), font(SANS, 9.5), leading=11)
        meta_line(draw, x + 7, y + h - 16, label, source)


def draw_map(draw):
    x0, y0, x1, y1 = 22, 572, 672, 688
    panel(draw, (x0, y0, x1, y1), fill=(232, 238, 230))
    draw.text((x0 + 8, y0 + 5), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=RED)
    mx0, my0, mx1, my1 = x0 + 10, y0 + 24, x1 - 10, y1 - 7
    draw.rectangle((mx0, my0, mx1, my1), fill=SEA, outline=RULE)

    def proj(lon, lat):
        return (mx0 + (lon + 180) / 360 * (mx1 - mx0), my0 + (75 - lat) / 130 * (my1 - my0))

    continents = [
        [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 70), (-85, 66), (-80, 62), (-76, 35), (-81, 25), (-90, 21), (-97, 16), (-105, 20), (-114, 29), (-122, 37), (-124, 46), (-132, 56), (-152, 60)],
        [(-79, 9), (-72, 12), (-64, 10), (-52, 5), (-44, -3), (-35, -8), (-39, -13), (-48, -25), (-58, -35), (-65, -41), (-72, -50), (-74, -40), (-70, -20), (-75, -15), (-80, -5)],
        [(-10, 36), (-9, 43), (-2, 49), (5, 58), (10, 57), (18, 56), (21, 60), (30, 60), (28, 71), (45, 68), (50, 60), (40, 52), (30, 46), (23, 40), (19, 42), (12, 44), (3, 43), (-2, 37)],
        [(-17, 15), (-10, 31), (10, 37), (20, 32), (32, 31), (35, 24), (43, 12), (51, 12), (48, 5), (40, -6), (40, -18), (35, -26), (26, -34), (19, -34), (12, -18), (9, -1), (-8, 4), (-13, 8)],
        [(30, 36), (36, 36), (48, 30), (56, 26), (60, 25), (66, 25), (72, 20), (76, 10), (80, 13), (88, 22), (92, 16), (98, 10), (100, 6), (104, 1), (107, 12), (109, 15), (114, 22), (121, 25), (122, 31), (127, 40), (130, 42), (141, 50), (156, 52), (170, 60), (178, 65), (160, 70), (120, 72), (90, 75), (60, 69), (45, 60), (38, 47), (30, 41)],
        [(113, -22), (114, -34), (124, -33), (129, -32), (137, -35), (140, -38), (146, -39), (150, -37), (153, -27), (146, -19), (142, -11), (136, -15), (132, -11), (126, -14), (122, -17), (117, -20)],
    ]
    for poly in continents:
        draw.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND, outline=RULE)
    # Pacific islands near the Solomons pin.
    for lon, lat in [(147, -9), (155, -6), (160, -9), (167, -16)]:
        cx, cy = proj(lon, lat)
        draw.ellipse((cx - 3, cy - 2, cx + 3, cy + 2), fill=LAND, outline=RULE)
    pins = {
        1: (56, 26), 2: (160, -9), 3: (98, 40), 4: (32, 49), 6: (43, 55),
        7: (37, 33), 8: (-77, 39), 10: (-75, 10), 11: (107, -6), 12: (90, 24),
        13: (27, 27), 18: (25, -2), 20: (-14, 14), 23: (78, 21), 25: (127, 40),
        29: (22, 39), 34: (-98, 39),
    }
    for n, (lon, lat) in pins.items():
        cx, cy = proj(lon, lat)
        draw.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill=RED, outline=(255, 255, 255), width=1)
        fnt = font(SANS_B, 6)
        draw.text((cx - text_w(draw, str(n), fnt) / 2, cy - 3), str(n), font=fnt, fill=(255, 255, 255))
    # Legend and verification key, side by side so nothing is clipped.
    lx, ly, lx1, ly1 = 680, 572, 1002, 688
    panel(draw, (lx, ly, lx1, ly1))
    draw.text((lx + 8, ly + 5), "REGIONS", font=font(SANS_B, 11), fill=RED)
    yy = ly + 22
    for name, count in REGION_COUNTS:
        draw.text((lx + 8, yy), name, font=font(SANS, 8.5), fill=INK)
        draw.text((lx + 118, yy), str(count), font=font(SANS_B, 8.5), fill=INK)
        yy += 11
    hx = lx + 150
    draw.text((hx, ly + 5), "HOW SURE", font=font(SANS_B, 11), fill=RED)
    yy = ly + 22
    for label, note in [("CONFIRMED", "2+ outlets"), ("OFFICIAL", "agency / court"), ("REPORTED", "one outlet"), ("CLAIM", "one side says")]:
        w = badge(draw, hx, yy, label)
        draw.text((hx + w + 5, yy + 2), note, font=font(SANS, 7.5), fill=MUTED)
        yy += 16
    draw.text((hx, yy + 4), "Pins match story numbers.", font=font(SANS, 7.5), fill=MUTED)


def draw_also(draw):
    x0, y0, x1, y1 = 22, 696, 1002, 936
    panel(draw, (x0, y0, x1, y1))
    draw.text((x0 + 8, y0 + 6), "ALSO ON 25 NOVEMBER", font=font(SANS_B, 14), fill=RED)
    draw.text((x1 - 238, y0 + 8), "ONE LINE EACH · BADGE + SOURCE", font=font(SANS_B, 8), fill=MUTED)
    cols = 3
    col_w = (x1 - x0 - 24) // cols
    rows = 9
    start_y = y0 + 30
    row_h = 23
    for idx, (n, label, source, headline) in enumerate(ALSO):
        col = idx // rows
        row = idx % rows
        x = x0 + 8 + col * col_w
        y = start_y + row * row_h
        if col:
            draw.line((x - 6, y0 + 28, x - 6, y1 - 8), fill=(210, 196, 166), width=1)
        draw.text((x, y), str(n), font=font(SANS_B, 10), fill=RED)
        hx = x + (22 if n >= 10 else 15)
        draw.text((hx, y), headline, font=font(SANS_B, 9.5), fill=INK)
        draw.text((hx, y + 12), f"{label} · {source}", font=font(SANS, 7.5), fill=MUTED)


def draw_footer(draw):
    x0, y0, x1, y1 = 22, 944, 1002, 1008
    panel(draw, (x0, y0, x1, y1), fill=(238, 231, 205))
    draw.text((x0 + 8, y0 + 5), "DATE CHECK", font=font(SANS_B, 12), fill=RED)
    lines = [
        "Left out on purpose: Riyadh tower strike, Huawei verdict, Nepal quake, Senegal CAS title and England T20I (all Tue 24 Nov);",
        "South Korea minister resignation (Sun 22 Nov); Myanmar ICJ judgment (19 Nov); Mississippi plane crash (Tue 24 Nov).",
        "Not yet: Hong Kong fire anniversary (Thu 26 Nov). 25 Nov is the International Day for the Elimination of Violence against Women.",
    ]
    draw_lines(draw, x0 + 8, y0 + 21, lines, font(SANS, 9), fill=INK, leading=10)
    draw.text((x0 + 8, y1 - 11), "Sources: Reuters · AP · BBC · AFP · CMSA · BEA · KCNA · BTA · FT — drawn in code; no photographs.", font=font(SANS_B, 8), fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle((8, 8, W - 9, H - 9), outline=INK, width=2)
    draw.rectangle((14, 14, W - 15, H - 15), outline=RULE, width=1)

    draw.text((22, 18), "ONE DAY OF WORLD NEWS · ONE PICTURE", font=font(SANS_B, 11), fill=RED)
    draw.text((W - 150, 18), "39 STORIES", font=font(SANS_B, 11), fill=RED)
    title = "Wednesday 25 November 2026"
    tf = font(SERIF_B, 50)
    draw.text(((W - text_w(draw, title, tf)) / 2, 34), title, font=tf, fill=INK)
    counts = "39 STORIES · 7 REGIONS + SPACE · 12 FIELDS · EVERY STORY DATED WEDNESDAY 25 NOVEMBER 2026"
    cf = font(SANS_B, 13)
    draw.text(((W - text_w(draw, counts, cf)) / 2, 92), counts, font=cf, fill=INK)
    draw.line((22, 112, 1002, 112), fill=INK, width=2)

    # Timeline.
    draw.text((22, 118), "THE DAY IN UTC", font=font(SANS_B, 12), fill=RED)
    draw.text((1002 - 250, 120), "EVENT OR WIRE-REPORT TIMES", font=font(SANS_B, 7), fill=MUTED)
    ty = 148
    draw.line((34, ty, 990, ty), fill=INK, width=2)
    for i, (tm, ev) in enumerate(TIMELINE):
        cx = 84 + i * 145
        draw.ellipse((cx - 4, ty - 4, cx + 4, ty + 4), fill=RED)
        draw.text((cx - text_w(draw, tm, font(SANS_B, 10)) / 2, ty - 18), tm, font=font(SANS_B, 10), fill=INK)
        lines = wrap(draw, ev, font(SANS, 8), 132, 2)
        draw_lines(draw, cx - 66, ty + 7, lines, font(SANS, 8), fill=MUTED, leading=9, align="center", width=132)

    draw_top3(draw)
    draw_grid(draw)
    draw_map(draw)
    draw_also(draw)
    draw_footer(draw)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    img.save(out_path, format="PNG", optimize=False, compress_level=6)


if __name__ == "__main__":
    main()
