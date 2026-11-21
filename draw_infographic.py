#!/usr/bin/env python3
"""Build-time script: draw the 1024x1024 news infographic entry.png.

Uses Pillow only. No network, no external images; every icon is drawn
with Pillow shapes. Run: python3 draw_infographic.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Palette: light theme, dark navy header, strong contrast.
NAVY = (15, 42, 68)
NAVY_LIGHT = (24, 68, 104)
BG = (238, 240, 243)
CARD = (255, 255, 255)
INK = (18, 24, 32)
MUTED = (70, 80, 92)
ACCENTS = [
    (178, 34, 34),    # summit: red
    (196, 110, 0),    # missiles: amber
    (0, 110, 110),    # denmark: teal
    (34, 120, 60),    # cop31: green
    (90, 60, 160),    # riemann: purple
    (30, 80, 160),    # sentence: blue
]

STORIES = [
    ("SUMMIT AFTERMATH",
     "Trump, Xi and Putin held trilateral talks in Shenzhen on 19 Nov. "
     "Trump then told European allies in Berlin that Putin is \"tired\" "
     "and ready for a deal."),
    ("MISSILES LAND IN POLAND",
     "Two Russian missiles and a suspected drone came down in south-east "
     "Poland during a huge overnight assault on Ukraine. No one was hurt; "
     "NATO called it a grave violation."),
    ("DENMARK EXPELS RUSSIAN DIPLOMAT",
     "Denmark expelled Russia's defence attache after intelligence said "
     "Moscow plotted to kill rapper Kyivstoner near Copenhagen. Two men "
     "were charged with attempted murder."),
    ("COP31 INTO OVERTIME",
     "UN climate talks in Antalya ran past their Friday deadline with no "
     "deal. The latest draft omits any mention of fossil fuels; a third "
     "draft was due Saturday morning."),
    ("A PROOF OF RIEMANN?",
     "Anthropic mathematician Levent Alpoege says he and the Claude "
     "chatbot have proved the Riemann hypothesis, with a computer-checked "
     "Lean formalisation. Verification is still pending."),
    ("19 YEARS FOR MURDER PLOT",
     "A New York court sentenced Indian national Nikhil Gupta to 235 "
     "months in prison for a murder-for-hire plot against activist "
     "Gurpatwant Singh Pannun."),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font; never exceeds max_w."""
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


def draw_icon(d, kind, x, y, s, color):
    """Distinct geometric icon inside a square of side s at (x, y)."""
    if kind == 0:  # three leaders: three overlapping circles
        r = s // 4
        for i, cx in enumerate((x + r, x + s // 2, x + s - r)):
            cy = y + s // 2 + (0 if i == 1 else 6)
            d.ellipse([cx - r, cy - r, cx + r, cy + r],
                      outline=color, width=4)
    elif kind == 1:  # missile: diagonal rocket, nose up-right, flame at tail
        d.polygon([(x + s * 0.55, y + s * 0.10), (x + s * 0.85, y + s * 0.40),
                   (x + s * 0.65, y + s * 0.60), (x + s * 0.35, y + s * 0.30)],
                  fill=color)
        d.polygon([(x + s * 0.55, y + s * 0.10), (x + s * 0.85, y + s * 0.40),
                   (x + s * 0.98, y + s * 0.02)], fill=color)
        d.polygon([(x + s * 0.35, y + s * 0.30), (x + s * 0.50, y + s * 0.45),
                   (x + s * 0.12, y + s * 0.42)], fill=color)
        d.polygon([(x + s * 0.50, y + s * 0.45), (x + s * 0.65, y + s * 0.60),
                   (x + s * 0.58, y + s * 0.88)], fill=color)
        d.line([x + s * 0.42, y + s * 0.52, x + s * 0.18, y + s * 0.76],
               fill=color, width=4)
        d.line([x + s * 0.52, y + s * 0.62, x + s * 0.30, y + s * 0.90],
               fill=color, width=4)
    elif kind == 2:  # expulsion: door frame with an outward arrow
        d.rectangle([x + 4, y + 4, x + s - 4, y + s - 4],
                    outline=color, width=4)
        d.line([x + s * 0.2, y + s * 0.5, x + s * 0.75, y + s * 0.5],
               fill=color, width=5)
        d.polygon([(x + s * 0.75, y + s * 0.3), (x + s * 0.95, y + s * 0.5),
                   (x + s * 0.75, y + s * 0.7)], fill=color)
    elif kind == 3:  # climate: globe circle with orbit arc
        d.ellipse([x + 6, y + 6, x + s - 6, y + s - 6],
                  outline=color, width=4)
        d.arc([x - 4, y + s * 0.15, x + s + 4, y + s * 0.85],
              start=200, end=340, fill=color, width=4)
        d.line([x + s * 0.25, y + s * 0.5, x + s * 0.75, y + s * 0.5],
               fill=color, width=3)
    elif kind == 4:  # maths: zeta glyph over a baseline axis
        d.line([x + 4, y + s - 8, x + s - 4, y + s - 8], fill=color, width=3)
        zeta = ImageFont.truetype(FONT_BOLD, 46)
        d.text((x + 8, y - 2), "\u03b6", font=zeta, fill=color)
    else:  # justice: scales — beam, post and two pans
        d.line([x + s // 2, y + 6, x + s // 2, y + s - 6], fill=color, width=4)
        d.line([x + 6, y + 14, x + s - 6, y + 14], fill=color, width=4)
        for cx in (x + 14, x + s - 14):
            d.line([cx, y + 14, cx, y + s - 22], fill=color, width=3)
            d.polygon([(cx - 12, y + s - 22), (cx + 12, y + s - 22),
                       (cx, y + s - 6)], outline=color, width=3)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_title = font(FONT_BOLD, 44)
    f_date = font(FONT_REG, 29)
    f_head = font(FONT_BOLD, 26)
    f_body = font(FONT_REG, 20)
    f_foot = font(FONT_REG, 17)

    # Header band.
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=NAVY_LIGHT)
    d.text((32, 22), "THE WORLD IN ONE IMAGE", font=f_title, fill=(255, 255, 255))
    d.text((32, 84), "Saturday 21 November 2026", font=f_date,
           fill=(190, 215, 235))

    # Grid: 2 cols x 3 rows.
    margin, gap = 24, 16
    grid_top, grid_bottom = 172, 946
    cw = (W - 2 * margin - gap) // 2
    ch = (grid_bottom - grid_top - 2 * gap) // 3
    for i, (headline, body) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (cw + gap)
        y0 = grid_top + row * (ch + gap)
        color = ACCENTS[i]
        d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], radius=12, fill=CARD)
        d.rounded_rectangle([x0, y0, x0 + cw, y0 + 8], radius=4, fill=color)
        # Icon, top-left.
        draw_icon(d, i, x0 + 16, y0 + 22, 52, color)
        # Headline beside the icon, max 2 lines.
        hx = x0 + 82
        hw = x0 + cw - 16 - hx
        hlines = wrap(d, headline, f_head, hw)[:2]
        hy = y0 + 24
        for ln in hlines:
            d.text((hx, hy), ln, font=f_head, fill=INK)
            hy += 31
        # Body, full card width below.
        bx = x0 + 16
        bw = cw - 32
        blines = wrap(d, body, f_body, bw)
        by = y0 + 92
        for ln in blines:
            d.text((bx, by), ln, font=f_body, fill=MUTED)
            by += 26
        # Fail loudly rather than silently overflowing the card.
        assert by <= y0 + ch - 8, f"card {i} body overflows: {by} > {y0 + ch - 8}"
        assert len(hlines) <= 2, f"card {i} headline overflows to 3 lines"

    # Footer.
    d.text((32, 962),
           "Sources: Reuters · AP · Al Jazeera · Scientific American · Manila Times · CNN",
           font=f_foot, fill=MUTED)
    d.text((32, 986),
           "Stories as reported on 21 November 2026 — exact dates in README.",
           font=f_foot, fill=MUTED)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
