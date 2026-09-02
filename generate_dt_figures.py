#!/usr/bin/env python3
"""
Generate 4 scientific figures (PNG) for the chapter
"Digital Twins and Intelligent Automation for Industry 5.0".
Uses only the Python standard library (no matplotlib / PIL).

Figure 1: Layered architecture of an intelligent digital twin
Figure 2: Edge-fog-cloud computing continuum
Figure 3: Closed-loop smart manufacturing workflow
Figure 4: Three pillars of Industry 5.0 and digital twin capabilities
"""

import struct
import zlib
import math
import os

OUTPUT_DIR = '/projects/sandbox/AMMAN/dt_figures'

# ─── Palette ───
DARK_BLUE = (31, 78, 121)
MED_BLUE = (46, 117, 182)
LIGHT_BLUE = (155, 194, 230)
PALE_BLUE = (222, 235, 247)
DARK_GREEN = (56, 118, 29)
MED_GREEN = (84, 172, 64)
LIGHT_GREEN = (198, 224, 180)
PALE_GREEN = (235, 245, 228)
ORANGE = (198, 89, 17)
LIGHT_ORANGE = (248, 203, 173)
PALE_ORANGE = (252, 235, 222)
RED = (192, 0, 0)
LIGHT_RED = (248, 203, 203)
PURPLE = (112, 48, 160)
LIGHT_PURPLE = (204, 180, 220)
PALE_PURPLE = (233, 224, 242)
GOLD = (191, 144, 0)
LIGHT_GOLD = (255, 230, 153)
GRAY = (110, 110, 110)
LIGHT_GRAY = (217, 217, 217)
PALE_GRAY = (242, 242, 242)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class PNGCanvas:
    """Minimal RGB PNG canvas built on a bytearray."""

    def __init__(self, width, height, bg=(255, 255, 255)):
        self.w = width
        self.h = height
        self.data = bytearray(width * height * 3)
        for i in range(width * height):
            self.data[i * 3] = bg[0]
            self.data[i * 3 + 1] = bg[1]
            self.data[i * 3 + 2] = bg[2]

    def pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            idx = (y * self.w + x) * 3
            self.data[idx] = color[0]
            self.data[idx + 1] = color[1]
            self.data[idx + 2] = color[2]

    def fill_rect(self, x1, y1, x2, y2, color):
        x1, x2 = max(0, min(x1, x2)), min(self.w - 1, max(x1, x2))
        y1, y2 = max(0, min(y1, y2)), min(self.h - 1, max(y1, y2))
        for y in range(y1, y2 + 1):
            idx = (y * self.w + x1) * 3
            for _ in range(x1, x2 + 1):
                self.data[idx] = color[0]
                self.data[idx + 1] = color[1]
                self.data[idx + 2] = color[2]
                idx += 3

    def rect(self, x1, y1, x2, y2, outline, fill=None, thick=1):
        if fill:
            self.fill_rect(x1, y1, x2, y2, fill)
        for t in range(thick):
            for x in range(max(0, x1), min(self.w, x2 + 1)):
                self.pixel(x, y1 + t, outline)
                self.pixel(x, y2 - t, outline)
            for y in range(max(0, y1), min(self.h, y2 + 1)):
                self.pixel(x1 + t, y, outline)
                self.pixel(x2 - t, y, outline)

    def round_panel(self, x1, y1, x2, y2, outline, fill):
        """A rectangle with visually clipped corners for a softer look."""
        self.fill_rect(x1 + 3, y1, x2 - 3, y2, fill)
        self.fill_rect(x1, y1 + 3, x2, y2 - 3, fill)
        self.rect(x1 + 3, y1, x2 - 3, y1, outline)
        self.rect(x1 + 3, y2, x2 - 3, y2, outline)
        for y in range(y1 + 3, y2 - 2):
            self.pixel(x1, y, outline)
            self.pixel(x2, y, outline)
        for x in range(x1 + 3, x2 - 2):
            self.pixel(x, y1, outline)
            self.pixel(x, y2, outline)

    def hline(self, x1, x2, y, color, thick=1):
        for t in range(thick):
            xx1, xx2 = max(0, min(x1, x2)), min(self.w - 1, max(x1, x2))
            for x in range(xx1, xx2 + 1):
                self.pixel(x, y + t, color)

    def vline(self, x, y1, y2, color, thick=1):
        for t in range(thick):
            yy1, yy2 = max(0, min(y1, y2)), min(self.h - 1, max(y1, y2))
            for y in range(yy1, yy2 + 1):
                self.pixel(x + t, y, color)

    def line(self, x1, y1, x2, y2, color, thick=1):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
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
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def arrow(self, x1, y1, x2, y2, color, thick=2, hs=9):
        self.line(x1, y1, x2, y2, color, thick)
        angle = math.atan2(y2 - y1, x2 - x1)
        for a_off in [0.5, -0.5]:
            ax = int(x2 - hs * math.cos(angle - a_off))
            ay = int(y2 - hs * math.sin(angle - a_off))
            self.line(x2, y2, ax, ay, color, thick)

    def circle(self, cx, cy, r, color, fill=None):
        if fill:
            for y in range(-r, r + 1):
                span = int(math.sqrt(max(0, r * r - y * y)))
                self.hline(cx - span, cx + span, cy + y, fill)
        x, y = r, 0
        err = 1 - r
        while x >= y:
            for px, py in [(cx + x, cy + y), (cx - x, cy + y), (cx + x, cy - y),
                           (cx - x, cy - y), (cx + y, cy + x), (cx - y, cy + x),
                           (cx + y, cy - x), (cx - y, cy - x)]:
                self.pixel(px, py, color)
            y += 1
            if err < 0:
                err += 2 * y + 1
            else:
                x -= 1
                err += 2 * (y - x) + 1

    def text(self, x, y, s, color, scale=1):
        for ch in s:
            bm = _FONT.get(ch)
            if bm is None:
                x += 6 * scale
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


# ─── Minimal 5x7 bitmap font ───
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
    '.': [0, 0, 0, 0, 0, 0b01100, 0b01100],
    ',': [0, 0, 0, 0, 0b01100, 0b00100, 0b01000],
    ':': [0, 0b01100, 0b01100, 0, 0b01100, 0b01100, 0],
    '-': [0, 0, 0, 0b11111, 0, 0, 0],
    '+': [0, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0],
    '/': [0b00001, 0b00010, 0b00010, 0b00100, 0b01000, 0b01000, 0b10000],
    '(': [0b00010, 0b00100, 0b01000, 0b01000, 0b01000, 0b00100, 0b00010],
    ')': [0b01000, 0b00100, 0b00010, 0b00010, 0b00010, 0b00100, 0b01000],
    '&': [0b01100, 0b10010, 0b10100, 0b01000, 0b10101, 0b10010, 0b01101],
    '%': [0b11001, 0b11001, 0b00010, 0b00100, 0b01000, 0b10011, 0b10011],
    '>': [0b10000, 0b01000, 0b00100, 0b00010, 0b00100, 0b01000, 0b10000],
    '<': [0b00001, 0b00010, 0b00100, 0b01000, 0b00100, 0b00010, 0b00001],
    '=': [0, 0, 0b11111, 0, 0b11111, 0, 0],
    '[': [0b01110, 0b01000, 0b01000, 0b01000, 0b01000, 0b01000, 0b01110],
    ']': [0b01110, 0b00010, 0b00010, 0b00010, 0b00010, 0b00010, 0b01110],
}


def _caption(c, text_str):
    c.text_c(c.w // 2, c.h - 22, text_str, BLACK, 1)


def gen_fig1():
    """Figure 1: Layered architecture of an intelligent digital twin."""
    c = PNGCanvas(760, 560)
    c.text_c(380, 14, "Layered Architecture of an Intelligent Digital Twin", DARK_BLUE, 2)

    layers = [
        ("SERVICE & CLOSED-LOOP CONTROL LAYER", 60, PALE_ORANGE, ORANGE,
         ["Dashboards, alerts, autonomous control loops, actuator commands"]),
        ("DIGITAL TWIN INTELLIGENCE LAYER", 160, PALE_PURPLE, PURPLE,
         ["Physics-based + data-driven models  |  AI / ML analytics",
          "Monitoring - Prediction - Prescription"]),
        ("CONNECTIVITY LAYER", 300, PALE_GREEN, DARK_GREEN,
         ["IoT protocols, time-sensitive networking, 5G, data pipelines"]),
        ("PHYSICAL ASSET LAYER", 400, PALE_BLUE, DARK_BLUE,
         ["Sensors - Actuators - Edge devices - Machines - Products"]),
    ]
    lx1, lx2 = 150, 610
    for title, y, fill, outline, lines in layers:
        h = 90 if len(lines) > 1 else 70
        c.round_panel(lx1, y, lx2, y + h, outline, fill)
        c.text_c((lx1 + lx2) // 2, y + 10, title, outline, 1)
        for i, ln in enumerate(lines):
            c.text_c((lx1 + lx2) // 2, y + 32 + i * 16, ln, BLACK, 1)

    # Up arrows (physical -> intelligence): data flow
    c.arrow(250, 400, 250, 250, MED_GREEN, 3, 10)
    c.text(255, 384, "data up", MED_GREEN, 1)
    # Down arrows (control commands)
    c.arrow(510, 250, 510, 400, ORANGE, 3, 10)
    c.text(430, 384, "control down", ORANGE, 1)
    # Intelligence <-> Service coupling
    c.arrow(380, 250, 380, 150, PURPLE, 2, 8)
    c.arrow(400, 150, 400, 250, ORANGE, 2, 8)

    # Human oversight side panel
    c.round_panel(632, 160, 752, 300, GOLD, LIGHT_GOLD)
    c.text_c(692, 172, "HUMAN", BLACK, 1)
    c.text_c(692, 188, "OVERSIGHT", BLACK, 1)
    c.text_c(692, 214, "Supervise", BLACK, 1)
    c.text_c(692, 230, "Override", BLACK, 1)
    c.text_c(692, 246, "Ethics &", BLACK, 1)
    c.text_c(692, 262, "strategy", BLACK, 1)
    c.arrow(632, 210, 610, 205, GOLD, 2, 7)

    # Physical <-> Virtual synchronization label
    c.round_panel(8, 200, 120, 300, MED_BLUE, PALE_BLUE)
    c.text_c(64, 214, "Physical-", BLACK, 1)
    c.text_c(64, 230, "Virtual", BLACK, 1)
    c.text_c(64, 246, "Sync", BLACK, 1)
    c.text_c(64, 268, "(bi-", BLACK, 1)
    c.text_c(64, 284, "directional)", BLACK, 1)

    _caption(c, "Figure 1. Layered architecture of an intelligent digital twin with bidirectional data-control flow.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_DT_Architecture.png'))
    print("  Figure_1_DT_Architecture.png done")


def gen_fig2():
    """Figure 2: Edge-fog-cloud computing continuum."""
    c = PNGCanvas(780, 520)
    c.text_c(390, 14, "Edge-Fog-Cloud Computing Continuum for Digital Twins", DARK_BLUE, 2)

    # Three tiers as vertical bands
    tiers = [
        (60, 250, PALE_BLUE, DARK_BLUE, "EDGE", "Near the asset",
         ["Safety interlocks", "Real-time control", "Local anomaly detect", "Latency: us - ms"]),
        (280, 500, PALE_GREEN, DARK_GREEN, "FOG", "Intermediate tier",
         ["Aggregation", "Multi-node analytics", "Local optimization", "Latency: ms - s"]),
        (520, 730, PALE_PURPLE, PURPLE, "CLOUD", "Central resources",
         ["Model training", "Cross-site data", "Long-term storage", "Latency: s - min"]),
    ]
    top, bot = 70, 380
    for x1, x2, fill, outline, name, sub, items in tiers:
        c.round_panel(x1, top, x2, bot, outline, fill)
        c.text_c((x1 + x2) // 2, top + 14, name, outline, 2)
        c.text_c((x1 + x2) // 2, top + 40, sub, BLACK, 1)
        for i, it in enumerate(items):
            c.text_c((x1 + x2) // 2, top + 70 + i * 26, it, BLACK, 1)

    # Arrows between tiers (data up, decisions down)
    c.arrow(255, 150, 275, 150, MED_GREEN, 3, 9)
    c.text(180, 130, "data up", MED_GREEN, 1)
    c.arrow(500, 150, 520, 150, MED_GREEN, 3, 9)
    c.arrow(520, 300, 500, 300, ORANGE, 3, 9)
    c.text(430, 315, "decisions", ORANGE, 1)
    c.arrow(275, 300, 255, 300, ORANGE, 3, 9)

    # Gradient bars: latency and compute
    c.text(60, 420, "Latency & data volume increase toward the cloud  ->", BLACK, 1)
    c.arrow(60, 445, 720, 445, MED_BLUE, 2, 9)
    c.text(60, 460, "Compute power & storage increase toward the cloud  ->", BLACK, 1)
    c.text(430, 480, "<-  Real-time responsiveness increases toward the edge", BLACK, 1)

    _caption(c, "Figure 2. The edge-fog-cloud continuum distributes computation across latency and resource tiers.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Edge_Cloud_Continuum.png'))
    print("  Figure_2_Edge_Cloud_Continuum.png done")


def gen_fig3():
    """Figure 3: Closed-loop smart manufacturing workflow."""
    c = PNGCanvas(720, 560)
    c.text_c(360, 14, "Closed-Loop Smart Manufacturing Workflow", DARK_BLUE, 2)

    cx, cy = 360, 300
    # Center: digital twin hub
    c.circle(cx, cy, 78, DARK_BLUE, PALE_BLUE)
    c.text_c(cx, cy - 18, "FACTORY", DARK_BLUE, 2)
    c.text_c(cx, cy + 2, "DIGITAL", DARK_BLUE, 2)
    c.text_c(cx, cy + 22, "TWIN", DARK_BLUE, 2)

    # Four stages around the cycle
    nodes = [
        ("PLAN", "Simulate & optimize\nschedules", cx, 90, MED_BLUE, LIGHT_BLUE),
        ("EXECUTE", "Dispatch to\nmachines & robots", 590, cy, MED_GREEN, LIGHT_GREEN),
        ("SENSE", "Collect real-time\nshop-floor data", cx, 500, ORANGE, LIGHT_ORANGE),
        ("ADAPT", "Reschedule &\nreoptimize", 130, cy, PURPLE, LIGHT_PURPLE),
    ]
    positions = []
    for title, desc, nx, ny, outline, fill in nodes:
        w, h = 150, 74
        c.round_panel(nx - w // 2, ny - h // 2, nx + w // 2, ny + h // 2, outline, fill)
        c.text_c(nx, ny - 24, title, outline, 2)
        for i, ln in enumerate(desc.split('\n')):
            c.text_c(nx, ny - 2 + i * 15, ln, BLACK, 1)
        positions.append((nx, ny))

    # Clockwise arrows between the four nodes
    order = [0, 1, 2, 3, 0]
    for a, b in zip(order, order[1:]):
        x1, y1 = positions[a]
        x2, y2 = positions[b]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        ox1, oy1 = int(x1 + dx / d * 80), int(y1 + dy / d * 50)
        ox2, oy2 = int(x2 - dx / d * 80), int(y2 - dy / d * 50)
        c.arrow(ox1, oy1, ox2, oy2, GRAY, 3, 10)

    # Spokes to the twin hub
    for nx, ny in positions:
        dx, dy = cx - nx, cy - ny
        d = math.hypot(dx, dy)
        c.line(int(nx + dx / d * 40), int(ny + dy / d * 40),
               int(cx - dx / d * 82), int(cy - dy / d * 82), LIGHT_GRAY, 1)

    c.text_c(360, 360, "Continuous feedback", GRAY, 1)
    c.text_c(360, 375, "keeps plan aligned", GRAY, 1)

    _caption(c, "Figure 3. Closed-loop smart manufacturing workflow mediated by the factory digital twin.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Manufacturing_Workflow.png'))
    print("  Figure_3_Manufacturing_Workflow.png done")


def gen_fig4():
    """Figure 4: Three pillars of Industry 5.0 and digital twin capabilities."""
    c = PNGCanvas(780, 540)
    c.text_c(390, 14, "Three Pillars of Industry 5.0 Served by Digital Twins", DARK_BLUE, 2)

    pillars = [
        ("HUMAN-CENTRICITY", 60, 260, MED_BLUE, PALE_BLUE,
         ["Worker assistance", "AR guidance", "Ergonomic modeling", "Augmented intelligence"]),
        ("SUSTAINABILITY", 280, 500, DARK_GREEN, PALE_GREEN,
         ["Energy optimization", "Carbon-aware control", "Circular production", "Life-cycle tracking"]),
        ("RESILIENCE", 520, 720, PURPLE, PALE_PURPLE,
         ["Predictive maintenance", "Supply-chain twins", "Disruption simulation", "Rapid adaptation"]),
    ]
    top, bot = 70, 330
    centers = []
    for name, x1, x2, outline, fill, items in pillars:
        c.round_panel(x1, top, x2, bot, outline, fill)
        # pillar "column" styling
        c.fill_rect(x1 + 6, top + 30, x2 - 6, top + 32, outline)
        c.text_c((x1 + x2) // 2, top + 10, name, outline, 1)
        for i, it in enumerate(items):
            c.text_c((x1 + x2) // 2, top + 55 + i * 34, it, BLACK, 1)
        centers.append(((x1 + x2) // 2, bot))

    # Base: digital twin foundation
    c.round_panel(60, 380, 720, 440, DARK_BLUE, PALE_BLUE)
    c.text_c(390, 396, "DIGITAL TWIN + INTELLIGENT AUTOMATION FOUNDATION", DARK_BLUE, 1)
    c.text_c(390, 416, "IoT - Cyber-physical systems - AI/ML - Edge/Cloud computing", BLACK, 1)
    for cxp, cyp in centers:
        c.arrow(cxp, 380, cxp, 335, GRAY, 2, 8)

    # Mutual reinforcement arcs (double arrows between pillars)
    c.arrow(255, 200, 285, 200, GOLD, 2, 8)
    c.arrow(285, 220, 255, 220, GOLD, 2, 8)
    c.arrow(495, 200, 525, 200, GOLD, 2, 8)
    c.arrow(525, 220, 495, 220, GOLD, 2, 8)
    c.text_c(390, 460, "Mutually reinforcing pillars built on a shared digital twin foundation", GRAY, 1)

    _caption(c, "Figure 4. The three pillars of Industry 5.0 and the digital twin capabilities that support each.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Industry5_Pillars.png'))
    print("  Figure_4_Industry5_Pillars.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating digital twin chapter figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print(f"\nAll 4 figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz / 1024:.1f} KB")


if __name__ == '__main__':
    main()
