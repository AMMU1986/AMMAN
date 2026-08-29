#!/usr/bin/env python3
"""
Generate 4 scientific figures (PNG) for Chapter 4:
Artificial Intelligence in Drug Discovery.
Pure Python standard library only (no matplotlib/PIL).
Reuses the PNGCanvas rendering approach established in generate_figures.py.
"""

import struct
import zlib
import math
import os

OUTPUT_DIR = '/projects/sandbox/AMMAN/ch4_figures'

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
TEAL = (0, 130, 130)
LIGHT_TEAL = (183, 222, 222)
GRAY = (128, 128, 128)
LIGHT_GRAY = (217, 217, 217)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class PNGCanvas:
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

    def round_rect(self, x1, y1, x2, y2, outline, fill=None):
        # simple rounded look via inset corners
        if fill:
            self.fill_rect(x1+2, y1, x2-2, y2, fill)
            self.fill_rect(x1, y1+2, x2, y2-2, fill)
        for x in range(max(0, x1+2), min(self.w, x2-1)):
            self.pixel(x, y1, outline)
            self.pixel(x, y2, outline)
        for y in range(max(0, y1+2), min(self.h, y2-1)):
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
    '|':[0b00100,0b00100,0b00100,0b00100,0b00100,0b00100,0b00100],
    '[':[0b01110,0b01000,0b01000,0b01000,0b01000,0b01000,0b01110],
    ']':[0b01110,0b00010,0b00010,0b00010,0b00010,0b00010,0b01110],
    '_':[0,0,0,0,0,0,0b11111],
    '?':[0b01110,0b10001,0b00001,0b00110,0b00100,0,0b00100],
    "'":[0b00100,0b00100,0b00100,0,0,0,0],
    '&':[0b01100,0b10010,0b10100,0b01000,0b10101,0b10010,0b01101],
    '#':[0b01010,0b11111,0b01010,0b01010,0b11111,0b01010,0b00000],
}


def gen_fig1():
    """Figure 1: AI-based target identification and validation workflow."""
    c = PNGCanvas(760, 500)
    c.text_c(380, 10, "AI-Driven Target Identification and Validation", BLACK, 2)

    # Layer 1: Data inputs (left column)
    c.text(20, 40, "Multi-Omics and Knowledge Inputs", DARK_BLUE, 1)
    inputs = [("Genomics / GWAS", MED_BLUE, LIGHT_BLUE),
              ("Transcriptomics", TEAL, LIGHT_TEAL),
              ("Proteomics", MED_GREEN, LIGHT_GREEN),
              ("Single-cell Atlas", ORANGE, LIGHT_ORANGE),
              ("Literature / KG", PURPLE, LIGHT_PURPLE)]
    iy = 60
    in_centers = []
    for label, oc, fc in inputs:
        c.round_rect(20, iy, 200, iy+42, oc, fc)
        c.text(32, iy+16, label, BLACK, 1)
        in_centers.append((200, iy+21))
        iy += 56

    # Layer 2: Integration engine (center)
    c.round_rect(290, 130, 480, 260, DARK_BLUE, PALE_BLUE)
    c.text_c(385, 150, "AI INTEGRATION", BLACK, 2)
    c.text_c(385, 175, "Graph Neural Nets", BLACK, 1)
    c.text_c(385, 195, "Multi-view Learning", BLACK, 1)
    c.text_c(385, 215, "Link Prediction", BLACK, 1)
    c.text_c(385, 235, "Network Analysis", BLACK, 1)
    for (x, y) in in_centers:
        c.arrow(x+4, y, 288, 195, GRAY, 1, 7)

    # Layer 3: Candidate target ranking
    c.round_rect(560, 70, 745, 200, MED_GREEN, LIGHT_GREEN)
    c.text_c(652, 85, "Ranked Targets", BLACK, 1)
    for i in range(4):
        yy = 108 + i*22
        c.fill_rect(575, yy, 575 + (110 - i*22), yy+12, MED_BLUE)
        c.text(575, yy+2, "T" + str(i+1), WHITE, 1)
    c.arrow(482, 160, 558, 130, BLACK, 2, 8)

    # Layer 4: Validation & tractability
    c.round_rect(560, 240, 745, 380, ORANGE, LIGHT_ORANGE)
    c.text_c(652, 255, "Validation and", BLACK, 1)
    c.text_c(652, 272, "Tractability", BLACK, 1)
    c.text(572, 295, "- Structure (AlphaFold)", BLACK, 1)
    c.text(572, 315, "- Druggable pocket", BLACK, 1)
    c.text(572, 335, "- Safety liabilities", BLACK, 1)
    c.text(572, 355, "- Modality choice", BLACK, 1)
    c.arrow(652, 200, 652, 238, BLACK, 2, 8)

    # Experimental feedback loop
    c.round_rect(290, 300, 480, 400, RED, LIGHT_RED)
    c.text_c(385, 320, "Experimental", BLACK, 1)
    c.text_c(385, 337, "Perturbation and", BLACK, 1)
    c.text_c(385, 354, "Phenotypic Assays", BLACK, 1)
    c.arrow(558, 330, 482, 350, RED, 2, 8)
    c.line(290, 350, 200, 350, RED, 2)
    c.line(200, 350, 200, 200, RED, 2)
    c.arrow(200, 200, 288, 200, RED, 2, 8)
    c.text(212, 175, "Iterative feedback", RED, 1)

    c.text(20, 470, "Figure 1: Integrated AI workflow for target identification and validation.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Target_Identification.png'))
    print("  Figure_1_Target_Identification.png done")


def gen_fig2():
    """Figure 2: Dual-encoder deep learning architecture for DTI prediction."""
    c = PNGCanvas(760, 480)
    c.text_c(380, 10, "Deep Learning Architecture for Drug-Target Interaction", BLACK, 2)

    # Drug branch (top)
    c.text(20, 45, "Drug (SMILES / Molecular Graph)", MED_GREEN, 1)
    c.round_rect(20, 65, 150, 110, MED_GREEN, LIGHT_GREEN)
    c.text_c(85, 80, "Molecule", BLACK, 1)
    c.text_c(85, 95, "Input", BLACK, 1)
    # small molecule glyph
    for (dx, dy) in [(0,0),(20,-8),(20,8),(40,0),(30,16)]:
        c.circle(100+dx, 130+dy, 5, MED_GREEN, LIGHT_GREEN)
    c.line(100,130,120,122,MED_GREEN,1); c.line(100,130,120,138,MED_GREEN,1)
    c.line(120,122,140,130,MED_GREEN,1); c.line(120,138,130,146,MED_GREEN,1)

    c.round_rect(180, 65, 320, 110, DARK_GREEN, LIGHT_GREEN)
    c.text_c(250, 78, "Drug Encoder", BLACK, 1)
    c.text_c(250, 95, "GNN / Transformer", BLACK, 1)
    c.arrow(150, 87, 178, 87, BLACK, 2, 7)

    # Target branch (bottom)
    c.text(20, 300, "Target (Amino-Acid Sequence)", MED_BLUE, 1)
    c.round_rect(20, 320, 150, 365, MED_BLUE, LIGHT_BLUE)
    c.text_c(85, 335, "Protein", BLACK, 1)
    c.text_c(85, 350, "Input", BLACK, 1)
    # helix glyph
    for i in range(8):
        xx = 95 + i*7
        yy = 390 + int(8*math.sin(i*0.9))
        c.circle(xx, yy, 3, MED_BLUE, LIGHT_BLUE)

    c.round_rect(180, 320, 320, 365, DARK_BLUE, LIGHT_BLUE)
    c.text_c(250, 333, "Target Encoder", BLACK, 1)
    c.text_c(250, 350, "CNN / Transformer", BLACK, 1)
    c.arrow(150, 342, 178, 342, BLACK, 2, 7)

    # Pretraining annotations
    c.text(180, 120, "pretrain: chemical corpus", GRAY, 1)
    c.text(180, 375, "pretrain: protein corpus", GRAY, 1)

    # Fusion
    c.round_rect(390, 190, 520, 285, PURPLE, LIGHT_PURPLE)
    c.text_c(455, 210, "FUSION", BLACK, 2)
    c.text_c(455, 235, "Concatenate /", BLACK, 1)
    c.text_c(455, 252, "Cross-Attention", BLACK, 1)
    c.arrow(320, 90, 388, 205, BLACK, 2, 8)
    c.arrow(320, 342, 388, 272, BLACK, 2, 8)

    # Prediction head
    c.round_rect(560, 190, 700, 285, ORANGE, LIGHT_ORANGE)
    c.text_c(630, 205, "Prediction", BLACK, 1)
    c.text_c(630, 225, "Head (MLP)", BLACK, 1)
    c.text_c(630, 250, "Interaction?", BLACK, 1)
    c.text_c(630, 267, "Affinity value", BLACK, 1)
    c.arrow(520, 237, 558, 237, BLACK, 2, 8)

    # Output
    c.text(600, 300, "Output", BLACK, 1)
    c.round_rect(560, 315, 700, 360, MED_GREEN, LIGHT_GREEN)
    c.text_c(630, 330, "Bind = 0.92", BLACK, 1)
    c.text_c(630, 345, "pKd = 7.8", BLACK, 1)
    c.arrow(630, 285, 630, 313, BLACK, 2, 7)

    c.text(20, 455, "Figure 2: Dual-encoder deep learning model for drug-target interaction prediction.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_DTI_Architecture.png'))
    print("  Figure_2_DTI_Architecture.png done")


def gen_fig3():
    """Figure 3: Closed-loop generative molecular design cycle."""
    c = PNGCanvas(760, 500)
    c.text_c(380, 10, "Closed-Loop Generative Molecular Design", BLACK, 2)

    cx, cy = 380, 270
    r = 150
    # Four nodes around a circle
    nodes = [
        ("GENERATIVE MODEL", "VAE / GAN / Diffusion", cx, cy - r, DARK_GREEN, LIGHT_GREEN),
        ("PROPERTY PREDICTORS", "Potency / ADMET / Tox", cx + r, cy, MED_BLUE, LIGHT_BLUE),
        ("SCORING and RANKING", "Multi-objective reward", cx, cy + r, ORANGE, LIGHT_ORANGE),
        ("OPTIMISATION", "RL / Bayesian search", cx - r, cy, PURPLE, LIGHT_PURPLE),
    ]
    centers = []
    for title, sub, nx, ny, oc, fc in nodes:
        c.round_rect(nx-95, ny-32, nx+95, ny+32, oc, fc)
        c.text_c(nx, ny-15, title, BLACK, 1)
        c.text_c(nx, ny+5, sub, BLACK, 1)
        centers.append((nx, ny))

    # Curved arrows (clockwise) approximated with straight segments
    def loop_arrow(a, b, col):
        (x1, y1) = centers[a]
        (x2, y2) = centers[b]
        dx, dy = x2-x1, y2-y1
        d = math.sqrt(dx*dx+dy*dy)
        ox, oy = dx/d, dy/d
        c.arrow(int(x1+ox*100), int(y1+oy*40), int(x2-ox*100), int(y2-oy*40), col, 2, 9)

    loop_arrow(0, 1, GRAY)
    loop_arrow(1, 2, GRAY)
    loop_arrow(2, 3, GRAY)
    loop_arrow(3, 0, GRAY)

    # Center annotation
    c.round_rect(cx-70, cy-20, cx+70, cy+20, GOLD, LIGHT_GOLD)
    c.text_c(cx, cy-10, "Iterate until", BLACK, 1)
    c.text_c(cx, cy+5, "objectives met", BLACK, 1)

    # Side panel: representations
    c.round_rect(560, 55, 745, 175, LIGHT_GRAY, (248, 248, 248))
    c.text(572, 62, "Representations:", BLACK, 1)
    c.text(572, 82, "- SMILES strings", DARK_GREEN, 1)
    c.text(572, 100, "- Molecular graphs", MED_BLUE, 1)
    c.text(572, 118, "- 3D pocket-aware", PURPLE, 1)
    c.text(572, 140, "Risk: reward", RED, 1)
    c.text(572, 156, "hacking / invalid", RED, 1)

    c.text(20, 470, "Figure 3: Closed-loop generative design integrating generation, prediction, and optimisation.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Generative_Design.png'))
    print("  Figure_3_Generative_Design.png done")


def gen_fig4():
    """Figure 4: Computational drug repurposing strategies."""
    c = PNGCanvas(760, 500)
    c.text_c(380, 10, "Computational Drug Repurposing Strategies", BLACK, 2)

    # Central existing-drug node
    c.round_rect(310, 210, 450, 280, DARK_BLUE, PALE_BLUE)
    c.text_c(380, 228, "Approved /", BLACK, 1)
    c.text_c(380, 245, "Investigational", BLACK, 1)
    c.text_c(380, 262, "Drug", BLACK, 1)

    # Four strategy boxes
    strategies = [
        ("Signature Matching", "Reverse disease\nexpression", 60, 60, TEAL, LIGHT_TEAL),
        ("Network Proximity", "Targets near\ndisease module", 520, 60, MED_GREEN, LIGHT_GREEN),
        ("Knowledge Graph", "Predict drug-\ndisease edges", 60, 340, PURPLE, LIGHT_PURPLE),
        ("EHR / Real-World", "Outcome signals\nin patient data", 520, 340, ORANGE, LIGHT_ORANGE),
    ]
    for title, sub, bx, by, oc, fc in strategies:
        c.round_rect(bx, by, bx+180, by+90, oc, fc)
        c.text_c(bx+90, by+16, title, BLACK, 1)
        for j, ln in enumerate(sub.split("\n")):
            c.text_c(bx+90, by+40+j*18, ln, BLACK, 1)

    # Arrows from strategies converging to central drug -> new indication
    c.arrow(240, 105, 312, 220, GRAY, 2, 8)
    c.arrow(520, 105, 448, 220, GRAY, 2, 8)
    c.arrow(240, 385, 312, 270, GRAY, 2, 8)
    c.arrow(520, 385, 448, 270, GRAY, 2, 8)

    # New indication output
    c.round_rect(300, 400, 460, 460, RED, LIGHT_RED)
    c.text_c(380, 418, "New Therapeutic", BLACK, 1)
    c.text_c(380, 436, "Indication", BLACK, 1)
    c.arrow(380, 280, 380, 398, BLACK, 2, 9)

    # Note on validation
    c.text_c(380, 300, "prioritise -> clinical trials", DARK_BLUE, 1)

    c.text(20, 480, "Figure 4: Complementary computational strategies for drug repurposing.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Drug_Repurposing.png'))
    print("  Figure_4_Drug_Repurposing.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Chapter 4 figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print("\nAll 4 figures saved to " + OUTPUT_DIR)
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print("  " + f + ": " + str(round(sz/1024, 1)) + " KB")


if __name__ == '__main__':
    main()
