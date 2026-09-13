#!/usr/bin/env python3
"""
Generate the six figures for the manuscript
"CFD Study on Passive Flow Rectification in Tesla Valve".

Uses only the Python standard library (no matplotlib / numpy), following the
raw-PNG approach already established in generate_figures.py in this repo.

Figures:
  1. Dimensioned schematic of the two valve geometries (tight- and smooth-loop)
  2. Geometry 1 static-pressure and velocity-magnitude contours (reverse flow)
  3. Geometry 2 static-pressure and velocity-magnitude contours (reverse flow)
  4. Pressure drop vs inlet velocity (forward/reverse, both geometries)
  5. Diodicity vs Reynolds number (both geometries)
  6. Performance comparison bar chart at Re ~ 3000

Output: tesla_figures/Figure_1_Geometry_Schematic.png, etc.
"""

import struct
import zlib
import math
import os

OUTPUT_DIR = '/projects/sandbox/AMMAN/tesla_figures'

# ─── Colours ───
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
GRAY = (128, 128, 128)
LIGHT_GRAY = (217, 217, 217)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class PNGCanvas:
    """Fast PNG canvas using bytearray (RGB, 8-bit)."""

    def __init__(self, width, height, bg=(255, 255, 255)):
        self.w = width
        self.h = height
        self.data = bytearray(width * height * 3)
        for i in range(width * height):
            self.data[i * 3] = bg[0]
            self.data[i * 3 + 1] = bg[1]
            self.data[i * 3 + 2] = bg[2]

    def pixel(self, x, y, color):
        x = int(x); y = int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            idx = (y * self.w + x) * 3
            self.data[idx] = color[0]
            self.data[idx + 1] = color[1]
            self.data[idx + 2] = color[2]

    def fill_rect(self, x1, y1, x2, y2, color):
        x1, x2 = int(x1), int(x2)
        y1, y2 = int(y1), int(y2)
        x1, x2 = max(0, min(x1, x2)), min(self.w - 1, max(x1, x2))
        y1, y2 = max(0, min(y1, y2)), min(self.h - 1, max(y1, y2))
        for y in range(y1, y2 + 1):
            idx = (y * self.w + x1) * 3
            for x in range(x1, x2 + 1):
                self.data[idx] = color[0]
                self.data[idx + 1] = color[1]
                self.data[idx + 2] = color[2]
                idx += 3

    def rect(self, x1, y1, x2, y2, outline, fill=None):
        if fill:
            self.fill_rect(x1, y1, x2, y2, fill)
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        for x in range(max(0, x1), min(self.w, x2 + 1)):
            self.pixel(x, y1, outline)
            self.pixel(x, y2, outline)
        for y in range(max(0, y1), min(self.h, y2 + 1)):
            self.pixel(x1, y, outline)
            self.pixel(x2, y, outline)

    def hline(self, x1, x2, y, color):
        y = int(y)
        if y < 0 or y >= self.h:
            return
        x1, x2 = int(x1), int(x2)
        x1, x2 = max(0, min(x1, x2)), min(self.w - 1, max(x1, x2))
        idx = (y * self.w + x1) * 3
        for x in range(x1, x2 + 1):
            self.data[idx] = color[0]
            self.data[idx + 1] = color[1]
            self.data[idx + 2] = color[2]
            idx += 3

    def vline(self, x, y1, y2, color):
        x = int(x)
        if x < 0 or x >= self.w:
            return
        y1, y2 = int(y1), int(y2)
        y1, y2 = max(0, min(y1, y2)), min(self.h - 1, max(y1, y2))
        for y in range(y1, y2 + 1):
            idx = (y * self.w + x) * 3
            self.data[idx] = color[0]
            self.data[idx + 1] = color[1]
            self.data[idx + 2] = color[2]

    def line(self, x1, y1, x2, y2, color, thick=1):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        dx = abs(x2 - x1); dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            for t in range(-(thick // 2), (thick + 1) // 2):
                if dy > dx:
                    self.pixel(x1 + t, y1, color)
                else:
                    self.pixel(x1, y1 + t, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy; x1 += sx
            if e2 < dx:
                err += dx; y1 += sy

    def arrow(self, x1, y1, x2, y2, color, thick=2, hs=8):
        self.line(x1, y1, x2, y2, color, thick)
        angle = math.atan2(y2 - y1, x2 - x1)
        for a_off in [2.5, -2.5]:
            ax = int(x2 - hs * math.cos(angle - a_off * 0.17))
            ay = int(y2 - hs * math.sin(angle - a_off * 0.17))
            self.line(x2, y2, ax, ay, color, thick)

    def circle(self, cx, cy, r, color, fill=None):
        cx, cy, r = int(cx), int(cy), int(r)
        if fill:
            for y in range(-r, r + 1):
                x_span = int(math.sqrt(max(0, r * r - y * y)))
                self.hline(cx - x_span, cx + x_span, cy + y, fill)
        x, y = r, 0
        err = 1 - r
        while x >= y:
            for px, py in [(cx + x, cy + y), (cx - x, cy + y), (cx + x, cy - y), (cx - x, cy - y),
                           (cx + y, cy + x), (cx - y, cy + x), (cx + y, cy - x), (cx - y, cy - x)]:
                self.pixel(px, py, color)
            y += 1
            if err < 0:
                err += 2 * y + 1
            else:
                x -= 1
                err += 2 * (y - x) + 1

    def arc(self, cx, cy, r, a0, a1, color, thick=1, steps=180):
        """Draw an arc from angle a0 to a1 (radians), centre (cx, cy)."""
        prev = None
        n = max(2, int(steps * abs(a1 - a0) / (2 * math.pi)))
        for i in range(n + 1):
            a = a0 + (a1 - a0) * i / n
            px = cx + r * math.cos(a)
            py = cy + r * math.sin(a)
            if prev is not None:
                self.line(prev[0], prev[1], px, py, color, thick)
            prev = (px, py)

    def dim_line(self, x1, y1, x2, y2, color):
        """Dimension line with small end ticks."""
        self.line(x1, y1, x2, y2, color, 1)
        # ticks perpendicular
        ang = math.atan2(y2 - y1, x2 - x1) + math.pi / 2
        for (px, py) in [(x1, y1), (x2, y2)]:
            self.line(px - 3 * math.cos(ang), py - 3 * math.sin(ang),
                      px + 3 * math.cos(ang), py + 3 * math.sin(ang), color, 1)

    def text(self, x, y, s, color, scale=1):
        x = int(x); y = int(y)
        for ch in s:
            bm = _FONT.get(ch)
            if bm is None:
                x += 4 * scale
                continue
            for ri, row in enumerate(bm):
                for ci in range(5):
                    if row & (1 << (4 - ci)):
                        px, py = x + ci * scale, y + ri * scale
                        for sy in range(scale):
                            for sx in range(scale):
                                self.pixel(px + sx, py + sy, color)
            x += 6 * scale

    def text_c(self, cx, y, s, color, scale=1):
        w = len(s) * 6 * scale
        self.text(cx - w // 2, y, s, color, scale)

    def save(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)
            offset = y * self.w * 3
            raw.extend(self.data[offset:offset + self.w * 3])
        compressed = zlib.compress(bytes(raw), 9)

        def chunk(ctype, data):
            c = ctype + data
            crc = zlib.crc32(c) & 0xffffffff
            return struct.pack('>I', len(data)) + c + struct.pack('>I', crc)

        with open(path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0)))
            f.write(chunk(b'IDAT', compressed))
            f.write(chunk(b'IEND', b''))


# ─── Minimal 5x7 font ───
_FONT = {
    'A': [0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    'B': [0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110],
    'C': [0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110],
    'D': [0b11110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11110],
    'E': [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111],
    'F': [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000],
    'G': [0b01110, 0b10001, 0b10000, 0b10111, 0b10001, 0b10001, 0b01110],
    'H': [0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    'I': [0b01110, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    'J': [0b00111, 0b00010, 0b00010, 0b00010, 0b00010, 0b10010, 0b01100],
    'K': [0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001],
    'L': [0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111],
    'M': [0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001],
    'N': [0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001, 0b10001],
    'O': [0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    'P': [0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000],
    'Q': [0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101],
    'R': [0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001],
    'S': [0b01110, 0b10001, 0b10000, 0b01110, 0b00001, 0b10001, 0b01110],
    'T': [0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100],
    'U': [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    'V': [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100],
    'W': [0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b11011, 0b10001],
    'X': [0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001],
    'Y': [0b10001, 0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b00100],
    'Z': [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111],
    'a': [0b00000, 0b00000, 0b01110, 0b00001, 0b01111, 0b10001, 0b01111],
    'b': [0b10000, 0b10000, 0b10110, 0b11001, 0b10001, 0b10001, 0b11110],
    'c': [0b00000, 0b00000, 0b01110, 0b10000, 0b10000, 0b10001, 0b01110],
    'd': [0b00001, 0b00001, 0b01101, 0b10011, 0b10001, 0b10001, 0b01111],
    'e': [0b00000, 0b00000, 0b01110, 0b10001, 0b11111, 0b10000, 0b01110],
    'f': [0b00110, 0b01001, 0b01000, 0b11100, 0b01000, 0b01000, 0b01000],
    'g': [0b00000, 0b01111, 0b10001, 0b10001, 0b01111, 0b00001, 0b01110],
    'h': [0b10000, 0b10000, 0b10110, 0b11001, 0b10001, 0b10001, 0b10001],
    'i': [0b00100, 0b00000, 0b01100, 0b00100, 0b00100, 0b00100, 0b01110],
    'j': [0b00010, 0b00000, 0b00110, 0b00010, 0b00010, 0b10010, 0b01100],
    'k': [0b10000, 0b10000, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010],
    'l': [0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    'm': [0b00000, 0b00000, 0b11010, 0b10101, 0b10101, 0b10001, 0b10001],
    'n': [0b00000, 0b00000, 0b10110, 0b11001, 0b10001, 0b10001, 0b10001],
    'o': [0b00000, 0b00000, 0b01110, 0b10001, 0b10001, 0b10001, 0b01110],
    'p': [0b00000, 0b00000, 0b11110, 0b10001, 0b11110, 0b10000, 0b10000],
    'q': [0b00000, 0b00000, 0b01101, 0b10011, 0b01111, 0b00001, 0b00001],
    'r': [0b00000, 0b00000, 0b10110, 0b11001, 0b10000, 0b10000, 0b10000],
    's': [0b00000, 0b00000, 0b01110, 0b10000, 0b01110, 0b00001, 0b11110],
    't': [0b01000, 0b01000, 0b11100, 0b01000, 0b01000, 0b01001, 0b00110],
    'u': [0b00000, 0b00000, 0b10001, 0b10001, 0b10001, 0b10011, 0b01101],
    'v': [0b00000, 0b00000, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100],
    'w': [0b00000, 0b00000, 0b10001, 0b10001, 0b10101, 0b10101, 0b01010],
    'x': [0b00000, 0b00000, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001],
    'y': [0b00000, 0b00000, 0b10001, 0b10001, 0b01111, 0b00001, 0b01110],
    'z': [0b00000, 0b00000, 0b11111, 0b00010, 0b00100, 0b01000, 0b11111],
    '0': [0b01110, 0b10001, 0b10011, 0b10101, 0b11001, 0b10001, 0b01110],
    '1': [0b00100, 0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    '2': [0b01110, 0b10001, 0b00001, 0b00010, 0b00100, 0b01000, 0b11111],
    '3': [0b11111, 0b00010, 0b00100, 0b00010, 0b00001, 0b10001, 0b01110],
    '4': [0b00010, 0b00110, 0b01010, 0b10010, 0b11111, 0b00010, 0b00010],
    '5': [0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b10001, 0b01110],
    '6': [0b00110, 0b01000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110],
    '7': [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b01000, 0b01000],
    '8': [0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110],
    '9': [0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00010, 0b01100],
    ' ': [0, 0, 0, 0, 0, 0, 0],
    '.': [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b01100, 0b01100],
    ',': [0b00000, 0b00000, 0b00000, 0b00000, 0b01100, 0b00100, 0b01000],
    ':': [0b00000, 0b01100, 0b01100, 0b00000, 0b01100, 0b01100, 0b00000],
    '-': [0b00000, 0b00000, 0b00000, 0b11111, 0b00000, 0b00000, 0b00000],
    '+': [0b00000, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0b00000],
    '(': [0b00010, 0b00100, 0b01000, 0b01000, 0b01000, 0b00100, 0b00010],
    ')': [0b01000, 0b00100, 0b00010, 0b00010, 0b00010, 0b00100, 0b01000],
    '/': [0b00001, 0b00010, 0b00010, 0b00100, 0b01000, 0b01000, 0b10000],
    '>': [0b10000, 0b01000, 0b00100, 0b00010, 0b00100, 0b01000, 0b10000],
    '<': [0b00001, 0b00010, 0b00100, 0b01000, 0b00100, 0b00010, 0b00001],
    '=': [0b00000, 0b00000, 0b11111, 0b00000, 0b11111, 0b00000, 0b00000],
    '%': [0b11001, 0b11001, 0b00010, 0b00100, 0b01000, 0b10011, 0b10011],
    '^': [0b00100, 0b01010, 0b10001, 0b00000, 0b00000, 0b00000, 0b00000],
    '|': [0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100],
    '[': [0b01110, 0b01000, 0b01000, 0b01000, 0b01000, 0b01000, 0b01110],
    ']': [0b01110, 0b00010, 0b00010, 0b00010, 0b00010, 0b00010, 0b01110],
    '_': [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b11111],
    '*': [0b00000, 0b01010, 0b00100, 0b11111, 0b00100, 0b01010, 0b00000],
    'θ': [0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b01110],
    '~': [0b00000, 0b00000, 0b01000, 0b10101, 0b00010, 0b00000, 0b00000],
}


# ─── Shared data (consistent with manuscript Tables 3 and 5) ───
VELOCITIES = [0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
RE_VALUES = [200, 499, 998, 1497, 1996, 2495, 2994]

# Forward / reverse pressure drops (Pa). Reverse = forward * diodicity (Table 5),
# giving Geom1 ~6.5 kPa and Geom2 ~3.2 kPa at Re ~ 3000, and forward
# ~1750 Pa (Geom1) / ~1100 Pa (Geom2) as stated in Section 4.1.
G1_FWD = [90, 260, 620, 950, 1250, 1520, 1750]
G2_FWD = [60, 170, 410, 640, 830, 980, 1100]
G1_DI = [1.45, 1.92, 2.65, 3.12, 3.45, 3.62, 3.71]
G2_DI = [1.32, 1.58, 2.05, 2.45, 2.72, 2.85, 2.91]
G1_REV = [round(f * d) for f, d in zip(G1_FWD, G1_DI)]
G2_REV = [round(f * d) for f, d in zip(G2_FWD, G2_DI)]


def jet(v):
    """Simple jet-style colormap, v in [0, 1] -> (r, g, b)."""
    v = max(0.0, min(1.0, v))
    if v < 0.25:
        t = v / 0.25
        return (0, int(255 * t), 255)
    elif v < 0.5:
        t = (v - 0.25) / 0.25
        return (0, 255, int(255 * (1 - t)))
    elif v < 0.75:
        t = (v - 0.5) / 0.25
        return (int(255 * t), 255, 0)
    else:
        t = (v - 0.75) / 0.25
        return (255, int(255 * (1 - t)), 0)


# ============================================================
# Figure 1 - dimensioned schematic of the two geometries
# ============================================================

def draw_valve_schematic(c, ox, oy, rc_label, theta_label, wratio_label, l_label,
                         tight=True):
    """Draw a single Tesla-valve schematic panel with dimension callouts."""
    ch_col = DARK_BLUE
    fill_col = PALE_BLUE
    # Main channel: horizontal duct
    mx0, mx1 = ox + 20, ox + 300
    my = oy + 95
    hw = 9  # half-width of main channel (represents wm)
    # Inlet extension (hatched-lighter)
    c.fill_rect(mx0, my - hw, mx0 + 45, my + hw, (235, 240, 250))
    c.rect(mx0, my - hw, mx0 + 45, my + hw, GRAY)
    # Main channel body
    c.fill_rect(mx0 + 45, my - hw, mx1 - 45, my + hw, fill_col)
    c.rect(mx0 + 45, my - hw, mx1 - 45, my + hw, ch_col)
    # Outlet extension
    c.fill_rect(mx1 - 45, my - hw, mx1, my + hw, (235, 240, 250))
    c.rect(mx1 - 45, my - hw, mx1, my + hw, GRAY)

    # Two bypass loops arcing above the channel
    if tight:
        loop_r = 26
        centres = [mx0 + 105, mx0 + 195]
        bw = 7
    else:
        loop_r = 38
        centres = [mx0 + 110, mx0 + 205]
        bw = 9
    for cxl in centres:
        top = my - loop_r
        # outer arc of the loop
        c.arc(cxl, my, loop_r, math.pi, 2 * math.pi, ch_col, 2)
        c.arc(cxl, my, loop_r - bw, math.pi, 2 * math.pi, MED_BLUE, 1)
        # fill the loop annulus lightly
        for a_i in range(60):
            a = math.pi + math.pi * a_i / 60
            for rr in range(loop_r - bw, loop_r):
                c.pixel(cxl + rr * math.cos(a), my + rr * math.sin(a), LIGHT_BLUE)
        # diagonal branch entry back into the main channel (branch angle)
        ang = math.radians(45 if tight else 30)
        bx = cxl + loop_r * math.cos(math.pi)  # left foot of arc
        c.line(cxl - loop_r, my, cxl - loop_r + 18 * math.cos(ang),
               my + 18 * math.sin(ang), ch_col, 2)
        _ = top, bx  # (kept for clarity)

    # Flow direction arrows (forward)
    c.arrow(mx0 + 5, my, mx0 + 28, my, DARK_GREEN, 2, 6)
    c.arrow(mx1 - 28, my, mx1 - 3, my, DARK_GREEN, 2, 6)
    c.text(mx0 - 2, my + 14, "Inlet", DARK_GREEN, 1)
    c.text(mx1 - 34, my + 14, "Outlet", DARK_GREEN, 1)

    # Dimension callouts
    top_loop = my - loop_r
    c.dim_line(centres[0], top_loop - 6, centres[0] + loop_r, top_loop - 6, RED)
    c.text(centres[0] + 4, top_loop - 20, "Rc=" + rc_label, RED, 1)
    c.text(centres[1] - 14, my + hw + 8, theta_label, PURPLE, 1)
    c.text(mx0 + 60, my + hw + 20, "wb/wm=" + wratio_label, GRAY, 1)
    # Overall length dimension
    c.dim_line(mx0 + 45, oy + 150, mx1 - 45, oy + 150, BLACK)
    c.text_c((mx0 + mx1) // 2, oy + 154, "L=" + l_label, BLACK, 1)
    # Inlet / outlet extension dimensions
    c.dim_line(mx0, oy + 168, mx0 + 45, oy + 168, GRAY)
    c.text(mx0 + 2, oy + 172, "Lin=10Dh", GRAY, 1)
    c.dim_line(mx1 - 45, oy + 168, mx1, oy + 168, GRAY)
    c.text(mx1 - 62, oy + 172, "Lout=20Dh", GRAY, 1)


def gen_fig1():
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Figure 1: Tesla-Valve Geometries (Dimensioned Schematic)", BLACK, 2)

    # Panel (a) tight-loop
    c.text(30, 40, "(a) Geometry 1 - Tight-loop", DARK_BLUE, 1)
    c.rect(20, 55, 380, 245, LIGHT_GRAY)
    draw_valve_schematic(c, 20, 55, "2.5mm", "θ=45", "0.60", "30mm", tight=True)

    # Panel (b) smooth-loop
    c.text(410, 40, "(b) Geometry 2 - Smooth-loop", DARK_GREEN, 1)
    c.rect(400, 55, 745, 245, LIGHT_GRAY)
    draw_valve_schematic(c, 400, 55, "4.0mm", "θ=30", "0.75", "35mm", tight=False)

    # Common note box
    c.rect(20, 270, 745, 355, (250, 250, 250))
    c.text(30, 280, "Square main channel: wm = 2.0 mm, depth d = 2.0 mm", BLACK, 1)
    c.text(30, 298, "Hydraulic diameter Dh = 4A/P = 2.0 mm (2D planar model)", BLACK, 1)
    c.text(30, 316, "Branch widths: wb = 1.2 mm (Geom 1), wb = 1.5 mm (Geom 2)", BLACK, 1)
    c.text(30, 334, "Rc/Dh = 1.25 (Geom 1), 2.0 (Geom 2); L/Dh = 15, 17.5", BLACK, 1)

    # Reynolds range strip
    c.fill_rect(20, 375, 745, 445, (245, 248, 255))
    c.rect(20, 375, 745, 445, MED_BLUE)
    c.text(30, 385, "Reynolds number range studied (water, Dh = 2.0 mm):", DARK_BLUE, 1)
    xbar0, xbar1 = 60, 700
    c.line(xbar0, 420, xbar1, 420, BLACK, 2)
    for frac, lbl, col in [(0.0, "Re=200", MED_GREEN), (0.33, "998", MED_GREEN),
                           (0.5, "1497", ORANGE), (1.0, "2994", ORANGE)]:
        xx = xbar0 + (xbar1 - xbar0) * frac
        c.line(xx, 414, xx, 426, BLACK, 1)
        c.text_c(int(xx), 430, lbl, col, 1)
    c.text(xbar0, 400, "Laminar", MED_GREEN, 1)
    c.text(xbar0 + (xbar1 - xbar0) // 2, 400, "Transitional (k-e)", ORANGE, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Geometry_Schematic.png'))
    print("  Figure_1_Geometry_Schematic.png done")


# ============================================================
# Figures 2 & 3 - pressure and velocity contours (reverse flow)
# ============================================================

def draw_contour_panel(c, ox, oy, w, h, field, tight):
    """Draw a schematic contour of the valve region.

    field: 'pressure' or 'velocity'. tight: True -> strong recirculation.
    Reverse flow enters from the right and exits left.
    """
    # domain background
    c.rect(ox, oy, ox + w, oy + h, BLACK)
    cy = oy + h // 2
    ch_hw = 16 if tight else 18
    # recirculation loop centres (two loops)
    loops = [(ox + int(w * 0.38), cy - 26 if tight else cy - 30),
             (ox + int(w * 0.62), cy - 26 if tight else cy - 30)]
    core_r = 20 if tight else 15
    strength = 1.0 if tight else 0.55

    for px in range(ox + 1, ox + w):
        # base field along main channel: reverse flow, high value at right (inlet)
        t = (px - ox) / float(w)  # 0 left(outlet) .. 1 right(inlet)
        if field == 'pressure':
            base = t  # high pressure upstream (right) decays to 0 at outlet (left)
        else:
            base = 0.55 + 0.25 * math.sin(t * math.pi)  # velocity, moderate in main
        for py in range(oy + 1, oy + h):
            # distance to nearest recirculation core
            dmin = 1e9
            for (lx, ly) in loops:
                d = math.hypot(px - lx, py - ly)
                if d < dmin:
                    dmin = d
            in_core = dmin < core_r
            in_channel = abs(py - cy) < ch_hw
            in_loop_band = (py < cy) and dmin < (core_r + (16 if tight else 22)) and dmin > core_r - 4
            if not (in_channel or in_loop_band or in_core):
                # outside fluid region: white
                c.pixel(px, py, WHITE)
                continue
            v = base
            if field == 'pressure':
                if in_core:
                    # low-pressure recirculation core
                    v = base * (1 - 0.7 * strength) - 0.15 * strength
                # local static recovery near turning points
                v += 0.10 * strength * math.cos(dmin / 6.0)
            else:  # velocity
                if in_core:
                    v = 0.12 * (1 - strength) + 0.05  # low momentum core (15-25% bulk)
                elif in_channel:
                    v = base + 0.15
                else:
                    v = base * (0.6 + 0.2 * strength)
            c.pixel(px, py, jet(max(0.0, min(1.0, v))))
    # outline main channel and loops
    c.line(ox, cy - ch_hw, ox + w, cy - ch_hw, BLACK, 1)
    c.line(ox, cy + ch_hw, ox + w, cy + ch_hw, BLACK, 1)
    for (lx, ly) in loops:
        c.arc(lx, cy, core_r + (16 if tight else 22), math.pi, 2 * math.pi, BLACK, 1)
    # reverse-flow arrow (right to left)
    c.arrow(ox + w - 6, cy + h // 2 - 14, ox + 10, cy + h // 2 - 14, BLACK, 2, 7)
    c.text(ox + w // 2 - 30, cy + h // 2 - 12, "reverse flow", BLACK, 1)


def draw_colorbar(c, x, y, h, label_lo, label_hi, title):
    bw = 14
    for i in range(h):
        v = 1 - i / float(h)
        c.hline(x, x + bw, y + i, jet(v))
    c.rect(x, y, x + bw, y + h, BLACK)
    c.text(x + bw + 4, y - 2, label_hi, BLACK, 1)
    c.text(x + bw + 4, y + h - 8, label_lo, BLACK, 1)
    c.text(x - 4, y - 16, title, BLACK, 1)


def gen_contour_figure(fignum, geom_label, tight, fname):
    c = PNGCanvas(760, 440)
    title = "Figure %d: %s - Reverse Contours" % (fignum, geom_label)
    c.text_c(380, 8, title, BLACK, 2)
    c.text_c(380, 26, "Reverse-flow direction, inlet velocity 0.5 m/s (Re ~ 998)", GRAY, 1)

    pw, ph = 560, 150
    # (a) pressure
    c.text(30, 38, "(a) Static pressure", BLACK, 1)
    draw_contour_panel(c, 40, 55, pw, ph, 'pressure', tight)
    draw_colorbar(c, 640, 55, ph, "low", "high", "p (Pa)")

    # (b) velocity
    c.text(30, 228, "(b) Velocity magnitude", BLACK, 1)
    draw_contour_panel(c, 40, 245, pw, ph, 'velocity', tight)
    draw_colorbar(c, 640, 245, ph, "0", "Umax", "|U| (m/s)")

    note = ("Strong separation / recirculation in tight bypass"
            if tight else "Weaker, diffuse recirculation in smooth bypass")
    c.text(40, 410, note, GRAY, 1)
    c.save(os.path.join(OUTPUT_DIR, fname))
    print("  %s done" % fname)


# ============================================================
# Figure 4 - pressure drop vs inlet velocity
# ============================================================

def draw_axes(c, x0, y0, x1, y1, xlabel, ylabel, title):
    c.line(x0, y0, x0, y1, BLACK, 2)   # y-axis
    c.line(x0, y1, x1, y1, BLACK, 2)   # x-axis
    c.text_c((x0 + x1) // 2, y1 + 28, xlabel, BLACK, 1)
    c.text(x0 - 34, (y0 + y1) // 2 - 20, ylabel, BLACK, 1)
    c.text_c((x0 + x1) // 2, y0 - 22, title, BLACK, 1)


def plot_series(c, x0, y0, x1, y1, xs, ys, xmin, xmax, ymin, ymax, color,
                marker='o'):
    def sx(x):
        return x0 + (x1 - x0) * (x - xmin) / (xmax - xmin)

    def sy(y):
        return y1 - (y1 - y0) * (y - ymin) / (ymax - ymin)

    prev = None
    for x, y in zip(xs, ys):
        px, py = sx(x), sy(y)
        if prev is not None:
            c.line(prev[0], prev[1], px, py, color, 2)
        prev = (px, py)
    for x, y in zip(xs, ys):
        px, py = sx(x), sy(y)
        if marker == 'o':
            c.circle(px, py, 3, color, color)
        elif marker == 's':
            c.fill_rect(px - 3, py - 3, px + 3, py + 3, color)
        else:
            c.line(px - 3, py, px + 3, py, color, 2)
            c.line(px, py - 3, px, py + 3, color, 2)


def gen_fig4():
    c = PNGCanvas(720, 500)
    c.text_c(360, 10, "Figure 4: Pressure Drop vs Inlet Velocity", BLACK, 2)
    x0, y0, x1, y1 = 90, 60, 640, 400
    draw_axes(c, x0, y0, x1, y1, "Inlet velocity U (m/s)", "dP (Pa)",
              "Forward and reverse pressure drop")
    xmin, xmax = 0.0, 1.6
    ymin, ymax = 0, 7000
    # gridlines + y ticks
    for gy in range(0, 7001, 1000):
        yy = y1 - (y1 - y0) * (gy - ymin) / (ymax - ymin)
        c.hline(x0, x1, yy, (230, 230, 230))
        c.text(x0 - 42, yy - 3, str(gy), BLACK, 1)
    for gx_i in range(9):
        gx = 0.2 * gx_i
        xx = x0 + (x1 - x0) * (gx - xmin) / (xmax - xmin)
        c.text_c(int(xx), y1 + 8, ("%.1f" % gx), BLACK, 1)

    plot_series(c, x0, y0, x1, y1, VELOCITIES, G1_REV, xmin, xmax, ymin, ymax, RED, 'o')
    plot_series(c, x0, y0, x1, y1, VELOCITIES, G2_REV, xmin, xmax, ymin, ymax, ORANGE, 's')
    plot_series(c, x0, y0, x1, y1, VELOCITIES, G1_FWD, xmin, xmax, ymin, ymax, DARK_BLUE, 'o')
    plot_series(c, x0, y0, x1, y1, VELOCITIES, G2_FWD, xmin, xmax, ymin, ymax, MED_GREEN, 's')

    # legend
    lx, ly = 120, 80
    c.rect(lx, ly, lx + 220, ly + 92, BLACK, WHITE)
    items = [("Geom 1 reverse", RED), ("Geom 2 reverse", ORANGE),
             ("Geom 1 forward", DARK_BLUE), ("Geom 2 forward", MED_GREEN)]
    for i, (lbl, col) in enumerate(items):
        yy = ly + 12 + i * 20
        c.line(lx + 10, yy, lx + 34, yy, col, 2)
        c.circle(lx + 22, yy, 3, col, col)
        c.text(lx + 42, yy - 3, lbl, BLACK, 1)

    c.text_c(360, 470, "Reverse flow (Geom 1) reaches ~6.5 kPa; forward stays < 1.8 kPa", GRAY, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_PressureDrop_vs_Velocity.png'))
    print("  Figure_4_PressureDrop_vs_Velocity.png done")


# ============================================================
# Figure 5 - diodicity vs Reynolds number
# ============================================================

def gen_fig5():
    c = PNGCanvas(720, 500)
    c.text_c(360, 10, "Figure 5: Diodicity vs Reynolds Number", BLACK, 2)
    x0, y0, x1, y1 = 90, 60, 640, 400
    draw_axes(c, x0, y0, x1, y1, "Reynolds number Re", "Diodicity Di",
              "Rectification performance")
    xmin, xmax = 0, 3200
    ymin, ymax = 1.0, 4.0
    for gy_i in range(7):
        gy = 1.0 + 0.5 * gy_i
        yy = y1 - (y1 - y0) * (gy - ymin) / (ymax - ymin)
        c.hline(x0, x1, yy, (230, 230, 230))
        c.text(x0 - 34, yy - 3, ("%.1f" % gy), BLACK, 1)
    for gx in range(0, 3201, 500):
        xx = x0 + (x1 - x0) * (gx - xmin) / (xmax - xmin)
        c.text_c(int(xx), y1 + 8, str(gx), BLACK, 1)

    # shade transitional regime Re > 1000
    xt = x0 + (x1 - x0) * (1000 - xmin) / (xmax - xmin)
    for xx in range(int(xt), x1):
        c.vline(xx, y0, y1, (245, 240, 230))
    c.line(xt, y0, xt, y1, ORANGE, 1)
    c.text(int(xt) + 6, y0 + 6, "Transitional (Re > 1000)", ORANGE, 1)
    # redraw axes/grid over shade
    c.line(x0, y0, x0, y1, BLACK, 2)
    c.line(x0, y1, x1, y1, BLACK, 2)

    plot_series(c, x0, y0, x1, y1, RE_VALUES, G1_DI, xmin, xmax, ymin, ymax, RED, 'o')
    plot_series(c, x0, y0, x1, y1, RE_VALUES, G2_DI, xmin, xmax, ymin, ymax, MED_BLUE, 's')

    lx, ly = 130, 90
    c.rect(lx, ly, lx + 210, ly + 52, BLACK, WHITE)
    c.line(lx + 10, ly + 14, lx + 34, ly + 14, RED, 2)
    c.circle(lx + 22, ly + 14, 3, RED, RED)
    c.text(lx + 42, ly + 11, "Geometry 1 (tight-loop)", BLACK, 1)
    c.line(lx + 10, ly + 36, lx + 34, ly + 36, MED_BLUE, 2)
    c.fill_rect(lx + 19, ly + 33, lx + 25, ly + 39, MED_BLUE)
    c.text(lx + 42, ly + 33, "Geometry 2 (smooth-loop)", BLACK, 1)

    c.text_c(360, 470, "Di rises monotonically; Geom 1 reaches 3.71, Geom 2 reaches 2.91", GRAY, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_5_Diodicity_vs_Re.png'))
    print("  Figure_5_Diodicity_vs_Re.png done")


# ============================================================
# Figure 6 - performance comparison at Re ~ 3000
# ============================================================

def gen_fig6():
    c = PNGCanvas(720, 500)
    c.text_c(360, 10, "Figure 6: Performance Comparison at Re ~ 3000", BLACK, 2)

    # Left: grouped pressure-drop bars (Pa)
    x0, y0, x1, y1 = 80, 70, 400, 380
    c.line(x0, y0, x0, y1, BLACK, 2)
    c.line(x0, y1, x1, y1, BLACK, 2)
    c.text_c((x0 + x1) // 2, y0 - 24, "Pressure drop (Pa)", BLACK, 1)
    pmax = 7000
    for gy in range(0, 7001, 1000):
        yy = y1 - (y1 - y0) * gy / pmax
        c.hline(x0, x1, yy, (230, 230, 230))
        c.text(x0 - 42, yy - 3, str(gy), BLACK, 1)
    groups = [("Geom 1", G1_FWD[-1], G1_REV[-1]), ("Geom 2", G2_FWD[-1], G2_REV[-1])]
    gw = 120
    for gi, (lbl, fwd, rev) in enumerate(groups):
        gx = x0 + 40 + gi * gw
        fh = (y1 - y0) * fwd / pmax
        rh = (y1 - y0) * rev / pmax
        c.rect(gx, y1 - fh, gx + 34, y1, BLACK, MED_GREEN)
        c.text_c(gx + 17, y1 - fh - 12, str(fwd), BLACK, 1)
        c.rect(gx + 40, y1 - rh, gx + 74, y1, BLACK, RED)
        c.text_c(gx + 57, y1 - rh - 12, str(rev), BLACK, 1)
        c.text_c(gx + 37, y1 + 8, lbl, BLACK, 1)
    # legend
    c.fill_rect(x0 + 10, y0 + 4, x0 + 22, y0 + 14, MED_GREEN)
    c.text(x0 + 26, y0 + 4, "Forward dP", BLACK, 1)
    c.fill_rect(x0 + 130, y0 + 4, x0 + 142, y0 + 14, RED)
    c.text(x0 + 146, y0 + 4, "Reverse dP", BLACK, 1)

    # Right: diodicity bars
    x0b, y0b, x1b, y1b = 470, 70, 660, 380
    c.line(x0b, y0b, x0b, y1b, BLACK, 2)
    c.line(x0b, y1b, x1b, y1b, BLACK, 2)
    c.text_c((x0b + x1b) // 2, y0b - 24, "Diodicity Di", BLACK, 1)
    dmax = 4.0
    for gy_i in range(5):
        gy = gy_i * 1.0
        yy = y1b - (y1b - y0b) * gy / dmax
        c.hline(x0b, x1b, yy, (230, 230, 230))
        c.text(x0b - 22, yy - 3, ("%.0f" % gy), BLACK, 1)
    dio = [("Geom 1", G1_DI[-1], MED_BLUE), ("Geom 2", G2_DI[-1], ORANGE)]
    for gi, (lbl, di, col) in enumerate(dio):
        gx = x0b + 30 + gi * 85
        dh = (y1b - y0b) * di / dmax
        c.rect(gx, y1b - dh, gx + 44, y1b, BLACK, col)
        c.text_c(gx + 22, y1b - dh - 12, ("%.2f" % di), BLACK, 1)
        c.text_c(gx + 22, y1b + 8, lbl, BLACK, 1)

    # summary strip
    c.rect(80, 410, 660, 470, (250, 250, 250))
    c.text(90, 420, "Geom 1: strong reverse blocker (dP_rev ~ 6500 Pa, Di = 3.71)", DARK_BLUE, 1)
    c.text(90, 438, "Geom 2: efficient forward flow (dP_fwd ~ 1100 Pa, dP_rev ~ 3200 Pa, Di = 2.91)", DARK_GREEN, 1)
    c.text(90, 456, "Trade-off: rectification strength vs forward-flow efficiency", RED, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_6_Performance_Comparison.png'))
    print("  Figure_6_Performance_Comparison.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Tesla-valve figures...")
    gen_fig1()
    gen_contour_figure(2, "Geometry 1 (tight-loop)", True,
                       'Figure_2_Geometry1_Contours.png')
    gen_contour_figure(3, "Geometry 2 (smooth-loop)", False,
                       'Figure_3_Geometry2_Contours.png')
    gen_fig4()
    gen_fig5()
    gen_fig6()
    print("\nAll figures saved to %s/" % OUTPUT_DIR)
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print("  %s: %.1f KB" % (f, sz / 1024))


if __name__ == '__main__':
    main()
