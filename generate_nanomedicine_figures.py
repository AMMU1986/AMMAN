#!/usr/bin/env python3
"""
Generate 4 scientific figures (PNG) for Chapter 10:
"AI-Enabled Nanomedicine and Smart Drug Delivery".

Uses only the Python standard library (a lightweight bytearray-based PNG
canvas identical to the one in generate_figures.py) so it runs in the
offline sandbox where matplotlib/Pillow are unavailable.
"""

import struct
import zlib
import math
import os
import random

OUTPUT_DIR = '/projects/sandbox/AMMAN/nanomedicine_figures'

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
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class PNGCanvas:
    """Fast PNG canvas using bytearray."""

    def __init__(self, width, height, bg=(255, 255, 255)):
        self.w = width
        self.h = height
        self.data = bytearray(bg[0:1] * (width * height * 3))
        # Fill with bg color
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
        # Outline
        for x in range(max(0,x1), min(self.w, x2+1)):
            self.pixel(x, y1, outline)
            self.pixel(x, y2, outline)
        for y in range(max(0,y1), min(self.h, y2+1)):
            self.pixel(x1, y, outline)
            self.pixel(x2, y, outline)

    def hline(self, x1, x2, y, color):
        if y < 0 or y >= self.h:
            return
        x1, x2 = max(0, min(x1, x2)), min(self.w-1, max(x1, x2))
        idx = (y * self.w + x1) * 3
        for x in range(x1, x2+1):
            self.data[idx] = color[0]
            self.data[idx+1] = color[1]
            self.data[idx+2] = color[2]
            idx += 3

    def vline(self, x, y1, y2, color):
        if x < 0 or x >= self.w:
            return
        y1, y2 = max(0, min(y1, y2)), min(self.h-1, max(y1, y2))
        for y in range(y1, y2+1):
            idx = (y * self.w + x) * 3
            self.data[idx] = color[0]
            self.data[idx+1] = color[1]
            self.data[idx+2] = color[2]

    def line(self, x1, y1, x2, y2, color, thick=1):
        dx = abs(x2-x1); dy = abs(y2-y1)
        sx = 1 if x1<x2 else -1
        sy = 1 if y1<y2 else -1
        err = dx - dy
        while True:
            for t in range(-(thick//2), (thick+1)//2):
                self.pixel(x1+t if dy>dx else x1, y1 if dy>dx else y1+t, color)
            if x1==x2 and y1==y2:
                break
            e2 = 2*err
            if e2 > -dy: err -= dy; x1 += sx
            if e2 < dx: err += dx; y1 += sy

    def arrow(self, x1, y1, x2, y2, color, thick=2, hs=8):
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
        # Outline using midpoint circle
        x, y = r, 0
        err = 1 - r
        while x >= y:
            for px, py in [(cx+x,cy+y),(cx-x,cy+y),(cx+x,cy-y),(cx-x,cy-y),
                           (cx+y,cy+x),(cx-y,cy+x),(cx+y,cy-x),(cx-y,cy-x)]:
                self.pixel(px, py, color)
            y += 1
            if err < 0:
                err += 2*y + 1
            else:
                x -= 1
                err += 2*(y-x) + 1

    def text(self, x, y, s, color, scale=1):
        FONT = _FONT
        for ch in s:
            bm = FONT.get(ch)
            if bm is None:
                x += 4*scale
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
            raw.append(0)  # filter
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
}







def gen_fig1():
    """Figure 1: Taxonomy of nanocarrier platforms for drug delivery."""
    c = PNGCanvas(760, 500)
    c.text_c(380, 8, "Nanocarrier Platforms for Drug Delivery", BLACK, 2)

    # Central node
    c.rect(300, 210, 460, 265, DARK_BLUE, PALE_BLUE)
    c.text_c(380, 224, "Nanocarrier", BLACK, 1)
    c.text_c(380, 240, "Platforms", BLACK, 1)

    platforms = [
        ("Liposomes", 60, 60, MED_BLUE, LIGHT_BLUE, "Doxil (approved)"),
        ("Polymeric NP", 300, 45, MED_GREEN, LIGHT_GREEN, "PLGA / PEG"),
        ("Lipid NP (LNP)", 540, 60, ORANGE, LIGHT_ORANGE, "mRNA vaccines"),
        ("Dendrimers", 590, 235, PURPLE, LIGHT_PURPLE, "PAMAM cores"),
        ("Inorganic NP", 540, 400, GOLD, LIGHT_GOLD, "Au / SiO2 / Fe3O4"),
        ("Micelles", 300, 415, RED, LIGHT_RED, "amphiphilic"),
        ("Protein / Exo", 60, 400, DARK_GREEN, LIGHT_GREEN, "albumin, EVs"),
        ("Carbon NM", 60, 235, GRAY, LIGHT_GRAY, "CNT / graphene"),
    ]
    bw, bh = 160, 52
    cx0, cy0 = 380, 237
    for label, bx, by, col, fill, sub in platforms:
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        c.text_c(bx + bw // 2, by + 12, label, BLACK, 1)
        c.text_c(bx + bw // 2, by + 30, sub, GRAY, 1)
        # connector to centre
        ex, ey = bx + bw // 2, by + bh // 2
        dx, dy = cx0 - ex, cy0 - ey
        d = math.sqrt(dx * dx + dy * dy)
        if d > 0:
            c.line(int(ex + dx / d * 30), int(ey + dy / d * 20),
                   int(cx0 - dx / d * 85), int(cy0 - dy / d * 30), LIGHT_GRAY, 1)

    c.text(40, 478, "Figure 1: Major nanocarrier classes and representative examples", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Nanocarrier_Platforms.png'))
    print("  Figure_1 done")


def gen_fig2():
    """Figure 2: ML workflow for nanoparticle design and property prediction."""
    c = PNGCanvas(760, 500)
    c.text_c(380, 8, "Machine Learning Workflow for Nanoparticle Design", BLACK, 2)

    # (a) Pipeline of stages
    stages = [
        ("Data\nCuration", 30, DARK_BLUE, PALE_BLUE),
        ("Feature\nDescriptors", 175, MED_BLUE, LIGHT_BLUE),
        ("Model\nTraining", 320, MED_GREEN, LIGHT_GREEN),
        ("Property\nPrediction", 465, ORANGE, LIGHT_ORANGE),
        ("Inverse\nDesign", 610, PURPLE, LIGHT_PURPLE),
    ]
    y0 = 55
    bw, bh = 120, 60
    centers = []
    for label, bx, col, fill in stages:
        l1, l2 = label.split("\n")
        c.rect(bx, y0, bx + bw, y0 + bh, col, fill)
        c.text_c(bx + bw // 2, y0 + 16, l1, BLACK, 1)
        c.text_c(bx + bw // 2, y0 + 34, l2, BLACK, 1)
        centers.append((bx + bw, y0 + bh // 2, bx))
    for i in range(len(centers) - 1):
        c.arrow(centers[i][0], centers[i][1], centers[i + 1][2], centers[i][1], GRAY, 2, 7)
    # feedback loop
    c.line(670, y0 + bh, 670, y0 + bh + 25, GOLD, 2)
    c.line(90, y0 + bh + 25, 670, y0 + bh + 25, GOLD, 2)
    c.arrow(90, y0 + bh + 25, 90, y0 + bh, GOLD, 2, 7)
    c.text_c(380, y0 + bh + 30, "Active-learning feedback loop", GOLD, 1)

    # (b) Descriptor categories
    c.text(30, 175, "(a) Descriptor categories", BLACK, 1)
    descs = ["Size / PDI", "Zeta potential", "Surface chem", "Shape / AR",
             "Ligand density", "Composition"]
    for i, d in enumerate(descs):
        bx = 40 + (i % 3) * 230
        by = 195 + (i // 3) * 34
        c.rect(bx, by, bx + 200, by + 26, MED_BLUE, LIGHT_BLUE)
        c.text_c(bx + 100, by + 8, d, BLACK, 1)

    # (c) Model accuracy bar chart (R^2 by task)
    c.text(30, 285, "(b) Reported model accuracy (R-squared)", BLACK, 1)
    tasks = [("Size", 0.94), ("EE%", 0.89), ("Release", 0.83),
             ("Toxicity", 0.79), ("Uptake", 0.86), ("Targeting", 0.81)]
    c.vline(60, 305, 455, BLACK)
    c.hline(60, 730, 455, BLACK)
    c.text(28, 305, "1.0", BLACK, 1)
    c.text(28, 380, "0.5", BLACK, 1)
    c.text(28, 450, "0.0", BLACK, 1)
    for i, (t, r2) in enumerate(tasks):
        bx = 90 + i * 105
        bh2 = int(r2 * 150)
        c.rect(bx, 455 - bh2, bx + 60, 455, BLACK, MED_GREEN)
        c.text_c(bx + 30, 460, t, BLACK, 1)
        c.text_c(bx + 30, 455 - bh2 - 11, f"{r2:.2f}", BLACK, 1)

    c.text(40, 480, "Figure 2: End-to-end ML pipeline and benchmarked prediction accuracy", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_ML_Workflow.png'))
    print("  Figure_2 done")


def gen_fig3():
    """Figure 3: Stimuli-responsive triggers and release mechanisms."""
    c = PNGCanvas(760, 500)
    c.text_c(380, 8, "Stimuli-Responsive Drug Release Mechanisms", BLACK, 2)

    # central nanoparticle
    c.circle(380, 250, 55, DARK_BLUE, PALE_BLUE)
    c.text_c(380, 240, "Smart", BLACK, 1)
    c.text_c(380, 254, "Carrier", BLACK, 1)
    # drug dots inside
    random.seed(3)
    for _ in range(14):
        a = random.uniform(0, 6.28)
        r = random.uniform(0, 42)
        c.circle(int(380 + r * math.cos(a)), int(250 + r * math.sin(a)), 3, RED, RED)

    triggers = [
        ("pH (acidic)", 60, 70, RED, LIGHT_RED, "tumor / endosome"),
        ("Redox (GSH)", 300, 55, PURPLE, LIGHT_PURPLE, "intracellular"),
        ("Enzyme", 540, 70, MED_GREEN, LIGHT_GREEN, "MMP / esterase"),
        ("Temperature", 600, 230, ORANGE, LIGHT_ORANGE, "hyperthermia"),
        ("Light (NIR)", 540, 400, GOLD, LIGHT_GOLD, "photothermal"),
        ("Magnetic", 300, 420, DARK_BLUE, LIGHT_BLUE, "external field"),
        ("Ultrasound", 60, 400, MED_BLUE, LIGHT_BLUE, "cavitation"),
    ]
    bw, bh = 150, 50
    for label, bx, by, col, fill, sub in triggers:
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        c.text_c(bx + bw // 2, by + 12, label, BLACK, 1)
        c.text_c(bx + bw // 2, by + 30, sub, GRAY, 1)
        ex, ey = bx + bw // 2, by + bh // 2
        dx, dy = 380 - ex, 250 - ey
        d = math.sqrt(dx * dx + dy * dy)
        if d > 0:
            c.arrow(int(ex + dx / d * 28), int(ey + dy / d * 20),
                    int(380 - dx / d * 62), int(250 - dy / d * 62), col, 2, 7)

    c.text(40, 478, "Figure 3: Internal and external stimuli triggering site-specific release", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Stimuli_Responsive.png'))
    print("  Figure_3 done")


def gen_fig4():
    """Figure 4: Closed-loop AI-optimized theranostic delivery system."""
    c = PNGCanvas(760, 500)
    c.text_c(380, 8, "AI-Optimized Closed-Loop Theranostic Delivery", BLACK, 2)

    # Loop of 5 nodes
    nodes = [
        ("Patient /\nBiomarkers", 320, 55, MED_BLUE, LIGHT_BLUE),
        ("Sensing &\nImaging", 560, 150, PURPLE, LIGHT_PURPLE),
        ("AI Dosing\nController", 500, 350, DARK_GREEN, LIGHT_GREEN),
        ("Responsive\nRelease", 200, 350, ORANGE, LIGHT_ORANGE),
        ("Smart\nNanocarrier", 130, 150, RED, LIGHT_RED),
    ]
    bw, bh = 150, 62
    centers = []
    for label, bx, by, col, fill in nodes:
        l1, l2 = label.split("\n")
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        c.text_c(bx + bw // 2, by + 18, l1, BLACK, 1)
        c.text_c(bx + bw // 2, by + 36, l2, BLACK, 1)
        centers.append((bx + bw // 2, by + bh // 2))
    order = [0, 1, 2, 3, 4, 0]
    for i in range(len(order) - 1):
        x1, y1 = centers[order[i]]
        x2, y2 = centers[order[i + 1]]
        dx, dy = x2 - x1, y2 - y1
        d = math.sqrt(dx * dx + dy * dy)
        if d > 0:
            c.arrow(int(x1 + dx / d * 88), int(y1 + dy / d * 40),
                    int(x2 - dx / d * 88), int(y2 - dy / d * 40), GRAY, 2, 8)

    # center annotation
    c.rect(300, 210, 460, 285, GOLD, LIGHT_GOLD)
    c.text_c(380, 224, "Reinforcement", BLACK, 1)
    c.text_c(380, 240, "Learning", BLACK, 1)
    c.text_c(380, 258, "dose optimisation", GRAY, 1)
    c.text_c(380, 272, "minimise toxicity", GRAY, 1)

    # performance callout
    c.rect(20, 430, 740, 465, DARK_BLUE, PALE_BLUE)
    c.text_c(380, 442, "Real-time monitoring - adaptive dosing - personalized therapy", BLACK, 1)

    c.text(40, 478, "Figure 4: Closed-loop theranostic architecture integrating AI control", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Closed_Loop_Theranostic.png'))
    print("  Figure_4 done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Chapter 10 figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print(f"\nAll figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz/1024:.1f} KB")


if __name__ == '__main__':
    main()
