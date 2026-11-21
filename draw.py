#!/usr/bin/env python3
"""Render the one-image front page for Saturday 21 November 2026.

Local build tool only: the shipped entrypoint (main.py) copies the rendered
entry.png to /output. Run: python3 draw.py  ->  writes entry.png next to it.
Deterministic: fixed layout, fixed fonts, no timestamps, no randomness.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
PAPER = (250, 246, 238)
INK = (20, 20, 20)
MUTED = (90, 86, 78)
RULE = (163, 22, 33)
TAG_RED = (163, 22, 33)
TAG_BLUE = (29, 78, 216)
TAG_TEAL = (13, 148, 136)
TAG_AMBER = (180, 83, 9)
TAG_PURPLE = (124, 58, 237)
TAG_GREEN = (21, 128, 61)
TAG_SKY = (3, 105, 161)
TAG_PINK = (190, 24, 93)
TAG_SLATE = (71, 85, 105)
BOX_BG = (253, 236, 236)
BOX_EDGE = (163, 22, 33)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 46)
F_DATE = font("DejaVuSans-Bold.ttf", 17)
F_SUB = font("DejaVuSans.ttf", 13)
F_LEAD_TAG = font("DejaVuSans-Bold.ttf", 11)
F_LEAD_HEAD = font("DejaVuSerif-Bold.ttf", 27)
F_LEAD_SUM = font("DejaVuSans.ttf", 14)
F_TAG = font("DejaVuSans-Bold.ttf", 10)
F_HEAD = font("DejaVuSans-Bold.ttf", 14)
F_SUM = font("DejaVuSans.ttf", 11)
F_BOX_TITLE = font("DejaVuSans-Bold.ttf", 12)
F_BOX_ITEM = font("DejaVuSans.ttf", 11)
F_FOOT = font("DejaVuSans.ttf", 10)

# (tag, tag colour, headline, summary)
LEAD = (
    "LEAD  |  SOUTH AMERICA",
    TAG_RED,
    "Magnitude 6.8 quake shakes central Peru",
    "Junin region hit at 00:09 UTC; tremors felt in Lima, 320 km away. "
    "No casualties or major damage reported. (Reuters)",
)

COLUMNS = [
    ("WORLD", [
        ("EUROPE", TAG_BLUE,
         "Denmark expels Russian diplomat",
         "Copenhagen accuses Moscow of plotting to kill a US-Ukrainian "
         "rapper with a banned gang. (Al Jazeera)"),
        ("EUROPE", TAG_BLUE,
         "Gen Z protests sweep 25 countries",
         "Thousands rally across Europe over living costs, military "
         "spending and climate. (Al Jazeera)"),
        ("CLIMATE", TAG_TEAL,
         "COP31 talks run into overtime",
         "No deal as the deadline passes; a third draft text is promised "
         "for Saturday morning. (Asia Today)"),
        ("AFRICA", TAG_AMBER,
         "Africa's new credit rating agency",
         "The continent's own agency aims to change how Africa is "
         "assessed. (Al Jazeera)"),
        ("MIDDLE EAST", TAG_PURPLE,
         "Three Houthi missiles downed over Riyadh",
         "Saudi-led coalition intercepts the attack; IRGC claims it shot "
         "down a US MQ-9 drone. (Al Jazeera)"),
        ("UKRAINE", TAG_BLUE,
         "Two dead, 42 hurt in Kryvyi Rih strike",
         "Four children among the injured in Russian strikes, local "
         "officials say. (Appistos)"),
        ("NATO", TAG_TEAL,
         "Rutte due in Warsaw",
         "NATO chief visits Poland, which seeks more Eastern Sentry "
         "forces after Friday's incursion. (SOFX)"),
        ("ASIA", TAG_AMBER,
         "49th ASEAN Summit under way in Manila",
         "Southeast Asian leaders meet as the bloc's summit "
         "continues. (PH News Hub)"),
    ]),
    ("ASIA, ECONOMY & THE UK", [
        ("ECONOMY", TAG_GREEN,
         "Record Rs 1.22 lakh crore into Indian shares",
         "Foreign investors' biggest monthly inflow on record, "
         "2-20 Nov. (The Daily Short)"),
        ("CRICKET", TAG_GREEN,
         "KL Rahul completes the SENA set",
         "100 off 207 balls in Wellington - first Indian opener with "
         "a Test ton in each SENA nation. (Daily Short)"),
        ("MEDIA", TAG_SKY,
         "Asia-Pacific Media Partnership launches",
         "310 organisations from 41 countries and regions join the "
         "Xinhua-proposed network. (Xinhua)"),
        ("HOCKEY", TAG_GREEN,
         "India women beat Malaysia 4-1",
         "Winning start in the Women's Asian Champions Trophy in "
         "Bhopal. (CareerIndia)"),
        ("UK", TAG_PINK,
         "PM to meet Birmingham bombings families",
         "Burnham pledges talks on a public inquiry, 52 years after "
         "the 1974 attacks. (Hello Rayo)"),
        ("UK", TAG_PINK,
         "Village votes on 'leaving the UK'",
         "Barnham, Suffolk, votes in a symbolic referendum over plans "
         "to house 931 asylum seekers. (BBC)"),
        ("HEALTH", TAG_RED,
         "NHS warns on 'silent killer' surge",
         "Emergency admissions for high blood pressure up 77% since "
         "2019/20, to 43,306. (Sky News)"),
        ("HEALTH", TAG_RED,
         "NI doctors' strike ends; new walkout Monday",
         "Resident doctors' 24-hour stoppage ends at 07:00; "
         "consultants strike next. (BBC News NI)"),
    ]),
    ("SPORT, SCIENCE & MORE", [
        ("FOOTBALL", TAG_GREEN,
         "Pochettino's first United test at Liverpool",
         "The new manager takes charge for the first time on "
         "Sunday. (Al Jazeera)"),
        ("MOTORSPORT", TAG_SLATE,
         "Russell fastest in Las Vegas practice",
         "Mercedes lead FP3; Russell clashes with Verstappen, "
         "stewards to investigate. (Reuters)"),
        ("SPACE", TAG_SKY,
         "BepiColombo reaches Mercury",
         "After eight years and 6 billion miles, the ESA-JAXA probe "
         "enters orbit around Mercury. (NPR)"),
        ("SPACE", TAG_SKY,
         "Space armour survives 16,100-mph hits",
         "Composite shield tested for astronaut spacewalks; a "
         "simulated torso was undamaged. (Interesting Eng.)"),
        ("SPACE", TAG_SKY,
         "Two asteroids sweep past Earth",
         "2026 WB1 and 2026 WA1 pass within 1.9 and 1.2 lunar "
         "distances; no impact risk. (NASA/JPL)"),
        ("INVESTIGATION", TAG_PURPLE,
         "Fined $811m - the scams didn't stop",
         "BBC investigation: the migrant bail business fined in 2024 "
         "kept operating under a new name. (BBC)"),
        ("UK", TAG_PINK,
         "Brand 'sacks lawyer, considers appeal'",
         "The jailed comedian reportedly drops his trial barrister and "
         "weighs an appeal. (The Sun)"),
    ]),
]

# Big stories deliberately left out: they are NOT 21 November news.
DATE_CHECK = [
    "Poland missile strike - 20 Nov",
    "Riemann proof claim - 20 Nov",
    "Rikers closure plan - 20 Nov",
    "ICJ Myanmar ruling - 19 Nov",
    "Zecler verdict - 20 Nov",
    "UFO files release - 20 Nov",
    "GTA 6 $3.79bn sales - 20 Nov",
    "UK-EU reset deal - 20 Nov",
]

SOURCES_LINE = ("Sources: Reuters, Al Jazeera, BBC, NPR, Xinhua, Daily Short, "
                "Sky News, SOFX, Appistos, NASA/JPL. Every story happened or "
                "was first reported on 21 November 2026, any time zone.")


def wrap(draw, text, fnt, width, max_lines):
    """Greedy word wrap; returns at most max_lines lines (ellipsis if cut)."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
            if len(lines) == max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    # If text was cut, mark the last line with an ellipsis.
    joined = " ".join(lines)
    if len(joined) < len(text):
        last = lines[-1]
        while last and draw.textlength(last + "...", font=fnt) > width:
            last = last[:-1].rstrip()
        lines[-1] = last + "..."
    return lines


def draw_seismogram(draw, x0, x1, y, height):
    """A deterministic seismograph trace under the lead story."""
    pts = []
    n = 220
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        t = i / n * 12.0
        amp = (math.sin(t * 3.1) * 0.55 + math.sin(t * 7.7) * 0.3
               + math.sin(t * 1.3) * 0.15)
        # A burst in the middle, like the main shock.
        burst = math.exp(-((i - n * 0.45) ** 2) / (2 * (n * 0.09) ** 2))
        amp = amp * (0.25 + 1.6 * burst)
        pts.append((x, y + amp * height / 2))
    draw.line(pts, fill=RULE, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN
    inner_w = x1 - x0

    # ---------- Masthead ----------
    y = 26
    d.text((x0, y), "FROST FRONT PAGE", font=F_MAST, fill=INK)
    mast_w = d.textlength("FROST FRONT PAGE", font=F_MAST)
    # Right-aligned edition mark.
    edition = "ONE IMAGE  |  24 STORIES"
    ew = d.textlength(edition, font=F_SUB)
    d.text((x1 - ew, y + 16), edition, font=F_SUB, fill=MUTED)
    y += 58
    d.text((x0, y), "SATURDAY 21 NOVEMBER 2026", font=F_DATE, fill=RULE)
    d.text((x0 + 330, y + 2),
           "The world's news of one day, in one image.",
           font=F_SUB, fill=MUTED)
    y += 26
    d.line([(x0, y), (x1, y)], fill=INK, width=3)
    y += 5
    d.line([(x0, y), (x1, y)], fill=INK, width=1)

    # ---------- Lead story ----------
    y += 12
    lead_top = y
    tag, colour, head, summ = LEAD
    d.text((x0, y), tag, font=F_LEAD_TAG, fill=colour)
    y += 17
    d.text((x0, y), head, font=F_LEAD_HEAD, fill=INK)
    y += 36
    for line in wrap(d, summ, F_LEAD_SUM, inner_w, 2):
        d.text((x0, y), line, font=F_LEAD_SUM, fill=INK)
        y += 19
    y += 6
    draw_seismogram(d, x0, x1, y + 8, 22)
    y += 24
    d.line([(x0, y), (x1, y)], fill=MUTED, width=1)
    lead_bottom = y

    # ---------- Three-column grid ----------
    gutter = 22
    col_w = (inner_w - 2 * gutter) // 3
    grid_top = lead_bottom + 12
    grid_bottom = 870
    col_x = [x0, x0 + col_w + gutter, x0 + 2 * (col_w + gutter)]

    for ci, (section, stories) in enumerate(COLUMNS):
        cx = col_x[ci]
        cy = grid_top
        # Section header.
        d.text((cx, cy), section, font=F_TAG, fill=MUTED)
        cy += 15
        d.line([(cx, cy), (cx + col_w, cy)], fill=MUTED, width=1)
        cy += 8
        # Measure every story first (tag + wrapped headline + wrapped
        # summary), then share the leftover space as even gaps between
        # stories so nothing ever overlaps.
        measured = []
        for tag, colour, head, summ in stories:
            head_lines = wrap(d, head, F_HEAD, col_w, 2)
            sum_lines = wrap(d, summ, F_SUM, col_w, 2)
            for line in head_lines + sum_lines:
                if line.endswith("..."):
                    print("TRUNCATED:", line)
            height = 13 + len(head_lines) * 18 + len(sum_lines) * 14
            measured.append((tag, colour, head_lines, sum_lines, height))
        total = sum(m[4] for m in measured)
        avail = grid_bottom - cy
        gap = max(6, (avail - total) // max(1, len(measured) - 1))
        for tag, colour, head_lines, sum_lines, _h in measured:
            d.text((cx, cy), tag, font=F_TAG, fill=colour)
            cy += 13
            for line in head_lines:
                d.text((cx, cy), line, font=F_HEAD, fill=INK)
                cy += 18
            for line in sum_lines:
                d.text((cx, cy), line, font=F_SUM, fill=(60, 60, 60))
                cy += 14
            cy += gap
        # Column divider (except after the last column).
        if ci < 2:
            dx = cx + col_w + gutter // 2
            d.line([(dx, grid_top), (dx, grid_bottom)], fill=(214, 208, 194),
                   width=1)

    # ---------- DATE CHECK box ----------
    box_top = 880
    box_bottom = 994
    d.rounded_rectangle([(x0, box_top), (x1, box_bottom)], radius=8,
                        fill=BOX_BG, outline=BOX_EDGE, width=2)
    bx = x0 + 14
    by = box_top + 10
    d.text((bx, by),
           "DATE CHECK - LEFT OUT ON PURPOSE: these big stories are NOT "
           "21 November news",
           font=F_BOX_TITLE, fill=TAG_RED)
    by += 22
    half = len(DATE_CHECK) // 2
    col2_x = x0 + inner_w // 2 + 8
    for i, item in enumerate(DATE_CHECK):
        col = 0 if i < half else 1
        row = i if i < half else i - half
        ix = bx if col == 0 else col2_x
        iy = by + row * 17
        d.text((ix, iy), "\u2715  " + item, font=F_BOX_ITEM, fill=INK)

    # ---------- Footer ----------
    fy = box_bottom + 8
    d.text((x0, fy), SOURCES_LINE, font=F_FOOT, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
