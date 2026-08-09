#!/usr/bin/env python3
"""
Generate 4 scientific figure images (PNG) for Chapter 1: AI-Driven Smart Computing.
Uses only Python standard library - PNGCanvas approach.
"""

import struct
import zlib
import math
import os
import random

OUTPUT_DIR = '/projects/sandbox/AMMAN/smart_computing_figures'

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
TEAL = (0, 128, 128)
LIGHT_TEAL = (180, 230, 230)
DARK_RED = (139, 0, 0)
NAVY = (0, 0, 128)



class PNGCanvas:
    """Fast PNG canvas using bytearray."""

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

    def rounded_rect(self, x1, y1, x2, y2, r, outline, fill=None):
        if fill:
            self.fill_rect(x1+r, y1, x2-r, y2, fill)
            self.fill_rect(x1, y1+r, x2, y2-r, fill)
            for cy, cx_c in [(y1+r, x1+r), (y1+r, x2-r), (y2-r, x1+r), (y2-r, x2-r)]:
                for dy in range(-r, r+1):
                    x_span = int(math.sqrt(max(0, r*r - dy*dy)))
                    self.hline(cx_c - x_span, cx_c + x_span, cy + dy, fill)
        self.hline(x1+r, x2-r, y1, outline)
        self.hline(x1+r, x2-r, y2, outline)
        self.vline(x1, y1+r, y2-r, outline)
        self.vline(x2, y1+r, y2-r, outline)

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
    '|':[0b00100,0b00100,0b00100,0b00100,0b00100,0b00100,0b00100],
    '[':[0b01110,0b01000,0b01000,0b01000,0b01000,0b01000,0b01110],
    ']':[0b01110,0b00010,0b00010,0b00010,0b00010,0b00010,0b01110],
    '_':[0b00000,0b00000,0b00000,0b00000,0b00000,0b00000,0b11111],
    '&':[0b01100,0b10010,0b10100,0b01000,0b10101,0b10010,0b01101],
    '#':[0b01010,0b01010,0b11111,0b01010,0b11111,0b01010,0b01010],
}



def gen_fig1():
    """Figure 1: Architecture of AI-Driven Smart Computing Systems"""
    c = PNGCanvas(800, 550, (250, 252, 255))
    c.text_c(400, 10, "Architecture of AI-Driven Smart Computing Systems", BLACK, 2)

    # Five layers stacked
    layers = [
        ("APPLICATION LAYER", "Decision Support, User Interfaces, Domain Services", DARK_BLUE, PALE_BLUE),
        ("INTELLIGENCE LAYER", "ML Models, Reasoning Engines, Knowledge Graphs", PURPLE, LIGHT_PURPLE),
        ("DATA LAYER", "Data Lakes, Stream Processing, Feature Stores", DARK_GREEN, LIGHT_GREEN),
        ("NETWORK LAYER", "5G/6G, Edge Nodes, Fog Computing", ORANGE, LIGHT_ORANGE),
        ("PERCEPTION LAYER", "Sensors, IoT Devices, Data Acquisition", RED, LIGHT_RED),
    ]
    ly = 50
    for name, desc, outline, fill in layers:
        c.rect(80, ly, 720, ly+65, outline, fill)
        c.text_c(400, ly+12, name, BLACK, 2)
        c.text_c(400, ly+38, desc, GRAY, 1)
        ly += 80
        if ly < 430:
            # Draw arrows between layers
            c.arrow(400, ly-12, 400, ly+2, GRAY, 2, 6)

    # Side annotations
    # Left: Data Flow Up
    c.arrow(45, 440, 45, 70, MED_BLUE, 2, 8)
    c.text(15, 240, "Data", MED_BLUE, 1)
    c.text(15, 252, "Flow", MED_BLUE, 1)

    # Right: Intelligence Flow Down
    c.arrow(755, 70, 755, 440, ORANGE, 2, 8)
    c.text(738, 240, "Intel", ORANGE, 1)
    c.text(738, 252, "Flow", ORANGE, 1)

    # Bottom section: key components
    c.rect(80, 465, 280, 530, DARK_BLUE, PALE_BLUE)
    c.text_c(180, 475, "Cloud Computing", BLACK, 1)
    c.text_c(180, 492, "GPU/TPU Clusters", GRAY, 1)
    c.text_c(180, 507, "Scalable Storage", GRAY, 1)

    c.rect(310, 465, 500, 530, DARK_GREEN, LIGHT_GREEN)
    c.text_c(405, 475, "Edge Computing", BLACK, 1)
    c.text_c(405, 492, "Local Inference", GRAY, 1)
    c.text_c(405, 507, "Low Latency", GRAY, 1)

    c.rect(530, 465, 720, 530, PURPLE, LIGHT_PURPLE)
    c.text_c(625, 475, "IoT Ecosystem", BLACK, 1)
    c.text_c(625, 492, "75B+ Devices", GRAY, 1)
    c.text_c(625, 507, "Zettabytes/Year", GRAY, 1)

    c.text_c(400, 540, "Figure 1: Layered architecture of AI-driven smart computing systems", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Architecture.png'))
    print("  Figure_1_Architecture.png done")



def gen_fig2():
    """Figure 2: Convergence of AI Technologies in Smart Computing Ecosystem"""
    c = PNGCanvas(800, 550, (252, 252, 255))
    c.text_c(400, 10, "Convergence of AI Technologies in Smart Computing", BLACK, 2)

    # Central hub
    c.circle(400, 275, 55, DARK_BLUE, PALE_BLUE)
    c.text_c(400, 262, "SMART", BLACK, 2)
    c.text_c(400, 280, "COMPUTING", BLACK, 1)

    # Surrounding technology nodes
    nodes = [
        ("AI/ML", 400, 100, PURPLE, LIGHT_PURPLE),
        ("Cloud", 580, 170, MED_BLUE, LIGHT_BLUE),
        ("Big Data", 620, 350, DARK_GREEN, LIGHT_GREEN),
        ("IoT", 400, 440, ORANGE, LIGHT_ORANGE),
        ("Edge", 180, 350, RED, LIGHT_RED),
        ("5G/6G", 190, 170, TEAL, LIGHT_TEAL),
    ]

    for label, nx, ny, outline, fill in nodes:
        c.circle(nx, ny, 40, outline, fill)
        c.text_c(nx, ny-4, label, BLACK, 2)
        # Draw connection to center
        dx, dy = 400-nx, 275-ny
        d = math.sqrt(dx*dx + dy*dy)
        if d > 0:
            sx = int(nx + dx/d * 42)
            sy = int(ny + dy/d * 42)
            ex = int(400 - dx/d * 57)
            ey = int(275 - dy/d * 57)
            c.line(sx, sy, ex, ey, GRAY, 2)

    # Interconnections between adjacent nodes (ring)
    for i in range(len(nodes)):
        j = (i+1) % len(nodes)
        nx1, ny1 = nodes[i][1], nodes[i][2]
        nx2, ny2 = nodes[j][1], nodes[j][2]
        dx, dy = nx2-nx1, ny2-ny1
        d = math.sqrt(dx*dx + dy*dy)
        if d > 0:
            sx = int(nx1 + dx/d * 42)
            sy = int(ny1 + dy/d * 42)
            ex = int(nx2 - dx/d * 42)
            ey = int(ny2 - dy/d * 42)
            c.line(sx, sy, ex, ey, LIGHT_GRAY, 1)

    # Data flow annotations
    c.text(30, 500, "Data flows from IoT through Edge/Cloud, processed by AI/ML,", BLACK, 1)
    c.text(30, 515, "delivering insights via 5G/6G in continuous feedback loops.", BLACK, 1)

    c.text_c(400, 540, "Figure 2: Convergence of AI technologies in the smart computing ecosystem", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Convergence.png'))
    print("  Figure_2_Convergence.png done")



def gen_fig3():
    """Figure 3: AI Applications Across Industry Sectors"""
    c = PNGCanvas(800, 550, (255, 253, 250))
    c.text_c(400, 10, "AI Applications Across Industry Sectors", BLACK, 2)

    # Grid of sector boxes
    sectors = [
        ("Healthcare", ["Diagnostics", "Drug Discovery", "Personalized Med"], DARK_BLUE, PALE_BLUE),
        ("Manufacturing", ["Predictive Maint.", "Quality Control", "Digital Twins"], DARK_GREEN, LIGHT_GREEN),
        ("Transportation", ["Autonomous Vehicles", "Traffic Opt.", "Route Planning"], PURPLE, LIGHT_PURPLE),
        ("Education", ["Adaptive Learning", "AI Tutoring", "Assessment"], ORANGE, LIGHT_ORANGE),
        ("Agriculture", ["Crop Monitoring", "Disease Detect.", "Yield Predict."], MED_GREEN, LIGHT_GREEN),
        ("Finance", ["Fraud Detection", "Algo Trading", "Risk Assessment"], RED, LIGHT_RED),
        ("Smart Cities", ["Energy Opt.", "Public Safety", "Infrastructure"], TEAL, LIGHT_TEAL),
        ("Energy", ["Grid Optimization", "Renewable Forecast", "Demand Response"], GOLD, LIGHT_GOLD),
    ]

    # 2 rows x 4 cols
    for idx, (name, apps, outline, fill) in enumerate(sectors):
        row = idx // 4
        col = idx % 4
        bx = 30 + col * 190
        by = 45 + row * 240
        c.rect(bx, by, bx+175, by+210, outline, fill)
        c.text_c(bx+87, by+10, name, BLACK, 2)
        c.hline(bx+10, bx+165, by+30, outline)
        for ai, app in enumerate(apps):
            c.text(bx+10, by+42+ai*18, "- " + app, BLACK, 1)

        # Add a bar chart mini-visualization
        chart_y = by + 110
        c.text(bx+10, chart_y, "AI Impact Level:", GRAY, 1)
        random.seed(idx * 7 + 42)
        bar_w = random.randint(100, 155)
        c.fill_rect(bx+10, chart_y+14, bx+10+bar_w, chart_y+24, outline)
        pct = int(bar_w / 155 * 100)
        c.text(bx+10+bar_w+5, chart_y+16, f"{pct}%", BLACK, 1)

        # Growth indicator
        c.text(bx+10, chart_y+35, "CAGR:", GRAY, 1)
        growth = random.randint(18, 45)
        c.text(bx+55, chart_y+35, f"{growth}%", outline, 1)
        c.text(bx+10, chart_y+52, "Market Size:", GRAY, 1)
        mkt = random.randint(5, 120)
        c.text(bx+85, chart_y+52, f"${mkt}B", outline, 1)

    c.text_c(400, 530, "Figure 3: AI application domains across major industry sectors", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Applications.png'))
    print("  Figure_3_Applications.png done")



def gen_fig4():
    """Figure 4: Future AI Computing Architecture and Sustainability Framework"""
    c = PNGCanvas(800, 550, (252, 255, 252))
    c.text_c(400, 10, "Sustainable AI Computing Architecture Framework", BLACK, 2)

    # Four quadrants
    # Top-left: Hardware Efficiency
    c.rect(20, 40, 385, 255, DARK_BLUE, PALE_BLUE)
    c.text_c(200, 50, "Hardware Efficiency", BLACK, 2)
    items_hw = ["Chiplet Architectures", "Wafer-Scale Integration",
                "3D Stacking", "Neuromorphic Chips", "Optical Interconnects"]
    for i, item in enumerate(items_hw):
        c.text(40, 75+i*28, ">> " + item, DARK_BLUE, 1)
    # Mini bar chart
    vals = [2, 5, 10, 50, 100]
    for i, v in enumerate(vals):
        bw = int(v / 100 * 160)
        c.fill_rect(40, 215-i*28-12, 40+bw, 215-i*28, MED_BLUE)

    # Top-right: Algorithmic Optimization
    c.rect(415, 40, 780, 255, DARK_GREEN, LIGHT_GREEN)
    c.text_c(597, 50, "Algorithmic Optimization", BLACK, 2)
    items_alg = ["Model Compression", "Mixture-of-Experts",
                 "Efficient Attention", "Knowledge Distillation", "Progressive Training"]
    for i, item in enumerate(items_alg):
        c.text(435, 75+i*28, ">> " + item, DARK_GREEN, 1)
    # Compression ratio visual
    ratios = [4, 8, 16, 32, 64]
    for i, r in enumerate(ratios):
        bw = int(r / 64 * 160)
        c.fill_rect(435, 215-i*28-12, 435+bw, 215-i*28, MED_GREEN)

    # Bottom-left: Energy & Sustainability
    c.rect(20, 270, 385, 490, ORANGE, LIGHT_ORANGE)
    c.text_c(200, 280, "Energy and Sustainability", BLACK, 2)
    items_en = ["Renewable Data Centers", "Carbon-Neutral Training",
                "Energy-Proportional Computing", "Green AI Metrics", "Lifecycle Assessment"]
    for i, item in enumerate(items_en):
        c.text(40, 305+i*28, ">> " + item, (180, 80, 0), 1)
    # Energy reduction curve
    for x in range(40, 350):
        t = (x-40)/310.0
        y = int(470 - 80*math.exp(-3*t))
        c.pixel(x, y, RED)
        c.pixel(x, y+1, RED)
    c.text(200, 478, "Energy per FLOP reduction", GRAY, 1)

    # Bottom-right: Resilience & Scale
    c.rect(415, 270, 780, 490, PURPLE, LIGHT_PURPLE)
    c.text_c(597, 280, "Resilience and Scale", BLACK, 2)
    items_res = ["Fault Tolerance", "Self-Healing Systems",
                 "ML Observability", "Chaos Engineering", "Antifragile Design"]
    for i, item in enumerate(items_res):
        c.text(435, 305+i*28, ">> " + item, PURPLE, 1)
    # Uptime visualization
    c.text(435, 445, "Target Availability:", GRAY, 1)
    c.fill_rect(435, 460, 735, 475, MED_BLUE)
    c.text(610, 462, "99.999%", WHITE, 1)

    # Center connector
    c.circle(400, 265, 25, GOLD, LIGHT_GOLD)
    c.text_c(400, 258, "AI", BLACK, 2)

    # Arrows from center to quadrants
    c.arrow(380, 255, 300, 200, GOLD, 1, 5)
    c.arrow(420, 255, 500, 200, GOLD, 1, 5)
    c.arrow(380, 278, 300, 340, GOLD, 1, 5)
    c.arrow(420, 278, 500, 340, GOLD, 1, 5)

    # Bottom label
    c.text_c(400, 505, "Roadmap: 2 TFLOPS/W (2024) -> 100 TFLOPS/W (2030+)", BLACK, 1)
    c.text_c(400, 520, "Training Energy: 100 GWh (2024) -> <1 GWh (2030+)", BLACK, 1)
    c.text_c(400, 538, "Figure 4: Multi-dimensional framework for sustainable AI computing", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Sustainability.png'))
    print("  Figure_4_Sustainability.png done")



def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating figures for Chapter 1: AI-Driven Smart Computing...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print(f"\nAll 4 figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz/1024:.1f} KB")


if __name__ == '__main__':
    main()
