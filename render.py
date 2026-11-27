"""Render the original, shape-only daily news front page."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
BG = "#F6F3EA"
INK = "#172425"
ACCENT = "#CB4628"
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(size, bold=False):
    return ImageFont.truetype(
        FONT_DIR + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size
    )


im = Image.new("RGB", (1024, 1024), BG)
d = ImageDraw.Draw(im)


def label(x, y, value, size, bold=False, fill=INK, limit=None):
    face = font(size, bold)
    if limit is not None:
        assert d.textlength(value, font=face) <= limit, (value, d.textlength(value, font=face), limit)
    d.text((x, y), value, font=face, fill=fill, anchor="lt")


def icon(x, y, kind):
    """A 28px geometric sign for each story."""
    if kind == "storm":
        d.polygon([(x+16,y),(x+3,y+16),(x+14,y+16),(x+9,y+29),(x+27,y+10),(x+17,y+10)], fill=ACCENT)
    elif kind in ("trump", "nz", "ecb", "asml"):
        d.rectangle((x+2,y+9,x+26,y+27), outline=ACCENT, width=3)
        d.polygon([(x,y+7),(x+14,y),(x+28,y+7)], fill=ACCENT)
        d.line((x+10,y+12,x+10,y+24), fill=ACCENT, width=3)
        d.line((x+19,y+12,x+19,y+24), fill=ACCENT, width=3)
    elif kind in ("ukraine", "kim"):
        d.polygon([(x+14,y),(x+28,y+27),(x,y+27)], outline=ACCENT, width=3)
        d.line((x+14,y+9,x+14,y+17), fill=ACCENT, width=3)
        d.ellipse((x+12,y+21,x+16,y+25), fill=ACCENT)
    elif kind == "uk":
        d.line((x,y+3,x+10,y+13,x+18,y+13,x+27,y+26), fill=ACCENT, width=4)
        d.line((x+16,y+26,x+27,y+26,x+27,y+15), fill=ACCENT, width=3)
    elif kind in ("houthi", "bangkok"):
        d.polygon([(x+14,y),(x+26,y+18),(x+24,y+25),(x+14,y+29),(x+3,y+24),(x+1,y+17)], fill=ACCENT)
        d.polygon([(x+14,y+13),(x+20,y+23),(x+14,y+26),(x+9,y+23)], fill=BG)
    elif kind == "musk":
        d.polygon([(x+14,y),(x+22,y+12),(x+22,y+24),(x+6,y+24),(x+6,y+12)], fill=ACCENT)
        d.ellipse((x+11,y+10,x+17,y+16), fill=BG)
        d.line((x+11,y+27,x+11,y+31), fill=ACCENT, width=3)
        d.line((x+18,y+27,x+18,y+31), fill=ACCENT, width=3)
    elif kind == "ferry":
        d.rectangle((x+7,y+5,x+22,y+17), outline=ACCENT, width=3)
        d.polygon([(x,y+18),(x+28,y+18),(x+22,y+27),(x+6,y+27)], fill=ACCENT)
    else:
        d.rectangle((x+4,y+4,x+24,y+24), outline=ACCENT, width=3)
        for z in (8, 18):
            d.line((x+z,y,x+z,y+28), fill=ACCENT, width=2)
            d.line((x,y+z,x+28,y+z), fill=ACCENT, width=2)


# Masthead and a date large enough to survive the thumbnail.
label(26, 15, "THE WORLD IN ONE DAY", 32, True)
label(26, 55, "Friday, 27 November 2026", 38, True, ACCENT)
d.line((26, 104, 998, 104), fill=INK, width=3)

for y, line in zip((119, 184, 249), ("DRONE STRIKE", "KILLS 2 ITALIANS", "IN KUWAIT")):
    label(26, y, line, 64, True, limit=740)
label(26, 322, "Iran denies role; Trump claims", 34)
label(26, 362, "'victory at hand'", 34)

# Flat refinery illustration: tanks, stacks, pipework and a drone silhouette.
d.ellipse((803,132,961,290), outline=ACCENT, width=3)
d.rectangle((823,230,938,281), fill=BG)
d.rectangle((825,222,864,278), outline=INK, width=4)
d.ellipse((825,213,864,234), fill=BG, outline=INK, width=4)
d.rectangle((881,206,899,278), fill=INK)
d.rectangle((918,190,934,278), fill=INK)
d.line((810,280,968,280), fill=ACCENT, width=5)
d.line((846,250,846,265,946,265,946,280), fill=INK, width=4)
d.polygon([(805,160),(878,171),(951,160),(898,181),(888,194),(870,194),(860,181)], fill=INK)
d.line((879,150,879,177), fill=INK, width=5)
d.line((851,153,907,153), fill=INK, width=4)

stories = [
    ("US STORM", "900,000+ lose power", "storm"),
    ("TRUMP'S CALL", "Tells Putin: pull back", "trump"),
    ("UKRAINE ALERT", "Warns of new air attack", "ukraine"),
    ("NZ DEADLOCK", "Luxon one seat short", "nz"),
    ("UK MIGRATION", "Lowest since '97, ex-COVID", "uk"),
    ("ECB PICK", "Spain's de Cos to lead", "ecb"),
    ("HOUTHI CLAIM", "Saudi refinery; oil up", "houthi"),
    ("BANGKOK FIRE", "Bangchak shuts all units", "bangkok"),
    ("KIM'S NUKES", "Urges wider tactical use", "kim"),
    ("MUSK PLEDGE", "SpaceX stock for US kids", "musk"),
    ("ASML CURBS", "Dutch resist US on China", "asml"),
    ("HK FERRY", "At least 25 injured", "ferry"),
    ("AI ATTACK TOOLS", "~4,200 exposed; Microsoft: 6+ groups use ARTEX", "ai"),
]

for i, (title, summary, kind) in enumerate(stories):
    row, col = divmod(i, 2)
    x = 26 + col * 500
    y = 410 + row * 86
    wide = i == 12
    width = 972 if wide else 472
    d.line((x, y, x+width, y), fill=INK, width=1)
    label(x, y+8, title, 44, True, limit=width-36)
    label(x, y+49, summary, 34, limit=width)
    icon(x+width-29, y+12, kind)

im.save(ROOT / "entry.png", optimize=True)
print("Rendered entry.png:", (ROOT / "entry.png").stat().st_size, "bytes")
