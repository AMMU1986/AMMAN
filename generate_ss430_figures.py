#!/usr/bin/env python3
"""
Generate 4 revised figures (PNG) for the SS430 filler-weldability manuscript.

Addresses reviewer comments:
  R1.1 - Figures 1-3 redrawn as clean, professional, to-scale schematics.
  R2.5 - Correct, clearly-labeled scale bars (fixes the "unreasonable scale"
         complaint on the metallographic cross-section).
  R1.4 - Figure 4 bar charts use the single authoritative dataset so there are
         no contradictions between abstract, tables, and figures.

Uses only the Python standard library (struct + zlib) via a self-contained
PNGCanvas class plus a 5x7 bitmap font, following the established repo pattern
in generate_figures.py. Do NOT add third-party dependencies (matplotlib etc.).
"""

import struct
import zlib
import math
import os

OUTPUT_DIR = '/projects/sandbox/AMMAN/manuscript_figures'

# Colors
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
STEEL = (188, 195, 205)
LIGHT_STEEL = (223, 228, 235)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class PNGCanvas:
    """Fast PNG canvas using bytearray (stdlib struct + zlib)."""

    def __init__(self, width, height, bg=(255, 255, 255)):
        self.w = width
        self.h = height
        self.data = bytearray(width * height * 3)
        for i in range(width * height):
            self.data[i*3] = bg[0]
            self.data[i*3+1] = bg[1]
            self.data[i*3+2] = bg[2]

    def pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            idx = (y * self.w + x) * 3
            self.data[idx] = color[0]
            self.data[idx+1] = color[1]
            self.data[idx+2] = color[2]

    def fill_rect(self, x1, y1, x2, y2, color):
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
        for x in range(max(0, x1), min(self.w, x2+1)):
            self.pixel(x, y1, outline)
            self.pixel(x, y2, outline)
        for y in range(max(0, y1), min(self.h, y2+1)):
            self.pixel(x1, y, outline)
            self.pixel(x2, y, outline)

    def hline(self, x1, x2, y, color, thick=1):
        for t in range(thick):
            yy = y + t
            if yy < 0 or yy >= self.h:
                continue
            a, b = max(0, min(x1, x2)), min(self.w-1, max(x1, x2))
            idx = (yy * self.w + a) * 3
            for x in range(a, b+1):
                self.data[idx] = color[0]
                self.data[idx+1] = color[1]
                self.data[idx+2] = color[2]
                idx += 3

    def vline(self, x, y1, y2, color, thick=1):
        for t in range(thick):
            xx = x + t
            if xx < 0 or xx >= self.w:
                continue
            a, b = max(0, min(y1, y2)), min(self.h-1, max(y1, y2))
            for y in range(a, b+1):
                idx = (y * self.w + xx) * 3
                self.data[idx] = color[0]
                self.data[idx+1] = color[1]
                self.data[idx+2] = color[2]

    def line(self, x1, y1, x2, y2, color, thick=1):
        dx = abs(x2-x1); dy = abs(y2-y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            for t in range(-(thick//2), (thick+1)//2):
                self.pixel(x1+t if dy > dx else x1, y1 if dy > dx else y1+t, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2*err
            if e2 > -dy:
                err -= dy; x1 += sx
            if e2 < dx:
                err += dx; y1 += sy

    def arrow(self, x1, y1, x2, y2, color, thick=2, hs=9):
        self.line(x1, y1, x2, y2, color, thick)
        angle = math.atan2(y2-y1, x2-x1)
        for a_off in [2.5, -2.5]:
            ax = int(x2 - hs * math.cos(angle - a_off * 0.17))
            ay = int(y2 - hs * math.sin(angle - a_off * 0.17))
            self.line(x2, y2, ax, ay, color, thick)

    def circle(self, cx, cy, r, color, fill=None):
        if fill:
            for y in range(-r, r+1):
                x_span = int(math.sqrt(max(0, r*r - y*y)))
                self.hline(cx - x_span, cx + x_span, cy + y, fill)
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

    def arc(self, cx, cy, r, a0, a1, color, steps=60):
        """Draw a circular arc from angle a0 to a1 (radians)."""
        prev = None
        for i in range(steps+1):
            a = a0 + (a1-a0)*i/steps
            px = int(cx + r*math.cos(a))
            py = int(cy + r*math.sin(a))
            if prev is not None:
                self.line(prev[0], prev[1], px, py, color, 1)
            prev = (px, py)

    def text(self, x, y, s, color, scale=1):
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

    def save(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)
            offset = y * self.w * 3
            raw.extend(self.data[offset:offset + self.w*3])
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


# Minimal 5x7 font
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
    ' ':[0b00000,0b00000,0b00000,0b00000,0b00000,0b00000,0b00000],
    '.':[0b00000,0b00000,0b00000,0b00000,0b00000,0b01100,0b01100],
    ',':[0b00000,0b00000,0b00000,0b00000,0b01100,0b00100,0b01000],
    ':':[0b00000,0b01100,0b01100,0b00000,0b01100,0b01100,0b00000],
    '-':[0b00000,0b00000,0b00000,0b11111,0b00000,0b00000,0b00000],
    '+':[0b00000,0b00100,0b00100,0b11111,0b00100,0b00100,0b00000],
    '(':[0b00010,0b00100,0b01000,0b01000,0b01000,0b00100,0b00010],
    ')':[0b01000,0b00100,0b00010,0b00010,0b00010,0b00100,0b01000],
    '/':[0b00001,0b00010,0b00010,0b00100,0b01000,0b01000,0b10000],
    '>':[0b10000,0b01000,0b00100,0b00010,0b00100,0b01000,0b10000],
    '<':[0b00001,0b00010,0b00100,0b01000,0b00100,0b00010,0b00001],
    '=':[0b00000,0b00000,0b11111,0b00000,0b11111,0b00000,0b00000],
    '%':[0b11001,0b11001,0b00010,0b00100,0b01000,0b10011,0b10011],
    '^':[0b00100,0b01010,0b10001,0b00000,0b00000,0b00000,0b00000],
    '|':[0b00100,0b00100,0b00100,0b00100,0b00100,0b00100,0b00100],
    '[':[0b01110,0b01000,0b01000,0b01000,0b01000,0b01000,0b01110],
    ']':[0b01110,0b00010,0b00010,0b00010,0b00010,0b00010,0b01110],
    '_':[0b00000,0b00000,0b00000,0b00000,0b00000,0b00000,0b11111],
    '#':[0b01010,0b01010,0b11111,0b01010,0b11111,0b01010,0b01010],
    'x':[0b00000,0b00000,0b10001,0b01010,0b00100,0b01010,0b10001],
}


def draw_scale_bar(c, x, y, length_px, label, color=BLACK):
    """Draw a horizontal scale bar with end ticks and a centered label."""
    c.hline(x, x + length_px, y, color, 2)
    c.vline(x, y - 5, y + 5, color, 2)
    c.vline(x + length_px, y - 5, y + 5, color, 2)
    c.text_c(x + length_px // 2, y + 8, label, color, 1)


def gen_fig1():
    """Figure 1: to-scale square-butt / bead-on-plate schematic (plan + side)."""
    c = PNGCanvas(900, 620)
    c.text_c(450, 12, "Square Butt Joint - AISI 430 (75 x 75 x 12 mm coupons)", BLACK, 2)

    # --- Scale: 4 px per mm for the plan view ---
    ppm = 4
    plate_mm = 75
    gap_mm = 2
    plate_px = plate_mm * ppm            # 300 px
    gap_px = gap_mm * ppm                # 8 px

    # --- (a) Plan view: two coupons side by side with a 2 mm root gap ---
    c.text(60, 50, "(a) Plan view", BLACK, 1)
    ax = 130
    ay = 80
    # Left coupon
    c.rect(ax, ay, ax + plate_px, ay + plate_px, DARK_BLUE, LIGHT_STEEL)
    # Right coupon (after the root gap)
    bx = ax + plate_px + gap_px
    c.rect(bx, ay, bx + plate_px, ay + plate_px, DARK_BLUE, LIGHT_STEEL)
    # Root gap (weld line) between coupons
    c.fill_rect(ax + plate_px + 1, ay, bx - 1, ay + plate_px, LIGHT_ORANGE)

    # Weld direction arrow along the joint
    joint_x = ax + plate_px + gap_px // 2
    c.arrow(joint_x, ay - 18, joint_x, ay + plate_px + 18, RED, 3, 12)
    c.text(joint_x + 10, ay + plate_px // 2 - 4, "Weld direction", RED, 1)

    # Coupon dimension callouts (75 mm each side)
    draw_scale_bar(c, ax, ay + plate_px + 22, plate_px, "75 mm", GRAY)
    draw_scale_bar(c, bx, ay + plate_px + 22, plate_px, "75 mm", GRAY)
    # Root gap callout
    c.text_c(joint_x, ay - 34, "2 mm root gap", BLACK, 1)
    c.line(joint_x, ay - 22, ax + plate_px, ay - 6, BLACK, 1)
    c.line(joint_x, ay - 22, bx, ay - 6, BLACK, 1)
    # 75 mm depth (into page) callout on the left edge
    draw_scale_bar_v(c, ax - 22, ay, plate_px, "75 mm", GRAY)

    # --- (b) Side view (transverse): thickness + 4-pass deposition sequence ---
    c.text(60, 430, "(b) Transverse section - four-pass deposition", BLACK, 1)
    ppm2 = 9                       # 9 px per mm for the thickness view
    thick_mm = 12
    thick_px = thick_mm * ppm2     # 108 px
    sx = 150
    sy = 460
    seg_w = plate_px               # keep width comparable to plan view (use 300)
    # Base plate halves with square (0 degree) edges and a 2 mm root gap
    gap2 = gap_mm * ppm2           # 18 px
    c.rect(sx, sy, sx + seg_w, sy + thick_px, DARK_BLUE, LIGHT_STEEL)
    rx = sx + seg_w + gap2
    c.rect(rx, sy, rx + seg_w, sy + thick_px, DARK_BLUE, LIGHT_STEEL)

    # Fill the joint gap with 4 stacked weld passes (numbered 1-4 from root up)
    weld_x1 = sx + seg_w + 1
    weld_x2 = rx - 1
    pass_colors = [LIGHT_ORANGE, LIGHT_GOLD, LIGHT_GREEN, LIGHT_BLUE]
    n_pass = 4
    for i in range(n_pass):
        # pass 1 at the root (bottom), pass 4 at the cap (top)
        py2 = sy + thick_px - i * (thick_px // n_pass)
        py1 = sy + thick_px - (i + 1) * (thick_px // n_pass)
        if i == n_pass - 1:
            py1 = sy
        c.fill_rect(weld_x1, py1, weld_x2, py2, pass_colors[i])
        c.rect(weld_x1, py1, weld_x2, py2, GRAY)
        c.text_c((weld_x1 + weld_x2) // 2, (py1 + py2) // 2 - 3, str(i + 1), BLACK, 1)

    # Thickness callout (12 mm)
    draw_scale_bar_v(c, sx - 22, sy, thick_px, "12 mm", GRAY)
    c.text(weld_x1 - 14, sy - 12, "Passes 1-4", BLACK, 1)
    c.text(sx + 40, sy + thick_px + 20, "0 degree groove (square butt), 2 mm root gap", BLACK, 1)

    # --- Main scale bar for the plan view: 10 mm reference ---
    draw_scale_bar(c, ax + 340, ay + plate_px + 52, 10 * ppm, "10 mm (plan view scale)", BLACK)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Weld_Joint_Schematic.png'))
    print("  Figure_1_Weld_Joint_Schematic.png done")


def draw_scale_bar_v(c, x, y, length_px, label, color=BLACK):
    """Vertical scale bar with end ticks and a rotated-ish label to the left."""
    c.vline(x, y, y + length_px, color, 2)
    c.hline(x - 5, x + 5, y, color, 2)
    c.hline(x - 5, x + 5, y + length_px, color, 2)
    # label placed to the left, stacked per character (poor-man vertical text)
    ly = y + length_px // 2 - len(label) * 4
    for ch in label:
        c.text(x - 16, ly, ch, color, 1)
        ly += 8


def gen_fig2():
    """Figure 2: weld transverse cross-section with a correctly scaled bar."""
    c = PNGCanvas(820, 560)
    c.text_c(410, 12, "Weld Transverse Cross-Section (AISI 430, 12 mm plate)", BLACK, 2)

    # Scale: 30 px per mm -> a 12 mm plate is 360 px tall (a realistic macro view)
    ppm = 30
    thick_mm = 12
    thick_px = thick_mm * ppm      # 360 px
    top = 70
    bot = top + thick_px           # 430
    left = 140
    right = 680                    # ~18 mm wide field of view

    # Base metal block
    c.rect(left, top, right, bot, BLACK, LIGHT_STEEL)

    cx = (left + right) // 2

    # Fusion zone: a symmetric weld bead spanning the full thickness (V-ish profile)
    fz_half_top = 130     # half width at cap (px)
    fz_half_bot = 70      # half width at root (px)
    for y in range(top, bot + 1):
        t = (y - top) / float(thick_px)
        half = int(fz_half_top - (fz_half_top - fz_half_bot) * t)
        c.hline(cx - half, cx + half, y, LIGHT_ORANGE)
    # FZ outline
    c.line(cx - fz_half_top, top, cx - fz_half_bot, bot, RED, 2)
    c.line(cx + fz_half_top, top, cx + fz_half_bot, bot, RED, 2)

    # HAZ band on each side of the FZ (~2 mm = 60 px wide)
    haz_px = 2 * ppm
    for y in range(top, bot + 1):
        t = (y - top) / float(thick_px)
        half = int(fz_half_top - (fz_half_top - fz_half_bot) * t)
        # left HAZ
        c.hline(cx - half - haz_px, cx - half, y, LIGHT_GOLD)
        # right HAZ
        c.hline(cx + half, cx + half + haz_px, y, LIGHT_GOLD)

    # Annotations with leader lines
    c.text(cx - 16, top + thick_px // 2 - 3, "FZ", BLACK, 1)
    # HAZ label (right)
    hx = cx + (fz_half_top + fz_half_bot) // 2 + haz_px // 2
    c.arrow(right + 60, top + 60, hx, top + 80, BLACK, 1, 7)
    c.text(right + 62, top + 52, "HAZ", BLACK, 1)
    # BM label
    c.arrow(right + 60, bot - 60, right - 40, bot - 40, BLACK, 1, 7)
    c.text(right + 62, bot - 68, "BM", BLACK, 1)
    # FZ leader from left
    c.arrow(left - 70, top + 40, cx - fz_half_top + 30, top + 40, RED, 1, 7)
    c.text(left - 100, top + 32, "Fusion", RED, 1)
    c.text(left - 100, top + 44, "zone", RED, 1)

    # Legend
    lx, ly = 150, 470
    c.fill_rect(lx, ly, lx+20, ly+14, LIGHT_ORANGE); c.rect(lx, ly, lx+20, ly+14, RED)
    c.text(lx+26, ly+3, "Fusion Zone (FZ)", BLACK, 1)
    c.fill_rect(lx+200, ly, lx+220, ly+14, LIGHT_GOLD); c.rect(lx+200, ly, lx+220, ly+14, GRAY)
    c.text(lx+226, ly+3, "Heat-Affected Zone (HAZ)", BLACK, 1)
    c.fill_rect(lx+470, ly, lx+490, ly+14, LIGHT_STEEL); c.rect(lx+470, ly, lx+490, ly+14, BLACK)
    c.text(lx+496, ly+3, "Base Metal (BM)", BLACK, 1)

    # CORRECT scale bar: 5 mm = 150 px, consistent with the 12 mm plate thickness
    draw_scale_bar(c, left, bot + 24, 5 * ppm, "5 mm", BLACK)
    # Plate-thickness callout confirms scale (12 mm across the section)
    draw_scale_bar_v(c, left - 30, top, thick_px, "12 mm (plate)", GRAY)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Weld_Cross_Section.png'))
    print("  Figure_2_Weld_Cross_Section.png done")


def gen_fig3():
    """Figure 3: ASTM E23 Charpy V-notch specimen drawing."""
    c = PNGCanvas(900, 560)
    c.text_c(450, 12, "ASTM E23 Charpy V-Notch Specimen (55 x 10 x 10 mm)", BLACK, 2)

    # Scale: length 55 mm -> 12 px/mm = 660 px; cross-section 10 mm -> 120 px
    ppm = 12
    length_px = 55 * ppm       # 660
    sq_px = 10 * ppm           # 120

    # --- (a) Side (length) view with V-notch at mid-length ---
    c.text(60, 46, "(a) Side view", BLACK, 1)
    sx = 120
    sy = 80
    c.rect(sx, sy, sx + length_px, sy + sq_px, BLACK, LIGHT_STEEL)

    # V-notch at mid-length, 2 mm deep, 45 degree included angle
    notch_depth = 2 * ppm      # 24 px
    ncx = sx + length_px // 2
    half_open = int(notch_depth * math.tan(math.radians(22.5)))  # half of 45 deg
    # notch opens from the top edge downward
    c.fill_rect(ncx - half_open - 6, sy, ncx + half_open + 6, sy + 2, WHITE)  # clear top line
    c.line(ncx - half_open, sy, ncx, sy + notch_depth, BLACK, 2)
    c.line(ncx + half_open, sy, ncx, sy + notch_depth, BLACK, 2)
    # root radius indicator
    c.arc(ncx, sy + notch_depth - 3, 4, 0, math.pi, RED, 20)

    # Notch callouts
    c.text(ncx + 30, sy + 6, "45 degree notch angle", BLACK, 1)
    c.line(ncx + 26, sy + 10, ncx + half_open, sy + 4, BLACK, 1)
    c.text(ncx + 30, sy + 22, "2 mm notch depth", BLACK, 1)
    c.line(ncx + 26, sy + 26, ncx, sy + notch_depth, BLACK, 1)
    c.text(ncx - 200, sy + 40, "0.25 mm root radius", RED, 1)
    c.line(ncx - 60, sy + 42, ncx, sy + notch_depth, RED, 1)

    # Length dimension callout (55 mm)
    draw_scale_bar(c, sx, sy + sq_px + 20, length_px, "55 mm", GRAY)
    # Height dimension (10 mm)
    draw_scale_bar_v(c, sx - 22, sy, sq_px, "10 mm", GRAY)

    # --- (b) End (cross-section) view: 10 x 10 mm ---
    c.text(60, 250, "(b) End view (10 x 10 mm)", BLACK, 1)
    ex = 140
    ey = 285
    c.rect(ex, ey, ex + sq_px, ey + sq_px, BLACK, LIGHT_STEEL)
    # notch on top edge
    ecx = ex + sq_px // 2
    c.line(ecx - half_open, ey, ecx, ey + notch_depth, BLACK, 2)
    c.line(ecx + half_open, ey, ecx, ey + notch_depth, BLACK, 2)
    draw_scale_bar(c, ex, ey + sq_px + 20, sq_px, "10 mm", GRAY)
    draw_scale_bar_v(c, ex - 22, ey, sq_px, "10 mm", GRAY)

    # --- (c) Notch placement: FZ and HAZ specimens ---
    c.text(360, 250, "(c) Notch placement across the weld", BLACK, 1)
    px = 380
    py = 300
    plen = 400
    ph = 70
    # a mini weld schematic with FZ (center) + HAZ bands
    c.rect(px, py, px + plen, py + ph, BLACK, LIGHT_STEEL)
    fz_w = 80
    fzc = px + plen // 2
    c.fill_rect(fzc - fz_w//2, py, fzc + fz_w//2, py + ph, LIGHT_ORANGE)
    c.fill_rect(fzc - fz_w//2 - 26, py, fzc - fz_w//2, py + ph, LIGHT_GOLD)
    c.fill_rect(fzc + fz_w//2, py, fzc + fz_w//2 + 26, py + ph, LIGHT_GOLD)
    c.rect(px, py, px + plen, py + ph, BLACK)
    c.text_c(fzc, py + ph//2 - 3, "FZ", BLACK, 1)
    c.text_c(fzc - fz_w//2 - 13, py + ph//2 - 3, "HAZ", BLACK, 1)
    c.text_c(fzc + fz_w//2 + 13, py + ph//2 - 3, "HAZ", BLACK, 1)
    c.text(px + 6, py + 6, "BM", BLACK, 1)
    # FZ notch position (arrow down into FZ)
    c.arrow(fzc, py - 24, fzc, py - 2, RED, 2, 8)
    c.text_c(fzc, py - 36, "FZ notch", RED, 1)
    # HAZ notch position
    c.arrow(fzc + fz_w//2 + 13, py + ph + 24, fzc + fz_w//2 + 13, py + ph + 2, PURPLE, 2, 8)
    c.text_c(fzc + fz_w//2 + 13, py + ph + 28, "HAZ notch", PURPLE, 1)

    # Scale bar for the specimen views
    draw_scale_bar(c, 120, 470, 10 * ppm, "10 mm (side/end scale)", BLACK)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Charpy_Specimen.png'))
    print("  Figure_3_Charpy_Specimen.png done")


def gen_fig4():
    """Figure 4: (a) Charpy impact toughness and (b) Vickers microhardness."""
    c = PNGCanvas(940, 540)
    c.text_c(470, 12, "Mechanical Properties of the Welded Joints", BLACK, 2)

    # ---------- (a) Charpy impact toughness (J) ----------
    # Authoritative FZ dataset: 309L=125, 410=45, 2594=100
    # Illustrative HAZ values: lower than FZ, 410 lowest.
    c.text(70, 46, "(a) Charpy impact toughness", BLACK, 1)
    ax0, ay0 = 90, 90         # plot top-left
    ax_bottom = 400           # y of x-axis
    axis_h = ax_bottom - ay0  # 310
    y_max = 150.0
    # axes
    c.vline(ax0, ay0, ax_bottom, BLACK, 2)
    c.hline(ax0, 440, ax_bottom, BLACK, 2)
    # y ticks + gridlines
    for v in range(0, 151, 25):
        yy = ax_bottom - int(v / y_max * axis_h)
        c.hline(ax0 - 5, ax0, yy, BLACK)
        c.text(ax0 - 34, yy - 3, str(v), BLACK, 1)
    # y axis label (stacked)
    lbl = "Impact toughness (J)"
    lyy = ay0 + 10
    for ch in lbl:
        c.text(ax0 - 62, lyy, ch, BLACK, 1)
        lyy += 8

    fillers = ["309L", "410", "2594"]
    fz_impact = [125, 45, 100]
    haz_impact = [70, 20, 55]     # illustrative, < FZ, 410 lowest
    group_w = 100
    bar_w = 34
    for i, name in enumerate(fillers):
        gx = ax0 + 25 + i * group_w
        # FZ bar
        h1 = int(fz_impact[i] / y_max * axis_h)
        c.rect(gx, ax_bottom - h1, gx + bar_w, ax_bottom, BLACK, MED_BLUE)
        c.text_c(gx + bar_w//2, ax_bottom - h1 - 12, str(fz_impact[i]), BLACK, 1)
        # HAZ bar
        h2 = int(haz_impact[i] / y_max * axis_h)
        c.rect(gx + bar_w + 4, ax_bottom - h2, gx + 2*bar_w + 4, ax_bottom, BLACK, ORANGE)
        c.text_c(gx + bar_w + 4 + bar_w//2, ax_bottom - h2 - 12, str(haz_impact[i]), BLACK, 1)
        # x label
        c.text_c(gx + bar_w + 2, ax_bottom + 8, name, BLACK, 1)
    c.text_c(265, ax_bottom + 24, "Filler metal", BLACK, 1)
    # legend
    lx, ly = 300, 100
    c.fill_rect(lx, ly, lx+18, ly+12, MED_BLUE); c.rect(lx, ly, lx+18, ly+12, BLACK)
    c.text(lx+24, ly+2, "Fusion zone (FZ)", BLACK, 1)
    c.fill_rect(lx, ly+20, lx+18, ly+32, ORANGE); c.rect(lx, ly+20, lx+18, ly+32, BLACK)
    c.text(lx+24, ly+22, "HAZ", BLACK, 1)

    # ---------- (b) Vickers microhardness (HV) ----------
    # Authoritative FZ dataset: 410=320, 2594=300, 309L=260
    c.text(560, 46, "(b) Vickers microhardness", BLACK, 1)
    bx0, by0 = 590, 90
    bx_bottom = 400
    baxis_h = bx_bottom - by0
    hv_max = 350.0
    c.vline(bx0, by0, bx_bottom, BLACK, 2)
    c.hline(bx0, 920, bx_bottom, BLACK, 2)
    for v in range(0, 351, 50):
        yy = bx_bottom - int(v / hv_max * baxis_h)
        c.hline(bx0 - 5, bx0, yy, BLACK)
        c.text(bx0 - 40, yy - 3, str(v), BLACK, 1)
    lbl2 = "Microhardness (HV)"
    lyy = by0 + 10
    for ch in lbl2:
        c.text(bx0 - 66, lyy, ch, BLACK, 1)
        lyy += 8

    # ordered to match manuscript (410, 2594, 309L)
    hv_names = ["410", "2594", "309L"]
    fz_hv = [320, 300, 260]
    haz_hv = [250, 235, 210]     # illustrative, dropping toward base-metal level
    for i, name in enumerate(hv_names):
        gx = bx0 + 25 + i * group_w
        h1 = int(fz_hv[i] / hv_max * baxis_h)
        c.rect(gx, bx_bottom - h1, gx + bar_w, bx_bottom, BLACK, MED_GREEN)
        c.text_c(gx + bar_w//2, bx_bottom - h1 - 12, str(fz_hv[i]), BLACK, 1)
        h2 = int(haz_hv[i] / hv_max * baxis_h)
        c.rect(gx + bar_w + 4, bx_bottom - h2, gx + 2*bar_w + 4, bx_bottom, BLACK, GOLD)
        c.text_c(gx + bar_w + 4 + bar_w//2, bx_bottom - h2 - 12, str(haz_hv[i]), BLACK, 1)
        c.text_c(gx + bar_w + 2, bx_bottom + 8, name, BLACK, 1)
    c.text_c(760, bx_bottom + 24, "Filler metal", BLACK, 1)
    lx2, ly2 = 780, 100
    c.fill_rect(lx2, ly2, lx2+18, ly2+12, MED_GREEN); c.rect(lx2, ly2, lx2+18, ly2+12, BLACK)
    c.text(lx2+24, ly2+2, "Fusion zone (FZ)", BLACK, 1)
    c.fill_rect(lx2, ly2+20, lx2+18, ly2+32, GOLD); c.rect(lx2, ly2+20, lx2+18, ly2+32, BLACK)
    c.text(lx2+24, ly2+22, "HAZ", BLACK, 1)

    c.text_c(470, 470, "FZ values: impact 309L=125 J, 410=45 J, 2594=100 J; hardness 410=320, 2594=300, 309L=260 HV", GRAY, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Impact_Hardness.png'))
    print("  Figure_4_Impact_Hardness.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating SS430 manuscript figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print(f"\nFigures saved to {OUTPUT_DIR}/")
    for f in ['Figure_1_Weld_Joint_Schematic.png', 'Figure_2_Weld_Cross_Section.png',
              'Figure_3_Charpy_Specimen.png', 'Figure_4_Impact_Hardness.png']:
        p = os.path.join(OUTPUT_DIR, f)
        sz = os.path.getsize(p)
        print(f"  {f}: {sz/1024:.1f} KB")


if __name__ == '__main__':
    main()
