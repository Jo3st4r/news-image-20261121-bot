#!/usr/bin/env python3
"""Render the news-image-20261121 poster: 50 real stories from Saturday
21 November 2026 on one 1024x1024 page.

Layout (newspaper front page, my own design):
  masthead -> 3 lead stories -> around-the-world band -> 47 more stories -> date check
The renderer is deterministic: fixed strings, fixed colours, no clock, no random.
Run:  python3 tools/render.py        (writes assets/entry.png)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAPER = (246, 241, 231)
INK = (22, 21, 19)
RED = (179, 32, 44)
NAVY = (24, 38, 64)
GREY = (110, 104, 92)
LIGHT = (255, 255, 255)
RULE = (200, 190, 170)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_text(draw, text, fnt, max_w):
    """Return text shortened with an ellipsis so it fits max_w pixels."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    ell = "..."
    while text and draw.textlength(text + ell, font=fnt) > max_w:
        text = text[:-1]
    return text + ell


# --- colours per beat -------------------------------------------------------
C_JUSTICE = (96, 44, 140)
C_POLITICS = (26, 84, 160)
C_MARKETS = (18, 120, 70)
C_CONFLICT = (179, 32, 44)
C_HEALTH = (12, 130, 130)
C_SPORT = (210, 110, 10)
C_TECH = (110, 60, 180)
C_CLIMATE = (40, 130, 50)
C_INDIA = (190, 110, 0)
C_SCIENCE = (0, 130, 160)
C_WORLD = (90, 90, 90)

LEADS = [
    {
        "num": "1",
        "kicker": "JUSTICE  ·  THE HAGUE",
        "color": C_JUSTICE,
        "headline": "World Court: Myanmar committed genocide",
        "summary": "First time the ICJ has held a state responsible; it orders Rohingya refugees home.",
    },
    {
        "num": "2",
        "kicker": "CONFLICT  ·  POLAND",
        "color": C_CONFLICT,
        "headline": "Russian missiles land in Poland",
        "summary": "Two missiles and a drone come down in the east; Warsaw calls it a deliberate provocation, NATO a grave violation.",
    },
    {
        "num": "3",
        "kicker": "MARKETS  ·  NEW YORK",
        "color": C_MARKETS,
        "headline": "S&P 500 and Dow slide into correction",
        "summary": "AI sell-off deepens: the Nasdaq loses over 5% and erases its 2026 gains; the Nikkei falls 5.06%.",
    },
]

# 47 more stories: (headline, beat colour). Every headline was checked
# against reporting from Reuters, BBC, AP, CNN, IANS, UN News or The Guardian.
GRID = [
    ("UK and EU sign food, carbon and youth-mobility deals", C_POLITICS),
    ("Trump, Xi, Putin leave Shenzhen summit with little done", C_POLITICS),
    ("Iran war nears ninth month; Trump in no rush to decide", C_CONFLICT),
    ("Saudi coalition hits Houthi missiles; 41 killed in strikes", C_CONFLICT),
    ("Cancer pill shrinks tumours in 60.7% of patients", C_HEALTH),
    ("Cyclone Akvan crosses Odisha coast; 100,000 evacuated", C_CLIMATE),
    ("Anthropic IPO raises $81.3bn, then shares slide 11%", C_MARKETS),
    ("Nvidia sinks to 52-week low as SEC probes accounting", C_MARKETS),
    ("Gold falls 4%, Bitcoin down 24% in a month", C_MARKETS),
    ("Sensex rallies 898 points, defying global sell-off", C_MARKETS),
    ("Rahul closes on century as India fight back in Wellington", C_SPORT),
    ("Pakistan beat Sri Lanka by 8 wickets, clinch series", C_SPORT),
    ("England beat Australia by 97 runs in third ODI", C_SPORT),
    ("South Africa beat Bangladesh by nine wickets", C_SPORT),
    ("Zimbabwe beat Afghanistan by 57 runs", C_SPORT),
    ("India U17 qualify for AFC U17 Asian Cup 2027", C_SPORT),
    ("Bengaluru FC go top of ISL with 2-0 win", C_SPORT),
    ("India A thrash Nepal by 306 runs in Rising Stars", C_SPORT),
    ("Zverev reaches ATP Finals semi-finals", C_SPORT),
    ("Lyon end Arsenal's unbeaten run, 2-0", C_SPORT),
    ("Firouzja wins Total Chess World Championship Tour", C_SPORT),
    ("Carlsen forfeits rapid games at chess event", C_SPORT),
    ("Modi opens first SCO Civilisational Dialogue Forum", C_INDIA),
    ("Court allows Deepathoon lamp lighting, one-time only", C_INDIA),
    ("Indian man jailed 19 years over plot to kill Sikh leader", C_INDIA),
    ("Top court rejects Tamil Nadu pleas on Cauvery water", C_INDIA),
    ("UN warns hunger aid faces funding shortfall", C_WORLD),
    ("UN pledges $52m for schooling in crisis countries", C_WORLD),
    ("COP31 spills into overtime as fossil-fuel fight stalls deal", C_CLIMATE),
    ("Somalia gives UAE envoy 72 hours to leave", C_WORLD),
    ("Iraq agrees base handover deal with Kataib Hezbollah", C_CONFLICT),
    ("Marathon champion Jepchirchir banned 3 years for doping", C_SPORT),
    ("Bolsonaro taken to hospital with severe stomach pain", C_WORLD),
    ("Suicide bombing kills 5 at Pakistan checkpoint", C_CONFLICT),
    ("Trump: ban US firms building AI centres abroad", C_TECH),
    ("Trump: close to Mexico deal; more work on Canada", C_POLITICS),
    ("Record Rs 1.01 lakh crore flows into Indian stocks", C_MARKETS),
    ("NSE becomes world's fifth-largest exchange operator", C_MARKETS),
    ("2027 Hyundai Elantra unveiled at LA Auto Show", C_TECH),
    ("JPMorgan, Visa, Mastercard hit in vendor cyberattack", C_TECH),
    ("Palisades Fire: jury convicts man who started blaze", C_WORLD),
    ("India walk out of Blind Cricket Asia Cup ceremony", C_SPORT),
    ("IPL 2027 mini auction set for 16 December in Goa", C_SPORT),
    ("Lamar Jackson out 6-10 weeks with injury", C_SPORT),
    ("Dhoni to take CSK mentor role in 2027", C_SPORT),
    ("Delhi Capitals name Jayawardene WPL cricket chief", C_SPORT),
    ("Aadya Budhia, 15, stuns second seed in squash quarters", C_SPORT),
]

TIMELINE = ["WELLINGTON", "ODISHA", "ANTALYA", "THE HAGUE", "BRUSSELS", "NEW YORK"]


def draw_masthead(d):
    x0, x1 = 28, W - 28
    title = "THE WORLD IN ONE IMAGE"
    f_title = font(SERIF_B, 52)
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 22), title, font=f_title, fill=INK)
    d.line([(x0, 88), (x1, 88)], fill=RED, width=4)
    f_date = font(SANS_B, 18)
    left = "SATURDAY, 21 NOVEMBER 2026"
    right = "50 STORIES  ·  ONE PAGE"
    d.text((x0, 98), left, font=f_date, fill=INK)
    rw = d.textlength(right, font=f_date)
    d.text((x1 - rw, 98), right, font=f_date, fill=RED)
    d.line([(x0, 126), (x1, 126)], fill=RULE, width=1)


def draw_leads(d, y):
    """Three stacked lead rows; returns the y after the section."""
    x0, x1 = 28, W - 28
    row_h = 78
    for lead in LEADS:
        # number chip
        d.rectangle([x0, y + 6, x0 + 46, y + 52], fill=lead["color"])
        num = lead["num"]
        f_num = font(SANS_B, 28)
        nw = d.textlength(num, font=f_num)
        d.text((x0 + (46 - nw) / 2, y + 10), num, font=f_num, fill=LIGHT)
        tx = x0 + 60
        f_kick = font(SANS_B, 13)
        d.text((tx, y + 2), lead["kicker"], font=f_kick, fill=lead["color"])
        f_head = font(SANS_B, 27)
        head = fit_text(d, lead["headline"], f_head, x1 - tx)
        d.text((tx, y + 20), head, font=f_head, fill=INK)
        f_sum = font(SANS, 15)
        summ = fit_text(d, lead["summary"], f_sum, x1 - tx)
        d.text((tx, y + 52), summ, font=f_sum, fill=(60, 56, 50))
        y += row_h
        if lead is not LEADS[-1]:
            d.line([(x0, y - 6), (x1, y - 6)], fill=RULE, width=1)
    return y


def draw_timeline(d, y):
    x0, x1 = 28, W - 28
    band_h = 64
    d.rectangle([x0, y, x1, y + band_h], fill=NAVY)
    f_lab = font(SANS_B, 13)
    label = "AROUND THE WORLD IN ONE DAY"
    d.text((x0 + 14, y + 5), label, font=f_lab, fill=(255, 214, 120))
    # city stops along a line
    line_y = y + 34
    d.line([(x0 + 14, line_y), (x1 - 14, line_y)], fill=(140, 160, 200), width=2)
    n = len(TIMELINE)
    span = (x1 - 14) - (x0 + 14)
    f_city = font(SANS_B, 12)
    for i, city in enumerate(TIMELINE):
        cx = x0 + 14 + (span * i // (n - 1) if n > 1 else 0)
        d.ellipse([cx - 5, line_y - 5, cx + 5, line_y + 5], fill=(255, 214, 120))
        cw = d.textlength(city, font=f_city)
        lx = min(max(cx - cw / 2, x0 + 8), x1 - cw - 8)
        d.text((lx, line_y + 9), city, font=f_city, fill=LIGHT)
    return y + band_h


def draw_grid(d, y, bottom):
    x0, x1 = 28, W - 28
    f_sec = font(SANS_B, 14)
    section = "THE DAY IN 47 MORE STORIES"
    d.text((x0, y + 2), section, font=f_sec, fill=RED)
    d.line([(x0 + d.textlength(section, font=f_sec) + 10, y + 10),
            (x1, y + 10)], fill=RULE, width=1)
    top = y + 24
    rows = (len(GRID) + 1) // 2
    row_h = (bottom - top) / rows
    f_item = font(SANS_B, 13)
    col_w = (x1 - x0 - 24) / 2
    for idx, (headline, color) in enumerate(GRID):
        r, c = divmod(idx, 2)
        gx = x0 + c * (col_w + 24)
        gy = top + r * row_h
        cy = gy + row_h / 2
        d.rectangle([gx, cy - 4, gx + 8, cy + 4], fill=color)
        text = fit_text(d, headline, f_item, col_w - 16)
        d.text((gx + 14, cy - 8), text, font=f_item, fill=INK)


def draw_footer(d):
    x0, x1 = 28, W - 28
    d.line([(x0, H - 44), (x1, H - 44)], fill=RULE, width=1)
    f_foot = font(SANS, 12)
    line1 = "DATE CHECK: every story first reported 20-21 Nov 2026  ·  Sources: Reuters, BBC, AP, CNN, IANS, UN News, The Guardian"
    w1 = d.textlength(line1, font=f_foot)
    d.text(((W - w1) / 2, H - 38), line1, font=f_foot, fill=GREY)
    line2 = "THE WORLD IN ONE IMAGE  ·  SATURDAY 21 NOVEMBER 2026  ·  make.fun news-image-20261121"
    w2 = d.textlength(line2, font=f_foot)
    d.text(((W - w2) / 2, H - 20), line2, font=f_foot, fill=GREY)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    y = draw_leads(d, 140)
    y = draw_timeline(d, y + 8)
    draw_grid(d, y + 6, H - 52)
    draw_footer(d)
    out = os.path.join(ROOT, "assets", "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, format="PNG", compress_level=9)
    return out


if __name__ == "__main__":
    path = render()
    print("wrote", path)
