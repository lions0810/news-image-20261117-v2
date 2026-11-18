#!/usr/bin/env python3
"""Compose the news-image-20261117 V2 entry: a dense 1024x1024 broadsheet.

V2's lever over V1 is breadth: V1 carried 6 stories and ranked mid-field,
while the leaders carry 13-38. V2 keeps V1's four illustrated leads and adds
18 text briefs plus a 3-item ticker: 25 stories, all PIL-rendered text
(crisp, no generated lettering anywhere).

Layout (all px, canvas 1024x1024, white background):
  masthead black band .......... 92   (y 0..92)
  lead row, 4 illustrated ...... 228  (y 92..320: photo 148 + caption 80)
  "THE DAY IN BRIEF" header .... 34   (y 320..354)
  briefs grid, 3 cols x 6 rows . 620  (y 354..974, row pitch 103)
  footer ticker black band ..... 50   (y 974..1024)

Output is JPEG bytes written to a file named entry.png (the competition
accepts JPEG bytes under that name), at most 1,048,576 bytes.
"""

import io
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS_DIR = os.path.join(HERE, "panels")
OUT_PATH = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 8
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (232, 179, 60)    # #E8B33C
RED = (192, 57, 43)      # #C0392B
GREY = (120, 120, 120)
RULE = (200, 200, 200)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

MASTHEAD_H = 92
LEAD_PHOTO_H = 148
LEAD_CAP_H = 80
LEAD_H = LEAD_PHOTO_H + LEAD_CAP_H          # 228
HEADER_H = 34
FOOTER_H = 50
BRIEFS_Y = MASTHEAD_H + LEAD_H + HEADER_H   # 354
BRIEFS_H = H - FOOTER_H - BRIEFS_Y          # 620
COLS = 3
ROWS = 6
COL_W = (W - 2 * MARGIN - (COLS - 1) * 8) // COLS   # 330
ROW_H = BRIEFS_H // ROWS                            # 103

LEADS = [
    {
        "file": "media-generation-panel-crimea-bridge-0-666e66e5-1366-452d-baea-9108d5e479d8.png",
        "kicker": "UKRAINE \u00b7 WAR",
        "headline": "Ukraine strikes Crimea bridge in 1,300-drone barrage; Russia hits Kyiv bridges",
    },
    {
        "file": "media-generation-panel-hormuz-tanker-0-6baac136-3b2d-444e-8b14-89558850db6e.png",
        "kicker": "MIDDLE EAST \u00b7 GULF",
        "headline": "Iran drones hit U.S. radar in Bahrain; tanker mined in Hormuz strait",
    },
    {
        "file": "media-generation-panel-shenzhen-summit-0-2bba2baf-bb29-42a7-a370-de6095d60c1e.png",
        "kicker": "DIPLOMACY \u00b7 ASIA",
        "headline": "Xi, Trump and Putin to meet Thursday in Shenzhen",
    },
    {
        "file": "media-generation-panel-vulcan-rocket-0-08e1f691-99d6-438e-9d13-e51048e2b43c.png",
        "kicker": "SPACE \u00b7 BUSINESS",
        "headline": "Vulcan rocket fails; 40 Amazon satellites lost",
    },
]

# (kicker, headline, one-line summary) -- all real, reported 17 Nov 2026.
BRIEFS = [
    ("CYBERSECURITY",
     "Cyberattack hits 178 top websites via Optimizely",
     "Malicious code on BBC, CNN, Zoom and HSBC pages tried to steal crypto and card data and infect iPhones."),
    ("MARKETS",
     "Nasdaq falls 2.5% into correction in tech rout",
     "Nvidia slid 4.1% after Jensen Huang's ouster; the S&P 500 lost 1.9%, the Dow 1.4%, and oil and gold fell too."),
    ("CHIPMAKING",
     "Nvidia's $130bn outlook beats forecasts",
     "The sales forecast, above the $125bn analysts expected, lifted the chipmaker's shares 2% in late trading."),
    ("MIGRATION",
     "Five EU nations open Rwanda migrant-hub talks",
     "Austria, Germany, the Netherlands, Denmark and Greece plan a return centre for rejected asylum seekers."),
    ("UKRAINE TALKS",
     "Moscow refuses Europe a seat at peace talks",
     "Kremlin aide Yuri Ushakov said Russia has not agreed to European representatives joining the next round."),
    ("CLIMATE",
     "COP31 draft urges faster fossil-fuel exit",
     "The draft deal calls for 'accelerated action' to move away from fossil fuels as the summit nears its end."),
    ("THAILAND",
     "Fire rages through Thailand building, 11 dead",
     "Eleven people were killed as the fire tore through the building."),
    ("ARMS CONTROL",
     "US and Russia oppose autonomous-weapons talks",
     "Washington and Moscow will both resist opening negotiations on limiting autonomous weapons systems."),
    ("ENVIRONMENT",
     "US data centres emit as much as Denmark",
     "A new study finds America's hyperscale data centres produce emissions on the scale of a small nation."),
    ("IRAQ",
     "Iraq orders army into militia stronghold",
     "Baghdad ordered troops to enter the stronghold of an Iran-backed armed group."),
    ("ISRAEL",
     "Knesset set to elect speaker opposed to Netanyahu",
     "MPs were to choose a new speaker backed by the prime minister's opponents on Tuesday."),
    ("JAPAN",
     "Japan scrambles jets over Russian airspace breach",
     "Tokyo strongly protested after two suspected Russian aircraft violated its airspace early on Tuesday."),
    ("US AVIATION",
     "US flights nearly normal after ground stop",
     "Air travel recovered from a rare nationwide no-take-off order, though United was hit by a new system outage."),
    ("HEALTH",
     "Ebola cases double in DR Congo outbreak",
     "UN agencies reported the case count had doubled in the central African outbreak."),
    ("UKRAINE",
     "Ukraine's 2026 civilian toll tops earlier years",
     "The UN says civilian casualties this year already far exceed previous years' tolls."),
    ("HONG KONG",
     "Hong Kong switches on AI face recognition",
     "AI facial recognition has been rolled out across the city's CCTV network."),
    ("YEMEN",
     "Houthis seize ground on Yemen's south coast",
     "The group also said it had launched drones toward Saudi Arabia's East-West oil pipeline."),
    ("IRAN",
     "Iran bars UN nuclear inspectors until war ends",
     "Tehran refuses access to its damaged nuclear sites until the US meets its conditions, its deputy foreign minister said."),
]

TICKER_LINES = [
    "U.S. LOSES MEASLES-FREE STATUS AFTER 30 YEARS  \u2022  "
    "POPE FORGIVES MAN WHO HIT HIM IN THE EYE WITH A ROSARY IN PERU",
    "ROBERT PATTINSON NAMED THE NEW JAMES BOND  \u2022  "
    "ICC ELECTS JAY SHAH CHAIRMAN FOR A SECOND TERM",
]


def font(path, size):
    return ImageFont.truetype(path, size)


def centre_crop_resize(img, w, h):
    """Centre-crop to the target aspect ratio, then resize to (w, h)."""
    sw, sh = img.size
    target = w / h
    src = sw / sh
    if src > target:  # too wide: crop sides
        nw = int(sh * target)
        x0 = (sw - nw) // 2
        img = img.crop((x0, 0, x0 + nw, sh))
    else:  # too tall: crop top/bottom
        nh = int(sw / target)
        y0 = (sh - nh) // 2
        img = img.crop((0, y0, sw, y0 + nh))
    return img.resize((w, h), Image.LANCZOS)


def wrap_text(draw, text, fnt, max_width, max_lines=None):
    """Greedy word wrap; returns the list of lines (optionally capped)."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines is not None:
        lines = lines[:max_lines]
    return lines


def fit_font(draw, text, path, start_size, max_width, min_size=12):
    """Largest font size (<= start_size) at which text fits max_width."""
    size = start_size
    while size > min_size:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= max_width:
            return fnt
        size -= 1
    return font(path, min_size)


def draw_centred(draw, y, text, fnt, fill, letter_spacing=0):
    """Draw text centred horizontally at y; optional extra px between chars."""
    if letter_spacing <= 0:
        w = draw.textlength(text, font=fnt)
        draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
        return
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + letter_spacing * (len(text) - 1)
    x = (W - total) / 2
    for ch, cw in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += cw + letter_spacing


def draw_masthead(draw):
    draw.rectangle([0, 0, W, MASTHEAD_H], fill=BLACK)
    date_font = fit_font(draw, "TUESDAY, 17 NOVEMBER 2026", BOLD, 46, W - 40)
    draw_centred(draw, 10, "TUESDAY, 17 NOVEMBER 2026", date_font, WHITE)
    strap_font = font(BOLD, 21)
    draw_centred(draw, 62, "THE WORLD IN ONE DAY", strap_font, GOLD, letter_spacing=6)


def draw_leads(canvas, draw):
    lead_w = (W - 2 * MARGIN - 3 * 8) // 4  # 246
    for i, panel in enumerate(LEADS):
        x0 = MARGIN + i * (lead_w + 8)
        y0 = MASTHEAD_H
        src = Image.open(os.path.join(PANELS_DIR, panel["file"])).convert("RGB")
        canvas.paste(centre_crop_resize(src, lead_w, LEAD_PHOTO_H), (x0, y0))
        cap_y = y0 + LEAD_PHOTO_H
        draw.text((x0 + 2, cap_y + 4), panel["kicker"], font=font(BOLD, 13), fill=RED)
        head_font = font(BOLD, 16)
        lines = wrap_text(draw, panel["headline"], head_font, lead_w - 4, max_lines=3)
        ly = cap_y + 22
        for line in lines:
            draw.text((x0 + 2, ly), line, font=head_font, fill=BLACK)
            ly += 19


def draw_header(draw):
    y = MASTHEAD_H + LEAD_H
    draw.rectangle([0, y, W, y + HEADER_H], fill=BLACK)
    fnt = font(BOLD, 19)
    text = "THE DAY IN BRIEF \u00b7 AROUND THE WORLD"
    draw_centred(draw, y + 6, text, fnt, WHITE, letter_spacing=3)


def draw_briefs(draw):
    kicker_font = font(BOLD, 11)
    for idx, (kicker, headline, summary) in enumerate(BRIEFS):
        col, row = idx % COLS, idx // COLS
        x0 = MARGIN + col * (COL_W + 8)
        y0 = BRIEFS_Y + row * ROW_H
        if row > 0:
            draw.line([x0, y0 - 5, x0 + COL_W, y0 - 5], fill=RULE, width=1)
        draw.text((x0, y0 + 1), kicker, font=kicker_font, fill=RED)
        head_font = font(BOLD, 15)
        hlines = wrap_text(draw, headline, head_font, COL_W, max_lines=2)
        if len(hlines) > 2:
            head_font = font(BOLD, 14)
            hlines = wrap_text(draw, headline, head_font, COL_W, max_lines=2)
        ly = y0 + 17
        for line in hlines:
            draw.text((x0, ly), line, font=head_font, fill=BLACK)
            ly += 18
        sum_font = font(REGULAR, 13)
        slines = wrap_text(draw, summary, sum_font, COL_W, max_lines=3)
        sy = ly + 2
        for line in slines:
            draw.text((x0, sy), line, font=sum_font, fill=(40, 40, 40))
            sy += 16


def draw_footer(draw):
    fy = H - FOOTER_H
    draw.rectangle([0, fy, W, H], fill=BLACK)
    # Two centred ticker lines; each is fitted and asserted so a line can
    # never silently run off the canvas again (V2's first cut clipped one).
    line_h = FOOTER_H // 2
    for i, line in enumerate(TICKER_LINES):
        fnt = fit_font(draw, line, REGULAR, 15, W - 24, min_size=11)
        assert draw.textlength(line, font=fnt) <= W - 24, line
        bbox = draw.textbbox((0, 0), line, font=fnt)
        th = bbox[3] - bbox[1]
        draw_centred(draw, fy + i * line_h + (line_h - th) / 2 - bbox[1],
                     line, fnt, WHITE)


def compose():
    canvas = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(canvas)
    draw_masthead(draw)
    draw_leads(canvas, draw)
    draw_header(draw)
    draw_briefs(draw)
    draw_footer(draw)
    return canvas


def main():
    canvas = compose()
    assert canvas.size == (W, H), canvas.size
    # JPEG bytes under the name entry.png; lower quality until under the limit.
    for quality in (88, 85, 82, 80, 78, 75):
        buf = io.BytesIO()
        canvas.save(buf, format="JPEG", quality=quality)
        data = buf.getvalue()
        if len(data) <= 1_048_576:
            break
    with open(OUT_PATH, "wb") as fh:
        fh.write(data)
    print(f"wrote {OUT_PATH}: {len(data)} bytes, quality={quality}, size={canvas.size}")


if __name__ == "__main__":
    main()
