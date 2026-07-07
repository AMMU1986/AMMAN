#!/usr/bin/env python3
"""
Generate 6 scientific figure images (PNG) for Chapter 16.
Uses only Python standard library - optimized with bytearray for speed.
"""

import struct
import zlib
import math
import os
import random

OUTPUT_DIR = '/projects/sandbox/AMMAN/figures'

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
    """Figure 1: AI Workflow Diagram"""
    c = PNGCanvas(700, 450)
    c.text_c(350, 8, "AI-Assisted Nanomaterial Design Workflow", BLACK, 2)

    # 6 boxes in cycle layout
    boxes = [
        ("Data Collection", 50, 80, DARK_BLUE, PALE_BLUE),
        ("Feature Eng.", 270, 55, MED_BLUE, LIGHT_BLUE),
        ("ML Training", 490, 80, DARK_GREEN, LIGHT_GREEN),
        ("Prediction", 550, 250, ORANGE, LIGHT_ORANGE),
        ("Inverse Design", 310, 340, PURPLE, LIGHT_PURPLE),
        ("Validation", 60, 280, RED, LIGHT_RED),
    ]
    bw, bh = 150, 50
    centers = []
    for label, bx, by, col, fill in boxes:
        c.rect(bx, by, bx+bw, by+bh, col, fill)
        c.text_c(bx+bw//2, by+bh//2-4, label, BLACK, 1)
        centers.append((bx+bw//2, by+bh//2))

    # Arrows
    pairs = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)]
    for i,j in pairs:
        x1,y1 = centers[i]; x2,y2 = centers[j]
        dx,dy = x2-x1, y2-y1
        d = math.sqrt(dx*dx+dy*dy)
        if d > 0:
            off = 85
            c.arrow(int(x1+dx/d*off), int(y1+dy/d*off),
                    int(x2-dx/d*off), int(y2-dy/d*off), GRAY, 2, 8)

    # Center: feedback loop
    c.rect(260, 185, 430, 225, GOLD, LIGHT_GOLD)
    c.text_c(345, 195, "Active Learning", BLACK, 1)
    c.text_c(345, 208, "Feedback Loop", BLACK, 1)

    # Data sources
    c.rect(10, 160, 150, 240, LIGHT_GRAY, (245,245,245))
    c.text(18, 168, "Sources:", BLACK, 1)
    c.text(18, 183, "- Materials Project", GRAY, 1)
    c.text(18, 198, "- OQMD/ICSD", GRAY, 1)
    c.text(18, 213, "- Experiments", GRAY, 1)
    c.text(18, 228, "- Literature", GRAY, 1)

    c.text(50, 420, "Figure 1: Iterative AI-assisted nanomaterial design cycle", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1.png'))
    print("  Figure_1.png done")


def gen_fig2():
    """Figure 2: ML Performance Comparison"""
    c = PNGCanvas(700, 450)
    c.text_c(350, 8, "ML Model Performance Comparison", BLACK, 2)

    # (a) Bar chart
    c.text(30, 35, "(a) Band Gap MAE (eV)", BLACK, 1)
    models = [("RF",0.45), ("SVM",0.52), ("XGB",0.28), ("CGCNN",0.31), ("MEGNet",0.27)]
    colors = [MED_BLUE, LIGHT_BLUE, ORANGE, MED_GREEN, DARK_GREEN]
    # Axes
    c.vline(50, 55, 210, BLACK)
    c.hline(50, 370, 210, BLACK)
    for i, (name, mae) in enumerate(models):
        bx = 70 + i*60
        bh = int(mae/0.6 * 145)
        c.rect(bx, 210-bh, bx+40, 210, BLACK, colors[i])
        c.text_c(bx+20, 215, name, BLACK, 1)
        c.text_c(bx+20, 210-bh-10, f"{mae:.2f}", BLACK, 1)
    c.text(20, 55, "0.6", BLACK, 1)
    c.text(20, 130, "0.3", BLACK, 1)
    c.text(20, 205, "0.0", BLACK, 1)

    # (b) Learning curves
    c.text(400, 35, "(b) Learning Curves", BLACK, 1)
    c.vline(420, 55, 210, BLACK)
    c.hline(420, 680, 210, BLACK)
    c.text(430, 215, "Training Size", BLACK, 1)
    c.text(395, 55, "MAE", BLACK, 1)
    for ci, (col, lbl) in enumerate([(RED,"RF"),(MED_BLUE,"GNN"),(ORANGE,"XGB")]):
        for x in range(430, 670):
            t = (x-430)/240.0
            base = [140, 155, 148][ci]
            rate = [2.0, 3.5, 2.8][ci]
            y = int(200 - base*(1-math.exp(-rate*t)))
            c.pixel(x, y, col); c.pixel(x, y+1, col)
        c.hline(610, 640, 65+ci*14, col)
        c.text(645, 62+ci*14, lbl, BLACK, 1)

    # (c) Radar-style comparison (simplified as grouped bars)
    c.text(30, 250, "(c) Multi-Property Performance (R-squared)", BLACK, 1)
    props = ["BandGap", "FormE", "Elastic", "Thermal", "Plasmon", "Catalys"]
    gnn_scores = [0.92, 0.96, 0.82, 0.72, 0.87, 0.78]
    rf_scores =  [0.75, 0.78, 0.62, 0.65, 0.72, 0.58]
    c.vline(50, 270, 420, BLACK)
    c.hline(50, 680, 420, BLACK)
    for i, (p, gs, rs) in enumerate(zip(props, gnn_scores, rf_scores)):
        bx = 70 + i*100
        gh = int(gs * 130)
        rh = int(rs * 130)
        c.rect(bx, 420-gh, bx+30, 420, BLACK, MED_BLUE)
        c.rect(bx+35, 420-rh, bx+65, 420, BLACK, ORANGE)
        c.text(bx, 425, p, BLACK, 1)
    c.hline(80, 130, 275, MED_BLUE)
    c.text(135, 272, "GNN", BLACK, 1)
    c.hline(180, 230, 275, ORANGE)
    c.text(235, 272, "RF", BLACK, 1)

    c.text(50, 437, "Figure 2: ML performance across properties", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2.png'))
    print("  Figure_2.png done")


def gen_fig3():
    """Figure 3: GAN Architecture"""
    c = PNGCanvas(700, 450)
    c.text_c(350, 8, "GAN Architecture for Nanomaterial Inverse Design", BLACK, 2)

    # (a) cGAN framework
    c.text(20, 35, "(a) Conditional GAN Framework", BLACK, 1)

    # Noise
    c.rect(20, 70, 110, 105, GRAY, LIGHT_GRAY)
    c.text_c(65, 80, "Noise z", BLACK, 1)
    # Target
    c.rect(20, 115, 110, 150, PURPLE, LIGHT_PURPLE)
    c.text_c(65, 125, "Target", BLACK, 1)
    # Generator
    c.rect(150, 75, 290, 145, DARK_GREEN, LIGHT_GREEN)
    c.text_c(220, 95, "GENERATOR", BLACK, 2)
    c.text_c(220, 120, "G(z|c)", BLACK, 1)
    # Arrows to gen
    c.arrow(110, 87, 150, 100, GRAY, 2, 6)
    c.arrow(110, 130, 150, 115, PURPLE, 2, 6)
    # Generated
    c.rect(330, 80, 440, 140, ORANGE, LIGHT_ORANGE)
    c.text_c(385, 95, "Generated", BLACK, 1)
    c.text_c(385, 112, "Structure", BLACK, 1)
    c.arrow(290, 110, 330, 110, BLACK, 2, 6)
    # Discriminator
    c.rect(490, 95, 630, 165, RED, LIGHT_RED)
    c.text_c(560, 110, "DISCRIMINATOR", BLACK, 1)
    c.text_c(560, 130, "D(x|c)", BLACK, 1)
    c.text_c(560, 148, "Real/Fake?", GRAY, 1)
    c.arrow(440, 110, 490, 125, BLACK, 2, 6)
    # Real data
    c.rect(490, 40, 630, 80, MED_BLUE, LIGHT_BLUE)
    c.text_c(560, 52, "Real Data", BLACK, 1)
    c.arrow(560, 80, 560, 95, MED_BLUE, 2, 6)
    # Output
    c.rect(650, 110, 695, 150, GOLD, LIGHT_GOLD)
    c.text_c(672, 123, "0/1", BLACK, 1)
    c.arrow(630, 130, 650, 130, BLACK, 2, 6)
    # Feedback
    c.line(672, 150, 672, 175, RED, 1)
    c.line(672, 175, 220, 175, RED, 1)
    c.arrow(220, 175, 220, 145, RED, 1, 6)
    c.text(380, 178, "Adversarial Loss", RED, 1)

    # (b) Generated vs Real
    c.text(20, 210, "(b) Generated vs Real Morphologies", BLACK, 1)
    c.text(20, 230, "Generated:", MED_GREEN, 1)
    for i in range(5):
        cx = 40 + i*55
        r = 12 + (i%3)*3
        c.circle(cx, 265, r, MED_GREEN, LIGHT_GREEN)
    c.text(20, 295, "Real:", MED_BLUE, 1)
    for i in range(5):
        cx = 40 + i*55
        r = 13 + (i%3)*2
        c.circle(cx, 325, r, MED_BLUE, LIGHT_BLUE)

    # (c) Property distributions
    c.text(350, 210, "(c) Property Distribution", BLACK, 1)
    c.vline(370, 230, 390, BLACK)
    c.hline(370, 690, 390, BLACK)
    c.text(490, 395, "Property Value", BLACK, 1)
    c.text(345, 230, "Freq", BLACK, 1)
    for x in range(380, 680):
        t1 = (x-510)/50.0
        y1 = int(380 - 120*math.exp(-t1*t1/2))
        c.pixel(x, y1, MED_BLUE); c.pixel(x, y1+1, MED_BLUE)
        t2 = (x-530)/55.0
        y2 = int(380 - 110*math.exp(-t2*t2/2))
        c.pixel(x, y2, MED_GREEN); c.pixel(x, y2+1, MED_GREEN)
    c.hline(600, 630, 240, MED_BLUE); c.text(635, 237, "Real", BLACK, 1)
    c.hline(600, 630, 255, MED_GREEN); c.text(635, 252, "Gen", BLACK, 1)

    c.text(50, 430, "Figure 3: GAN framework for inverse nanomaterial design", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3.png'))
    print("  Figure_3.png done")


def gen_fig4():
    """Figure 4: RL Framework"""
    c = PNGCanvas(700, 450)
    c.text_c(350, 8, "Reinforcement Learning for Nanomaterial Design", BLACK, 2)

    # (a) Agent-Environment
    c.text(20, 35, "(a) RL Agent-Environment Loop", BLACK, 1)
    c.rect(40, 60, 190, 140, DARK_BLUE, PALE_BLUE)
    c.text_c(115, 80, "RL AGENT", BLACK, 2)
    c.text_c(115, 105, "DQN/PPO", BLACK, 1)
    c.text_c(115, 120, "Policy Net", GRAY, 1)
    c.rect(40, 200, 190, 290, DARK_GREEN, LIGHT_GREEN)
    c.text_c(115, 215, "ENVIRONMENT", BLACK, 1)
    c.text_c(115, 240, "NanoMaterial", BLACK, 1)
    c.text_c(115, 258, "Simulator", BLACK, 1)
    c.text_c(115, 275, "(DFT/ML)", GRAY, 1)
    # Arrows
    c.arrow(190, 110, 230, 170, ORANGE, 2, 6)
    c.text(195, 128, "Action", ORANGE, 1)
    c.arrow(230, 230, 190, 170, MED_BLUE, 2, 6)
    c.text(195, 195, "State", MED_BLUE, 1)
    c.arrow(40, 200, 40, 140, RED, 2, 6)
    c.text(5, 165, "Reward", RED, 1)

    # (b) Convergence
    c.text(290, 35, "(b) Training Convergence", BLACK, 1)
    c.vline(310, 55, 180, BLACK)
    c.hline(310, 500, 180, BLACK)
    c.text(380, 185, "Episodes", BLACK, 1)
    c.text(280, 55, "R", BLACK, 1)
    for ci, (col, lbl, rate) in enumerate(
            [(RED,"DQN",2.5),(MED_BLUE,"PPO",4.0),(MED_GREEN,"A2C",3.2)]):
        for x in range(320, 490):
            t = (x-320)/170.0
            y = int(170 - 100*(1-math.exp(-rate*t)))
            c.pixel(x, y, col); c.pixel(x, y+1, col)
        c.hline(510, 535, 62+ci*14, col)
        c.text(540, 59+ci*14, lbl, BLACK, 1)

    # (c) Pareto front
    c.text(20, 310, "(c) Pareto Front", BLACK, 1)
    c.vline(50, 325, 420, BLACK)
    c.hline(50, 690, 420, BLACK)
    c.text(300, 425, "Stability (eV/atom)", BLACK, 1)
    c.text(15, 325, "Band Gap", BLACK, 1)
    pts = [(70,410),(120,395),(180,380),(260,368),(350,360),(450,355),(560,352),(650,350)]
    for i in range(len(pts)-1):
        c.line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], RED, 2)
    for px, py in pts:
        c.circle(px, py, 4, RED, RED)
    # Dominated
    random.seed(42)
    for _ in range(20):
        px = random.randint(80, 660)
        py = random.randint(360, 415)
        front_y = 410 - (px-70)*0.1
        if py > front_y + 8:
            c.circle(px, py, 3, LIGHT_BLUE, LIGHT_BLUE)
    c.circle(580, 330, 4, RED, RED); c.text(590, 327, "Pareto", BLACK, 1)
    c.circle(580, 345, 3, LIGHT_BLUE, LIGHT_BLUE); c.text(590, 342, "Dominated", BLACK, 1)

    c.text(50, 437, "Figure 4: RL framework with convergence and Pareto front", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4.png'))
    print("  Figure_4.png done")


def gen_fig5():
    """Figure 5: HTS and Active Learning"""
    c = PNGCanvas(700, 450)
    c.text_c(350, 8, "High-Throughput Screening and Active Learning", BLACK, 2)

    # (a) Funnel
    c.text(20, 35, "(a) Screening Funnel", BLACK, 1)
    stages = [("10^6 Enumerated", 220, PALE_BLUE, DARK_BLUE),
              ("10^5 Stable", 180, LIGHT_BLUE, MED_BLUE),
              ("10^4 Filtered", 140, LIGHT_GREEN, DARK_GREEN),
              ("10^2 Validated", 100, LIGHT_ORANGE, ORANGE),
              ("10 Confirmed", 60, LIGHT_RED, RED)]
    fy = 55
    cx_f = 130
    for label, w, fill, outline in stages:
        c.rect(cx_f-w//2, fy, cx_f+w//2, fy+32, outline, fill)
        c.text_c(cx_f, fy+12, label, BLACK, 1)
        fy += 42
        if fy < 260:
            c.arrow(cx_f, fy-8, cx_f, fy+2, GRAY, 1, 5)

    # (b) Active learning loop
    c.text(290, 35, "(b) Active Learning Loop", BLACK, 1)
    al = [("ML Model", 400, 60, MED_BLUE, LIGHT_BLUE),
          ("Uncertainty", 530, 130, PURPLE, LIGHT_PURPLE),
          ("Experiment", 470, 220, MED_GREEN, LIGHT_GREEN),
          ("Update DB", 340, 170, ORANGE, LIGHT_ORANGE)]
    for label, bx, by, col, fill in al:
        c.rect(bx-50, by, bx+50, by+35, col, fill)
        c.text_c(bx, by+12, label, BLACK, 1)
    c.arrow(450, 77, 490, 130, GRAY, 1, 6)
    c.arrow(540, 165, 510, 220, GRAY, 1, 6)
    c.arrow(420, 237, 370, 205, GRAY, 1, 6)
    c.arrow(370, 170, 380, 95, GRAY, 1, 6)
    c.text_c(440, 155, "Iterate", GOLD, 1)

    # (c) Efficiency comparison
    c.text(20, 290, "(c) Sampling Efficiency", BLACK, 1)
    c.vline(50, 310, 420, BLACK)
    c.hline(50, 350, 420, BLACK)
    c.text(150, 425, "Experiments", BLACK, 1)
    c.text(20, 310, "Best", BLACK, 1)
    for x in range(60, 340):
        t = (x-60)/280.0
        yr = int(410 - 80*(1-math.exp(-1.5*t)))
        c.pixel(x, yr, RED); c.pixel(x, yr+1, RED)
        ya = int(410 - 95*(1-math.exp(-5*t)))
        c.pixel(x, ya, MED_BLUE); c.pixel(x, ya+1, MED_BLUE)
    c.hline(250, 280, 315, RED); c.text(285, 312, "Random", BLACK, 1)
    c.hline(250, 280, 330, MED_BLUE); c.text(285, 327, "Active", BLACK, 1)
    c.text(100, 340, "3-10x faster", MED_BLUE, 1)

    # Self-driving lab box
    c.rect(390, 275, 690, 430, DARK_BLUE, PALE_BLUE)
    c.text_c(540, 285, "Self-Driving Laboratory", BLACK, 2)
    c.text(405, 310, "- AI Planning Module", MED_BLUE, 1)
    c.text(405, 330, "- Robotic Synthesis", MED_GREEN, 1)
    c.text(405, 350, "- Auto Characterization", ORANGE, 1)
    c.text(405, 370, "- Closed-loop Feedback", PURPLE, 1)
    c.text(405, 400, ">95% yield, <100 iters", RED, 1)

    c.text(50, 437, "Figure 5: HTS funnel, active learning, self-driving labs", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_5.png'))
    print("  Figure_5.png done")


def gen_fig6():
    """Figure 6: Forensic Applications"""
    c = PNGCanvas(700, 450)
    c.text_c(350, 8, "AI-Designed Nanomaterials for Forensic Applications", BLACK, 2)

    # (a) Fingerprint
    c.text(10, 35, "(a) Fingerprint", BLACK, 1)
    c.rect(10, 50, 170, 210, DARK_BLUE, (240,245,255))
    for i in range(7):
        y = 70 + i*18
        for x in range(20, 160):
            yp = y + int(4*math.sin((x+i*8)*0.1))
            c.pixel(x, yp, MED_BLUE)
            if x % 12 == 0:
                c.pixel(x, yp-1, MED_GREEN)
                c.pixel(x+1, yp-1, MED_GREEN)
    c.text(15, 195, "QD: 5-20x SNR", MED_GREEN, 1)

    # (b) SERS
    c.text(185, 35, "(b) SERS Substrate", BLACK, 1)
    c.rect(185, 50, 345, 210, ORANGE, (255,248,240))
    for row in range(4):
        for col in range(4):
            nx = 210 + col*33
            ny = 75 + row*33
            c.circle(nx, ny, 8, ORANGE, LIGHT_ORANGE)
            if col < 3:
                c.hline(nx+8, nx+25, ny, RED)
    c.text(190, 195, "EF 10^6-10^10", RED, 1)

    # (c) Biosensor
    c.text(360, 35, "(c) Biosensor Array", BLACK, 1)
    c.rect(360, 50, 520, 210, DARK_GREEN, (240,255,240))
    sens_col = [MED_BLUE, RED, MED_GREEN, PURPLE, ORANGE, GOLD]
    sens_lbl = ["Bld", "Sal", "Sem", "Swe", "Uri", "DNA"]
    for i, (sc, sl) in enumerate(zip(sens_col, sens_lbl)):
        row, col = i//3, i%3
        sx = 375 + col*48
        sy = 65 + row*70
        c.rect(sx, sy, sx+35, sy+35, BLACK, sc)
        c.text(sx+3, sy+40, sl, BLACK, 1)

    # (d) Explosive
    c.text(535, 35, "(d) Explosive Detect", BLACK, 1)
    c.rect(535, 50, 690, 210, RED, (255,240,240))
    for row in range(3):
        for col in range(3):
            hx = 570 + col*38
            hy = 80 + row*38
            for a in range(6):
                a1 = math.radians(60*a)
                a2 = math.radians(60*(a+1))
                x1 = int(hx + 12*math.cos(a1))
                y1 = int(hy + 12*math.sin(a1))
                x2 = int(hx + 12*math.cos(a2))
                y2 = int(hy + 12*math.sin(a2))
                c.line(x1, y1, x2, y2, RED, 1)
    c.text(540, 195, "MOF: PPT level", RED, 1)

    # Bottom: response patterns
    c.text(10, 225, "Sensor Response Patterns:", BLACK, 1)
    c.rect(10, 240, 690, 420, LIGHT_GRAY, (250,250,250))
    analytes = ["TNT", "RDX", "Cocaine", "Fentanyl", "Blood"]
    random.seed(7)
    ch_colors = [MED_BLUE, MED_GREEN, ORANGE, PURPLE, RED, GOLD]
    for i, an in enumerate(analytes):
        by = 255 + i*32
        c.text(20, by+4, an, BLACK, 1)
        bx = 100
        for j in range(6):
            bar_l = random.randint(20, 80)
            c.fill_rect(bx, by, bx+bar_l, by+12, ch_colors[j])
            bx += bar_l + 3
    # Legend
    for j in range(6):
        c.fill_rect(100+j*70, 405, 115+j*70, 415, ch_colors[j])
        c.text(118+j*70, 407, f"Ch{j+1}", BLACK, 1)
    c.text(500, 405, ">95% accuracy", DARK_GREEN, 1)

    c.text(50, 435, "Figure 6: AI nanomaterials for forensic science", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_6.png'))
    print("  Figure_6.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    gen_fig5()
    gen_fig6()
    print(f"\nAll 6 figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz/1024:.1f} KB")


if __name__ == '__main__':
    main()
