#!/usr/bin/env python3
"""
Pure-Python (stdlib-only) PNG line-chart renderer. Draws the REAL solver curves
stored in results_data.py. No matplotlib. Produces 7 publication-style figures.
"""

import struct
import zlib
import os
import math
from results_data import DATA

OUT = "/projects/sandbox/AMMAN/fractional_figures"
os.makedirs(OUT, exist_ok=True)

W, H = 820, 560
ML, MR, MT, MB = 95, 40, 60, 70   # margins
PW = W - ML - MR
PH = H - MT - MB

# simple 5x7 bitmap font for axis labels / legend (digits, letters, symbols)
FONT = {
    '0': ["01110","10001","10011","10101","11001","10001","01110"],
    '1': ["00100","01100","00100","00100","00100","00100","01110"],
    '2': ["01110","10001","00001","00010","00100","01000","11111"],
    '3': ["11111","00010","00100","00010","00001","10001","01110"],
    '4': ["00010","00110","01010","10010","11111","00010","00010"],
    '5': ["11111","10000","11110","00001","00001","10001","01110"],
    '6': ["00110","01000","10000","11110","10001","10001","01110"],
    '7': ["11111","00001","00010","00100","01000","01000","01000"],
    '8': ["01110","10001","10001","01110","10001","10001","01110"],
    '9': ["01110","10001","10001","01111","00001","00010","01100"],
    '.': ["00000","00000","00000","00000","00000","01100","01100"],
    '-': ["00000","00000","00000","11111","00000","00000","00000"],
    '=': ["00000","00000","11111","00000","11111","00000","00000"],
    ' ': ["00000","00000","00000","00000","00000","00000","00000"],
    'a': ["00000","00000","01110","00001","01111","10001","01111"],
    'b': ["10000","10000","11110","10001","10001","10001","11110"],
    'c': ["00000","00000","01111","10000","10000","10000","01111"],
    'd': ["00001","00001","01111","10001","10001","10001","01111"],
    'e': ["00000","00000","01110","10001","11111","10000","01110"],
    'f': ["00110","01000","11110","01000","01000","01000","01000"],
    'g': ["00000","01111","10001","10001","01111","00001","01110"],
    'h': ["10000","10000","11110","10001","10001","10001","10001"],
    'i': ["00100","00000","01100","00100","00100","00100","01110"],
    'k': ["10000","10000","10010","10100","11000","10100","10010"],
    'l': ["01100","00100","00100","00100","00100","00100","01110"],
    'm': ["00000","00000","11010","10101","10101","10101","10101"],
    'n': ["00000","00000","11110","10001","10001","10001","10001"],
    'o': ["00000","00000","01110","10001","10001","10001","01110"],
    'p': ["00000","11110","10001","10001","11110","10000","10000"],
    'r': ["00000","00000","10110","11000","10000","10000","10000"],
    's': ["00000","00000","01111","10000","01110","00001","11110"],
    't': ["01000","01000","11110","01000","01000","01001","00110"],
    'u': ["00000","00000","10001","10001","10001","10011","01101"],
    'v': ["00000","00000","10001","10001","10001","01010","00100"],
    'z': ["00000","00000","11111","00010","00100","01000","11111"],
    'A': ["01110","10001","10001","11111","10001","10001","10001"],
    'N': ["10001","11001","10101","10011","10001","10001","10001"],
    'C': ["01111","10000","10000","10000","10000","10000","01111"],
    'S': ["01111","10000","10000","01110","00001","00001","11110"],
    'R': ["11110","10001","10001","11110","10100","10010","10001"],
    'D': ["11110","10001","10001","10001","10001","10001","11110"],
    'F': ["11111","10000","10000","11110","10000","10000","10000"],
    'G': ["01111","10000","10000","10011","10001","10001","01111"],
    'P': ["11110","10001","10001","11110","10000","10000","10000"],
    'T': ["11111","00100","00100","00100","00100","00100","00100"],
    'w': ["00000","00000","10001","10001","10101","10101","01010"],
    'x': ["00000","00000","10001","01010","00100","01010","10001"],
    'y': ["00000","00000","10001","10001","01111","00001","01110"],
    'q': ["00000","01111","10001","10001","01111","00001","00001"],
    'j': ["00010","00000","00110","00010","00010","10010","01100"],
    "'": ["00100","00100","00100","00000","00000","00000","00000"],
    '(': ["00010","00100","01000","01000","01000","00100","00010"],
    ')': ["01000","00100","00010","00010","00010","00100","01000"],
}

PALETTE = [(31,78,160),(200,40,40),(20,140,70),(210,150,20),(120,40,150),(0,0,0)]


def new_canvas():
    return [[(255,255,255) for _ in range(W)] for _ in range(H)]


def setpx(img, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        img[y][x] = c


def draw_line(img, x0, y0, x1, y1, c, thick=1):
    x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
    dx = abs(x1 - x0); dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        for ox in range(-(thick//2), thick//2+1):
            for oy in range(-(thick//2), thick//2+1):
                setpx(img, x0+ox, y0+oy, c)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2*err
        if e2 > -dy: err -= dy; x0 += sx
        if e2 < dx: err += dx; y0 += sy


def draw_text(img, x, y, text, c=(0,0,0), scale=2):
    cx = int(round(x)); y = int(round(y))
    for ch in text:
        g = FONT.get(ch, FONT[' '])
        for ry in range(7):
            for rx in range(5):
                if g[ry][rx] == '1':
                    for sx in range(scale):
                        for sy in range(scale):
                            setpx(img, cx+rx*scale+sx, y+ry*scale+sy, c)
        cx += (5*scale + scale)


def draw_text_vert(img, x, y, text, c=(0,0,0), scale=2):
    # draw rotated 90deg (bottom-to-top) for y-axis label
    cy = int(round(y)); x = int(round(x))
    for ch in text:
        g = FONT.get(ch, FONT[' '])
        for ry in range(7):
            for rx in range(5):
                if g[ry][rx] == '1':
                    for sx in range(scale):
                        for sy in range(scale):
                            setpx(img, x+ry*scale+sy, cy-rx*scale-sx, c)
        cy -= (5*scale + scale)


def save_png(img, path):
    raw = b''
    for row in img:
        raw += b'\x00'
        for (r,g,b) in row:
            raw += struct.pack('BBB', r, g, b)
    def chunk(t, d):
        c = t + d
        return struct.pack('>I', len(d)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0))
    idat = chunk(b'IDAT', zlib.compress(raw, 9))
    iend = chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(sig + ihdr + idat + iend)


def plot_xy(path, series, xlabel, ylabel, title, legend_prefix="", xr=None, yr=None):
    """series: list of (label, xs, ys). Draw axes, gridlines, curves, legend."""
    img = new_canvas()
    # gather ranges
    allx = [v for (_,xs,ys) in series for v in xs]
    ally = [v for (_,xs,ys) in series for v in ys]
    xmin, xmax = (xr if xr else (min(allx), max(allx)))
    ymin, ymax = (yr if yr else (min(ally), max(ally)))
    if ymax == ymin: ymax += 1.0
    if xmax == xmin: xmax += 1.0
    pad = 0.05*(ymax-ymin); ymin -= pad; ymax += pad

    def sx(x): return ML + (x - xmin)/(xmax - xmin)*PW
    def sy(y): return MT + (1 - (y - ymin)/(ymax - ymin))*PH

    # plot frame
    draw_line(img, ML, MT, ML, MT+PH, (0,0,0), 2)
    draw_line(img, ML, MT+PH, ML+PW, MT+PH, (0,0,0), 2)
    # gridlines + ticks (5 each)
    for i in range(6):
        gx = ML + i*PW/5
        draw_line(img, gx, MT, gx, MT+PH, (225,225,225), 1)
        draw_line(img, gx, MT+PH, gx, MT+PH+6, (0,0,0), 1)
        val = xmin + i*(xmax-xmin)/5
        draw_text(img, gx-14, MT+PH+12, ("%.2f"%val), (0,0,0), 2)
        gy = MT + i*PH/5
        draw_line(img, ML, gy, ML+PW, gy, (225,225,225), 1)
        draw_line(img, ML-6, gy, ML, gy, (0,0,0), 1)
        valy = ymax - i*(ymax-ymin)/5
        draw_text(img, ML-62, gy-6, ("%.2f"%valy), (0,0,0), 2)

    # curves
    for idx,(label,xs,ys) in enumerate(series):
        c = PALETTE[idx % len(PALETTE)]
        pts = [(sx(xs[k]), sy(ys[k])) for k in range(len(xs))]
        for k in range(len(pts)-1):
            draw_line(img, pts[k][0], pts[k][1], pts[k+1][0], pts[k+1][1], c, 2)

    # legend box (top-right inside plot)
    lx = ML + PW - 180; ly = MT + 12
    for idx,(label,xs,ys) in enumerate(series):
        c = PALETTE[idx % len(PALETTE)]
        draw_line(img, lx, ly+idx*22+6, lx+28, ly+idx*22+6, c, 3)
        draw_text(img, lx+34, ly+idx*22, (legend_prefix+label), (0,0,0), 2)

    # labels
    draw_text(img, ML + PW//2 - len(xlabel)*6, MT+PH+40, xlabel, (0,0,0), 2)
    draw_text_vert(img, 20, MT+PH//2 + len(ylabel)*6, ylabel, (0,0,0), 2)
    draw_text(img, ML, 20, title, (0,0,0), 2)
    save_png(img, path)
    print("  wrote", path)


def main():
    d = DATA

    # Fig 1
    s = []
    for a in [1.0,0.9,0.7,0.5]:
        s.append(("a="+("%.1f"%a), d["fig1"]["eta"], d["fig1"]["curves"][a]))
    plot_xy(OUT+"/Figure_1_velocity_alpha.png", s, "eta", "f (eta)",
            "Fig 1 velocity vs alpha", xr=(0,1))

    # Fig 2
    s = []
    for g in [0.0,0.3,0.6,0.9]:
        s.append(("g="+("%.1f"%g), d["fig2"]["eta"], d["fig2"]["curves"][g]))
    plot_xy(OUT+"/Figure_2_temperature_gammaT.png", s, "eta", "theta",
            "Fig 2 temperature vs gammaT", xr=(0,1))

    # Fig 3
    s = []
    for b in [0.1,0.4,0.8,1.2]:
        s.append(("b="+("%.1f"%b), d["fig3"]["eta"], d["fig3"]["curves"][b]))
    plot_xy(OUT+"/Figure_3_velocity_beta.png", s, "eta", "f (eta)",
            "Fig 3 velocity vs beta", xr=(0,1))

    # Fig 4
    s = []
    for name in ["brick","platelet","blade"]:
        s.append((name, d["fig4"]["eta"], d["fig4"]["curves"][name]))
    plot_xy(OUT+"/Figure_4_temperature_shape.png", s, "eta", "theta",
            "Fig 4 temperature vs shape", xr=(0,1))

    # Fig 5
    s = []
    for sr in [0.0,0.05,0.10,0.15]:
        s.append(("Sr="+("%.2f"%sr), d["fig5"]["eta"], d["fig5"]["curves"][sr]))
    plot_xy(OUT+"/Figure_5_concentration_Sr.png", s, "eta", "Phi",
            "Fig 5 concentration vs Sr", xr=(0,1))

    # Fig 6
    s = []
    for rd in [0.2,0.6,1.0,1.5]:
        s.append(("Rd="+("%.1f"%rd), d["fig6"]["eta"], d["fig6"]["curves"][rd]))
    plot_xy(OUT+"/Figure_6_temperature_Rd.png", s, "eta", "theta",
            "Fig 6 temperature vs Rd", xr=(0,1))

    # Fig 7 (Nu vs alpha for three shapes)
    s = []
    for name in ["brick","platelet","blade"]:
        s.append((name, d["fig7"]["alpha"], d["fig7"]["curves"][name]))
    plot_xy(OUT+"/Figure_7_Nu_alpha_shape.png", s, "alpha", "Nu lower disk",
            "Fig 7 Nu vs alpha and shape", xr=(0.5,1.0))


if __name__ == "__main__":
    main()
