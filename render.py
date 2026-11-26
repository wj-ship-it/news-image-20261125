#!/usr/bin/env python3
"""Render news-frontpage.png: a newspaper front page summing up
25 November 2026 world news. Pure PIL, no network."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 48
CONTENT = W - 2 * MARGIN  # 928

INK = (18, 18, 18)
PAPER = (253, 252, 247)
GREY = (90, 90, 90)
RULE = (40, 40, 40)

SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

STORIES = [
    ("TANKERS HIT BY MINES IN STRAIT OF HORMUZ",
     "Two oil tankers struck naval mines, explode and catch fire, "
     "Iran's Revolutionary Guard says."),
    ("HOUTHIS HIT SAUDI REFINERY AT RAS TANURA",
     "Attack sets fires at the refinery; Riyadh's tallest tower struck "
     "again, 11 people injured."),
    ("ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF IN GAZA",
     "Mohammad Abuelouf, his wife and two daughters killed in a "
     "Gaza City apartment strike."),
    ("UKRAINE DRONES SET FIRE TO TWO RUSSIAN REFINERIES",
     "Rosneft plants in the Samara region burn overnight; Putin vows "
     "'inevitable' retaliation."),
    ("HUAWEI CONVICTED IN US COURT",
     "Federal jury finds the Chinese firm guilty of trade-secret theft "
     "conspiracy and bank fraud."),
    ("TECH SELLOFF DEEPENS AS NVIDIA SLIDES AGAIN",
     "Nvidia falls about 5%, SoftBank down 15%; Nikkei drops 2.8%, "
     "South Korea's Kospi 6.2%."),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_block(draw, x, y, width, headline, summary, h_size, s_size,
               h_leading, s_leading, gap=10):
    """Draw one story block; returns the y just below the summary."""
    h_font = font(SERIF_BOLD, h_size)
    s_font = font(SANS, s_size)
    lines = wrap(draw, headline, h_font, width)
    y_cur = y
    for line in lines:
        draw.text((x, y_cur), line, font=h_font, fill=INK)
        y_cur += h_leading
    y_cur += gap
    for line in wrap(draw, summary, s_font, width):
        draw.text((x, y_cur), line, font=s_font, fill=INK)
        y_cur += s_leading
    return y_cur


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead ----
    mast = font(SERIF_BOLD, 104)
    title = "THE WORLD"
    tw = draw.textlength(title, font=mast)
    draw.text(((W - tw) / 2, 34), title, font=mast, fill=INK)

    date_font = font(SANS_BOLD, 24)
    dateline = "W E D N E S D A Y   2 5   N O V E M B E R   2 0 2 6"
    dw = draw.textlength(dateline, font=date_font)
    draw.text(((W - dw) / 2, 158), dateline, font=date_font, fill=INK)

    # Double rule under the masthead.
    draw.line([(MARGIN, 198), (W - MARGIN, 198)], fill=RULE, width=4)
    draw.line([(MARGIN, 206), (W - MARGIN, 206)], fill=RULE, width=1)

    # ---- Lead story (full width) ----
    y = draw_block(draw, MARGIN, 228, CONTENT,
                   STORIES[0][0], STORIES[0][1],
                   h_size=46, s_size=25, h_leading=56, s_leading=34, gap=12)

    # Rule under the lead story.
    draw.line([(MARGIN, y + 14), (W - MARGIN, y + 14)], fill=RULE, width=2)
    grid_top = y + 30

    # ---- Grid: two rows of two, then one full-width story ----
    col_w = (CONTENT - 28) // 2  # 450
    col2_x = MARGIN + col_w + 28

    # Row 1: stories 2 and 3.
    end1 = draw_block(draw, MARGIN, grid_top, col_w,
                      STORIES[1][0], STORIES[1][1],
                      h_size=30, s_size=20, h_leading=38, s_leading=27, gap=8)
    end2 = draw_block(draw, col2_x, grid_top, col_w,
                      STORIES[2][0], STORIES[2][1],
                      h_size=30, s_size=20, h_leading=38, s_leading=27, gap=8)
    row1_bottom = max(end1, end2)

    # Vertical divider between the two columns, row 1.
    draw.line([(MARGIN + col_w + 14, grid_top),
               (MARGIN + col_w + 14, row1_bottom)], fill=(170, 170, 160), width=1)

    # Rule between row 1 and row 2.
    draw.line([(MARGIN, row1_bottom + 16), (W - MARGIN, row1_bottom + 16)],
              fill=RULE, width=1)
    row2_top = row1_bottom + 32

    # Row 2: stories 4 and 5.
    end3 = draw_block(draw, MARGIN, row2_top, col_w,
                      STORIES[3][0], STORIES[3][1],
                      h_size=30, s_size=20, h_leading=38, s_leading=27, gap=8)
    end4 = draw_block(draw, col2_x, row2_top, col_w,
                      STORIES[4][0], STORIES[4][1],
                      h_size=30, s_size=20, h_leading=38, s_leading=27, gap=8)
    row2_bottom = max(end3, end4)

    draw.line([(MARGIN + col_w + 14, row2_top),
               (MARGIN + col_w + 14, row2_bottom)], fill=(170, 170, 160), width=1)

    # Rule between row 2 and the final story.
    draw.line([(MARGIN, row2_bottom + 16), (W - MARGIN, row2_bottom + 16)],
              fill=RULE, width=1)
    last_top = row2_bottom + 32

    # Final story (full width).
    end5 = draw_block(draw, MARGIN, last_top, CONTENT,
                      STORIES[5][0], STORIES[5][1],
                      h_size=34, s_size=21, h_leading=42, s_leading=28, gap=10)

    # Footer rule and line.
    draw.line([(MARGIN, H - 56), (W - MARGIN, H - 56)], fill=RULE, width=2)
    foot = font(SANS, 18)
    footer = "THE WORLD  ·  WEDNESDAY 25 NOVEMBER 2026  ·  SIX STORIES, ONE PAGE"
    fw = draw.textlength(footer, font=foot)
    draw.text(((W - fw) / 2, H - 40), footer, font=foot, fill=GREY)

    img.save("news-frontpage.png", "PNG")
    print("wrote news-frontpage.png", img.size, img.mode)


if __name__ == "__main__":
    main()
