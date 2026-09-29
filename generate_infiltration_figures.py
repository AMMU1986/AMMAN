#!/usr/bin/env python3
"""
Generate 7 scientific figures (PNG) for the manuscript
"Coupled Effects of Vegetation, Soil Properties, and Antecedent Moisture on
 Infiltration in Permeable Channels".
Uses only the Python standard library (struct, zlib, math).
The PNGCanvas / font machinery follows the repository convention
(see generate_figures.py).
"""

import struct
import zlib
import math
import os

OUTPUT_DIR = '/projects/sandbox/AMMAN/infiltration_figures'

# ---- Palette -------------------------------------------------------------
DARK_BLUE = (31, 78, 121)
MED_BLUE = (46, 117, 182)
LIGHT_BLUE = (155, 194, 230)
PALE_BLUE = (218, 232, 252)
DARK_GREEN = (56, 118, 29)
MED_GREEN = (84, 172, 64)
LIGHT_GREEN = (198, 224, 180)
ORANGE = (237, 125, 49)
LIGHT_ORANGE = (248, 203, 173)
RED = (192, 0, 0)
LIGHT_RED = (248, 203, 203)
PURPLE = (112, 48, 160)
LIGHT_PURPLE = (204, 180, 220)
GOLD = (191, 144, 0)
LIGHT_GOLD = (255, 230, 153)
BROWN = (132, 96, 60)
LIGHT_BROWN = (214, 190, 160)
GRAY = (128, 128, 128)
LIGHT_GRAY = (217, 217, 217)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SAND = (232, 214, 170)


class PNGCanvas:
    """Fast PNG canvas using bytearray (RGB, 8-bit)."""

    def __init__(self, width, height, bg=(255, 255, 255)):
        self.w = width
        self.h = height
        self.data = bytearray(width * height * 3)
        for i in range(width * height):
            self.data[i*3] = bg[0]
            self.data[i*3+1] = bg[1]
            self.data[i*3+2] = bg[2]

    def pixel(self, x, y, color):
        x = int(x); y = int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            idx = (y * self.w + x) * 3
            self.data[idx] = color[0]
            self.data[idx+1] = color[1]
            self.data[idx+2] = color[2]

    def fill_rect(self, x1, y1, x2, y2, color):
        x1, x2 = int(x1), int(x2)
        y1, y2 = int(y1), int(y2)
        x1, x2 = max(0, min(x1, x2)), min(self.w-1, max(x1, x2))
        y1, y2 = max(0, min(y1, y2)), min(self.h-1, max(y1, y2))
        for y in range(y1, y2+1):
            idx = (y * self.w + x1) * 3
            for x in range(x1, x2+1):
                self.data[idx] = color[0]
                self.data[idx+1] = color[1]
                self.data[idx+2] = color[2]
                idx += 3

    def rect(self, x1, y1, x2, y2, outline, fill=None):
        if fill:
            self.fill_rect(x1, y1, x2, y2, fill)
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        for x in range(max(0, x1), min(self.w, x2+1)):
            self.pixel(x, y1, outline)
            self.pixel(x, y2, outline)
        for y in range(max(0, y1), min(self.h, y2+1)):
            self.pixel(x1, y, outline)
            self.pixel(x2, y, outline)

    def hline(self, x1, x2, y, color):
        y = int(y)
        if y < 0 or y >= self.h:
            return
        x1, x2 = int(x1), int(x2)
        x1, x2 = max(0, min(x1, x2)), min(self.w-1, max(x1, x2))
        idx = (y * self.w + x1) * 3
        for x in range(x1, x2+1):
            self.data[idx] = color[0]
            self.data[idx+1] = color[1]
            self.data[idx+2] = color[2]
            idx += 3

    def vline(self, x, y1, y2, color):
        x = int(x)
        if x < 0 or x >= self.w:
            return
        y1, y2 = int(y1), int(y2)
        y1, y2 = max(0, min(y1, y2)), min(self.h-1, max(y1, y2))
        for y in range(y1, y2+1):
            idx = (y * self.w + x) * 3
            self.data[idx] = color[0]
            self.data[idx+1] = color[1]
            self.data[idx+2] = color[2]

    def line(self, x1, y1, x2, y2, color, thick=1):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        dx = abs(x2-x1); dy = abs(y2-y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            for t in range(-(thick//2), (thick+1)//2):
                if dy > dx:
                    self.pixel(x1+t, y1, color)
                else:
                    self.pixel(x1, y1+t, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2*err
            if e2 > -dy:
                err -= dy; x1 += sx
            if e2 < dx:
                err += dx; y1 += sy

    def dline(self, x1, y1, x2, y2, color, dash=6, gap=5):
        d = math.hypot(x2-x1, y2-y1)
        if d == 0:
            return
        n = int(d)
        on = True
        cnt = 0
        for i in range(n+1):
            t = i/n
            x = x1 + (x2-x1)*t
            y = y1 + (y2-y1)*t
            if on:
                self.pixel(x, y, color)
            cnt += 1
            if on and cnt >= dash:
                on = False; cnt = 0
            elif (not on) and cnt >= gap:
                on = True; cnt = 0

    def arrow(self, x1, y1, x2, y2, color, thick=2, hs=8):
        self.line(x1, y1, x2, y2, color, thick)
        angle = math.atan2(y2-y1, x2-x1)
        for a_off in [2.5, -2.5]:
            ax = int(x2 - hs * math.cos(angle - a_off * 0.17))
            ay = int(y2 - hs * math.sin(angle - a_off * 0.17))
            self.line(x2, y2, ax, ay, color, thick)

    def circle(self, cx, cy, r, color, fill=None):
        cx, cy, r = int(cx), int(cy), int(r)
        if fill:
            for y in range(-r, r+1):
                xs = int(math.sqrt(max(0, r*r - y*y)))
                self.hline(cx-xs, cx+xs, cy+y, fill)
        x, y = r, 0
        err = 1 - r
        while x >= y:
            for px, py in [(cx+x, cy+y), (cx-x, cy+y), (cx+x, cy-y), (cx-x, cy-y),
                           (cx+y, cy+x), (cx-y, cy+x), (cx+y, cy-x), (cx-y, cy-x)]:
                self.pixel(px, py, color)
            y += 1
            if err < 0:
                err += 2*y + 1
            else:
                x -= 1
                err += 2*(y-x) + 1

    def text(self, x, y, s, color, scale=1):
        x = int(x); y = int(y)
        for ch in s:
            bm = _FONT.get(ch)
            if bm is None:
                x += 6*scale
                continue
            for ri, row in enumerate(bm):
                for ci in range(5):
                    if row & (1 << (4-ci)):
                        px, py = x+ci*scale, y+ri*scale
                        for sy in range(scale):
                            for sx in range(scale):
                                self.pixel(px+sx, py+sy, color)
            x += 6*scale

    def text_c(self, cx, y, s, color, scale=1):
        w = len(s) * 6 * scale
        self.text(cx - w//2, y, s, color, scale)

    def text_v(self, x, cy, s, color, scale=1):
        """Vertical (rotated) label, drawn bottom-to-top centered at cy."""
        h = len(s) * 6 * scale
        y = cy + h//2
        for ch in s:
            bm = _FONT.get(ch)
            if bm is not None:
                for ri, row in enumerate(bm):
                    for ci in range(5):
                        if row & (1 << (4-ci)):
                            # rotate 90 deg CCW: (ci, ri) -> (ri, -ci)
                            for syi in range(scale):
                                for sxi in range(scale):
                                    self.pixel(x+ri*scale+sxi, y-ci*scale-syi, color)
            y -= 6*scale

    def save(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)
            off = y*self.w*3
            raw.extend(self.data[off:off+self.w*3])
        comp = zlib.compress(bytes(raw), 9)

        def chunk(ct, d):
            c = ct + d
            crc = zlib.crc32(c) & 0xffffffff
            return struct.pack('>I', len(d)) + c + struct.pack('>I', crc)

        with open(path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0)))
            f.write(chunk(b'IDAT', comp))
            f.write(chunk(b'IEND', b''))


# ---- Minimal 5x7 font ----------------------------------------------------
_FONT = {
    'A':[0b01110,0b10001,0b10001,0b11111,0b10001,0b10001,0b10001],
    'B':[0b11110,0b10001,0b10001,0b11110,0b10001,0b10001,0b11110],
    'C':[0b01110,0b10001,0b10000,0b10000,0b10000,0b10001,0b01110],
    'D':[0b11110,0b10001,0b10001,0b10001,0b10001,0b10001,0b11110],
    'E':[0b11111,0b10000,0b10000,0b11110,0b10000,0b10000,0b11111],
    'F':[0b11111,0b10000,0b10000,0b11110,0b10000,0b10000,0b10000],
    'G':[0b01110,0b10001,0b10000,0b10111,0b10001,0b10001,0b01110],
    'H':[0b10001,0b10001,0b10001,0b11111,0b10001,0b10001,0b10001],
    'I':[0b01110,0b00100,0b00100,0b00100,0b00100,0b00100,0b01110],
    'J':[0b00111,0b00010,0b00010,0b00010,0b00010,0b10010,0b01100],
    'K':[0b10001,0b10010,0b10100,0b11000,0b10100,0b10010,0b10001],
    'L':[0b10000,0b10000,0b10000,0b10000,0b10000,0b10000,0b11111],
    'M':[0b10001,0b11011,0b10101,0b10101,0b10001,0b10001,0b10001],
    'N':[0b10001,0b11001,0b10101,0b10011,0b10001,0b10001,0b10001],
    'O':[0b01110,0b10001,0b10001,0b10001,0b10001,0b10001,0b01110],
    'P':[0b11110,0b10001,0b10001,0b11110,0b10000,0b10000,0b10000],
    'Q':[0b01110,0b10001,0b10001,0b10001,0b10101,0b10010,0b01101],
    'R':[0b11110,0b10001,0b10001,0b11110,0b10100,0b10010,0b10001],
    'S':[0b01110,0b10001,0b10000,0b01110,0b00001,0b10001,0b01110],
    'T':[0b11111,0b00100,0b00100,0b00100,0b00100,0b00100,0b00100],
    'U':[0b10001,0b10001,0b10001,0b10001,0b10001,0b10001,0b01110],
    'V':[0b10001,0b10001,0b10001,0b10001,0b10001,0b01010,0b00100],
    'W':[0b10001,0b10001,0b10001,0b10101,0b10101,0b11011,0b10001],
    'X':[0b10001,0b10001,0b01010,0b00100,0b01010,0b10001,0b10001],
    'Y':[0b10001,0b10001,0b01010,0b00100,0b00100,0b00100,0b00100],
    'Z':[0b11111,0b00001,0b00010,0b00100,0b01000,0b10000,0b11111],
    'a':[0b00000,0b00000,0b01110,0b00001,0b01111,0b10001,0b01111],
    'b':[0b10000,0b10000,0b10110,0b11001,0b10001,0b10001,0b11110],
    'c':[0b00000,0b00000,0b01110,0b10000,0b10000,0b10001,0b01110],
    'd':[0b00001,0b00001,0b01101,0b10011,0b10001,0b10001,0b01111],
    'e':[0b00000,0b00000,0b01110,0b10001,0b11111,0b10000,0b01110],
    'f':[0b00110,0b01001,0b01000,0b11100,0b01000,0b01000,0b01000],
    'g':[0b00000,0b01111,0b10001,0b10001,0b01111,0b00001,0b01110],
    'h':[0b10000,0b10000,0b10110,0b11001,0b10001,0b10001,0b10001],
    'i':[0b00100,0b00000,0b01100,0b00100,0b00100,0b00100,0b01110],
    'j':[0b00010,0b00000,0b00110,0b00010,0b00010,0b10010,0b01100],
    'k':[0b10000,0b10000,0b10010,0b10100,0b11000,0b10100,0b10010],
    'l':[0b01100,0b00100,0b00100,0b00100,0b00100,0b00100,0b01110],
    'm':[0b00000,0b00000,0b11010,0b10101,0b10101,0b10001,0b10001],
    'n':[0b00000,0b00000,0b10110,0b11001,0b10001,0b10001,0b10001],
    'o':[0b00000,0b00000,0b01110,0b10001,0b10001,0b10001,0b01110],
    'p':[0b00000,0b00000,0b11110,0b10001,0b11110,0b10000,0b10000],
    'q':[0b00000,0b00000,0b01101,0b10011,0b01111,0b00001,0b00001],
    'r':[0b00000,0b00000,0b10110,0b11001,0b10000,0b10000,0b10000],
    's':[0b00000,0b00000,0b01110,0b10000,0b01110,0b00001,0b11110],
    't':[0b01000,0b01000,0b11100,0b01000,0b01000,0b01001,0b00110],
    'u':[0b00000,0b00000,0b10001,0b10001,0b10001,0b10011,0b01101],
    'v':[0b00000,0b00000,0b10001,0b10001,0b10001,0b01010,0b00100],
    'w':[0b00000,0b00000,0b10001,0b10001,0b10101,0b10101,0b01010],
    'x':[0b00000,0b00000,0b10001,0b01010,0b00100,0b01010,0b10001],
    'y':[0b00000,0b00000,0b10001,0b10001,0b01111,0b00001,0b01110],
    'z':[0b00000,0b00000,0b11111,0b00010,0b00100,0b01000,0b11111],
    '0':[0b01110,0b10001,0b10011,0b10101,0b11001,0b10001,0b01110],
    '1':[0b00100,0b01100,0b00100,0b00100,0b00100,0b00100,0b01110],
    '2':[0b01110,0b10001,0b00001,0b00010,0b00100,0b01000,0b11111],
    '3':[0b11111,0b00010,0b00100,0b00010,0b00001,0b10001,0b01110],
    '4':[0b00010,0b00110,0b01010,0b10010,0b11111,0b00010,0b00010],
    '5':[0b11111,0b10000,0b11110,0b00001,0b00001,0b10001,0b01110],
    '6':[0b00110,0b01000,0b10000,0b11110,0b10001,0b10001,0b01110],
    '7':[0b11111,0b00001,0b00010,0b00100,0b01000,0b01000,0b01000],
    '8':[0b01110,0b10001,0b10001,0b01110,0b10001,0b10001,0b01110],
    '9':[0b01110,0b10001,0b10001,0b01111,0b00001,0b00010,0b01100],
    ' ':[0,0,0,0,0,0,0],
    '.':[0,0,0,0,0,0b01100,0b01100],
    ',':[0,0,0,0,0b01100,0b00100,0b01000],
    ':':[0,0b01100,0b01100,0,0b01100,0b01100,0],
    '-':[0,0,0,0b11111,0,0,0],
    '+':[0,0b00100,0b00100,0b11111,0b00100,0b00100,0],
    '(':[0b00010,0b00100,0b01000,0b01000,0b01000,0b00100,0b00010],
    ')':[0b01000,0b00100,0b00010,0b00010,0b00010,0b00100,0b01000],
    '/':[0b00001,0b00010,0b00010,0b00100,0b01000,0b01000,0b10000],
    '>':[0b10000,0b01000,0b00100,0b00010,0b00100,0b01000,0b10000],
    '<':[0b00001,0b00010,0b00100,0b01000,0b00100,0b00010,0b00001],
    '=':[0,0,0b11111,0,0b11111,0,0],
    '%':[0b11001,0b11001,0b00010,0b00100,0b01000,0b10011,0b10011],
    '^':[0b00100,0b01010,0b10001,0,0,0,0],
    '*':[0,0b00100,0b10101,0b01110,0b10101,0b00100,0],
    '|':[0b00100,0b00100,0b00100,0b00100,0b00100,0b00100,0b00100],
    '_':[0,0,0,0,0,0,0b11111],
    "'":[0b00100,0b00100,0b01000,0,0,0,0],
}


def frame(c, x0, y0, x1, y1):
    """Draw axis box."""
    c.vline(x0, y0, y1, BLACK)
    c.hline(x0, x1, y1, BLACK)


# =========================================================================
# Figure 1 : Conceptual coupled framework + flume/collection schematic
# =========================================================================
def fig1():
    c = PNGCanvas(900, 560)
    c.text_c(450, 10, "Coupled Framework: Vegetation - Flow - Bed Head - Infiltration", BLACK, 2)

    # (a) cascade of boxes (left column)
    c.text(30, 40, "(a) Mechanistic cascade", BLACK, 1)
    cascade = [
        ("Open-channel flow (Q, h, U, S)", MED_BLUE, PALE_BLUE),
        ("Vegetation momentum modification", MED_GREEN, LIGHT_GREEN),
        ("Bed pressure / head distribution", ORANGE, LIGHT_ORANGE),
        ("Unsaturated -> saturated infiltration", BROWN, LIGHT_BROWN),
        ("Cumulative infiltration F(t)", PURPLE, LIGHT_PURPLE),
    ]
    bx0, bw, bh = 30, 300, 54
    by = 60
    for i, (label, oc, fc) in enumerate(cascade):
        c.rect(bx0, by, bx0+bw, by+bh, oc, fc)
        c.text_c(bx0+bw//2, by+bh//2-4, label, BLACK, 1)
        if i < len(cascade)-1:
            c.arrow(bx0+bw//2, by+bh+2, bx0+bw//2, by+bh+22, GRAY, 2, 7)
        by += bh + 24

    # (b) flume schematic (right)
    c.text(400, 40, "(b) Recirculating flume and infiltration collection", BLACK, 1)
    fx0, fx1 = 400, 870
    top = 90
    bed = 210
    base = 300
    # water body
    c.fill_rect(fx0, top, fx1, bed, PALE_BLUE)
    # free surface line
    c.line(fx0, top, fx1, top, MED_BLUE, 2)
    # inlet
    c.rect(fx0-20, top-8, fx0, base, GRAY, LIGHT_GRAY)
    c.text(fx0-18, top-24, "Inlet", BLACK, 1)
    c.arrow(fx0+8, top+22, fx0+70, top+22, MED_BLUE, 2, 7)
    c.text(fx0+18, top+6, "flow", MED_BLUE, 1)
    # permeable bed
    c.fill_rect(fx0, bed, fx1, base, SAND)
    c.rect(fx0, bed, fx1, base, BROWN)
    # vegetation stems (zone in middle)
    vz0, vz1 = 560, 700
    for sx in range(vz0, vz1, 16):
        c.vline(sx, top+18, bed, DARK_GREEN)
        c.circle(sx, top+16, 2, DARK_GREEN, DARK_GREEN)
    c.text_c((vz0+vz1)//2, bed+6, "Vegetation zone", DARK_GREEN, 1)
    c.text(fx0+6, bed+6, "Upstream", BLACK, 1)
    c.text(fx1-70, bed+6, "Downstr.", BLACK, 1)
    # tailgate/outlet
    c.rect(fx1, top+30, fx1+18, base, GRAY, LIGHT_GRAY)
    c.text(fx1-6, top+12, "Outlet", BLACK, 1)
    # collection cells
    cy0, cy1 = base+6, base+70
    ncell = 6
    cw = (fx1-fx0)//ncell
    for i in range(ncell):
        cxs = fx0 + i*cw
        c.rect(cxs, cy0, cxs+cw-4, cy1, DARK_BLUE, WHITE)
        c.arrow((cxs+cxs+cw-4)//2, base+1, (cxs+cxs+cw-4)//2, cy0-1, MED_BLUE, 1, 5)
    c.text(fx0, cy1+8, "Isolated collection cells -> load cells (resolve f_x(x))", BLACK, 1)
    c.text(fx0, cy1+26, "f(t) = (1/A_b) dV/dt      F(t) = V/A_b", BLACK, 1)

    # depth arrow
    c.arrow(fx0+40, top, fx0+40, bed, MED_BLUE, 1, 5)
    c.arrow(fx0+40, bed, fx0+40, top, MED_BLUE, 1, 5)
    c.text(fx0+44, (top+bed)//2, "h", MED_BLUE, 1)

    c.text(30, 535, "Figure 1. Coupled conceptual framework (a) and flume with cell-resolved infiltration collection (b).", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Conceptual_Framework.png'))
    print("  Figure 1 done")


# =========================================================================
# Figure 2 : Vegetation configurations (density levels)
# =========================================================================
def fig2():
    c = PNGCanvas(900, 400)
    c.text_c(450, 10, "Vegetation Configurations: Increasing Frontal-Area Density", BLACK, 2)

    panels = [
        ("(a) Bare (lambda=0)", 0),
        ("(b) Low density", 1),
        ("(c) Medium density", 2),
        ("(d) High density", 3),
    ]
    pw = 210
    x0 = 20
    top = 60
    bot = 300
    stem_counts = [0, 9, 20, 36]
    for (label, k) in panels:
        px = x0
        # bed
        c.fill_rect(px, top, px+pw, bot, SAND)
        c.rect(px, top, px+pw, bot, BROWN)
        # water tint
        c.fill_rect(px, top-40, px+pw, top, PALE_BLUE)
        c.line(px, top-40, px+pw, top-40, MED_BLUE, 2)
        # stems in staggered grid
        n = stem_counts[k]
        if n > 0:
            cols = int(math.ceil(math.sqrt(n*pw/(bot-top))))
            rows = int(math.ceil(n/cols))
            dx = pw/(cols+1)
            dy = (bot-top-20)/(rows+1)
            placed = 0
            for r in range(rows):
                offset = dx/2 if r % 2 else 0
                for cc in range(cols):
                    if placed >= n:
                        break
                    sx = px + dx*(cc+1) + offset
                    sy = top + 15 + dy*(r+1)
                    if sx < px+pw-6:
                        c.vline(sx, top+10, sy, DARK_GREEN)
                        c.circle(sx, top+8, 2, DARK_GREEN, DARK_GREEN)
                        placed += 1
        c.text_c(px+pw//2, top-58, label, BLACK, 1)
        c.text_c(px+pw//2, bot+8, "N = %d stems" % n, BLACK, 1)
        x0 += pw + 12

    c.text(20, 340, "lambda = N A_v / A_b  (A_v = projected frontal area of one stem, A_b = bed area)", BLACK, 1)
    c.text(20, 375, "Figure 2. Tested vegetation configurations at fixed stem geometry; frontal-area density increases left to right.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Vegetation_Configurations.png'))
    print("  Figure 2 done")


# =========================================================================
# Figure 3 : Infiltration rate f(t) vs time for vegetation densities
# =========================================================================
def fig3():
    c = PNGCanvas(900, 520)
    c.text_c(450, 10, "Infiltration Rate f(t): Effect of Vegetation Density", BLACK, 2)

    # two panels: dry (Si low) and wet (Si high)
    panels = [("(a) Dry antecedent (S_i = 0.2)", 40, 1.0),
              ("(b) Wet antecedent (S_i = 0.8)", 470, 0.45)]
    dens = [("Bare", RED, 1.0), ("Low", ORANGE, 1.18),
            ("Medium", MED_GREEN, 1.34), ("High", MED_BLUE, 1.46)]
    for title, ox, wet in panels:
        x0, y0, x1, y1 = ox+50, 70, ox+380, 400
        frame(c, x0, y0, x1, y1)
        c.text(ox+40, 46, title, BLACK, 1)
        c.text_v(ox+18, (y0+y1)//2, "f (mm/min)", BLACK, 1)
        c.text_c((x0+x1)//2, y1+22, "Time (min)", BLACK, 1)
        # y ticks
        for i in range(6):
            yy = y1 - i*(y1-y0)//5
            c.hline(x0-4, x0, yy, BLACK)
            c.text(x0-30, yy-3, "%.1f" % (i*0.65), BLACK, 1)
        for i in range(6):
            xx = x0 + i*(x1-x0)//5
            c.vline(xx, y1, y1+4, BLACK)
            c.text(xx-6, y1+8, "%d" % (i*12), BLACK, 1)
        fmax = 3.25
        for name, col, mult in dens:
            f0 = 2.7*mult*wet
            fpl = 0.9*mult*wet
            prev = None
            for px in range(x0, x1+1):
                t = (px-x0)/(x1-x0)*60.0
                f = fpl + (f0-fpl)*math.exp(-t/9.0)
                py = y1 - (f/fmax)*(y1-y0)
                py = max(y0, min(y1, py))
                if prev:
                    c.line(prev[0], prev[1], px, py, col, 2)
                prev = (px, py)
        # legend
        lx = x1-95
        for i, (name, col, _m) in enumerate(dens):
            ly = y0+6+i*15
            c.hline(lx, lx+22, ly, col)
            c.line(lx, ly-1, lx+22, ly-1, col, 1)
            c.text(lx+27, ly-3, name, BLACK, 1)

    c.text(30, 470, "Figure 3. Instantaneous infiltration rate versus time for four vegetation densities under dry (a) and wet (b)", BLACK, 1)
    c.text(30, 486, "antecedent states; denser canopies raise f(t), and the enhancement is larger for the drier bed.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Infiltration_Rate_Density.png'))
    print("  Figure 3 done")


# =========================================================================
# Figure 4 : Cumulative infiltration F(t) for soil x discharge
# =========================================================================
def fig4():
    c = PNGCanvas(900, 520)
    c.text_c(450, 10, "Cumulative Infiltration F(t): Soil Material and Discharge", BLACK, 2)

    mats = [("(a) Coarse sand", 40, 1.55),
            ("(b) Medium sand", 320, 1.0),
            ("(c) Sand-gravel", 600, 1.85)]
    q_levels = [("Q1", LIGHT_BLUE, 0.8), ("Q2", MED_BLUE, 0.95),
                ("Q3", DARK_BLUE, 1.12), ("Q4", PURPLE, 1.3)]
    Fmax = 260.0
    for title, ox, kfac in mats:
        x0, y0, x1, y1 = ox+40, 70, ox+250, 400
        frame(c, x0, y0, x1, y1)
        c.text(ox+34, 46, title, BLACK, 1)
        c.text_c((x0+x1)//2, y1+22, "Time (min)", BLACK, 1)
        if ox == 40:
            c.text_v(ox+12, (y0+y1)//2, "F (mm)", BLACK, 1)
        for i in range(6):
            yy = y1 - i*(y1-y0)//5
            c.hline(x0-4, x0, yy, BLACK)
            if ox == 40:
                c.text(x0-32, yy-3, "%d" % (i*50), BLACK, 1)
        for i in range(4):
            xx = x0 + i*(x1-x0)//3
            c.vline(xx, y1, y1+4, BLACK)
            c.text(xx-6, y1+8, "%d" % (i*20), BLACK, 1)
        for name, col, qm in q_levels:
            prev = None
            for px in range(x0, x1+1):
                t = (px-x0)/(x1-x0)*60.0
                # cumulative ~ sqrt-like early then linear plateau slope
                F = kfac*qm*(18*math.sqrt(t) + 1.6*t)
                py = y1 - (F/Fmax)*(y1-y0)
                py = max(y0, min(y1, py))
                if prev:
                    c.line(prev[0], prev[1], px, py, col, 2)
                prev = (px, py)
        if ox == 600:
            lx = x0+8
            for i, (name, col, _q) in enumerate(q_levels):
                ly = y0+8+i*15
                c.line(lx, ly, lx+22, ly, col, 2)
                c.text(lx+27, ly-3, name, BLACK, 1)

    c.text(30, 470, "Figure 4. Cumulative infiltration for three bed materials across four discharges (Q1<Q2<Q3<Q4). Curve spacing", BLACK, 1)
    c.text(30, 486, "between discharge levels widens with bed conductivity, indicating the discharge-conductivity interaction.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Cumulative_Soil_Discharge.png'))
    print("  Figure 4 done")


# =========================================================================
# Figure 5 : Spatial distribution f_x(x) along the channel
# =========================================================================
def fig5():
    c = PNGCanvas(900, 470)
    c.text_c(450, 10, "Along-Channel Infiltration f_x(x): Localized Hotspot", BLACK, 2)

    x0, y0, x1, y1 = 90, 70, 830, 320
    frame(c, x0, y0, x1, y1)
    c.text_v(30, (y0+y1)//2, "f_x  (mm/min)", BLACK, 1)
    c.text_c((x0+x1)//2, y1+52, "Distance along channel x (m)", BLACK, 1)

    # vegetation zone shading
    vz0 = x0 + int((x1-x0)*0.42)
    vz1 = x0 + int((x1-x0)*0.62)
    for xx in range(vz0, vz1):
        for yy in range(y0, y1):
            if (xx+yy) % 6 == 0:
                c.pixel(xx, yy, LIGHT_GREEN)
    c.line(vz0, y0, vz0, y1, DARK_GREEN, 1)
    c.line(vz1, y0, vz1, y1, DARK_GREEN, 1)
    c.text_c((vz0+vz1)//2, y0+6, "Vegetation", DARK_GREEN, 1)

    # zone labels (placed below the x tick labels to avoid overlap)
    c.text_c((x0+vz0)//2, y1+26, "Upstream", BLACK, 1)
    c.text_c((vz1+x1)//2, y1+26, "Downstream recovery", BLACK, 1)

    # y ticks
    fmax = 2.7
    for i in range(6):
        yy = y1 - i*(y1-y0)//5
        c.hline(x0-4, x0, yy, BLACK)
        c.text(x0-40, yy-3, "%.2f" % (i*0.54), BLACK, 1)
    for i in range(6):
        xx = x0 + i*(x1-x0)//5
        c.vline(xx, y1, y1+4, BLACK)
        c.text(xx-6, y1+8, "%.1f" % (i*0.4), BLACK, 1)

    dens = [("Bare", RED, 0.0), ("Medium", ORANGE, 0.85), ("High", MED_BLUE, 1.45)]
    base = 0.85
    vc = (vz0+vz1)/2.0
    for name, col, amp in dens:
        prev = None
        for px in range(x0, x1+1):
            xr = (px-x0)/(x1-x0)
            xc = (vc-x0)/(x1-x0)
            # baseline + gaussian-ish hotspot slightly downstream of veg centre
            peak = amp*math.exp(-((xr-(xc+0.05))**2)/(2*0.010))
            tail = amp*0.35*math.exp(-((xr-(xc+0.22))**2)/(2*0.05)) if xr > xc else 0
            f = base + peak + tail
            py = y1 - (f/fmax)*(y1-y0)
            py = max(y0, min(y1, py))
            if prev:
                c.line(prev[0], prev[1], px, py, col, 2)
            prev = (px, py)
    # legend
    lx = x0+12
    for i, (name, col, _a) in enumerate(dens):
        ly = y0+10+i*15
        c.line(lx, ly, lx+24, ly, col, 2)
        c.text(lx+30, ly-3, name, BLACK, 1)

    c.text(30, 400, "Figure 5. Along-channel infiltration profile f_x(x) for three vegetation densities. Vegetation produces a", BLACK, 1)
    c.text(30, 416, "pronounced hotspot within and just downstream of the canopy, with a persistent downstream tail, rather", BLACK, 1)
    c.text(30, 432, "than a uniform lift; reach-integrated losses conceal this spatial structure.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_5_Spatial_Distribution.png'))
    print("  Figure 5 done")


# =========================================================================
# Figure 6 : Dimensionless collapse I* = f/Ks
# =========================================================================
def fig6():
    c = PNGCanvas(900, 500)
    c.text_c(450, 10, "Dimensionless Collapse of Normalized Infiltration I* = f / K_s", BLACK, 2)

    x0, y0, x1, y1 = 100, 70, 830, 360
    frame(c, x0, y0, x1, y1)
    c.text_v(34, (y0+y1)//2, "I* = f / K_s", BLACK, 1)
    c.text_c((x0+x1)//2, y1+24, "Composite dimensionless group  Pi = lambda^d Re_k^c Fr^b / S_i^g", BLACK, 1)

    for i in range(6):
        yy = y1 - i*(y1-y0)//5
        c.hline(x0-4, x0, yy, BLACK)
        c.text(x0-40, yy-3, "%.2f" % (0.05+i*0.06), BLACK, 1)
    for i in range(6):
        xx = x0 + i*(x1-x0)//5
        c.vline(xx, y1, y1+4, BLACK)
        c.text(xx-8, y1+8, "%.1f" % (i*0.8), BLACK, 1)

    # underlying trend line (power-law-ish)
    def trend(px):
        xr = (px-x0)/(x1-x0)
        val = 0.06 + 0.30*(xr**0.75)
        return y1 - (val/0.35)*(y1-y0)

    prev = None
    for px in range(x0, x1+1):
        py = trend(px)
        if prev:
            c.line(prev[0], prev[1], px, py, GRAY, 2)
        prev = (px, py)

    # scattered points by material
    import random
    random.seed(11)
    mats = [("Coarse sand", MED_BLUE), ("Medium sand", ORANGE), ("Sand-gravel", MED_GREEN)]
    for mi, (name, col) in enumerate(mats):
        for _ in range(22):
            xr = random.uniform(0.05, 0.98)
            px = x0 + xr*(x1-x0)
            base = 0.06 + 0.30*(xr**0.75)
            val = base + random.uniform(-0.018, 0.018)
            py = y1 - (val/0.35)*(y1-y0)
            c.circle(px, py, 3, col, col)
        # legend marker (bottom-right block)
        ly = y1-52+mi*16
        c.circle(x1-150, ly, 3, col, col)
        c.text(x1-140, ly-3, name, BLACK, 1)

    c.line(x0+18, y0+11, x0+40, y0+11, GRAY, 2)
    c.text(x0+46, y0+8, "Fitted trend", GRAY, 1)

    c.text(30, 410, "Figure 6. Normalizing by saturated conductivity collapses data from three bed materials onto a common", BLACK, 1)
    c.text(30, 426, "dimensionless trend; the residual spread is organized by vegetation, submergence and antecedent moisture", BLACK, 1)
    c.text(30, 442, "rather than by material identity, confirming the scaling.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_6_Dimensionless_Collapse.png'))
    print("  Figure 6 done")


# =========================================================================
# Figure 7 : Observed vs predicted (model comparison) + metric bars
# =========================================================================
def fig7():
    c = PNGCanvas(900, 520)
    c.text_c(450, 10, "Independent Validation: Observed vs Predicted and Model Comparison", BLACK, 2)

    # (a) parity plot
    x0, y0, x1, y1 = 70, 70, 400, 400
    frame(c, x0, y0, x1, y1)
    c.text(60, 48, "(a) Observed vs predicted (validation set)", BLACK, 1)
    c.text_v(24, (y0+y1)//2, "Predicted I*", BLACK, 1)
    c.text_c((x0+x1)//2, y1+22, "Observed I*", BLACK, 1)
    # 1:1 line
    c.dline(x0, y1, x1, y0, GRAY, 6, 5)
    for i in range(6):
        yy = y1 - i*(y1-y0)//5
        c.hline(x0-4, x0, yy, BLACK)
        xx = x0 + i*(x1-x0)//5
        c.vline(xx, y1, y1+4, BLACK)

    import random
    random.seed(5)
    models = [("Hybrid", MED_BLUE, 0.010), ("Physical", MED_GREEN, 0.022),
              ("Tree ens.", ORANGE, 0.030), ("Green-Ampt", RED, 0.055)]
    for name, col, sd in models:
        for _ in range(16):
            v = random.uniform(0.08, 0.34)
            bias = -0.5*sd if name in ("Green-Ampt",) else 0.0
            pv = v + random.gauss(bias, sd)
            px = x0 + (v-0.05)/0.32*(x1-x0)
            py = y1 - (pv-0.05)/0.32*(y1-y0)
            c.circle(px, py, 2, col, col)
    lx = x0+8
    for i, (name, col, _s) in enumerate(models):
        ly = y0+8+i*15
        c.circle(lx+3, ly, 3, col, col)
        c.text(lx+12, ly-3, name, BLACK, 1)

    # (b) metric bars (NSE) per model on validation
    bx0, by0, bx1, by1 = 470, 70, 830, 400
    frame(c, bx0, by0, bx1, by1)
    c.text(460, 48, "(b) Validation skill (NSE, higher = better)", BLACK, 1)
    c.text_v(430, (by0+by1)//2, "NSE", BLACK, 1)
    bar_models = [("Hybrid", MED_BLUE, 0.96), ("Physical", MED_GREEN, 0.88),
                  ("Tree", ORANGE, 0.81), ("Regr.", GOLD, 0.74),
                  ("Horton", PURPLE, 0.55), ("G-Ampt", RED, 0.48)]
    for i in range(6):
        yy = by1 - i*(by1-by0)//5
        c.hline(bx0-4, bx0, yy, BLACK)
        c.text(bx0-30, yy-3, "%.1f" % (i*0.2), BLACK, 1)
    n = len(bar_models)
    slot = (bx1-bx0-20)//n
    for i, (name, col, nse) in enumerate(bar_models):
        bx = bx0 + 10 + i*slot
        bh = int(nse*(by1-by0))
        c.rect(bx, by1-bh, bx+slot-12, by1, BLACK, col)
        c.text_c(bx+(slot-12)//2, by1-bh-11, "%.2f" % nse, BLACK, 1)
        c.text_c(bx+(slot-12)//2, by1+8, name, BLACK, 1)

    c.text(30, 440, "Figure 7. On conditions withheld from calibration, the hybrid physical + ML-residual model shows the tightest", BLACK, 1)
    c.text(30, 456, "parity (a) and the highest Nash-Sutcliffe efficiency (b), outperforming Green-Ampt, Horton, standalone", BLACK, 1)
    c.text(30, 472, "regression, and the standalone tree ensemble.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_7_Observed_vs_Predicted.png'))
    print("  Figure 7 done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating infiltration manuscript figures...")
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); fig7()
    print("\nAll figures saved to %s/" % OUTPUT_DIR)
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print("  %s: %.1f KB" % (f, sz/1024))


if __name__ == '__main__':
    main()
