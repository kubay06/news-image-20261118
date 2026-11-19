#!/usr/bin/env python3
"""Build entry.png for the make.fun news-image-20261118 bounty.

One 1024x1024 newspaper-style image summing up Wednesday 18 November 2026.
All text is drawn with real fonts (PIL); the three illustrations are original
flat editorial artwork generated for this entry (no text inside them).

Run:  python3 build_image.py   -> writes entry.png next to this script.
Deterministic: no timestamps, no randomness, fixed crop boxes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
PAPER = (251, 247, 236)
INK = (27, 27, 27)
RED = (179, 38, 30)
NAVY = (18, 50, 79)
GOLD = (176, 128, 20)
TEAL = (14, 110, 110)
MUTED = (90, 86, 74)
LINE = (216, 208, 188)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s)
SERIF = lambda s: font("LiberationSerif-Regular.ttf", s)
SERIF_I = lambda s: font("LiberationSerif-Italic.ttf", s)
SANS_B = lambda s: font("LiberationSans-Bold.ttf", s)
SANS = lambda s: font("LiberationSans-Regular.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap using real text widths. Returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill, leading=None):
    """Draw wrapped text, return y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def crop_to(img, tw, th):
    """Center-crop img to the target aspect ratio, then resize to tw x th."""
    sw, sh = img.size
    target = tw / th
    if sw / sh > target:  # too wide -> trim sides
        nw = int(sh * target)
        x0 = (sw - nw) // 2
        img = img.crop((x0, 0, x0 + nw, sh))
    else:  # too tall -> trim top/bottom
        nh = int(sw / target)
        y0 = (sh - nh) // 2
        img = img.crop((0, y0, sw, y0 + nh))
    return img.resize((tw, th), Image.LANCZOS)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin
    R = W - M  # right edge

    # ---------------- masthead ----------------
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(56)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 16), title, font=tf, fill=INK)
    d.line([(M, 88), (R, 88)], fill=INK, width=3)
    d.line([(M, 94), (R, 94)], fill=INK, width=1)

    # dateline row
    d.text((M, 104), "WEDNESDAY, 18 NOVEMBER 2026", font=SANS_B(20), fill=RED)
    tag = "ONE IMAGE  ·  SIX STORIES"
    d.text((R - d.textlength(tag, font=SANS_B(15)), 108), tag,
           font=SANS_B(15), fill=MUTED)

    # ---------------- lead story: Gulf ----------------
    LY, LH = 132, 268
    d.rectangle([M, LY, R, LY + LH], fill=PANEL, outline=LINE, width=1)
    gulf = Image.open(os.path.join(
        ASSETS, "media-generation-gulf-hormuz-0-13284b96-b0b9-4a4c-8e0a-f79ec274c888.png"))
    img.paste(crop_to(gulf, 430, LH), (M, LY))
    d.line([(M + 430, LY), (M + 430, LY + LH)], fill=LINE, width=1)

    tx = M + 452
    twd = R - M - 452 - 14
    y = LY + 14
    d.text((tx, y), "MIDDLE EAST  ·  STRAIT OF HORMUZ", font=SANS_B(15), fill=RED)
    y += 26
    y = draw_wrapped(
        d, tx, y,
        "U.S. jets strike Iranian missile site after drone attacks on Gulf bases",
        SERIF_B(30), twd, INK, leading=34)
    y += 6
    y = draw_wrapped(
        d, tx, y,
        "Iran fired drones at U.S. bases in Bahrain and Kuwait. Washington hit "
        "back on Qeshm Island. Tankers burned in the Strait of Hormuz.",
        SERIF(19), twd, (51, 51, 51), leading=24)
    d.text((tx, LY + LH - 26),
           "Sources: Reuters · AP · AFP", font=SANS(13), fill=MUTED)

    # ---------------- 2 x 2 grid ----------------
    GY, GH, GAP = 416, 326, 16
    CW = (R - M - GAP) // 2
    CH = (GH - GAP) // 2
    cells = [
        # (kicker, kicker color, headline, caption, image or None, tag)
        ("ASIA  ·  APEC SUMMIT", NAVY,
         "Xi, Putin meet in Shenzhen as APEC gathers",
         "Trilateral talks with Trump set for Thursday. Quad leaders meet in "
         "Manila for the first time in over two years.",
         None, "CHINA · RUSSIA · U.S."),
        ("UNITED STATES  ·  SENATE", RED,
         "Democrats take the Senate as Peltola wins Alaska",
         "Peltola beats Sen. Dan Sullivan 50.1% to 45.8%. The Senate flips to "
         "56–44 — the ninth seat to change hands.",
         None, "FIRST ALASKA NATIVE IN THE SENATE"),
        ("MARKETS  ·  TECH", GOLD,
         "Nvidia posts a record $115.8B quarter",
         "Revenue up 103% on AI demand; profit $65.3B. The board says it will "
         "not reinstate founder Jensen Huang as CEO.",
         None, "GUIDANCE: ~$130B NEXT QUARTER"),
        ("WEATHER  ·  BAY OF BENGAL", TEAL,
         "Cyclone Akvan heads for India's east coast",
         "Landfall expected Friday near Andhra Pradesh; winds 120–130 km/h, "
         "gusting 145.",
         "media-generation-cyclone-akvan-0-ce5619d3-3512-49a5-b0e0-b49334c47677.png",
         "ORANGE ALERT · 3RD BAY STORM IN A MONTH"),
    ]
    for i, (kicker, kc, head, cap, imgname, tag) in enumerate(cells):
        cx = M + (i % 2) * (CW + GAP)
        cy = GY + (i // 2) * (CH + GAP)
        d.rectangle([cx, cy, cx + CW, cy + CH], fill=PANEL, outline=LINE, width=1)
        ix = cx
        if imgname:  # cyclone cell: illustration on the right
            cyc = Image.open(os.path.join(ASSETS, imgname))
            img.paste(crop_to(cyc, 150, CH), (cx + CW - 150, cy))
            d.line([(cx + CW - 150, cy), (cx + CW - 150, cy + CH)], fill=LINE, width=1)
            txw = CW - 150 - 28
        else:
            txw = CW - 28
        tx = cx + 14
        y = cy + 12
        d.text((tx, y), kicker, font=SANS_B(13), fill=kc)
        y += 22
        y = draw_wrapped(d, tx, y, head, SERIF_B(23), txw, INK, leading=26)
        y += 4
        # Auto-fit the caption: shrink until it ends above the tag line.
        avail = (cy + CH - 28) - y
        for csize in (16, 15, 14, 13):
            clines = wrap(d, cap, SERIF(csize), txw)
            if len(clines) * int(csize * 1.25) <= avail:
                break
        y = draw_wrapped(d, tx, y, cap, SERIF(csize), txw, (51, 51, 51),
                         leading=int(csize * 1.25))
        d.text((tx, cy + CH - 22), tag, font=SANS_B(11), fill=MUTED)

    # ---------------- Voyager band ----------------
    VY, VH = 758, 132
    d.rectangle([M, VY, R, VY + VH], fill=NAVY)
    voy = Image.open(os.path.join(
        ASSETS, "media-generation-voyager-probe-0-181519d1-3437-4a8f-a953-c627ec2ed0e2.png"))
    img.paste(crop_to(voy, 210, VH), (M, VY))
    d.line([(M + 210, VY), (M + 210, VY + VH)], fill=(60, 90, 120), width=1)
    tx = M + 230
    twd = R - M - 230 - 14
    y = VY + 12
    d.text((tx, y), "SPACE  ·  A FIRST", font=SANS_B(14), fill=(212, 168, 60))
    y += 23
    y = draw_wrapped(d, tx, y,
                     "Voyager 1 reaches one light-day from Earth",
                     SERIF_B(26), twd, WHITE, leading=29)
    y += 3
    draw_wrapped(d, tx, y,
                 "16.1 billion miles out, 49 years after launch — the farthest any "
                 "human-made object has flown. Its signals now take a day each way.",
                 SERIF(17), twd, (220, 228, 235), leading=21)

    # ---------------- ALSO TODAY ticker ----------------
    TY = 906
    d.text((M, TY), "ALSO TODAY", font=SANS_B(15), fill=RED)
    ticker = ("Ebola in DR Congo tops 11,000 cases   ·   U.S. loses measles-free "
              "status after 26 years   ·   Kerch Bridge road span collapses")
    draw_wrapped(d, M + 118, TY - 1, ticker, SANS(15), R - M - 118, INK, leading=19)

    # ---------------- footer ----------------
    d.line([(M, 966), (R, 966)], fill=LINE, width=1)
    foot = ("Sources: Reuters, AP, AFP, CNN, USA Today, NASA/JPL, PAHO, WHO, IMD, "
            "Skymet. Illustrations: original artwork. Entry for the make.fun "
            "bounty “Sum up 18 November's world news in one image”.")
    draw_wrapped(d, M, 974, foot, SANS(12), R - M, MUTED, leading=15)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out}  {img.size[0]}x{img.size[1]}  {size} bytes "
          f"({size / 1048576:.2f} MiB)")
    assert size <= 1024 * 1024, "entry.png exceeds the 1 MiB limit"
    return out


if __name__ == "__main__":
    main()
