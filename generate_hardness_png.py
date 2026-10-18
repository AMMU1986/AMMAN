#!/usr/bin/env python3
"""
Render the API X70 SMAW microhardness traverse (with/without hydrogen charging)
to a PNG, using ONLY the Python standard library (zlib, struct).

Reads hardness_profile_data.csv (produced by generate_hardness_profile.py) and
writes hardness_profile.png. A tiny built-in 5x7 bitmap font is used for all
text, so no fonts, matplotlib, PIL, cairo or browser are required.
"""

import csv
import struct
import zlib

# ---------------------------------------------------------------------------
# 5x7 bitmap font (row-major, 5 wide x 7 tall). '#' = pixel on.
# ---------------------------------------------------------------------------
F = {
 ' ': ["     ","     ","     ","     ","     ","     ","     "],
 '-': ["     ","     ","     "," ### ","     ","     ","     "],
 '.': ["     ","     ","     ","     ","     "," ##  "," ##  "],
 ',': ["     ","     ","     ","     ","  #  ","  #  "," #   "],
 '(': ["   # ","  #  "," #   "," #   "," #   ","  #  ","   # "],
 ')': [" #   ","  #  ","   # ","   # ","   # ","  #  "," #   "],
 '/': ["    #","    #","   # ","  #  "," #   ","#    ","#    "],
 ':': ["     ","  #  ","  #  ","     ","  #  ","  #  ","     "],
 '+': ["     ","  #  ","  #  ","#####","  #  ","  #  ","     "],
 '>': ["#    "," #   ","  #  ","   # ","  #  "," #   ","#    "],
 '0': [" ### ","#   #","#  ##","# # #","##  #","#   #"," ### "],
 '1': ["  #  "," ##  ","  #  ","  #  ","  #  ","  #  "," ### "],
 '2': [" ### ","#   #","    #","   # ","  #  "," #   ","#####"],
 '3': ["#####","   # ","  #  ","   # ","    #","#   #"," ### "],
 '4': ["   # ","  ## "," # # ","#  # ","#####","   # ","   # "],
 '5': ["#####","#    ","#### ","    #","    #","#   #"," ### "],
 '6': [" ### ","#    ","#    ","#### ","#   #","#   #"," ### "],
 '7': ["#####","    #","   # ","  #  "," #   "," #   "," #   "],
 '8': [" ### ","#   #","#   #"," ### ","#   #","#   #"," ### "],
 '9': [" ### ","#   #","#   #"," ####","    #","    #"," ### "],
 'A': [" ### ","#   #","#   #","#####","#   #","#   #","#   #"],
 'B': ["#### ","#   #","#   #","#### ","#   #","#   #","#### "],
 'C': [" ### ","#   #","#    ","#    ","#    ","#   #"," ### "],
 'D': ["#### ","#   #","#   #","#   #","#   #","#   #","#### "],
 'E': ["#####","#    ","#    ","#### ","#    ","#    ","#####"],
 'F': ["#####","#    ","#    ","#### ","#    ","#    ","#    "],
 'G': [" ### ","#   #","#    ","# ###","#   #","#   #"," ### "],
 'H': ["#   #","#   #","#   #","#####","#   #","#   #","#   #"],
 'I': [" ### ","  #  ","  #  ","  #  ","  #  ","  #  "," ### "],
 'J': ["  ###","   # ","   # ","   # ","#  # ","#  # "," ##  "],
 'K': ["#   #","#  # ","# #  ","##   ","# #  ","#  # ","#   #"],
 'L': ["#    ","#    ","#    ","#    ","#    ","#    ","#####"],
 'M': ["#   #","## ##","# # #","# # #","#   #","#   #","#   #"],
 'N': ["#   #","##  #","# # #","# # #","#  ##","#   #","#   #"],
 'O': [" ### ","#   #","#   #","#   #","#   #","#   #"," ### "],
 'P': ["#### ","#   #","#   #","#### ","#    ","#    ","#    "],
 'Q': [" ### ","#   #","#   #","#   #","# # #","#  # "," ## #"],
 'R': ["#### ","#   #","#   #","#### ","# #  ","#  # ","#   #"],
 'S': [" ####","#    ","#    "," ### ","    #","    #","#### "],
 'T': ["#####","  #  ","  #  ","  #  ","  #  ","  #  ","  #  "],
 'U': ["#   #","#   #","#   #","#   #","#   #","#   #"," ### "],
 'V': ["#   #","#   #","#   #","#   #","#   #"," # # ","  #  "],
 'W': ["#   #","#   #","#   #","# # #","# # #","## ##","#   #"],
 'X': ["#   #","#   #"," # # ","  #  "," # # ","#   #","#   #"],
 'Y': ["#   #","#   #"," # # ","  #  ","  #  ","  #  ","  #  "],
 'Z': ["#####","    #","   # ","  #  "," #   ","#    ","#####"],
 'a': ["     ","     "," ### ","    #"," ####","#   #"," ####"],
 'b': ["#    ","#    ","#### ","#   #","#   #","#   #","#### "],
 'c': ["     ","     "," ### ","#   #","#    ","#   #"," ### "],
 'd': ["    #","    #"," ####","#   #","#   #","#   #"," ####"],
 'e': ["     ","     "," ### ","#   #","#####","#    "," ### "],
 'f': ["  ## "," #   ","###  "," #   "," #   "," #   "," #   "],
 'g': ["     "," ####","#   #","#   #"," ####","    #"," ### "],
 'h': ["#    ","#    ","#### ","#   #","#   #","#   #","#   #"],
 'i': ["  #  ","     "," ##  ","  #  ","  #  ","  #  "," ### "],
 'j': ["   # ","     ","  ## ","   # ","   # ","#  # "," ##  "],
 'k': ["#    ","#    ","#  # ","# #  ","##   ","# #  ","#  # "],
 'l': [" ##  ","  #  ","  #  ","  #  ","  #  ","  #  "," ### "],
 'm': ["     ","     ","## # ","# # #","# # #","# # #","#   #"],
 'n': ["     ","     ","#### ","#   #","#   #","#   #","#   #"],
 'o': ["     ","     "," ### ","#   #","#   #","#   #"," ### "],
 'p': ["     ","#### ","#   #","#   #","#### ","#    ","#    "],
 'q': ["     "," ####","#   #","#   #"," ####","    #","    #"],
 'r': ["     ","     ","# ## ","##  #","#    ","#    ","#    "],
 's': ["     ","     "," ####","#    "," ### ","    #","#### "],
 't': [" #   "," #   ","#### "," #   "," #   "," #  #","  ## "],
 'u': ["     ","     ","#   #","#   #","#   #","#  ##"," ## #"],
 'v': ["     ","     ","#   #","#   #","#   #"," # # ","  #  "],
 'w': ["     ","     ","#   #","#   #","# # #","# # #"," # # "],
 'x': ["     ","     ","#   #"," # # ","  #  "," # # ","#   #"],
 'y': ["     ","#   #","#   #","#   #"," ####","    #"," ### "],
 'z': ["     ","     ","#####","   # ","  #  "," #   ","#####"],
}

GLYPH_W, GLYPH_H = 5, 7

# ---------------------------------------------------------------------------
# Image buffer
# ---------------------------------------------------------------------------
W, H = 1300, 800
img = bytearray([255]) * (W * H * 3)


def set_px(x, y, rgb):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        img[i], img[i + 1], img[i + 2] = rgb


def fill_rect(x0, y0, x1, y1, rgb):
    if x1 < x0:
        x0, x1 = x1, x0
    if y1 < y0:
        y0, y1 = y1, y0
    for y in range(max(0, y0), min(H, y1 + 1)):
        base = y * W * 3
        for x in range(max(0, x0), min(W, x1 + 1)):
            i = base + x * 3
            img[i], img[i + 1], img[i + 2] = rgb


def draw_dot(x, y, r, rgb):
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                set_px(x + dx, y + dy, rgb)


def draw_line(x0, y0, x1, y1, rgb, thick=1):
    x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    r = max(0, thick // 2)
    while True:
        if r == 0:
            set_px(x0, y0, rgb)
        else:
            draw_dot(x0, y0, r, rgb)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def dashed_vline(x, y0, y1, rgb, dash=7, gap=5):
    y = y0
    while y < y1:
        draw_line(x, y, x, min(y + dash, y1), rgb, 1)
        y += dash + gap


def text(x, y, s, rgb, scale=2, spacing=1):
    """Top-left anchored text; returns total pixel width drawn."""
    cx = x
    for ch in s:
        g = F.get(ch, F.get(ch.upper()))
        if g is None:
            cx += (GLYPH_W + spacing) * scale
            continue
        for r in range(GLYPH_H):
            row = g[r]
            for c in range(GLYPH_W):
                if row[c] != ' ':
                    fill_rect(cx + c * scale, y + r * scale,
                              cx + c * scale + scale - 1,
                              y + r * scale + scale - 1, rgb)
        cx += (GLYPH_W + spacing) * scale
    return cx - x


def text_w(s, scale=2, spacing=1):
    return len(s) * (GLYPH_W + spacing) * scale


def text_center(xc, y, s, rgb, scale=2):
    text(xc - text_w(s, scale) // 2, y, s, rgb, scale)

# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------
BLACK = (0, 0, 0)
DGREY = (51, 51, 51)
GREY = (90, 90, 90)
GRID = (223, 223, 223)
LGREY = (190, 190, 190)
BLUE = (31, 95, 208)
RED = (208, 32, 32)
C_BM = (234, 242, 233)
C_HAZ = (253, 236, 236)
C_FZ = (234, 240, 251)

# ---------------------------------------------------------------------------
# Plot geometry
# ---------------------------------------------------------------------------
ML, MR, MT, MB = 120, 300, 140, 90
PW, PH = W - ML - MR, H - MT - MB
X_MIN, X_MAX = -8.0, 8.0
Y_MIN, Y_MAX = 170.0, 300.0
X_TICKS = [-8, -6, -4, -2, 0, 2, 4, 6, 8]
Y_TICKS = [170, 190, 210, 230, 250, 270, 290]


def px(x):
    return int(round(ML + (x - X_MIN) / (X_MAX - X_MIN) * PW))


def py(y):
    return int(round(MT + (Y_MAX - y) / (Y_MAX - Y_MIN) * PH))

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
xs, y_unch, y_chg = [], [], []
with open("hardness_profile_data.csv", newline="") as f:
    r = csv.reader(f)
    next(r)
    for row in r:
        xs.append(float(row[0]))
        y_unch.append(float(row[2]))
        y_chg.append(float(row[3]))

# ---------------------------------------------------------------------------
# Draw: region bands
# ---------------------------------------------------------------------------
bands = [(-8.0, -7.5, C_BM, "BM"), (-7.5, -5.0, C_HAZ, "HAZ"),
         (-5.0, 5.0, C_FZ, "Weld (FZ)"), (5.0, 7.5, C_HAZ, "HAZ"),
         (7.5, 8.0, C_BM, "BM")]
for x0, x1, col, lab in bands:
    fill_rect(px(x0), MT, px(x1), MT + PH, col)

# horizontal gridlines + y tick labels
for yt in Y_TICKS:
    yc = py(yt)
    draw_line(ML, yc, ML + PW, yc, GRID, 1)
    text(ML - 44, yc - 7, str(yt), DGREY, 2)

# vertical dashed region boundaries
for xb in (-7.5, -5.0, 5.0, 7.5):
    dashed_vline(px(xb), MT, MT + PH, LGREY)

# band labels (top, inside plot)
for x0, x1, col, lab in bands:
    xm = (px(x0) + px(x1)) // 2
    sc = 2
    text_center(xm, MT + 8, lab, GREY, sc)

# data curves
for i in range(len(xs) - 1):
    draw_line(px(xs[i]), py(y_unch[i]), px(xs[i + 1]), py(y_unch[i + 1]), BLUE, 2)
for i in range(len(xs) - 1):
    draw_line(px(xs[i]), py(y_chg[i]), px(xs[i + 1]), py(y_chg[i + 1]), RED, 2)

# plot frame
draw_line(ML, MT, ML + PW, MT, DGREY, 2)
draw_line(ML, MT + PH, ML + PW, MT + PH, DGREY, 2)
draw_line(ML, MT, ML, MT + PH, DGREY, 2)
draw_line(ML + PW, MT, ML + PW, MT + PH, DGREY, 2)

# x ticks + labels
for xt in X_TICKS:
    xc = px(xt)
    draw_line(xc, MT + PH, xc, MT + PH + 7, DGREY, 2)
    text_center(xc, MT + PH + 14, str(xt), DGREY, 2)

# axis titles (horizontal)
text_center(ML + PW // 2, MT + PH + 46, "Distance from weld centreline (mm)", BLACK, 2)
text(ML - 44, MT - 26, "Vickers microhardness (HV0.5)", BLACK, 2)

# title + subtitle
text(ML, 24, "API X70 SMAW weldment - microhardness traverse", BLACK, 3)
text(ML, 64, "Effect of cathodic hydrogen charging "
             "(0.5 M H2SO4 + 5 g/L thiourea, 50 mA/cm2, 10 h)", GREY, 2)

# legend box (right margin)
lx, ly, lw, lh = ML + PW + 30, MT, 250, 220
fill_rect(lx, ly, lx + lw, ly + lh, (255, 255, 255))
draw_line(lx, ly, lx + lw, ly, LGREY, 1)
draw_line(lx, ly + lh, lx + lw, ly + lh, LGREY, 1)
draw_line(lx, ly, lx, ly + lh, LGREY, 1)
draw_line(lx + lw, ly, lx + lw, ly + lh, LGREY, 1)
text(lx + 14, ly + 14, "Legend", BLACK, 3)
draw_line(lx + 14, ly + 56, lx + 54, ly + 56, BLUE, 3)
text(lx + 64, ly + 48, "Without charging", BLACK, 2)
draw_line(lx + 14, ly + 86, lx + 54, ly + 86, RED, 3)
text(lx + 64, ly + 78, "With H charging", BLACK, 2)
text(lx + 14, ly + 118, "Region HV (unch -> chg):", GREY, 2)
text(lx + 14, ly + 146, "BM  214 -> 220", DGREY, 2)
text(lx + 14, ly + 170, "FZ  196 -> 209", DGREY, 2)
text(lx + 14, ly + 194, "HAZ 252.6 -> 275", DGREY, 2)

# ---------------------------------------------------------------------------
# Encode PNG (stdlib only)
# ---------------------------------------------------------------------------
def png_chunk(tag, data):
    return (struct.pack(">I", len(data)) + tag + data +
            struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))


raw = bytearray()
for y in range(H):
    raw.append(0)  # filter type 0
    raw.extend(img[y * W * 3:(y + 1) * W * 3])

sig = b"\x89PNG\r\n\x1a\n"
ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)  # 8-bit RGB
idat = zlib.compress(bytes(raw), 9)
with open("hardness_profile.png", "wb") as f:
    f.write(sig)
    f.write(png_chunk(b"IHDR", ihdr))
    f.write(png_chunk(b"IDAT", idat))
    f.write(png_chunk(b"IEND", b""))

print("Wrote hardness_profile.png ({}x{} px)".format(W, H))
