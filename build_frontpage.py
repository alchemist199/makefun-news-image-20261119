#!/usr/bin/env python3
"""Draw the front page for make.fun news-image-20261119.

Deterministic: fixed layout, fixed fonts, no timestamps, no network,
no randomness. Renders entry.png (1024x1024) next to this script.
Requires Pillow (used here at build time only; main.py is stdlib only).
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
INK = (17, 17, 17)
PAPER = (247, 243, 234)
RED = (163, 18, 18)
GREY = (90, 86, 78)
RULE = (120, 116, 106)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 82)
F_DATE = font("DejaVuSans-Bold.ttf", 25)
F_KICK = font("DejaVuSans-Bold.ttf", 16)
F_LEAD = font("DejaVuSerif-Bold.ttf", 40)
F_LEAD_SUB = font("DejaVuSans.ttf", 20)
F_TAG = font("DejaVuSans-Bold.ttf", 15)
F_HEAD = font("DejaVuSerif-Bold.ttf", 23)
F_SUM = font("DejaVuSans.ttf", 17)
F_STRIP_HEAD = font("DejaVuSans-Bold.ttf", 16)
F_STRIP = font("DejaVuSans.ttf", 16)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines, each fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    for line in lines:
        assert draw.textlength(line, font=fnt) <= max_w, (
            "line too wide: %r" % line
        )
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


def draw_globe(draw, cx, cy, r):
    """Simple line globe: outline, meridians, parallels, three dots."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    for k in (0.45, 0.85):
        rx = int(r * k)
        draw.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=INK, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=INK, width=2)
    for dy in (-int(r * 0.5), int(r * 0.5)):
        half = int((r * r - dy * dy) ** 0.5)
        draw.line([(cx - half, cy + dy), (cx + half, cy + dy)],
                  fill=INK, width=2)
    for dx, dy, label in ((-0.55, -0.35, "US"), (0.15, -0.55, "CN"),
                          (0.55, -0.15, "RU")):
        px, py = cx + int(r * dx), cy + int(r * dy)
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED)
        draw.text((px + 8, py - 8), label, font=F_TAG, fill=RED)


LEAD_HEAD = "Trump, Xi and Putin meet in first three-way summit"
LEAD_SUB = ("The three leaders hold talks in Shenzhen on the sidelines of "
            "the APEC forum, the first time they have met together.")

GRID = [
    ("UKRAINE",
     "Ukraine hits Crimean Bridge a third time",
     "Crimea head closes bridge traffic temporarily as damage is assessed."),
    ("MIDDLE EAST",
     "Iran strikes Gulf states after US hits Qeshm",
     "Kuwait says it repelled an Iranian attack; IAEA says Iran's "
     "uranium stockpile is now unverifiable."),
    ("THE HAGUE",
     "ICJ to rule on Myanmar Rohingya case",
     "The court delivers its judgment in the genocide case against Myanmar."),
    ("MARKETS",
     "Anthropic raises record sum in market debut",
     "The AI firm's stock market debut sets a record for money raised."),
    ("WASHINGTON",
     "Jeffries nominated, set to be first Black Speaker",
     "Democrats nominate Hakeem Jeffries to lead the US House."),
    ("ASIA",
     "North Korea expands uranium enrichment",
     "IAEA says enrichment grew at the Yongbyon nuclear site."),
    ("GAZA",
     "Israel delays E1 settlement plan",
     "IDF operates against a Hamas tunnel west of Gaza's Yellow Line."),
    ("CARACAS",
     "US and Venezuela restore military ties",
     "The two countries agree to resume training and intelligence sharing."),
]

STRIP_ITEMS = [
    "Cyclone Akvan nears India's east coast; Odisha prepares",
    "EU governments back Indonesia trade pact to counter US tariffs",
    "Istanbul mayor Imamoglu jailed with eight others, barred from politics",
    "\"Human\" is Cambridge Dictionary's word of 2026",
    "NASA's Voyager 1 believed to have passed a light-day from Earth",
    "GTA VI targets 30 FPS on consoles, no 60 FPS mode at launch; "
    "about 1,600 developers worked on it",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # ---- Masthead ----
    title = "THE WORLD"
    tw = d.textlength(title, font=F_MAST)
    d.text(((W - tw) / 2, 14), title, font=F_MAST, fill=INK)
    date = "THURSDAY, 19 NOVEMBER 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 106), date, font=F_DATE, fill=RED)
    rule(d, x0, x1, 142, 3)
    rule(d, x0, x1, 147, 1)

    # ---- Lead story ----
    ly = 162
    d.text((x0, ly), "LEAD STORY  |  SHENZHEN, CHINA", font=F_KICK, fill=RED)
    lead_w = 640
    lines = wrap(d, LEAD_HEAD, F_LEAD, lead_w)
    assert len(lines) <= 2, "lead headline wrapped to %d lines" % len(lines)
    y = draw_lines(d, lines, F_LEAD, x0, ly + 26, INK, 48)
    sub = wrap(d, LEAD_SUB, F_LEAD_SUB, lead_w)
    assert len(sub) <= 3, "lead sub wrapped to %d lines" % len(sub)
    y = draw_lines(d, sub, F_LEAD_SUB, x0, y + 8, INK, 26)
    assert y <= 348, "lead block overflow: %d" % y
    draw_globe(d, 852, 250, 82)
    d.text((772, 344), "Three leaders, one table",
           font=F_TAG, fill=GREY)

    rule(d, x0, x1, 366, 2)

    # ---- Grid: 2 columns x 4 rows ----
    gy = 380
    col_w = (x1 - x0 - 28) // 2
    row_h = 128
    for i, (tag, head, summ) in enumerate(GRID):
        col, row = i % 2, i // 2
        cx = x0 + col * (col_w + 28)
        cy = gy + row * row_h
        d.text((cx, cy), tag, font=F_TAG, fill=RED)
        hl = wrap(d, head, F_HEAD, col_w)
        assert len(hl) <= 2, "headline wrapped to %d: %r" % (len(hl), head)
        y = draw_lines(d, hl, F_HEAD, cx, cy + 22, INK, 28)
        sl = wrap(d, summ, F_SUM, col_w)
        assert len(sl) <= 3, "summary wrapped to %d: %r" % (len(sl), summ)
        y = draw_lines(d, sl, F_SUM, cx, y + 4, INK, 22)
        assert y <= cy + row_h - 2, "cell overflow: %r ends %d" % (head, y)
        if col == 0:
            d.line([(cx + col_w + 14, cy + 4), (cx + col_w + 14,
                    cy + row_h - 12)], fill=RULE, width=1)

    rule(d, x0, x1, 900, 2)

    # ---- Bottom strip: also today ----
    sy = 914
    d.text((x0, sy), "ALSO TODAY", font=F_STRIP_HEAD, fill=RED)
    strip_text = "  •  ".join(STRIP_ITEMS)
    lines = wrap(d, strip_text, F_STRIP, x1 - x0)
    assert len(lines) <= 4, "strip wrapped to %d lines" % len(lines)
    draw_lines(d, lines, F_STRIP, x0, sy + 24, INK, 21)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
