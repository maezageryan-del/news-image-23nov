#!/usr/bin/env python3
"""Render the Monday 23 November 2026 world-news broadsheet, 1024x1024 PNG.

Deterministic: fixed palette, fixed fonts, fixed layout, no network, no clock.
Reads stories.json next to this script; writes entry.png next to it.
"""
import json
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (250, 244, 230)
INK = (26, 24, 20)
RED = (160, 28, 20)
BLUE = (24, 64, 110)
LIGHT_BLUE = (176, 200, 224)
GREY = (110, 104, 92)
LIGHT = (238, 231, 216)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)         # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)     # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)           # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def centre(draw, cx, y, s, fnt, fill=INK):
    draw.text((cx, y), s, font=fnt, fill=fill, anchor="ma")


def rule(draw, y, x0=16, x1=1008, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_globe_cracked(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=LIGHT_BLUE,
                 outline=BLUE, width=3)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=BLUE, width=2)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=BLUE, width=2)
    draw.line([(cx - 6, cy - r + 4), (cx + 8, cy - 8), (cx - 4, cy + 6),
               (cx + 10, cy + r - 6)], fill=RED, width=3)
    draw.line([(cx - r + 6, cy - 4), (cx - 2, cy + 2), (cx - r + 10, cy + 10)],
              fill=INK, width=2)


def draw_tanker(draw, cx, cy, w):
    hull = [(cx - w, cy), (cx + w, cy), (cx + w - 12, cy + 16),
            (cx - w + 12, cy + 16)]
    draw.polygon(hull, fill=INK)
    draw.rectangle([cx - w + 14, cy - 18, cx - w + 46, cy], fill=INK)
    draw.rectangle([cx + w - 52, cy - 26, cx + w - 20, cy], fill=RED)
    for k, yy in enumerate((cy + 26, cy + 34)):
        draw.arc([cx - w - 8, yy - 6, cx + w + 8, yy + 6], 0, 180,
                 fill=BLUE, width=2)
    for k in range(3):
        x0 = cx - w + 8 + k * 26
        draw.line([(x0, cy - 20 - k * 3), (x0 + 6, cy - 28 - k * 3),
                   (x0 + 12, cy - 20 - k * 3)], fill=GREY, width=2)


def draw_nato_star(draw, cx, cy, r):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=BLUE, outline=INK)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=WHITE, outline=INK)
    draw.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8],
                 outline=GREY, width=2)


def draw_pictogram(draw, n, x, y, s):
    """Small pictogram per medium story, inside a s x s box at (x, y)."""
    cx, cy = x + s / 2, y + s / 2
    if n == 4:  # shield / Patriots
        draw.polygon([(cx, y + 2), (x + s - 2, y + 10), (x + s - 2, cy + 8),
                      (cx, y + s - 2), (x + 2, cy + 8), (x + 2, y + 10)],
                     outline=BLUE, width=2)
        draw.line([(cx, y + 12), (cx, y + s - 10)], fill=RED, width=2)
    elif n == 5:  # burning ship
        draw.polygon([(x + 2, cy + 4), (x + s - 2, cy + 4), (x + s - 8, cy + 12),
                      (x + 8, cy + 12)], fill=INK)
        draw.polygon([(cx - 4, cy - 10), (cx + 6, cy - 2), (cx - 8, cy - 2)],
                     fill=RED)
    elif n == 6:  # warship / anchor-ish
        draw.rectangle([x + 4, cy, x + s - 4, cy + 8], fill=INK)
        draw.rectangle([cx - 3, y + 6, cx + 3, cy + 2], fill=INK)
        draw.line([(x + 4, cy + 14), (x + s - 4, cy + 14)], fill=BLUE, width=2)
    elif n == 7:  # handshake flags
        draw.polygon([(x + 2, y + 6), (x + s / 2 - 2, y + 6),
                      (x + s / 2 - 2, y + s - 6), (x + 2, y + s - 6)],
                     fill=RED)
        draw.polygon([(x + s / 2 + 2, y + 6), (x + s - 2, y + 6),
                      (x + s - 2, y + s - 6), (x + s / 2 + 2, y + s - 6)],
                     fill=BLUE)
    elif n == 8:  # flame
        draw.polygon([(cx, y + 2), (cx + 10, cy + 2), (cx, y + s - 2),
                      (cx - 10, cy + 2)], fill=RED)
    elif n == 9:  # falling chart
        draw.line([(x + 2, y + 4), (x + s / 2, cy), (x + s - 2, y + s - 4)],
                  fill=RED, width=3)
        draw.line([(x + 2, y + s - 4), (x + s - 2, y + s - 4)], fill=GREY,
                  width=1)
    elif n == 10:  # tennis ball
        draw.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], fill=(200, 220, 60),
                     outline=INK, width=2)
        draw.arc([x + 3, y + 3, x + s - 3, y + s - 3], 300, 60, fill=INK,
                 width=2)
    elif n == 11:  # football
        draw.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], fill=WHITE,
                     outline=INK, width=2)
        draw.polygon([(cx - 4, cy - 5), (cx + 5, cy - 2), (cx + 3, cy + 6),
                      (cx - 5, cy + 4)], fill=INK)
    elif n == 12:  # cricket bat + ball
        draw.line([(x + 4, y + s - 4), (cx + 6, y + 4)], fill=(150, 100, 40),
                  width=5)
        draw.ellipse([cx + 2, y + 2, cx + 12, y + 12], fill=RED)
    else:  # 13: music note
        draw.ellipse([x + 4, y + s - 10, x + 14, y + s - 2], fill=INK)
        draw.line([(x + 13, y + s - 6), (x + 13, y + 4)], fill=INK, width=2)
        draw.line([(x + 13, y + 4), (x + s - 4, y + 8)], fill=INK, width=2)


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    stories = {s["n"]: s for s in data["stories"]}

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # subtle paper texture: deterministic diagonal hatch, very light
    for yy in range(0, H, 4):
        d.line([(0, yy), (W, yy)], fill=(246, 240, 224), width=1)
    for xx in range(0, W, 8):
        d.line([(xx, 0), (xx, H)], fill=(247, 241, 226), width=1)
    # thin outer frame (top edge above the top-strip text)
    d.rectangle([6, 2, W - 7, H - 7], outline=INK, width=1)

    # (1) top strip
    centre(d, W // 2, 5, "36 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED "
           "MONDAY 23 NOVEMBER 2026", SANS_B(13), INK)
    rule(d, 24, width=2)

    # (2) masthead
    centre(d, W // 2, 26, "Monday 23 November 2026", SERIF_B(46), INK)
    rule(d, 88, width=2)

    # (3) red ticker band
    d.rectangle([0, 92, W, 120], fill=RED)
    centre(d, W // 2, 99, "COP31 COLLAPSES  ·  HORMUZ ATTACKS PEAK  ·  "
           "NATO MEETS TODAY  ·  MOLLY MELDRUM DIES AT 83", SANS_B(16), WHITE)

    # (4) timeline spine
    y = 128
    text(d, (16, y), "OVERNIGHT → MONDAY", SANS_B(12), RED)
    tl = [("Sun", "COP31 collapse"), ("Sun night", "Bahrain strikes"),
          ("05:30", "Molly dies"), ("Today", "NATO meets"),
          ("Today", "PMIs land")]
    tx = 190
    for label, item in tl:
        text(d, (tx, y), label, SANS_B(11), BLUE)
        tw = d.textlength(label, font=SANS_B(11))
        text(d, (tx + tw + 4, y), item, SANS(11), INK)
        tx += tw + 4 + d.textlength(item, font=SANS(11)) + 26
        if tx < 1000:
            d.line([(tx - 16, y + 2), (tx - 16, y + 12)], fill=GREY, width=1)
    rule(d, 148)

    # (5) numbers strip — 6 big numerals
    nums = [("44h", "Longest COP ever —\n44h overtime"),
            ("3", "tankers struck\nsince Friday"),
            ("720/9", "record Test total\nin Wellington"),
            ("−14%", "Nvidia on\nFriday"),
            ("24", "body bags,\nBanten"),
            ("491", "migrants\nintercepted")]
    cw = (W - 32) // 6
    y = 154
    for i, (big, small) in enumerate(nums):
        x0 = 16 + i * cw
        centre(d, x0 + cw // 2, y, big, SERIF_B(28), RED if i % 2 == 0 else BLUE)
        for j, ln in enumerate(small.split("\n")):
            centre(d, x0 + cw // 2, y + 36 + j * 13, ln, SANS(10), INK)
        if i:
            d.line([(x0, y + 4), (x0, y + 60)], fill=GREY, width=1)
    rule(d, 222)

    # (6) region colour bar
    regions = [("Asia", 14, (160, 28, 20)), ("Europe", 7, (24, 64, 110)),
               ("Africa", 5, (40, 130, 90)), ("Middle East", 4, (200, 120, 20)),
               ("Global", 3, (110, 104, 92)), ("Asia-Pacific", 2, (90, 60, 140)),
               ("North America", 1, (60, 140, 160))]
    total = sum(v for _, v, _ in regions)
    x = 16
    y = 230
    for name, v, col in regions:
        wseg = int((W - 32) * v / total)
        d.rectangle([x, y, x + wseg - 2, y + 14], fill=col)
        x += wseg
    x = 16
    y = 248
    for name, v, col in regions:
        label = "%s %d" % (name, v)
        text(d, (x, y), label, SANS_B(11), INK)
        x += d.textlength(label, font=SANS_B(11)) + 22
    rule(d, 266)

    # (7) three lead panels
    lead_art = {1: draw_globe_cracked, 2: draw_tanker, 3: draw_nato_star}
    pw, ph, gap = 325, 156, 8
    y0 = 274
    for i, n in enumerate((1, 2, 3)):
        s = stories[n]
        x0 = 16 + i * (pw + gap)
        d.rectangle([x0, y0, x0 + pw, y0 + ph], outline=INK, width=2)
        d.rectangle([x0, y0, x0 + pw, y0 + 20], fill=RED)
        text(d, (x0 + 6, y0 + 3), "%d  ·  %s" % (n, s["region"].upper()),
             SANS_B(12), WHITE)
        # headline full width, then illustration left + deck right
        hl = wrap(d, s["headline"], SERIF_B(16), pw - 12)
        for j, ln in enumerate(hl[:2]):
            text(d, (x0 + 6, y0 + 24 + j * 19), ln, SERIF_B(16), INK)
        ay = y0 + 66
        if n == 1:
            draw_globe_cracked(d, x0 + 52, ay + 26, 24)
        elif n == 2:
            draw_tanker(d, x0 + 52, ay + 22, 34)
        else:
            draw_nato_star(d, x0 + 52, ay + 26, 24)
        hx = x0 + 104
        for j, ln in enumerate(wrap(d, s["deck"], SANS(10), pw - 116)[:5]):
            text(d, (hx, ay + j * 12), ln, SANS(10), INK)
        if s["date_note"]:
            text(d, (x0 + 6, y0 + ph - 32), s["date_note"], SANS_B(10), RED)
        text(d, (x0 + 6, y0 + ph - 17), "Source: " + s["source"],
             SANS(10), GREY)
    rule(d, y0 + ph + 8)

    # (8) ten medium panels, 5 x 2
    mw, mh = 196, 102
    y0 = 446
    for idx, n in enumerate(range(4, 14)):
        s = stories[n]
        col, row = (idx % 5), (idx // 5)
        x0 = 16 + col * (mw + 6)
        yy = y0 + row * (mh + 6)
        d.rectangle([x0, yy, x0 + mw, yy + mh], outline=INK, width=1,
                    fill=WHITE)
        text(d, (x0 + 6, yy + 4), "%d" % n, SERIF_B(14), RED)
        draw_pictogram(d, n, x0 + 26, yy + 4, 26)
        if s["date_note"]:
            text(d, (x0 + 60, yy + 6), s["date_note"], SANS_B(9), RED)
        hl = wrap(d, s["headline"], SERIF_B(12), mw - 12)
        for j, ln in enumerate(hl[:2]):
            text(d, (x0 + 6, yy + 32 + j * 15), ln, SERIF_B(12), INK)
        dy = yy + 32 + min(len(hl), 2) * 15 + 2
        dl = wrap(d, s["deck"], SANS(9), mw - 12)
        for j, ln in enumerate(dl[:2]):
            text(d, (x0 + 6, dy + j * 11), ln, SANS(9), INK)
        text(d, (x0 + 6, yy + mh - 13), s["source"] + "  ·  " + s["region"],
             SANS(8), GREY)
    rule(d, y0 + 2 * mh + 12)

    # (9) world-map strip with numbered pins
    my0 = 672
    text(d, (16, my0), "WHERE IT HAPPENED", SANS_B(13), INK)
    text(d, (16, my0 + 16), "Pins 1–13 mark the lead and medium stories.",
         SANS(10), GREY)
    map_x0, map_y0, map_w, map_h = 16, my0 + 32, 992, 60
    d.rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + map_h],
                fill=(226, 236, 244), outline=BLUE, width=1)
    # rough continent blobs (simplified, stylised)
    blobs = [
        [(60, 22), (150, 12), (210, 26), (190, 52), (120, 58), (70, 44)],
        [(250, 18), (330, 10), (380, 26), (360, 50), (300, 56), (262, 40)],
        [(420, 14), (560, 8), (640, 22), (620, 52), (520, 60), (440, 44)],
        [(700, 30), (800, 18), (880, 30), (860, 56), (760, 60), (710, 48)],
        [(880, 62), (940, 62), (950, 70), (890, 70)],
    ]
    for blob in blobs:
        d.polygon([(map_x0 + bx, map_y0 + by) for bx, by in blob],
                  fill=LIGHT_BLUE, outline=BLUE)
    pins = {1: (36.9, 30.7), 2: (26.5, 56.2), 3: (50.85, 4.35),
            4: (50.45, 30.52), 5: (60.0, 25.0), 6: (32.1, 20.07),
            7: (28.6, 77.2), 8: (-6.1, 106.1), 9: (37.4, -122.0),
            10: (45.07, 7.69), 11: (53.4, -2.99), 12: (-41.29, 174.78),
            13: (-37.81, 144.96)}
    for n, (lat, lon) in pins.items():
        px = map_x0 + int((lon + 180) / 360 * map_w)
        py = map_y0 + int((90 - lat) / 180 * map_h)
        # nudge the crowded Europe cluster apart so pins stay legible
        px += {3: 0, 4: 12, 5: 14, 6: 10, 10: -16, 11: -20}.get(n, 0)
        py += {3: -7, 4: -7, 5: -8, 6: 9, 10: 9, 11: -5}.get(n, 0)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE,
                  width=1)
        centre(d, px, py - 6, str(n), SANS_B(9), WHITE)
    rule(d, my0 + 32 + map_h + 8)

    # (10) ALSO list 14–36, two columns
    ly0 = 780
    text(d, (16, ly0), "ALSO ON MONDAY 23 NOVEMBER — 23 MORE STORIES",
         SANS_B(13), RED)
    cols = [list(range(14, 26)), list(range(26, 37))]
    for ci, col_ns in enumerate(cols):
        x0 = 16 + ci * 504
        for j, n in enumerate(col_ns):
            s = stories[n]
            yy = ly0 + 18 + j * 11
            line = "%d. %s (%s)" % (n, s["headline"], s["source"])
            if s["date_note"]:
                line += " — " + s["date_note"]
            text(d, (x0, yy), line, SANS(9), INK)

    # (11) DATE CHECK + CLAIMS CHECKED boxes
    by0 = 936
    bw = 496
    d.rectangle([16, by0, 16 + bw, by0 + 56], outline=RED, width=2)
    text(d, (26, by0 + 4), "DATE CHECK", SANS_B(11), RED)
    dc = ("Left out as earlier days' news: Las Vegas GP — Verstappen wins "
          "(Sat 21 Nov) · UK–EU post-Brexit deals signed (Fri 20 Nov) · "
          "El Chapo Isidro captured (20–21 Nov) · ICJ Myanmar genocide "
          "ruling (19 Nov).")
    for j, ln in enumerate(wrap(d, dc, SANS(10), bw - 20)):
        text(d, (26, by0 + 18 + j * 12), ln, SANS(10), INK)
    x1 = 512
    d.rectangle([x1, by0, x1 + bw, by0 + 56], outline=BLUE, width=2)
    text(d, (x1 + 10, by0 + 4), "CLAIMS CHECKED", SANS_B(11), BLUE)
    cc = ("COP31 'Antalya Pact' — REJECTED Sunday, not agreed (first "
          "reported Mon in Asia) · Iran 14-tanker convoy — sailing "
          "unconfirmed, not shown · Sudan drones from Ethiopia — single "
          "low-authority source, not shown.")
    for j, ln in enumerate(wrap(d, cc, SANS(10), bw - 20)):
        text(d, (x1 + 10, by0 + 18 + j * 12), ln, SANS(10), INK)

    # (12) footer
    centre(d, W // 2, 1000,
           "Every story here happened, or was first reported, on Monday 23 "
           "November 2026; overnight events are labelled with their night. "
           "Officials' counts are attributed.",
           SANS(9), GREY)

    img.save(os.path.join(HERE, "entry.png"), optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
