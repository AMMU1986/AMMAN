#!/usr/bin/env python3
"""
Generate 4 scientific figure images (PNG) for the Agritourism & Regenerative Landscapes book.
Uses only Python standard library.
"""

import struct
import zlib
import math
import os
import random

OUTPUT_DIR = '/projects/sandbox/AMMAN/agritourism_figures'

# Colors
DARK_BLUE = (31, 78, 121)
MED_BLUE = (46, 117, 182)
LIGHT_BLUE = (155, 194, 230)
PALE_BLUE = (218, 232, 252)
DARK_GREEN = (56, 118, 29)
MED_GREEN = (84, 172, 64)
LIGHT_GREEN = (198, 224, 180)
PALE_GREEN = (232, 245, 220)
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
BROWN = (139, 90, 43)
LIGHT_BROWN = (210, 180, 140)
TEAL = (0, 128, 128)
LIGHT_TEAL = (180, 230, 230)


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
        for x in range(max(0, x1), min(self.w, x2+1)):
            self.pixel(x, y1, outline)
            self.pixel(x, y2, outline)
        for y in range(max(0, y1), min(self.h, y2+1)):
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
                self.pixel(x1+t if dy > dx else x1, y1 if dy > dx else y1+t, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2*err
            if e2 > -dy:
                err -= dy; x1 += sx
            if e2 < dx:
                err += dx; y1 += sy

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
    '&':[0b01100,0b10010,0b10100,0b01000,0b10101,0b10010,0b01101],
    '$':[0b00100,0b01111,0b10100,0b01110,0b00101,0b11110,0b00100],
    '#':[0b01010,0b01010,0b11111,0b01010,0b11111,0b01010,0b01010],
    '|':[0b00100,0b00100,0b00100,0b00100,0b00100,0b00100,0b00100],
    '[':[0b01110,0b01000,0b01000,0b01000,0b01000,0b01000,0b01110],
    ']':[0b01110,0b00010,0b00010,0b00010,0b00010,0b00010,0b01110],
    '_':[0b00000,0b00000,0b00000,0b00000,0b00000,0b00000,0b11111],
    ';':[0b00000,0b01100,0b01100,0b00000,0b01100,0b00100,0b01000],
    "'":[0b01100,0b00100,0b01000,0b00000,0b00000,0b00000,0b00000],
}


def gen_fig1():
    """Figure 1: Conceptual Framework - Synergy of Regenerative Agriculture and Agritourism"""
    c = PNGCanvas(800, 500)
    c.text_c(400, 10, "Figure 1: Conceptual Framework - Synergy of", BLACK, 2)
    c.text_c(400, 30, "Regenerative Agriculture and Agritourism", BLACK, 2)

    # Left circle: Regenerative Agriculture
    c.circle(230, 250, 140, DARK_GREEN, PALE_GREEN)
    c.text_c(180, 150, "REGENERATIVE", DARK_GREEN, 2)
    c.text_c(180, 170, "AGRICULTURE", DARK_GREEN, 2)
    c.text(100, 210, "- Soil Health", BLACK, 1)
    c.text(100, 225, "- Biodiversity", BLACK, 1)
    c.text(100, 240, "- Water Cycles", BLACK, 1)
    c.text(100, 255, "- Carbon Seq.", BLACK, 1)
    c.text(100, 270, "- Holistic Grazing", BLACK, 1)
    c.text(100, 285, "- Cover Cropping", BLACK, 1)

    # Right circle: Agritourism
    c.circle(570, 250, 140, DARK_BLUE, PALE_BLUE)
    c.text_c(620, 150, "AGRICULTURAL", DARK_BLUE, 2)
    c.text_c(620, 170, "TOURISM", DARK_BLUE, 2)
    c.text(530, 210, "- Farm Stays", BLACK, 1)
    c.text(530, 225, "- Farm-to-Table", BLACK, 1)
    c.text(530, 240, "- Education", BLACK, 1)
    c.text(530, 255, "- Cultural Events", BLACK, 1)
    c.text(530, 270, "- Nature Trails", BLACK, 1)
    c.text(530, 285, "- Workshops", BLACK, 1)

    # Overlap zone
    c.fill_rect(340, 200, 460, 300, LIGHT_GOLD)
    c.rect(340, 200, 460, 300, GOLD)
    c.text_c(400, 210, "SYNERGY", GOLD, 2)
    c.text(350, 235, "Revenue", BLACK, 1)
    c.text(350, 250, "Education", BLACK, 1)
    c.text(350, 265, "Community", BLACK, 1)
    c.text(350, 280, "Resilience", BLACK, 1)

    # Bottom outcomes
    c.rect(50, 380, 250, 470, DARK_GREEN, LIGHT_GREEN)
    c.text_c(150, 390, "ECOLOGICAL", BLACK, 2)
    c.text(60, 415, "Soil restoration", BLACK, 1)
    c.text(60, 430, "Biodiversity gain", BLACK, 1)
    c.text(60, 445, "Carbon storage", BLACK, 1)

    c.rect(300, 380, 500, 470, ORANGE, LIGHT_ORANGE)
    c.text_c(400, 390, "ECONOMIC", BLACK, 2)
    c.text(310, 415, "Revenue streams", BLACK, 1)
    c.text(310, 430, "Local employment", BLACK, 1)
    c.text(310, 445, "Market access", BLACK, 1)

    c.rect(550, 380, 750, 470, PURPLE, LIGHT_PURPLE)
    c.text_c(650, 390, "SOCIAL", BLACK, 2)
    c.text(560, 415, "Knowledge transfer", BLACK, 1)
    c.text(560, 430, "Cultural revival", BLACK, 1)
    c.text(560, 445, "Food literacy", BLACK, 1)

    # Arrows from synergy to outcomes
    c.arrow(400, 300, 150, 380, GRAY, 2, 6)
    c.arrow(400, 300, 400, 380, GRAY, 2, 6)
    c.arrow(400, 300, 650, 380, GRAY, 2, 6)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Conceptual_Framework.png'))
    print("  Figure_1 done")


def gen_fig2():
    """Figure 2: Farm Design Layout for Regeneration and Visitor Experience"""
    c = PNGCanvas(800, 500)
    c.text_c(400, 10, "Figure 2: Integrated Farm Design for", BLACK, 2)
    c.text_c(400, 30, "Regeneration and Visitor Experience", BLACK, 2)

    # Farm zones
    # Zone 1: Welcome/Visitor Hub
    c.rect(50, 60, 200, 160, DARK_BLUE, PALE_BLUE)
    c.text_c(125, 70, "ZONE 1:", DARK_BLUE, 2)
    c.text_c(125, 90, "Visitor Hub", DARK_BLUE, 1)
    c.text(60, 110, "- Parking", BLACK, 1)
    c.text(60, 125, "- Welcome Center", BLACK, 1)
    c.text(60, 140, "- Farm Shop", BLACK, 1)

    # Zone 2: Demonstration area
    c.rect(220, 60, 400, 160, DARK_GREEN, LIGHT_GREEN)
    c.text_c(310, 70, "ZONE 2:", DARK_GREEN, 2)
    c.text_c(310, 90, "Demo Fields", DARK_GREEN, 1)
    c.text(230, 110, "- Polycultures", BLACK, 1)
    c.text(230, 125, "- Cover Crops", BLACK, 1)
    c.text(230, 140, "- Compost Sites", BLACK, 1)

    # Zone 3: Nature/Biodiversity
    c.rect(420, 60, 600, 160, MED_GREEN, PALE_GREEN)
    c.text_c(510, 70, "ZONE 3:", MED_GREEN, 2)
    c.text_c(510, 90, "Biodiversity", MED_GREEN, 1)
    c.text(430, 110, "- Wildlife Hab.", BLACK, 1)
    c.text(430, 125, "- Bird Trails", BLACK, 1)
    c.text(430, 140, "- Wetlands", BLACK, 1)

    # Zone 4: Production
    c.rect(620, 60, 780, 160, BROWN, LIGHT_BROWN)
    c.text_c(700, 70, "ZONE 4:", BROWN, 2)
    c.text_c(700, 90, "Production", BROWN, 1)
    c.text(630, 110, "- Grazing Pad.", BLACK, 1)
    c.text(630, 125, "- Agroforestry", BLACK, 1)
    c.text(630, 140, "- No-till Fields", BLACK, 1)

    # Connecting trails (dotted lines)
    for x in range(200, 220):
        if x % 4 < 2:
            c.pixel(x, 110, ORANGE)
    for x in range(400, 420):
        if x % 4 < 2:
            c.pixel(x, 110, ORANGE)
    for x in range(600, 620):
        if x % 4 < 2:
            c.pixel(x, 110, ORANGE)

    # Visitor flow arrows
    c.arrow(200, 110, 220, 110, ORANGE, 2, 6)
    c.arrow(400, 110, 420, 110, ORANGE, 2, 6)
    c.arrow(600, 110, 620, 110, ORANGE, 2, 6)

    # Water management section
    c.rect(50, 185, 780, 300, TEAL, LIGHT_TEAL)
    c.text_c(400, 195, "WATER MANAGEMENT SYSTEM", TEAL, 2)
    # Swales
    for i in range(5):
        x = 100 + i * 140
        c.line(x, 230, x+100, 230, DARK_BLUE, 2)
        c.line(x, 230, x+20, 250, DARK_BLUE, 1)
        c.line(x+100, 230, x+80, 250, DARK_BLUE, 1)
        c.text(x+20, 255, "Swale " + str(i+1), BLACK, 1)
    c.text(60, 275, "Keyline Design: Water harvesting > Infiltration > Groundwater recharge", BLACK, 1)

    # Experience zones
    c.rect(50, 320, 270, 480, ORANGE, LIGHT_ORANGE)
    c.text_c(160, 330, "HANDS-ON ZONE", ORANGE, 2)
    c.text(60, 355, "- Soil workshops", BLACK, 1)
    c.text(60, 370, "- Planting days", BLACK, 1)
    c.text(60, 385, "- Harvest events", BLACK, 1)
    c.text(60, 400, "- Composting demos", BLACK, 1)
    c.text(60, 415, "- Seed saving", BLACK, 1)
    c.text(60, 440, "Capacity: 30 ppl", GRAY, 1)
    c.text(60, 455, "Duration: 2-4 hrs", GRAY, 1)

    c.rect(290, 320, 520, 480, PURPLE, LIGHT_PURPLE)
    c.text_c(405, 330, "CULINARY ZONE", PURPLE, 2)
    c.text(300, 355, "- Farm kitchen", BLACK, 1)
    c.text(300, 370, "- Dining pavilion", BLACK, 1)
    c.text(300, 385, "- Tasting events", BLACK, 1)
    c.text(300, 400, "- Cooking classes", BLACK, 1)
    c.text(300, 415, "- Preserving", BLACK, 1)
    c.text(300, 440, "Capacity: 50 ppl", GRAY, 1)
    c.text(300, 455, "Duration: 3-5 hrs", GRAY, 1)

    c.rect(540, 320, 780, 480, MED_BLUE, LIGHT_BLUE)
    c.text_c(660, 330, "LEARNING ZONE", MED_BLUE, 2)
    c.text(550, 355, "- Classroom space", BLACK, 1)
    c.text(550, 370, "- Citizen science", BLACK, 1)
    c.text(550, 385, "- Bird watching", BLACK, 1)
    c.text(550, 400, "- Soil monitoring", BLACK, 1)
    c.text(550, 415, "- School programs", BLACK, 1)
    c.text(550, 440, "Capacity: 40 ppl", GRAY, 1)
    c.text(550, 455, "Duration: 1-3 hrs", GRAY, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Farm_Design_Layout.png'))
    print("  Figure_2 done")


def gen_fig3():
    """Figure 3: Stakeholder Ecosystem and Policy Framework"""
    c = PNGCanvas(800, 500)
    c.text_c(400, 10, "Figure 3: Stakeholder Ecosystem and", BLACK, 2)
    c.text_c(400, 30, "Policy Framework for Regenerative Agritourism", BLACK, 2)

    # Central node: Regenerative Farm
    c.circle(400, 250, 55, DARK_GREEN, LIGHT_GREEN)
    c.text_c(400, 235, "REGENERATIVE", BLACK, 1)
    c.text_c(400, 248, "FARM", BLACK, 2)
    c.text_c(400, 268, "(Central Hub)", GRAY, 1)

    # Stakeholders around the central farm
    stakeholders = [
        ("Local Gov.", 150, 120, MED_BLUE, LIGHT_BLUE),
        ("Tourists", 400, 80, ORANGE, LIGHT_ORANGE),
        ("Nat'l Policy", 650, 120, PURPLE, LIGHT_PURPLE),
        ("Community", 130, 300, TEAL, LIGHT_TEAL),
        ("Educators", 250, 420, GOLD, LIGHT_GOLD),
        ("NGOs", 550, 420, RED, LIGHT_RED),
        ("Markets", 670, 300, BROWN, LIGHT_BROWN),
    ]

    for label, sx, sy, col, fill in stakeholders:
        c.circle(sx, sy, 40, col, fill)
        c.text_c(sx, sy-4, label, BLACK, 1)
        # Draw line to center
        dx = 400 - sx
        dy = 250 - sy
        d = math.sqrt(dx*dx + dy*dy)
        if d > 0:
            c.line(int(sx + dx/d*42), int(sy + dy/d*42),
                   int(400 - dx/d*57), int(250 - dy/d*57), GRAY, 1)

    # Policy framework box (right side)
    c.rect(540, 55, 790, 230, PURPLE)
    c.text_c(665, 60, "POLICY FRAMEWORK", PURPLE, 2)
    c.text(550, 85, "1. Tax Incentives", BLACK, 1)
    c.text(550, 100, "2. Grants/Subsidies", BLACK, 1)
    c.text(550, 115, "3. Zoning Support", BLACK, 1)
    c.text(550, 130, "4. Certification", BLACK, 1)
    c.text(550, 145, "5. Infrastructure", BLACK, 1)
    c.text(550, 160, "6. Training Programs", BLACK, 1)
    c.text(550, 175, "7. Market Access", BLACK, 1)
    c.text(550, 190, "8. Research Funding", BLACK, 1)
    c.text(550, 210, "Goal: Enable transition", GRAY, 1)

    # Infrastructure needs box (left side)
    c.rect(10, 55, 270, 200, MED_BLUE)
    c.text_c(140, 60, "INFRASTRUCTURE", MED_BLUE, 2)
    c.text(20, 85, "- Rural roads/access", BLACK, 1)
    c.text(20, 100, "- Broadband internet", BLACK, 1)
    c.text(20, 115, "- Waste management", BLACK, 1)
    c.text(20, 130, "- Water/sanitation", BLACK, 1)
    c.text(20, 145, "- Signage/waymarks", BLACK, 1)
    c.text(20, 160, "- Safety systems", BLACK, 1)
    c.text(20, 180, "Priority: Connectivity", GRAY, 1)

    # Bottom: Knowledge flows
    c.rect(100, 460, 700, 495, GOLD, LIGHT_GOLD)
    c.text_c(400, 470, "KNOWLEDGE FLOW: Farm > Community > Schools > Policy > Market > Farm", BLACK, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Stakeholder_Ecosystem.png'))
    print("  Figure_3 done")


def gen_fig4():
    """Figure 4: Challenges and Resilience Model"""
    c = PNGCanvas(800, 500)
    c.text_c(400, 10, "Figure 4: Challenges, Resilience Strategies,", BLACK, 2)
    c.text_c(400, 30, "and Holistic Model for Sustainable Agritourism", BLACK, 2)

    # Left panel: Challenges
    c.rect(20, 55, 260, 340, RED, LIGHT_RED)
    c.text_c(140, 62, "CHALLENGES", RED, 2)
    c.text(30, 85, "1. Greenwashing", BLACK, 1)
    c.text(30, 100, "2. Climate extremes", BLACK, 1)
    c.text(30, 115, "3. Overcrowding", BLACK, 1)
    c.text(30, 130, "4. Infrastructure", BLACK, 1)
    c.text(30, 145, "5. Equity/Access", BLACK, 1)
    c.text(30, 160, "6. Policy gaps", BLACK, 1)
    c.text(30, 175, "7. Seasonal income", BLACK, 1)
    c.text(30, 190, "8. Scale limits", BLACK, 1)

    # Severity bars
    sevs = [7, 9, 6, 8, 7, 8, 6, 5]
    for i, s in enumerate(sevs):
        y = 85 + i * 15
        bar_w = int(s * 8)
        c.fill_rect(175, y, 175 + bar_w, y + 10, RED)
    c.text(30, 215, "Severity (1-10):", BLACK, 1)
    c.fill_rect(130, 215, 180, 225, RED)
    c.text(185, 215, "High", BLACK, 1)

    # Resilience strategies
    c.text(30, 245, "ADAPTIVE CAPACITY:", DARK_GREEN, 1)
    c.text(30, 265, "+ Crop diversity", DARK_GREEN, 1)
    c.text(30, 280, "+ Water buffering", DARK_GREEN, 1)
    c.text(30, 295, "+ Income diversity", DARK_GREEN, 1)
    c.text(30, 310, "+ Soil carbon", DARK_GREEN, 1)
    c.text(30, 325, "+ Community bonds", DARK_GREEN, 1)

    # Center: Resilience model (bar chart)
    c.rect(280, 55, 530, 340, DARK_GREEN, PALE_GREEN)
    c.text_c(405, 62, "RESILIENCE INDEX", DARK_GREEN, 2)

    # Bar chart of resilience dimensions
    dims = [("Ecol.", 85), ("Econ.", 70), ("Soc.", 75), ("Gov.", 60), ("Infra.", 55)]
    for i, (label, val) in enumerate(dims):
        bx = 300 + i * 42
        bh = int(val * 2.2)
        c.fill_rect(bx, 310 - bh, bx + 30, 310, MED_GREEN)
        c.rect(bx, 310 - bh, bx + 30, 310, DARK_GREEN)
        c.text(bx, 315, label, BLACK, 1)
        c.text(bx+5, 310 - bh - 12, str(val), BLACK, 1)

    c.text(290, 335, "Score range: 0-100", GRAY, 1)

    # Right panel: Holistic Model
    c.rect(550, 55, 790, 340, PURPLE, LIGHT_PURPLE)
    c.text_c(670, 62, "HOLISTIC MODEL", PURPLE, 2)

    # Concentric circles representing layers
    c.circle(670, 200, 100, PURPLE, LIGHT_PURPLE)
    c.circle(670, 200, 70, MED_BLUE, LIGHT_BLUE)
    c.circle(670, 200, 40, DARK_GREEN, LIGHT_GREEN)
    c.text_c(670, 193, "FARM", WHITE, 2)
    c.text_c(670, 165, "Community", BLACK, 1)
    c.text_c(670, 115, "Policy/Market", BLACK, 1)

    c.text(560, 310, "Inside-out approach:", GRAY, 1)
    c.text(560, 325, "Farm > Community > System", GRAY, 1)

    # Bottom: Timeline/roadmap
    c.rect(20, 360, 790, 490, GOLD, LIGHT_GOLD)
    c.text_c(400, 365, "IMPLEMENTATION ROADMAP", GOLD, 2)

    phases = [
        ("Year 1-2", "Assessment\nPlanning\nPilot"),
        ("Year 3-4", "Transition\nInfrastructure\nTraining"),
        ("Year 5-7", "Scaling\nCertification\nNetworking"),
        ("Year 8+", "Maturity\nReplication\nAdvocacy"),
    ]
    for i, (yr, desc) in enumerate(phases):
        bx = 50 + i * 185
        c.rect(bx, 395, bx + 160, 480, BLACK)
        c.text_c(bx + 80, 400, yr, BLACK, 2)
        lines = desc.split('\n')
        for j, ln in enumerate(lines):
            c.text(bx + 10, 425 + j * 15, ln, BLACK, 1)
        if i < 3:
            c.arrow(bx + 160, 437, bx + 185, 437, ORANGE, 2, 6)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Challenges_Resilience.png'))
    print("  Figure_4 done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating agritourism figures...")
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
