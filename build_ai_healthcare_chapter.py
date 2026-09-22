#!/usr/bin/env python3
"""
Build the "AI in Personalized Healthcare" book chapter.

1. Generates 4 schematic figures (PNG) using a pure-stdlib canvas.
2. Builds a Word .docx from Chapter_AI_Personalized_Healthcare.md with the
   figures EMBEDDED inline, tables rendered as real Word tables, styled
   headings, captions and a hanging-indent reference list.

No third-party libraries are required (no matplotlib / PIL / python-docx).
"""

import os
import re
import struct
import zlib
import zipfile
import math

BASE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(BASE, 'healthcare_figures')
MD_FILE = os.path.join(BASE, 'Chapter_AI_Personalized_Healthcare.md')
DOCX_FILE = os.path.join(BASE, 'Chapter_AI_Personalized_Healthcare.docx')

# ============================================================
# Palette
# ============================================================
DARK_BLUE = (31, 78, 121); MED_BLUE = (46, 117, 182); LIGHT_BLUE = (189, 215, 238)
PALE_BLUE = (222, 235, 247); DARK_GREEN = (56, 118, 29); MED_GREEN = (112, 173, 71)
LIGHT_GREEN = (198, 224, 180); ORANGE = (197, 90, 17); LIGHT_ORANGE = (248, 203, 173)
RED = (192, 0, 0); LIGHT_RED = (248, 206, 204); PURPLE = (112, 48, 160)
LIGHT_PURPLE = (204, 180, 220); GOLD = (191, 143, 0); LIGHT_GOLD = (255, 230, 153)
TEAL = (0, 130, 130); LIGHT_TEAL = (183, 222, 222); GRAY = (110, 110, 110)
LIGHT_GRAY = (222, 222, 222); BLACK = (0, 0, 0); WHITE = (255, 255, 255)


# ============================================================
# Part 1: Pure-stdlib PNG canvas (adapted from generate_figures.py)
# ============================================================
class PNGCanvas:
    def __init__(self, width, height, bg=(255, 255, 255)):
        self.w = width
        self.h = height
        self.data = bytearray(width * height * 3)
        for i in range(width * height):
            self.data[i*3] = bg[0]; self.data[i*3+1] = bg[1]; self.data[i*3+2] = bg[2]

    def pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            idx = (y * self.w + x) * 3
            self.data[idx] = color[0]; self.data[idx+1] = color[1]; self.data[idx+2] = color[2]

    def fill_rect(self, x1, y1, x2, y2, color):
        x1, x2 = max(0, min(x1, x2)), min(self.w-1, max(x1, x2))
        y1, y2 = max(0, min(y1, y2)), min(self.h-1, max(y1, y2))
        for y in range(y1, y2+1):
            idx = (y * self.w + x1) * 3
            for x in range(x1, x2+1):
                self.data[idx] = color[0]; self.data[idx+1] = color[1]; self.data[idx+2] = color[2]
                idx += 3

    def rect(self, x1, y1, x2, y2, outline, fill=None, thick=1):
        if fill:
            self.fill_rect(x1, y1, x2, y2, fill)
        for t in range(thick):
            for x in range(max(0, x1), min(self.w, x2+1)):
                self.pixel(x, y1+t, outline); self.pixel(x, y2-t, outline)
            for y in range(max(0, y1), min(self.h, y2+1)):
                self.pixel(x1+t, y, outline); self.pixel(x2-t, y, outline)

    def hline(self, x1, x2, y, color):
        if y < 0 or y >= self.h:
            return
        x1, x2 = max(0, min(x1, x2)), min(self.w-1, max(x1, x2))
        idx = (y * self.w + x1) * 3
        for x in range(x1, x2+1):
            self.data[idx] = color[0]; self.data[idx+1] = color[1]; self.data[idx+2] = color[2]
            idx += 3

    def vline(self, x, y1, y2, color):
        if x < 0 or x >= self.w:
            return
        y1, y2 = max(0, min(y1, y2)), min(self.h-1, max(y1, y2))
        for y in range(y1, y2+1):
            idx = (y * self.w + x) * 3
            self.data[idx] = color[0]; self.data[idx+1] = color[1]; self.data[idx+2] = color[2]

    def line(self, x1, y1, x2, y2, color, thick=1):
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

    def arrow(self, x1, y1, x2, y2, color, thick=2, hs=9):
        self.line(x1, y1, x2, y2, color, thick)
        angle = math.atan2(y2-y1, x2-x1)
        for a_off in [2.6, -2.6]:
            ax = int(x2 - hs * math.cos(angle - a_off * 0.16))
            ay = int(y2 - hs * math.sin(angle - a_off * 0.16))
            self.line(x2, y2, ax, ay, color, thick)

    def round_panel(self, x1, y1, x2, y2, outline, fill):
        """Filled rectangle with clipped corners for a softer look."""
        self.fill_rect(x1+2, y1, x2-2, y2, fill)
        self.fill_rect(x1, y1+2, x2, y2-2, fill)
        for x in range(x1+2, x2-1):
            self.pixel(x, y1, outline); self.pixel(x, y2, outline)
        for y in range(y1+2, y2-1):
            self.pixel(x1, y, outline); self.pixel(x2, y, outline)
        # corners
        for (cx, cy) in [(x1+1, y1+1), (x2-1, y1+1), (x1+1, y2-1), (x2-1, y2-1)]:
            self.pixel(cx, cy, outline)

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
    ' ':[0,0,0,0,0,0,0],
    '.':[0,0,0,0,0,0b01100,0b01100], ',':[0,0,0,0,0b01100,0b00100,0b01000],
    ':':[0,0b01100,0b01100,0,0b01100,0b01100,0], '-':[0,0,0,0b11111,0,0,0],
    '+':[0,0b00100,0b00100,0b11111,0b00100,0b00100,0], '/':[0b00001,0b00010,0b00010,0b00100,0b01000,0b01000,0b10000],
    '(':[0b00010,0b00100,0b01000,0b01000,0b01000,0b00100,0b00010], ')':[0b01000,0b00100,0b00010,0b00010,0b00010,0b00100,0b01000],
    '&':[0b01100,0b10010,0b10100,0b01000,0b10101,0b10010,0b01101], '>':[0b10000,0b01000,0b00100,0b00010,0b00100,0b01000,0b10000],
    '<':[0b00001,0b00010,0b00100,0b01000,0b00100,0b00010,0b00001], '=':[0,0,0b11111,0,0b11111,0,0],
    '_':[0,0,0,0,0,0,0b11111], "'":[0b00100,0b00100,0b01000,0,0,0,0],
}


# ============================================================
# Part 2: The four figures
# ============================================================
def _title(c, s):
    c.text_c(c.w//2, 12, s, DARK_BLUE, 2)
    c.hline(60, c.w-60, 34, LIGHT_GRAY)


def _box(c, x, y, w, h, outline, fill, lines, tcol=BLACK, scale=1, header=None):
    c.round_panel(x, y, x+w, y+h, outline, fill)
    n = len(lines)
    total = n * (8*scale + 3)
    ty = y + (h - total)//2 + 2
    for ln in lines:
        c.text_c(x+w//2, ty, ln, tcol, scale)
        ty += 8*scale + 3


def gen_fig1():
    """Conceptual framework: data -> techniques -> applications with feedback."""
    c = PNGCanvas(920, 600)
    _title(c, "AI in Personalized Healthcare: An Integrative Framework")

    # Column headers
    col_x = [40, 360, 680]
    col_w = 200
    heads = [("BIOMEDICAL DATA", DARK_BLUE, PALE_BLUE),
             ("AI TECHNIQUES", DARK_GREEN, LIGHT_GREEN),
             ("CLINICAL APPLICATIONS", ORANGE, LIGHT_ORANGE)]
    for i, (h, oc, fc) in enumerate(heads):
        c.round_panel(col_x[i], 52, col_x[i]+col_w, 82, oc, fc)
        c.text_c(col_x[i]+col_w//2, 62, h, oc, 1)

    data_items = ["Genomics / Omics", "Medical Imaging", "Electronic Records",
                  "Wearables / IoMT", "Lifestyle Data"]
    tech_items = ["Machine Learning", "Deep Learning", "NLP",
                  "Computer Vision", "Reinforcement L.", "Generative AI"]
    app_items = ["Prevention", "Diagnosis", "Prognosis",
                 "Treatment Planning", "Disease Mgmt."]

    def col(items, x, oc, fc):
        y = 100
        bh = 46
        gap = 8
        centers = []
        for it in items:
            c.round_panel(x, y, x+col_w, y+bh, oc, fc)
            c.text_c(x+col_w//2, y+bh//2-3, it, BLACK, 1)
            centers.append((x, y+bh//2, x+col_w, y+bh//2))
            y += bh + gap
        return centers

    dc = col(data_items, col_x[0], MED_BLUE, PALE_BLUE)
    tc = col(tech_items, col_x[1], MED_GREEN, LIGHT_GREEN)
    ac = col(app_items, col_x[2], ORANGE, LIGHT_ORANGE)

    # Bundled arrows between columns
    for (_, y, xr, _) in dc:
        c.arrow(xr+2, y, col_x[1]-2, 150 + ((y-123)//10), MED_BLUE, 1, 6)
    for (xl, y, _, _) in tc:
        c.arrow(col_x[1]+col_w+2, y, col_x[2]-2, 150 + ((y-123)//10), MED_GREEN, 1, 6)

    # Feedback loop arrow along the bottom (applications -> data)
    c.arrow(col_x[2]+col_w//2, 452, col_x[2]+col_w//2, 520, GOLD, 2, 8)
    c.hline(col_x[0]+col_w//2, col_x[2]+col_w//2, 520, GOLD)
    c.vline(col_x[0]+col_w//2, 470, 520, GOLD)
    c.arrow(col_x[0]+col_w//2, 490, col_x[0]+col_w//2, 452, GOLD, 2, 8)
    c.round_panel(360, 505, 560, 535, GOLD, LIGHT_GOLD)
    c.text_c(460, 515, "Continuous Feedback Loop", GOLD, 1)

    c.text_c(c.w//2, 566, "Figure 1. Data sources feed AI techniques that drive applications across the care continuum.", GRAY, 1)
    c.save(os.path.join(FIG_DIR, 'Figure_1_Framework.png'))
    print("  Figure_1_Framework.png")


def gen_fig2():
    """Continuum of care: five stages with progression and feedback."""
    c = PNGCanvas(920, 430)
    _title(c, "AI Across the Continuum of Care")

    stages = [("PREVENTION", ["Risk prediction", "Biomarkers", "Screening"], MED_BLUE, PALE_BLUE),
              ("DIAGNOSIS", ["Imaging AI", "Decision support", "Radiomics"], TEAL, LIGHT_TEAL),
              ("PROGNOSIS", ["Outcome", "Trajectory", "Survival"], MED_GREEN, LIGHT_GREEN),
              ("TREATMENT", ["Pharmaco-", "genomics", "Therapy match"], ORANGE, LIGHT_ORANGE),
              ("MANAGEMENT", ["Monitoring", "Adaptation", "Follow-up"], PURPLE, LIGHT_PURPLE)]
    n = len(stages)
    bw = 150; bh = 130; gap = (c.w - 40 - n*bw)//(n-1)
    x = 20; y = 90
    centers = []
    for i, (h, items, oc, fc) in enumerate(stages):
        c.round_panel(x, y, x+bw, y+bh, oc, fc)
        c.round_panel(x, y, x+bw, y+26, oc, oc)
        c.text_c(x+bw//2, y+9, h, WHITE, 1)
        ty = y+38
        for it in items:
            c.text_c(x+bw//2, ty, it, BLACK, 1)
            ty += 16
        centers.append((x+bw, y+bh//2, x, y+bh//2, x+bw//2))
        if i < n-1:
            nx = x+bw+gap
            c.arrow(x+bw+3, y+bh//2, nx-3, y+bh//2, GRAY, 3, 10)
        x += bw + gap

    # Feedback arrow from Management back to Prevention (data feedback)
    x0 = centers[0][4]; x4 = centers[-1][4]
    c.vline(x4, y+bh, y+bh+55, GOLD)
    c.hline(x0, x4, y+bh+55, GOLD)
    c.vline(x0, y+bh, y+bh+55, GOLD)
    c.arrow(x0, y+bh+30, x0, y+bh+3, GOLD, 2, 8)
    c.text_c(c.w//2, y+bh+40, "Continuous data feedback enables adaptive, personalized care", GOLD, 1)

    c.text_c(c.w//2, 400, "Figure 2. AI capabilities distributed across successive, interconnected phases of care.", GRAY, 1)
    c.save(os.path.join(FIG_DIR, 'Figure_2_Continuum.png'))
    print("  Figure_2_Continuum.png")


def gen_fig3():
    """IoMT / RPM layered ecosystem."""
    c = PNGCanvas(920, 540)
    _title(c, "AI-Enabled IoMT and Remote Patient Monitoring Ecosystem")

    layers = [
        ("PATIENT & SENSOR LAYER", ["Wearables", "Implantables", "Home sensors", "Smartphone"], MED_BLUE, PALE_BLUE),
        ("EDGE LAYER", ["Local pre-processing", "Signal filtering", "Low-latency alerts"], TEAL, LIGHT_TEAL),
        ("CLOUD AI LAYER", ["Data integration", "ML / DL models", "Anomaly detection", "Prediction"], DARK_GREEN, LIGHT_GREEN),
        ("CLINICAL DECISION LAYER", ["Clinician dashboards", "Prioritized alerts", "Personalized plan"], ORANGE, LIGHT_ORANGE),
    ]
    y = 56; lh = 92; gap = 18; x1 = 60; x2 = c.w-60
    mids = []
    for h, items, oc, fc in layers:
        c.round_panel(x1, y, x2, y+lh, oc, fc)
        c.round_panel(x1, y, x1+220, y+lh, oc, oc)
        # header vertical-ish label
        c.text_c(x1+110, y+lh//2-4, h, WHITE, 1)
        # items across
        iw = (x2 - (x1+240)) // len(items)
        ix = x1+240
        for it in items:
            c.round_panel(ix+6, y+18, ix+iw-6, y+lh-18, oc, WHITE)
            c.text_c(ix+iw//2, y+lh//2-3, it, BLACK, 1)
            ix += iw
        mids.append((y, y+lh))
        y += lh + gap

    # down arrows (data up->processed down)
    cx = c.w//2
    for i in range(len(layers)-1):
        c.arrow(cx-120, mids[i][1]+2, cx-120, mids[i+1][0]-2, MED_BLUE, 2, 8)
    # feedback up arrow (interventions back to patient)
    for i in range(len(layers)-1, 0, -1):
        c.arrow(cx+120, mids[i][0]-2, cx+120, mids[i-1][1]+2, ORANGE, 2, 8)
    c.text(cx-190, 500, "Data flow (bottom-up)", MED_BLUE, 1)
    c.text(cx+40, 500, "Feedback / intervention (top-down)", ORANGE, 1)

    c.text_c(c.w//2, 522, "Figure 3. Closed-loop flow from sensors through edge and cloud analytics to clinical action.", GRAY, 1)
    c.save(os.path.join(FIG_DIR, 'Figure_3_IoMT.png'))
    print("  Figure_3_IoMT.png")


def gen_fig4():
    """Four emerging enablers around a central hub."""
    c = PNGCanvas(920, 600)
    _title(c, "Emerging Enablers of Trustworthy Precision Medicine")

    cx, cy = c.w//2, 310
    # central hub
    c.round_panel(cx-115, cy-45, cx+115, cy+45, DARK_BLUE, PALE_BLUE)
    c.text_c(cx, cy-14, "TRUSTWORTHY", DARK_BLUE, 2)
    c.text_c(cx, cy+8, "PRECISION MEDICINE", DARK_BLUE, 1)

    quad = [
        ("MULTIMODAL INTEGRATION", ["Fuse imaging, omics,", "clinical & sensor data", "-> higher accuracy"], MED_GREEN, LIGHT_GREEN, cx-360, cy-200),
        ("EXPLAINABLE AI (XAI)", ["Transparent reasoning", "Feature attribution", "-> clinician trust"], ORANGE, LIGHT_ORANGE, cx+70, cy-200),
        ("DIGITAL TWINS", ["Virtual patient replica", "In-silico simulation", "-> personalized planning"], PURPLE, LIGHT_PURPLE, cx-360, cy+110),
        ("FEDERATED LEARNING", ["Train without sharing", "raw data + privacy", "-> secure collaboration"], TEAL, LIGHT_TEAL, cx+70, cy+110),
    ]
    bw, bh = 290, 92
    for h, items, oc, fc, x, y in quad:
        c.round_panel(x, y, x+bw, y+bh, oc, fc)
        c.round_panel(x, y, x+bw, y+24, oc, oc)
        c.text_c(x+bw//2, y+8, h, WHITE, 1)
        ty = y+32
        for it in items:
            c.text_c(x+bw//2, ty, it, BLACK, 1)
            ty += 16
    # explicit connectors
    c.arrow(cx-215, cy-154, cx-95, cy-30, MED_GREEN, 2, 8)
    c.arrow(cx+215, cy-154, cx+95, cy-30, ORANGE, 2, 8)
    c.arrow(cx-215, cy+156, cx-95, cy+32, PURPLE, 2, 8)
    c.arrow(cx+215, cy+156, cx+95, cy+32, TEAL, 2, 8)

    c.text_c(c.w//2, 566, "Figure 4. Four interlocking enablers advancing accuracy, transparency, personalization and privacy.", GRAY, 1)
    c.save(os.path.join(FIG_DIR, 'Figure_4_Enablers.png'))
    print("  Figure_4_Enablers.png")


def create_figures():
    os.makedirs(FIG_DIR, exist_ok=True)
    print("Generating figures...")
    gen_fig1(); gen_fig2(); gen_fig3(); gen_fig4()


# ============================================================
# Part 3: DOCX generation (OOXML) with embedded images
# ============================================================
# Map figure number -> (filename, pixel width, pixel height)
FIGURES = {
    1: ('Figure_1_Framework.png', 920, 600),
    2: ('Figure_2_Continuum.png', 920, 430),
    3: ('Figure_3_IoMT.png', 920, 540),
    4: ('Figure_4_Enablers.png', 920, 600),
}
EMU_PER_PX = 9525
MAX_WIDTH_EMU = int(6.3 * 914400)  # ~6.3 inch content width

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults><w:rPrDefault><w:rPr>
    <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
    <w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1"><w:name w:val="Normal"/><w:pPr><w:jc w:val="both"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="120"/></w:pPr><w:rPr><w:b/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="60"/></w:pPr><w:rPr><w:sz w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="25"/><w:szCs w:val="25"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Abstract"><w:name w:val="Abstract"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:right="480"/></w:pPr><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="References"><w:name w:val="References"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="240"/></w:pPr><w:rPr><w:i/><w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption"><w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="180" w:after="60"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="ImagePara"><w:name w:val="ImagePara"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="0"/></w:pPr></w:style>
</w:styles>'''


def escape_xml(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


def make_run(text, bold=False, italic=False, sz=None, sup=False):
    props = []
    if bold: props.append('<w:b/>')
    if italic: props.append('<w:i/>')
    if sup: props.append('<w:vertAlign w:val="superscript"/>')
    if sz: props.append(f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
    rpr = ('<w:rPr>' + ''.join(props) + '</w:rPr>') if props else ''
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'


def parse_inline(text):
    """Handle **bold**, *italic*, and ^(superscript)."""
    # superscript first: ^(...)
    runs = []
    token = re.compile(r'(\*\*.*?\*\*|\*[^*]+?\*|\^\([^)]*\))')
    for part in token.split(text):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            runs.append(make_run(part[2:-2], bold=True))
        elif part.startswith('*') and part.endswith('*'):
            runs.append(make_run(part[1:-1], italic=True))
        elif part.startswith('^(') and part.endswith(')'):
            runs.append(make_run(part[2:-1], sup=True))
        else:
            runs.append(make_run(part))
    return ''.join(runs)


def para(text, style='Normal'):
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{parse_inline(text)}</w:p>'


def image_paragraph(fig_num, rel_id):
    fname, pw, ph = FIGURES[fig_num]
    cx = min(pw * EMU_PER_PX, MAX_WIDTH_EMU)
    cy = int(cx * ph / pw)
    drawing = f'''<w:p><w:pPr><w:pStyle w:val="ImagePara"/></w:pPr><w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0">
<wp:extent cx="{cx}" cy="{cy}"/>
<wp:effectExtent l="0" t="0" r="0" b="0"/>
<wp:docPr id="{fig_num}" name="Figure{fig_num}"/>
<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>
<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:nvPicPr><pic:cNvPr id="{fig_num}" name="{fname}"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed="{rel_id}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''
    return drawing


def make_table(headers, rows):
    n = len(headers)
    total = 9200
    col_w = total // n
    tbl = ['<w:tbl>']
    tbl.append('<w:tblPr><w:tblW w:w="%d" w:type="dxa"/><w:tblLayout w:type="fixed"/>' % total)
    tbl.append('<w:tblBorders>' + ''.join(
        f'<w:{e} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV')) + '</w:tblBorders></w:tblPr>')
    tbl.append('<w:tblGrid>' + f'<w:gridCol w:w="{col_w}"/>' * n + '</w:tblGrid>')
    # header
    tbl.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
    for h in headers:
        tbl.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="1F4E79"/><w:vAlign w:val="center"/></w:tcPr>' % col_w)
        hrun = (f'<w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
                f'<w:t xml:space="preserve">{escape_xml(h.strip())}</w:t></w:r>')
        tbl.append(f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>{hrun}</w:p></w:tc>')
    tbl.append('</w:tr>')
    # data rows
    for ri, row in enumerate(rows):
        shade = 'F2F6FC' if ri % 2 == 0 else 'FFFFFF'
        tbl.append('<w:tr>')
        for ci in range(n):
            cell = row[ci].strip() if ci < len(row) else ''
            tbl.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="%s"/></w:tcPr>' % (col_w, shade))
            tbl.append(f'<w:p><w:pPr><w:spacing w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>{make_run(cell, sz=20)}</w:p></w:tc>')
        tbl.append('</w:tr>')
    tbl.append('</w:tbl><w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>')
    return ''.join(tbl)


def build_body(md, image_rel_ids):
    lines = md.split('\n')
    out = []
    i = 0
    n = len(lines)
    in_refs = False
    title_done = False
    while i < n:
        line = lines[i].rstrip()
        s = line.strip()
        if not s:
            i += 1; continue
        if s == '---':
            i += 1; continue

        # Title / front matter
        if line.startswith('# ') and not line.startswith('## '):
            out.append(para(s[2:].strip(), 'Title')); title_done = True
            i += 1; continue
        if line.startswith('## '):
            htext = s[3:].strip()
            if htext.lower() == 'references':
                in_refs = True
            out.append(para(htext, 'Heading1'))
            i += 1; continue
        if line.startswith('### '):
            out.append(para(s[4:].strip(), 'Heading2'))
            i += 1; continue

        # Image insertion
        m = re.match(r'\[Insert Figure (\d+) here\]', s)
        if m:
            num = int(m.group(1))
            out.append(image_paragraph(num, image_rel_ids[num]))
            # next line is the caption "Figure N. ..."
            if i+1 < n and lines[i+1].strip().startswith(f'Figure {num}'):
                out.append(para(lines[i+1].strip(), 'Caption'))
                i += 2
            else:
                i += 1
            continue
        if re.match(r'\[Insert Table \d+ here\]', s):
            i += 1; continue  # caption handled below

        # Table caption line "Table N. ..."
        if re.match(r'^Table \d+\.', s) and '|' not in s:
            out.append(para(s, 'TableCaption'))
            i += 1; continue
        # Stray figure caption (not preceded by insert) - render as caption
        if re.match(r'^Figure \d+\.', s):
            out.append(para(s, 'Caption'))
            i += 1; continue

        # Markdown table
        if s.startswith('|') and i+1 < n and re.match(r'^\|[\s:\-|]+\|', lines[i+1].strip()):
            headers = [c.strip() for c in s.strip('|').split('|')]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            out.append(make_table(headers, rows))
            continue

        # Front-matter subtitle lines (before first heading) -> centered subtitle
        if not any(x.startswith('## ') for x in lines[:i]) and title_done:
            out.append(para(s, 'Subtitle'))
            i += 1; continue

        # Reference entry
        if in_refs and re.match(r'^\[\d+\]', s):
            out.append(para(s, 'References'))
            i += 1; continue

        # Keywords / Book / bold-led lines and normal paragraphs
        out.append(para(s, 'Normal'))
        i += 1
    return '\n'.join(out)


def create_docx():
    with open(MD_FILE, encoding='utf-8') as f:
        md = f.read()

    # relationship ids: styles=rId1, images start at rId2
    image_rel_ids = {}
    rel_entries = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    rid = 2
    media = {}
    for num in sorted(FIGURES):
        fname = FIGURES[num][0]
        relid = f'rId{rid}'
        image_rel_ids[num] = relid
        rel_entries.append(f'<Relationship Id="{relid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{fname}"/>')
        with open(os.path.join(FIG_DIR, fname), 'rb') as fh:
            media[f'word/media/{fname}'] = fh.read()
        rid += 1

    word_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 + ''.join(rel_entries) + '</Relationships>')

    body = build_body(md, image_rel_ids)

    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
 xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
 xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<w:body>
{body}
<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>
<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>
</w:body></w:document>'''

    with zipfile.ZipFile(DOCX_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
        for path, blob in media.items():
            zf.writestr(path, blob)

    print(f"Created {DOCX_FILE} ({os.path.getsize(DOCX_FILE)/1024:.1f} KB)")


if __name__ == '__main__':
    create_figures()
    print("\nBuilding DOCX...")
    create_docx()
    print("Done.")
