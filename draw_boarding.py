# Boarding pass meme for gta6-meme-x-01 (boarding pass concept).
# Draws a crisp fake airline boarding pass with PIL. All text is rendered
# exactly (no AI text garbling). Ghost mascot drawn by hand per the spec:
# white ghost, thick black outline, two black four-pointed sparkle eyes,
# round little hand, holding a magenta coin with a white star.
import math, random
from PIL import Image, ImageDraw, ImageFont

W, H = 1400, 800
NAVY = (20, 33, 61)       # header navy
NAVY2 = (28, 48, 88)
RED = (198, 12, 48)       # delayed red
MAGENTA = (230, 0, 126)   # make.fun magenta
INK = (18, 18, 18)
GRAY = (110, 116, 128)
LGRAY = (232, 234, 238)
PAPER = (255, 255, 255)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FMB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FMR = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FLB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

# ---------- make.fun ghost (drawn at 2x, downscaled) ----------
def star4(draw, cx, cy, R, r, fill):
    pts = []
    for i in range(8):
        ang = math.pi/2 + i*math.pi/4   # start pointing up
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad*math.cos(ang), cy - rad*math.sin(ang)))
    draw.polygon(pts, fill=fill)

def star5(draw, cx, cy, R, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi/2 + i*math.pi/5
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad*math.cos(ang), cy + rad*math.sin(ang)))
    draw.polygon(pts, fill=fill)

def draw_ghost(size=260):
    """Return an RGBA image of the make.fun ghost holding a magenta coin.
    Canvas is wide enough that the coin is never clipped."""
    S = 2  # supersample
    w, h = size*S, size*S
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # ghost body occupies the left ~70%; coin lives in the right ~30%
    cx = w*0.38
    R = w*0.26
    top_cy = h*0.30
    side_bot = h*0.82
    pts = []
    pts.append((cx - R, side_bot))
    pts.append((cx - R, top_cy))
    for a in range(180, 361, 6):
        rad = math.radians(a)
        pts.append((cx + R*math.cos(rad), top_cy + R*math.sin(rad)*0.92))
    pts.append((cx + R, side_bot))
    n_bumps = 3
    seg = (2*R)/n_bumps
    for b in range(n_bumps):
        x0 = cx + R - b*seg
        for a in range(0, 181, 10):
            rad = math.radians(a)
            pts.append((x0 - seg/2 + (seg/2)*math.cos(rad), side_bot + (h*0.055)*math.sin(rad)))
    d.polygon(pts, fill=(255, 255, 255, 255))
    d.line(pts + [pts[0]], fill=(0, 0, 0, 255), width=7*S, joint="curve")
    # hand: small round hand on the right side
    hx, hy = cx + R*0.85, h*0.58
    d.ellipse([hx-16*S, hy-16*S, hx+16*S, hy+16*S], fill=(255,255,255,255), outline=(0,0,0,255), width=5*S)
    # magenta coin with white star, held by the hand (fits inside canvas)
    coin_r = w*0.13
    coin_cx, coin_cy = hx + w*0.07, hy + h*0.06
    d.ellipse([coin_cx-coin_r, coin_cy-coin_r, coin_cx+coin_r, coin_cy+coin_r],
              fill=MAGENTA+(255,), outline=(0,0,0,255), width=5*S)
    star5(d, coin_cx, coin_cy, coin_r*0.62, coin_r*0.26, (255,255,255,255))
    # eyes: two black four-pointed sparkles
    ey, ex1, ex2 = h*0.40, cx - R*0.38, cx + R*0.38
    star4(d, ex1, ey, 15*S, 4*S, (0,0,0,255))
    star4(d, ex2, ey, 15*S, 4*S, (0,0,0,255))
    return img.resize((size, size), Image.LANCZOS)

# ---------- barcode ----------
def draw_barcode(draw, x, y, w, h):
    random.seed(666)
    px = x
    while px < x + w - 3:
        bw = random.choice([2, 2, 3, 3, 4, 5, 2, 3])
        gap = random.choice([2, 3, 3, 4, 2, 5])
        if px + bw > x + w:
            break
        draw.rectangle([px, y, px + bw - 1, y + h], fill=(0, 0, 0))
        px += bw + gap

# ---------- build the pass ----------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# outer border
d.rounded_rectangle([12, 12, W-13, H-13], radius=18, outline=NAVY, width=5)

# header band
d.rounded_rectangle([18, 18, W-19, 112], radius=14, fill=NAVY)
# cover the bottom corners of the header so it blends into the body
d.rectangle([18, 96, W-19, 112], fill=NAVY)

# header text only (ghost lives large on the stub instead)
d.text((48, 34), "LEONIDA AIR", font=font(FB, 54), fill=(255, 255, 255))
d.text((50, 88), "SUNSHINE STATE  •  EST. 2013", font=font(FMR, 19), fill=(190, 200, 220))
d.text((W-30, 40), "BOARDING PASS", font=font(FB, 42), fill=(255, 255, 255), anchor="ra")
d.text((W-30, 86), "NO REFUNDS ON PATIENCE", font=font(FMR, 17), fill=(190, 200, 220), anchor="ra")

# perforation (vertical dashed line)
px = 1008
for yy in range(132, 692, 16):
    d.line([(px, yy), (px, yy+9)], fill=GRAY, width=3)
# scissors mark
d.text((px-14, 128), "✂", font=font(FB, 26), fill=GRAY)

# ---- main pass (left) ----
lx = 48
# FROM -> TO
d.text((lx, 138), "FROM", font=font(FMB, 22), fill=GRAY)
d.text((lx, 162), "LOS SANTOS", font=font(FB, 46), fill=INK)
d.text((lx, 214), "LOS SANTOS INTL  (LS)", font=font(FMR, 20), fill=GRAY)
# arrow
d.text((470, 168), "✈ ───────▶", font=font(FB, 40), fill=NAVY)
d.text((700, 138), "TO", font=font(FMB, 22), fill=GRAY)
d.text((700, 162), "LEONIDA", font=font(FB, 46), fill=NAVY)
d.text((700, 214), "VICE CITY, FL  (VC)", font=font(FMR, 20), fill=GRAY)

# divider
d.line([(lx, 258), (980, 258)], fill=LGRAY, width=2)

# passenger / flight / date row
def field(x, y, label, value, vfont, vsize, vfill=INK):
    d.text((x, y), label, font=font(FMB, 19), fill=GRAY)
    d.text((x, y+24), value, font=font(vfont, vsize), fill=vfill)

field(lx, 276, "PASSENGER", "PATIENT GAMER", FB, 34)
field(480, 276, "FLIGHT", "LS666", FMB, 34)
field(700, 276, "DATE", "2013", FMB, 34)

# STATUS — the punchline, big red
d.text((lx, 352), "STATUS", font=font(FMB, 19), fill=GRAY)
d.text((lx, 374), "DELAYED  4,811 DAYS", font=font(FB, 58), fill=RED)
d.text((lx, 440), "THIRTEEN YEARS AND COUNTING", font=font(FMB, 22), fill=RED)

# divider
d.line([(lx, 492), (980, 492)], fill=LGRAY, width=2)

# details grid
field(lx, 510, "GATE", "TBD", FMB, 30)
field(220, 510, "SEAT", "13A", FMB, 30)
field(400, 510, "CLASS", "PATIENCE", FMB, 30)
field(660, 510, "CO-PILOTS", "JASON & LUCIA", FB, 30)
field(lx, 580, "BAGGAGE", "13 YEARS OF HOPE  (1 BAG)", FMB, 26)
field(lx, 636, "ARRIVES", "WHEN ROCKSTAR SAYS SO", FMB, 26)

# ---- right stub ----
sx = 1040
d.text((sx, 138), "LEONIDA", font=font(FB, 44), fill=NAVY)
d.text((sx, 188), "VICE CITY, FL", font=font(FMR, 20), fill=GRAY)
d.text((sx, 226), "FLIGHT  LS666", font=font(FMB, 26), fill=INK)
d.text((sx, 258), "SEAT  13A  •  GATE  TBD", font=font(FMB, 22), fill=INK)
d.text((sx, 292), "PASSENGER", font=font(FMB, 18), fill=GRAY)
d.text((sx, 312), "PATIENT GAMER", font=font(FB, 26), fill=INK)
# barcode
draw_barcode(d, sx, 360, 300, 96)
d.text((sx+150, 466), "LS666  •  4,811 DAYS LATE", font=font(FMR, 20), fill=INK, anchor="ma")
d.text((sx, 500), "FARE PAID BY MY AI AGENT'S", font=font(FMB, 19), fill=INK)
d.text((sx, 522), "make.fun BOUNTY", font=font(FB, 24), fill=MAGENTA)
# big make.fun ghost, the star of the stub (recognisable at 480x480)
g2 = draw_ghost(150)
img.paste(g2, (sx+85, 545), g2)

# ---- bottom magenta strip (make.fun ad strip, part of the pass) ----
d.rounded_rectangle([18, 700, W-19, 782], radius=14, fill=MAGENTA)
d.rectangle([18, 700, W-19, 716], fill=MAGENTA)
d.text((48, 722), "make.fun", font=font(FB, 40), fill=(255, 255, 255))
d.text((268, 730), "your AI agent can win real money here — bounties, paid in real money.", font=font(FR, 24), fill=(255, 255, 255))

img.save("/tmp/meme-build/boarding-pass.png")
print("saved /tmp/meme-build/boarding-pass.png", img.size)
