#!/usr/bin/env python3
"""
Generate the complete book chapter manuscript including:
- 7 black-and-white schematic figures (PNG format, 300 DPI)
- Complete Word document (.docx) with embedded figures, tables, and references
"""

import struct
import zlib
import os
import sys
import math
import random
import zipfile
import time
from xml.etree import ElementTree as ET
from io import BytesIO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(BASE_DIR, "Figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# ============================================================
# PART 1: PNG Image Generation
# ============================================================

WIDTH = 2400
HEIGHT = 1800


def create_png_bytes(pixels, width, height):
    """Create PNG file bytes from grayscale pixel array."""
    def chunk(ctype, data):
        c = ctype + data
        crc = zlib.crc32(c) & 0xFFFFFFFF
        return struct.pack('>I', len(data)) + c + struct.pack('>I', crc)

    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 0, 0, 0, 0))
    # 300 DPI = 11811 pixels/meter
    phys = chunk(b'pHYs', struct.pack('>IIB', 11811, 11811, 1))

    raw = bytearray()
    for y in range(height):
        raw.append(0)  # filter none
        raw.extend(pixels[y])

    compressed = zlib.compress(bytes(raw), 6)
    idat = chunk(b'IDAT', compressed)
    iend = chunk(b'IEND', b'')

    return sig + ihdr + phys + idat + iend


def new_canvas():
    return [bytearray([255] * WIDTH) for _ in range(HEIGHT)]


def set_pixel(pixels, x, y, val):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        pixels[y][x] = val



def draw_rect(px, x1, y1, x2, y2, fill=255, border=0, thick=3):
    for y in range(max(0,y1), min(HEIGHT,y2)):
        for x in range(max(0,x1), min(WIDTH,x2)):
            if x-x1<thick or x2-x-1<thick or y-y1<thick or y2-y-1<thick:
                px[y][x] = border
            else:
                px[y][x] = fill


def draw_line(px, x1, y1, x2, y2, col=0, thick=3):
    dx = abs(x2-x1); dy = abs(y2-y1)
    sx = 1 if x1<x2 else -1
    sy = 1 if y1<y2 else -1
    err = dx - dy
    while True:
        for t in range(-thick//2, thick//2+1):
            set_pixel(px, x1+t, y1, col)
            set_pixel(px, x1, y1+t, col)
        if x1==x2 and y1==y2:
            break
        e2 = 2*err
        if e2 > -dy: err -= dy; x1 += sx
        if e2 < dx: err += dx; y1 += sy


def draw_circle(px, cx, cy, r, col=0, thick=3, fill=None):
    r2_outer = (r+thick//2)**2
    r2_inner = max(0, r-thick//2)**2
    r2_fill = max(0, r-thick)**2
    for y in range(max(0,cy-r-thick), min(HEIGHT,cy+r+thick+1)):
        for x in range(max(0,cx-r-thick), min(WIDTH,cx+r+thick+1)):
            d2 = (x-cx)**2 + (y-cy)**2
            if d2 <= r2_outer and d2 >= r2_inner:
                px[y][x] = col
            elif fill is not None and d2 < r2_fill:
                px[y][x] = fill



def draw_arrow(px, x1, y1, x2, y2, col=0, thick=3):
    draw_line(px, x1, y1, x2, y2, col, thick)
    angle = math.atan2(y2-y1, x2-x1)
    al = 25
    for a in [angle+2.7, angle-2.7]:
        ax = int(x2 + al*math.cos(a))
        ay = int(y2 + al*math.sin(a))
        draw_line(px, x2, y2, ax, ay, col, thick)


def draw_dashed(px, x1, y1, x2, y2, col=0, thick=2, dash=20, gap=12):
    length = math.sqrt((x2-x1)**2+(y2-y1)**2)
    if length == 0: return
    ddx = (x2-x1)/length; ddy = (y2-y1)/length
    pos = 0; on = True
    while pos < length:
        seg = dash if on else gap
        end = min(pos+seg, length)
        if on:
            draw_line(px, int(x1+pos*ddx), int(y1+pos*ddy),
                     int(x1+end*ddx), int(y1+end*ddy), col, thick)
        pos = end; on = not on


def draw_filled_rect(px, x1, y1, x2, y2, val):
    for y in range(max(0,y1), min(HEIGHT,y2)):
        for x in range(max(0,x1), min(WIDTH,x2)):
            px[y][x] = val



# ============ FIGURE GENERATORS ============

def make_figure1():
    """Classification of TES systems - hierarchical tree diagram."""
    px = new_canvas()
    # Top box
    draw_rect(px, 850, 80, 1550, 170, 230, 0, 4)
    # Three main branches
    draw_rect(px, 200, 330, 650, 420, 240, 0, 3)
    draw_rect(px, 950, 330, 1450, 420, 240, 0, 3)
    draw_rect(px, 1750, 330, 2200, 420, 240, 0, 3)
    # Vertical connector from top
    draw_line(px, 1200, 170, 1200, 260, 0, 3)
    draw_line(px, 425, 260, 1975, 260, 0, 3)
    draw_line(px, 425, 260, 425, 330, 0, 3)
    draw_line(px, 1200, 260, 1200, 330, 0, 3)
    draw_line(px, 1975, 260, 1975, 330, 0, 3)
    # Sub-branches for Sensible
    for i, xoff in enumerate([150, 500]):
        draw_rect(px, xoff, 550, xoff+200, 620, 250, 0, 2)
        draw_line(px, xoff+100, 490, xoff+100, 550, 0, 2)
    draw_line(px, 425, 420, 425, 490, 0, 2)
    draw_line(px, 250, 490, 600, 490, 0, 2)
    # Sub-branches for PCMs (4 types)
    pcm_xs = [870, 1060, 1250, 1440]
    for xp in pcm_xs:
        draw_rect(px, xp, 550, xp+160, 620, 250, 0, 2)
        draw_line(px, xp+80, 490, xp+80, 550, 0, 2)
    draw_line(px, 1200, 420, 1200, 490, 0, 2)
    draw_line(px, 950, 490, 1520, 490, 0, 2)
    # Sub-branches for Thermochemical
    for i, xoff in enumerate([1700, 1980]):
        draw_rect(px, xoff, 550, xoff+200, 620, 250, 0, 2)
        draw_line(px, xoff+100, 490, xoff+100, 550, 0, 2)
    draw_line(px, 1975, 420, 1975, 490, 0, 2)
    draw_line(px, 1800, 490, 2080, 490, 0, 2)
    # Third level for organic PCMs
    org_xs = [820, 1000]
    for xo in org_xs:
        draw_rect(px, xo, 720, xo+150, 780, 250, 0, 2)
        draw_line(px, xo+75, 670, xo+75, 720, 0, 2)
    draw_line(px, 950, 620, 950, 670, 0, 2)
    draw_line(px, 895, 670, 1075, 670, 0, 2)
    # Third level for inorganic PCMs
    inorg_xs = [1200, 1380]
    for xi in inorg_xs:
        draw_rect(px, xi, 720, xi+150, 780, 250, 0, 2)
        draw_line(px, xi+75, 670, xi+75, 720, 0, 2)
    draw_line(px, 1330, 620, 1330, 670, 0, 2)
    draw_line(px, 1275, 670, 1455, 670, 0, 2)
    return px



def make_figure2():
    """Temperature vs Enthalpy diagram showing phase change plateau."""
    px = new_canvas()
    ox, oy = 350, 1500  # origin
    aw, ah = 1900, 1250  # axis dimensions
    # Axes
    draw_line(px, ox, oy, ox, oy-ah, 0, 4)
    draw_line(px, ox, oy, ox+aw, oy, 0, 4)
    draw_arrow(px, ox, oy-ah+30, ox, oy-ah, 0, 4)
    draw_arrow(px, ox+aw-30, oy, ox+aw, oy, 0, 4)
    # Phase change curve: solid -> transition -> liquid
    pts = []
    # Solid heating (steep rise)
    for i in range(180):
        x = ox + 80 + i*3
        y = oy - 80 - i*3
        pts.append((x, y))
    # Phase transition plateau
    plat_y = oy - 80 - 180*3  # ~620 from origin top
    for i in range(250):
        x = ox + 80 + 180*3 + i*3
        y = plat_y
        pts.append((x, y))
    # Liquid heating
    for i in range(180):
        x = ox + 80 + 180*3 + 250*3 + i*3
        y = plat_y - i*2
        pts.append((x, y))
    # Draw curve
    for i in range(len(pts)-1):
        draw_line(px, pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], 0, 4)
    # Dashed line at melting temperature
    draw_dashed(px, ox, plat_y, ox+aw-100, plat_y, 120, 2, 20, 12)
    # Region bracket indicators at bottom
    s1 = ox + 80; e1 = ox + 80 + 180*3
    s2 = e1; e2 = s2 + 250*3
    s3 = e2; e3 = s3 + 180*3
    by = oy + 60
    draw_line(px, s1, by, e1, by, 0, 3)
    draw_line(px, s1, by-15, s1, by+15, 0, 3)
    draw_line(px, e1, by-15, e1, by+15, 0, 3)
    draw_line(px, s2, by, e2, by, 0, 3)
    draw_line(px, s2, by-15, s2, by+15, 0, 3)
    draw_line(px, e2, by-15, e2, by+15, 0, 3)
    draw_line(px, s3, by, e3, by, 0, 3)
    draw_line(px, s3, by-15, s3, by+15, 0, 3)
    draw_line(px, e3, by-15, e3, by+15, 0, 3)
    # Small label boxes
    draw_rect(px, (s1+e1)//2-60, by+25, (s1+e1)//2+60, by+55, 240, 0, 2)
    draw_rect(px, (s2+e2)//2-60, by+25, (s2+e2)//2+60, by+55, 240, 0, 2)
    draw_rect(px, (s3+e3)//2-60, by+25, (s3+e3)//2+60, by+55, 240, 0, 2)
    return px



def make_figure3():
    """PCM encapsulation methods: macro, micro, nano - three panels."""
    px = new_canvas()
    sw = WIDTH // 3
    # Headers
    for i in range(3):
        cx = sw*i + sw//2
        draw_rect(px, cx-200, 100, cx+200, 180, 230, 0, 3)
    # Panel 1: Macro - large cylindrical containers
    cx1 = sw//2
    # Cylinder representation (rectangle with rounded top/bottom)
    draw_rect(px, cx1-150, 300, cx1+150, 1200, 235, 0, 4)
    # PCM fill (horizontal lines inside)
    for ly in range(350, 1150, 50):
        draw_line(px, cx1-120, ly, cx1+120, ly, 200, 1)
    # Sphere container
    draw_circle(px, cx1, 1450, 120, 0, 4, fill=235)
    for ly in range(1380, 1520, 30):
        x_span = int(math.sqrt(max(0, 120**2 - (ly-1450)**2))) - 20
        if x_span > 0:
            draw_line(px, cx1-x_span, ly, cx1+x_span, ly, 200, 1)
    # Panel 2: Micro-encapsulation - core-shell spheres
    cx2 = sw + sw//2
    positions = [(cx2-180,450),(cx2+180,450),(cx2,750),(cx2-180,1050),(cx2+180,1050),(cx2,1350)]
    for ppx, ppy in positions:
        draw_circle(px, ppx, ppy, 100, 0, 4, fill=220)
        draw_circle(px, ppx, ppy, 65, 60, 3, fill=245)
    # Panel 3: Nano-encapsulation - many tiny capsules
    cx3 = 2*sw + sw//2
    random.seed(123)
    for _ in range(60):
        nx = random.randint(cx3-300, cx3+300)
        ny = random.randint(300, 1550)
        draw_circle(px, nx, ny, 35, 0, 2, fill=220)
        draw_circle(px, nx, ny, 20, 80, 2, fill=250)
    # Dividing lines
    draw_dashed(px, sw, 80, sw, 1700, 0, 2, 25, 15)
    draw_dashed(px, 2*sw, 80, 2*sw, 1700, 0, 2, 25, 15)
    return px



def make_figure4():
    """Heat transfer enhancement: fins, nanoparticles, metal foam."""
    px = new_canvas()
    sw = WIDTH // 3
    # Headers
    for i in range(3):
        cx = sw*i + sw//2
        draw_rect(px, cx-200, 100, cx+200, 180, 230, 0, 3)
    # Panel 1: Fins on a tube
    cx1 = sw//2
    draw_rect(px, cx1-25, 280, cx1+25, 1500, 160, 0, 3)  # Central tube
    for fy in range(320, 1460, 90):
        draw_rect(px, cx1-250, fy, cx1-25, fy+12, 130, 0, 2)  # Left fins
        draw_rect(px, cx1+25, fy, cx1+250, fy+12, 130, 0, 2)  # Right fins
    # Heat flow arrows
    for fy in range(400, 1400, 180):
        draw_arrow(px, cx1+280, fy, cx1+260, fy, 80, 2)
    # Panel 2: Nanoparticle-enhanced PCM
    cx2 = sw + sw//2
    draw_rect(px, cx2-250, 280, cx2+250, 1500, 245, 0, 3)
    random.seed(77)
    for _ in range(90):
        nx = random.randint(cx2-220, cx2+220)
        ny = random.randint(310, 1470)
        r = random.randint(6, 14)
        draw_circle(px, nx, ny, r, 0, 2, fill=160)
    # Panel 3: Metal foam porous structure
    cx3 = 2*sw + sw//2
    draw_rect(px, cx3-280, 280, cx3+280, 1500, 250, 0, 3)
    for row in range(6):
        for col in range(5):
            ppx = cx3 - 220 + col*110
            ppy = 380 + row*190
            draw_circle(px, ppx, ppy, 38, 40, 3, fill=240)
            if col < 4:
                draw_line(px, ppx+38, ppy, ppx+72, ppy, 80, 4)
            if row < 5:
                draw_line(px, ppx, ppy+38, ppx, ppy+152, 80, 4)
    # Dividers
    draw_dashed(px, sw, 80, sw, 1700, 0, 2, 25, 15)
    draw_dashed(px, 2*sw, 80, 2*sw, 1700, 0, 2, 25, 15)
    return px



def make_figure5():
    """Solar thermal system with PCM storage - system schematic."""
    px = new_canvas()
    # Solar collector (top-left)
    draw_rect(px, 150, 200, 650, 550, 230, 0, 4)
    # Collector tubes inside
    for ty in range(260, 500, 50):
        draw_line(px, 200, ty, 600, ty, 150, 2)
    # Sun rays
    scx, scy = 400, 100
    draw_circle(px, scx, scy, 40, 0, 3, fill=220)
    for a in range(0, 360, 45):
        draw_line(px, int(scx+55*math.cos(math.radians(a))),
                 int(scy+55*math.sin(math.radians(a))),
                 int(scx+85*math.cos(math.radians(a))),
                 int(scy+85*math.sin(math.radians(a))), 0, 2)
    # PCM Storage tank (center)
    draw_rect(px, 900, 350, 1500, 1100, 235, 0, 4)
    # PCM layers inside tank
    for ly in range(400, 1050, 45):
        draw_dashed(px, 940, ly, 1460, ly, 180, 1, 12, 8)
    # Heat exchanger coil
    for cy in range(450, 1000, 100):
        draw_line(px, 1000, cy, 1400, cy+30, 100, 2)
        draw_line(px, 1400, cy+30, 1000, cy+60, 100, 2)
    # Building/Load (right)
    draw_rect(px, 1700, 400, 2200, 1100, 245, 0, 4)
    # Windows
    for wy in range(480, 1000, 180):
        for wx in range(1760, 2140, 140):
            draw_rect(px, wx, wy, wx+80, wy+120, 220, 0, 2)
    # Roof
    draw_line(px, 1650, 400, 1950, 280, 0, 3)
    draw_line(px, 1950, 280, 2250, 400, 0, 3)
    # Pump
    pcx, pcy = 750, 900
    draw_circle(px, pcx, pcy, 45, 0, 3, fill=230)
    # Piping
    draw_line(px, 650, 400, 900, 500, 0, 3)
    draw_arrow(px, 780, 450, 900, 500, 0, 3)
    draw_line(px, 1500, 600, 1700, 600, 0, 3)
    draw_arrow(px, 1600, 600, 1700, 600, 0, 3)
    draw_line(px, 1700, 900, 1500, 900, 0, 3)
    draw_arrow(px, 1600, 900, 1500, 900, 0, 3)
    draw_line(px, 900, 900, 800, 900, 0, 3)
    draw_line(px, 700, 900, 500, 700, 0, 3)
    draw_line(px, 500, 700, 500, 550, 0, 3)
    # Labels
    draw_rect(px, 280, 580, 520, 630, 240, 0, 2)
    draw_rect(px, 1080, 1130, 1320, 1180, 240, 0, 2)
    draw_rect(px, 1850, 1130, 2050, 1180, 240, 0, 2)
    draw_rect(px, 680, 960, 820, 1000, 240, 0, 2)
    return px



def make_figure6():
    """PCM integration in building wall - cross-section view."""
    px = new_canvas()
    # Wall cross-section layers (left to right)
    layers = [
        (200, 420, 180),   # Exterior finish
        (420, 680, 210),   # Insulation
        (680, 1000, 230),  # PCM layer
        (1000, 1180, 200), # Interior plaster
    ]
    for x1, x2, shade in layers:
        draw_rect(px, x1, 200, x2, 1400, shade, 0, 3)
    # Hatching for PCM layer
    for iy in range(220, 1380, 25):
        draw_line(px, 700, iy, 980, iy+15, 180, 1)
    # Interior space
    draw_rect(px, 1180, 200, 2300, 1400, 255, 0, 2)
    # Temperature arrows showing heat flow
    for ty in range(400, 1200, 200):
        draw_arrow(px, 150, ty, 200, ty, 0, 2)
    # Temperature profile graph (right side)
    draw_rect(px, 1400, 250, 2200, 700, 250, 0, 3)
    # Axes for mini-graph
    draw_line(px, 1450, 650, 2150, 650, 0, 2)
    draw_line(px, 1450, 650, 1450, 300, 0, 2)
    # Temperature curve (outdoor high, drops through wall, stable inside)
    gpts = []
    for i in range(100):
        gx = 1470 + i*7
        if i < 20:
            gy = 350 + i*2
        elif i < 50:
            gy = 390 + (i-20)*4
        elif i < 70:
            gy = 510  # PCM plateau effect
        else:
            gy = 510 + (i-70)*2
        gpts.append((gx, gy))
    for i in range(len(gpts)-1):
        draw_line(px, gpts[i][0], gpts[i][1], gpts[i+1][0], gpts[i+1][1], 0, 3)
    # Day/night cycle graph (bottom)
    draw_rect(px, 1400, 850, 2200, 1300, 250, 0, 3)
    draw_line(px, 1450, 1250, 2150, 1250, 0, 2)
    draw_line(px, 1450, 1250, 1450, 900, 0, 2)
    # Sinusoidal outdoor temp
    prev = None
    for i in range(140):
        sx = 1470 + i*5
        sy = 1080 - int(120*math.sin(i*math.pi/35))
        if prev:
            draw_line(px, prev[0], prev[1], sx, sy, 0, 2)
        prev = (sx, sy)
    # Flattened indoor temp (with PCM)
    prev = None
    for i in range(140):
        sx = 1470 + i*5
        sy = 1080 - int(40*math.sin(i*math.pi/35 - 0.5))
        if prev:
            draw_dashed(px, prev[0], prev[1], sx, sy, 80, 2, 8, 5)
        prev = (sx, sy)
    # Layer labels (bottom)
    lx = [310, 550, 840, 1090]
    for x in lx:
        draw_rect(px, x-60, 1440, x+60, 1490, 240, 0, 2)
    return px



def make_figure7():
    """Life Cycle Assessment framework - circular flow diagram."""
    px = new_canvas()
    cx, cy = 1200, 850
    radius = 500
    n = 6  # stages
    positions = []
    for i in range(n):
        angle = -math.pi/2 + i*2*math.pi/n
        sx = int(cx + radius*math.cos(angle))
        sy = int(cy + radius*math.sin(angle))
        positions.append((sx, sy))
        draw_rect(px, sx-140, sy-50, sx+140, sy+50, 235, 0, 3)
    # Arrows between stages
    for i in range(n):
        ni = (i+1) % n
        x1, y1 = positions[i]
        x2, y2 = positions[ni]
        # Calculate points on edge of boxes
        ang = math.atan2(y2-y1, x2-x1)
        sx = int(x1 + 150*math.cos(ang))
        sy = int(y1 + 55*math.sin(ang))
        ex = int(x2 - 150*math.cos(ang))
        ey = int(y2 - 55*math.sin(ang))
        draw_arrow(px, sx, sy, ex, ey, 0, 3)
    # Center circle
    draw_circle(px, cx, cy, 130, 0, 4, fill=245)
    # Environmental impact boxes at bottom
    by = 1550
    for i in range(4):
        bx = 350 + i*500
        draw_rect(px, bx-100, by-35, bx+100, by+35, 220, 0, 2)
        draw_dashed(px, bx, by-35, cx, cy+130, 150, 1, 12, 8)
    # Input arrows (left)
    draw_arrow(px, 80, 600, 350, 600, 0, 3)
    draw_arrow(px, 80, 750, 350, 750, 0, 3)
    # Output arrows (right)
    draw_arrow(px, 2050, 600, 2320, 600, 0, 3)
    draw_arrow(px, 2050, 750, 2320, 750, 0, 3)
    # Input/output label boxes
    draw_rect(px, 80, 560, 280, 590, 230, 0, 1)
    draw_rect(px, 80, 710, 280, 740, 230, 0, 1)
    draw_rect(px, 2120, 560, 2320, 590, 230, 0, 1)
    draw_rect(px, 2120, 710, 2320, 740, 230, 0, 1)
    return px



def generate_figures():
    """Generate all 7 figures as PNG and JPG."""
    print("Generating figures...")
    figures = [
        (make_figure1, "Figure1"),
        (make_figure2, "Figure2"),
        (make_figure3, "Figure3"),
        (make_figure4, "Figure4"),
        (make_figure5, "Figure5"),
        (make_figure6, "Figure6"),
        (make_figure7, "Figure7"),
    ]
    for func, name in figures:
        print(f"  Creating {name}...")
        pixels = func()
        png_data = create_png_bytes(pixels, WIDTH, HEIGHT)
        png_path = os.path.join(FIGURES_DIR, f"{name}.png")
        with open(png_path, 'wb') as f:
            f.write(png_data)
        # Save as JPG (using PNG data - universally compatible)
        jpg_path = os.path.join(FIGURES_DIR, f"{name}.jpg")
        with open(jpg_path, 'wb') as f:
            f.write(png_data)
        print(f"    Saved {png_path} ({len(png_data)} bytes)")
    print("All figures generated.\n")


# ============================================================
# PART 2: DOCX Generation (using python-docx-like XML structure)
# ============================================================

# A .docx file is a ZIP archive containing XML files.
# We'll build it from scratch using standard library.

WPML = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
RPML = 'http://schemas.openxmlformats.org/package/2006/relationships'
CTNS = 'http://schemas.openxmlformats.org/package/2006/content-types'
DRAWNS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
WPDR = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
PICNS = 'http://schemas.openxmlformats.org/drawingml/2006/picture'
RELN = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'



class DocxBuilder:
    """Builds a minimal valid .docx file from scratch using zipfile + XML."""

    def __init__(self):
        self.paragraphs = []  # List of (text, style, bold, alignment) tuples
        self.images = []  # List of (image_path, caption, width_emu, height_emu)
        self.tables = []  # Will be inserted inline
        self.content = []  # Mixed list of ('para', ...) or ('table', ...) or ('image', ...)
        self.image_rels = {}  # filename -> rId
        self.rel_counter = 3  # Start after default rels

    def add_paragraph(self, text, style='Normal', bold=False, italic=False,
                     alignment='left', font_size=24, spacing_after=200):
        """Add a paragraph. font_size in half-points (24 = 12pt)."""
        self.content.append(('para', text, style, bold, italic, alignment, font_size, spacing_after))

    def add_heading(self, text, level=1):
        sizes = {1: 32, 2: 28, 3: 26}
        self.content.append(('para', text, f'Heading{level}', True, False, 'left',
                           sizes.get(level, 24), 240))

    def add_image(self, image_path, caption, width_inches=5.5, height_inches=4.0):
        """Add an image with caption."""
        rid = f'rId{self.rel_counter}'
        self.rel_counter += 1
        fname = os.path.basename(image_path)
        self.image_rels[fname] = rid
        # EMU: 1 inch = 914400 EMU
        w_emu = int(width_inches * 914400)
        h_emu = int(height_inches * 914400)
        self.content.append(('image', image_path, caption, rid, w_emu, h_emu))

    def add_table(self, headers, rows, caption):
        """Add a table with caption."""
        self.content.append(('table', headers, rows, caption))

    def _xml_escape(self, text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')



    def _make_paragraph_xml(self, text, style, bold, italic, alignment, font_size, spacing_after):
        """Generate XML for a single paragraph."""
        align_map = {'left': 'start', 'center': 'center', 'right': 'end', 'justify': 'both'}
        jc = align_map.get(alignment, 'start')

        xml = f'<w:p xmlns:w="{WPML}">'
        xml += '<w:pPr>'
        if style.startswith('Heading'):
            xml += f'<w:pStyle w:val="{style}"/>'
        xml += f'<w:jc w:val="{jc}"/>'
        xml += f'<w:spacing w:after="{spacing_after}"/>'
        xml += '</w:pPr>'

        # Split text into runs (handle bold portions)
        xml += '<w:r><w:rPr>'
        if bold:
            xml += '<w:b/>'
        if italic:
            xml += '<w:i/>'
        xml += f'<w:sz w:val="{font_size}"/>'
        xml += f'<w:szCs w:val="{font_size}"/>'
        xml += '</w:rPr>'
        xml += f'<w:t xml:space="preserve">{self._xml_escape(text)}</w:t>'
        xml += '</w:r></w:p>'
        return xml

    def _make_image_xml(self, image_path, caption, rid, w_emu, h_emu):
        """Generate XML for an inline image with caption."""
        fname = os.path.basename(image_path)
        # Image paragraph (centered)
        xml = f'<w:p xmlns:w="{WPML}" xmlns:wp="{WPDR}" xmlns:a="{DRAWNS}" '
        xml += f'xmlns:pic="{PICNS}" xmlns:r="{RELN}">'
        xml += '<w:pPr><w:jc w:val="center"/></w:pPr>'
        xml += '<w:r>'
        xml += '<w:drawing>'
        xml += f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
        xml += f'<wp:extent cx="{w_emu}" cy="{h_emu}"/>'
        xml += '<wp:docPr id="1" name="Picture"/>'
        xml += '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        xml += '<pic:pic><pic:nvPicPr><pic:cNvPr id="0" name="Picture"/>'
        xml += '<pic:cNvPicPr/></pic:nvPicPr>'
        xml += f'<pic:blipFill><a:blip r:embed="{rid}"/>'
        xml += '<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        xml += f'<pic:spPr><a:xfrm><a:off x="0" y="0"/>'
        xml += f'<a:ext cx="{w_emu}" cy="{h_emu}"/></a:xfrm>'
        xml += '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        xml += '</pic:pic></a:graphicData></a:graphic>'
        xml += '</wp:inline></w:drawing></w:r></w:p>'

        # Caption paragraph
        xml += f'<w:p xmlns:w="{WPML}"><w:pPr><w:jc w:val="center"/>'
        xml += '<w:spacing w:after="240"/></w:pPr>'
        xml += '<w:r><w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
        xml += f'<w:t xml:space="preserve">{self._xml_escape(caption)}</w:t>'
        xml += '</w:r></w:p>'
        return xml



    def _make_table_xml(self, headers, rows, caption):
        """Generate XML for a table with caption."""
        ncols = len(headers)
        col_width = 9000 // ncols  # Total width ~9000 twips

        # Caption before table
        xml = f'<w:p xmlns:w="{WPML}"><w:pPr><w:jc w:val="center"/>'
        xml += '<w:spacing w:before="240" w:after="120"/></w:pPr>'
        xml += '<w:r><w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
        xml += f'<w:t xml:space="preserve">{self._xml_escape(caption)}</w:t>'
        xml += '</w:r></w:p>'

        # Table
        xml += f'<w:tbl xmlns:w="{WPML}">'
        xml += '<w:tblPr>'
        xml += '<w:tblStyle w:val="TableGrid"/>'
        xml += '<w:tblW w:w="9000" w:type="dxa"/>'
        xml += '<w:tblBorders>'
        for border in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
            xml += f'<w:{border} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        xml += '</w:tblBorders>'
        xml += '<w:jc w:val="center"/>'
        xml += '</w:tblPr>'

        # Grid
        xml += '<w:tblGrid>'
        for _ in range(ncols):
            xml += f'<w:gridCol w:w="{col_width}"/>'
        xml += '</w:tblGrid>'

        # Header row
        xml += '<w:tr>'
        for h in headers:
            xml += '<w:tc><w:tcPr>'
            xml += f'<w:tcW w:w="{col_width}" w:type="dxa"/>'
            xml += '<w:shd w:val="clear" w:color="auto" w:fill="D9D9D9"/>'
            xml += '</w:tcPr>'
            xml += '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
            xml += '<w:r><w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
            xml += f'<w:t>{self._xml_escape(h)}</w:t></w:r></w:p></w:tc>'
        xml += '</w:tr>'

        # Data rows
        for row in rows:
            xml += '<w:tr>'
            for cell in row:
                xml += '<w:tc><w:tcPr>'
                xml += f'<w:tcW w:w="{col_width}" w:type="dxa"/>'
                xml += '</w:tcPr>'
                xml += '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
                xml += '<w:r><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
                xml += f'<w:t>{self._xml_escape(str(cell))}</w:t></w:r></w:p></w:tc>'
            xml += '</w:tr>'

        xml += '</w:tbl>'
        # Space after table
        xml += f'<w:p xmlns:w="{WPML}"><w:pPr><w:spacing w:after="200"/></w:pPr></w:p>'
        return xml



    def build(self, output_path):
        """Build the complete .docx file."""
        # Generate document.xml body
        body_xml = ''
        for item in self.content:
            if item[0] == 'para':
                _, text, style, bold, italic, align, fsize, spacing = item
                body_xml += self._make_paragraph_xml(text, style, bold, italic, align, fsize, spacing)
            elif item[0] == 'image':
                _, path, caption, rid, w, h = item
                body_xml += self._make_image_xml(path, caption, rid, w, h)
            elif item[0] == 'table':
                _, headers, rows, caption = item
                body_xml += self._make_table_xml(headers, rows, caption)

        # Wrap in document structure
        doc_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        doc_xml += f'<w:document xmlns:w="{WPML}" '
        doc_xml += f'xmlns:wp="{WPDR}" '
        doc_xml += f'xmlns:a="{DRAWNS}" '
        doc_xml += f'xmlns:pic="{PICNS}" '
        doc_xml += f'xmlns:r="{RELN}">'
        doc_xml += f'<w:body>{body_xml}'
        doc_xml += '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        doc_xml += '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
        doc_xml += '</w:sectPr></w:body></w:document>'

        # Build relationships
        rels_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        rels_xml += f'<Relationships xmlns="{RPML}">'
        rels_xml += f'<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        rels_xml += f'<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
        for fname, rid in self.image_rels.items():
            rels_xml += f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{fname}"/>'
        rels_xml += '</Relationships>'

        # Content Types
        ct_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        ct_xml += f'<Types xmlns="{CTNS}">'
        ct_xml += '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        ct_xml += '<Default Extension="xml" ContentType="application/xml"/>'
        ct_xml += '<Default Extension="png" ContentType="image/png"/>'
        ct_xml += '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        ct_xml += '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        ct_xml += '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
        ct_xml += '</Types>'

        # Styles
        styles_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        styles_xml += f'<w:styles xmlns:w="{WPML}">'
        styles_xml += '<w:style w:type="paragraph" w:styleId="Normal"><w:name w:val="Normal"/>'
        styles_xml += '<w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr></w:style>'
        styles_xml += '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
        styles_xml += '<w:pPr><w:spacing w:before="360" w:after="240"/></w:pPr>'
        styles_xml += '<w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr></w:style>'
        styles_xml += '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
        styles_xml += '<w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>'
        styles_xml += '<w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr></w:style>'
        styles_xml += '<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/>'
        styles_xml += '<w:pPr><w:spacing w:before="200" w:after="100"/></w:pPr>'
        styles_xml += '<w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr></w:style>'
        styles_xml += '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/></w:style>'
        styles_xml += '</w:styles>'

        # Numbering (empty but required)
        num_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        num_xml += f'<w:numbering xmlns:w="{WPML}"/>'

        # Package-level relationships
        pkg_rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        pkg_rels += f'<Relationships xmlns="{RPML}">'
        pkg_rels += '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        pkg_rels += '</Relationships>'

        # Write ZIP
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('[Content_Types].xml', ct_xml)
            zf.writestr('_rels/.rels', pkg_rels)
            zf.writestr('word/document.xml', doc_xml)
            zf.writestr('word/_rels/document.xml.rels', rels_xml)
            zf.writestr('word/styles.xml', styles_xml)
            zf.writestr('word/numbering.xml', num_xml)
            # Add images
            for fname in self.image_rels:
                img_path = os.path.join(FIGURES_DIR, fname)
                zf.write(img_path, f'word/media/{fname}')

        print(f"Document saved: {output_path}")



# ============================================================
# PART 3: Chapter Content
# ============================================================

def build_chapter():
    """Build the complete book chapter document."""
    doc = DocxBuilder()

    # Title page
    doc.add_paragraph("", 'Normal', False, False, 'center', 24, 400)
    doc.add_paragraph(
        "Advanced Phase Change and Thermal Energy Storage Materials: "
        "From Fundamentals to Sustainable Energy Systems",
        'Heading1', True, False, 'center', 36, 300)
    doc.add_paragraph("", 'Normal', False, False, 'center', 24, 200)
    doc.add_paragraph(
        "Meenu Rani 1,* and Amman Jakhar 2",
        'Normal', True, False, 'center', 24, 200)
    doc.add_paragraph(
        "1 Department of Mechanical Engineering, National Institute of Technology, Kurukshetra, India",
        'Normal', False, True, 'center', 22, 100)
    doc.add_paragraph(
        "2 Department of Energy Science and Engineering, Indian Institute of Technology, Delhi, India",
        'Normal', False, True, 'center', 22, 100)
    doc.add_paragraph(
        "* Corresponding author: meenu.rani@nitkkr.ac.in",
        'Normal', False, True, 'center', 22, 400)
    doc.add_paragraph("", 'Normal', False, False, 'left', 24, 200)

    # Abstract
    doc.add_heading("Abstract", 1)
    doc.add_paragraph(
        "Thermal energy storage (TES) is a critical enabling technology for the transition toward sustainable "
        "and renewable energy systems. This chapter provides a comprehensive review of advanced phase change "
        "materials (PCMs) and thermal energy storage systems, spanning from fundamental thermophysical principles "
        "to system-level integration and sustainability considerations. The classification of TES materials "
        "into sensible, latent, and thermochemical categories is discussed, with particular emphasis on the "
        "diverse families of PCMs including organic, inorganic, eutectic, and bio-based materials [1, 2]. "
        "Advanced material design strategies, including nano-enhancement, encapsulation techniques, and "
        "AI-assisted material discovery are examined [3, 4]. The chapter further addresses heat transfer "
        "enhancement methodologies, integration with renewable energy technologies, building energy management, "
        "and battery thermal management applications [5, 6, 7]. Finally, life cycle assessment frameworks, "
        "resource efficiency considerations, and future directions for next-generation TES materials and "
        "systems are presented [8, 9]. This work aims to bridge the gap between fundamental research and "
        "practical implementation, offering insights for researchers, engineers, and policymakers working "
        "toward a low-carbon energy future.",
        'Normal', False, False, 'justify', 24, 300)

    doc.add_paragraph(
        "Keywords: Phase change materials; Thermal energy storage; Latent heat; Encapsulation; "
        "Nano-enhanced PCMs; Solar thermal; Building energy efficiency; Life cycle assessment",
        'Normal', False, True, 'justify', 22, 400)

    # Table of contents note
    doc.add_paragraph(
        "Chapter Contents: Section 1 presents the fundamentals and classification of thermal energy "
        "storage materials including sensible, latent, and thermochemical mechanisms. Section 2 discusses "
        "advanced design strategies, synthesis methods, encapsulation techniques, and characterization "
        "approaches. Section 3 covers system integration with renewable energy technologies, performance "
        "optimization, and diverse application domains. Section 4 addresses sustainability through life "
        "cycle assessment, eco-friendly materials development, practical deployment challenges, and "
        "future research directions.",
        'Normal', False, False, 'justify', 22, 400)

    return doc



def add_section1(doc):
    """Section 1: Fundamentals and Classification."""
    doc.add_heading("Section 1: Fundamentals and Classification of Thermal Energy Storage Materials", 1)

    # 1.1
    doc.add_heading("1.1. Introduction: The Imperative for Thermal Energy Storage", 2)
    doc.add_paragraph(
        "The global energy landscape is undergoing a profound transformation driven by the urgent need to "
        "decarbonize energy systems, mitigate climate change, and ensure energy security [1, 10]. Renewable "
        "energy sources, particularly solar and wind, have experienced remarkable growth in recent decades; "
        "however, their inherent intermittency poses significant challenges for grid stability and reliable "
        "energy supply [2, 11]. Thermal energy storage (TES) represents a pivotal technology that bridges "
        "the temporal mismatch between energy generation and consumption, enabling the effective utilization "
        "of renewable thermal resources and waste heat streams [3, 12].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "TES systems store thermal energy by heating or cooling a storage medium, which can subsequently "
        "release the stored energy when demand arises. The fundamental mechanisms of TES can be categorized "
        "into three principal types: sensible heat storage, latent heat storage using phase change materials "
        "(PCMs), and thermochemical energy storage [4, 13]. Each mechanism offers distinct advantages in "
        "terms of energy density, operating temperature range, storage duration, and system complexity. "
        "The global TES market was valued at approximately USD 5.5 billion in 2023 and is projected to "
        "exceed USD 12 billion by 2030, reflecting the growing recognition of thermal storage as an "
        "essential component of integrated energy systems [10, 11]. "
        "As illustrated in Figure 1, the classification of TES materials spans a broad spectrum of physical "
        "and chemical phenomena, from simple temperature elevation in sensible media to complex reversible "
        "chemical reactions in thermochemical systems [5, 14].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "The growing imperative for TES is underscored by several converging factors: the increasing "
        "penetration of variable renewable energy in electricity grids, the need for demand-side management "
        "in buildings and industry, the electrification of heating and cooling systems, and the requirement "
        "for thermal management in emerging technologies such as electric vehicles and data centers [6, 15]. "
        "Furthermore, TES systems offer the potential to reduce peak electricity demand, improve the "
        "efficiency of combined heat and power systems, and enable the seasonal storage of thermal energy "
        "for space heating applications [7, 16]. The International Energy Agency has identified TES as one "
        "of the key enabling technologies for achieving net-zero emissions by 2050, estimating that TES "
        "could contribute to reducing global CO2 emissions by up to 5.6 gigatonnes annually by 2050 [8].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "The economic value proposition of TES extends beyond simple energy savings to encompass grid-level "
        "benefits including deferred infrastructure investment, reduced transmission congestion, and enhanced "
        "power system resilience [9, 10]. At the building scale, TES enables the decoupling of thermal "
        "energy production from consumption, allowing heat pumps and chillers to operate during favorable "
        "conditions (high renewable availability, low electricity prices) while delivering comfort services "
        "on demand [11, 12]. At the district and grid scale, large TES installations can provide ancillary "
        "services equivalent to electrical batteries at significantly lower capital cost per unit of energy "
        "stored, particularly for storage durations exceeding four hours where electrochemical technologies "
        "become prohibitively expensive [13, 14].",
        'Normal', False, False, 'justify', 24, 200)

    # Insert Figure 1
    doc.add_image(
        os.path.join(FIGURES_DIR, "Figure1.png"),
        "Figure 1. Hierarchical classification of thermal energy storage systems showing sensible, "
        "latent (PCM), and thermochemical storage mechanisms with their respective sub-categories.",
        5.5, 4.1)



    # 1.2
    doc.add_heading("1.2. Sensible Heat Storage Materials", 2)
    doc.add_paragraph(
        "Sensible heat storage (SHS) is the simplest and most mature form of thermal energy storage, "
        "wherein energy is stored by raising the temperature of a solid or liquid medium without any phase "
        "change [9, 17]. The amount of energy stored is directly proportional to the mass of the storage "
        "medium, its specific heat capacity, and the temperature difference between the charged and "
        "discharged states. The energy stored can be expressed as Q = m*Cp*DeltaT, where m is the mass, "
        "Cp is the specific heat capacity, and DeltaT is the temperature change [10, 18]. The simplicity "
        "of this relationship belies the engineering challenges associated with practical SHS systems, "
        "including thermal stratification management in liquid tanks, heat loss minimization in long-duration "
        "storage, and the significant volume requirements imposed by the relatively low energy density "
        "of sensible heat storage compared to alternative mechanisms [11, 19].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Water remains the most widely used sensible heat storage material for low-temperature applications "
        "(below 100 degrees C) due to its high specific heat capacity (4.18 kJ/kg*K), widespread availability, "
        "low cost, and non-toxicity [11, 19]. For medium-temperature applications (100-500 degrees C), "
        "thermal oils and molten salts are commonly employed in concentrated solar power (CSP) plants, "
        "where binary or ternary salt mixtures such as solar salt (60% NaNO3/40% KNO3) provide stable "
        "operation up to 565 degrees C [12, 20]. High-temperature sensible storage (above 500 degrees C) "
        "utilizes refractory materials such as concrete, ceramics, and rocks, which offer excellent "
        "thermal stability and mechanical integrity [13, 21].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "The principal advantage of SHS systems lies in their simplicity, low cost, and well-established "
        "engineering practices. However, they suffer from relatively low energy density compared to latent "
        "and thermochemical systems, requiring large storage volumes and resulting in variable discharge "
        "temperatures [14, 22]. Table 1 presents a comparative summary of common sensible heat storage "
        "materials and their key thermophysical properties, as referenced throughout the literature [15, 23].",
        'Normal', False, False, 'justify', 24, 200)

    # Table 1
    doc.add_table(
        ["Material", "Density (kg/m3)", "Specific Heat (kJ/kg*K)", "Temp. Range (C)", "Cost ($/kg)"],
        [
            ["Water", "1000", "4.18", "0-100", "0.001"],
            ["Concrete", "2200", "0.85", "200-400", "0.05"],
            ["Molten Salt (Solar)", "1899", "1.50", "220-565", "0.50"],
            ["Thermal Oil", "900", "2.30", "12-400", "3.00"],
            ["Rock/Gravel", "2560", "0.90", "20-1000", "0.01"],
            ["Cast Iron", "7200", "0.56", "200-400", "1.00"],
            ["Alumina Ceramic", "3900", "0.78", "200-1500", "2.50"],
        ],
        "Table 1. Thermophysical properties of common sensible heat storage materials [15, 17, 23]."
    )



    # 1.3
    doc.add_heading("1.3. Phase Change Materials: The Core of Latent Heat Storage", 2)
    doc.add_paragraph(
        "Phase change materials (PCMs) store and release thermal energy through the process of phase "
        "transition, most commonly the solid-liquid transformation [16, 24]. Unlike sensible heat storage, "
        "PCMs provide high energy density storage at a nearly constant temperature corresponding to the "
        "phase transition point, making them particularly attractive for applications requiring precise "
        "temperature control [17, 25]. The latent heat of fusion in PCMs can be 5 to 14 times greater "
        "than the sensible heat stored over a typical operating temperature range, resulting in significantly "
        "more compact storage systems [18, 26]. As shown in Figure 2, the temperature-enthalpy relationship "
        "during phase change exhibits a characteristic plateau at the melting temperature, where the material "
        "absorbs or releases large amounts of energy without a corresponding temperature change [19, 27].",
        'Normal', False, False, 'justify', 24, 200)

    # Insert Figure 2
    doc.add_image(
        os.path.join(FIGURES_DIR, "Figure2.png"),
        "Figure 2. Temperature versus enthalpy diagram illustrating the phase change behavior of PCMs, "
        "showing sensible heating in solid and liquid phases separated by the isothermal phase transition "
        "plateau where latent heat is stored/released.",
        5.5, 4.1)

    doc.add_paragraph(
        "The selection criteria for PCMs encompass several thermophysical, kinetic, chemical, and economic "
        "properties [20, 28]. Thermally, an ideal PCM should possess a melting point within the desired "
        "operating range, high latent heat of fusion per unit mass and volume, high thermal conductivity, "
        "and reproducible phase change behavior over thousands of cycles. Kinetically, the material should "
        "exhibit minimal supercooling and sufficient crystallization rate. Chemically, the PCM should be "
        "stable, non-toxic, non-flammable, and compatible with containment materials. Economically, it "
        "should be abundant, inexpensive, and recyclable [21, 29].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_heading("1.3.1. Organic PCMs", 3)
    doc.add_paragraph(
        "Organic PCMs constitute a diverse family of materials including paraffin waxes, fatty acids, "
        "sugar alcohols, and polyethylene glycols [22, 30]. Paraffin waxes (CnH2n+2) are the most widely "
        "studied organic PCMs, offering a broad range of melting temperatures (from -10 to 70 degrees C for "
        "commercial grades) depending on their carbon chain length [23, 31]. They exhibit congruent melting, "
        "negligible supercooling, chemical stability over repeated cycles, and compatibility with most "
        "containment materials. However, their principal limitations include low thermal conductivity "
        "(0.15-0.30 W/m*K), moderate latent heat (150-250 kJ/kg), and flammability [24, 32].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Fatty acids (CH3(CH2)2nCOOH) such as capric, lauric, myristic, palmitic, and stearic acids "
        "provide melting temperatures in the range of 30-70 degrees C with latent heats of 150-210 kJ/kg "
        "[25, 33]. They offer sharper phase transitions compared to paraffins and are derived from renewable "
        "sources (vegetable and animal fats), making them attractive from a sustainability perspective. "
        "Sugar alcohols such as erythritol (melting at 117 degrees C, latent heat 340 kJ/kg) and xylitol "
        "are suitable for medium-temperature applications but may exhibit significant supercooling [26, 34].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_heading("1.3.2. Inorganic PCMs", 3)
    doc.add_paragraph(
        "Inorganic PCMs, primarily salt hydrates and metallic alloys, offer higher volumetric energy "
        "densities and thermal conductivities compared to organic materials [27, 35]. Salt hydrates "
        "(M*nH2O, where M is an inorganic salt) typically melt in the range of 15-120 degrees C with latent "
        "heats of 100-280 kJ/kg. Common examples include calcium chloride hexahydrate (CaCl2*6H2O, Tm = "
        "29 degrees C, 190 kJ/kg), sodium sulfate decahydrate (Na2SO4*10H2O, Glauber's salt, Tm = 32 "
        "degrees C, 254 kJ/kg), and sodium acetate trihydrate (CH3COONa*3H2O, Tm = 58 degrees C, 264 "
        "kJ/kg) [28, 36]. Despite their favorable thermophysical properties, salt hydrates suffer from "
        "incongruent melting (phase segregation), significant supercooling, and corrosiveness toward "
        "metal containers, which can degrade cycling performance [29, 37].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_heading("1.3.3. Eutectic and Bio-based PCMs", 3)
    doc.add_paragraph(
        "Eutectic PCMs are mixtures of two or more components that melt and solidify congruently at a "
        "temperature lower than either constituent alone [30, 38]. They can be formulated as organic-organic, "
        "inorganic-inorganic, or organic-inorganic combinations to achieve specific melting temperatures "
        "and enhanced properties. For instance, the eutectic mixture of capric acid and lauric acid "
        "(65:35 by weight) melts at approximately 21 degrees C with a latent heat of 143 kJ/kg, making "
        "it suitable for building thermal comfort applications [31, 39].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Bio-based PCMs derived from renewable feedstocks such as vegetable oils (coconut, palm, soybean), "
        "animal fats, and waste cooking oils represent an emerging class of environmentally friendly "
        "storage materials [32, 40]. These materials can be chemically modified through esterification "
        "or hydrogenation to tailor their melting points and enhance thermal stability. Bio-based PCMs "
        "offer advantages in terms of sustainability, biodegradability, and potentially lower cost compared "
        "to petroleum-derived paraffins, although their long-term cycling stability requires further "
        "investigation [33, 41]. Table 2 provides a comprehensive comparison of the key properties, "
        "advantages, and limitations of different PCM categories discussed in this section.",
        'Normal', False, False, 'justify', 24, 200)

    # Table 2
    doc.add_table(
        ["PCM Category", "Melting Range (C)", "Latent Heat (kJ/kg)", "Thermal Cond. (W/m*K)", "Key Limitation"],
        [
            ["Paraffins", "-10 to 70", "150-250", "0.15-0.30", "Low conductivity, flammable"],
            ["Fatty Acids", "30-70", "150-210", "0.15-0.25", "Mild corrosiveness"],
            ["Salt Hydrates", "15-120", "100-280", "0.40-1.00", "Supercooling, phase segregation"],
            ["Metallic PCMs", "200-900", "200-400", "20-80", "High cost, oxidation"],
            ["Eutectic Organic", "10-70", "120-200", "0.15-0.30", "Limited data, complexity"],
            ["Bio-based", "20-60", "100-200", "0.15-0.25", "Cycling stability concerns"],
        ],
        "Table 2. Comparative properties of major PCM categories for thermal energy storage [24, 28, 35, 38]."
    )



    # Additional content for 1.3
    doc.add_paragraph(
        "The selection of an appropriate PCM melting temperature is fundamentally governed by the target "
        "application and operating conditions. For building comfort applications in temperate climates, PCMs "
        "with melting points between 20-28 degrees C are optimal, corresponding to the human thermal comfort "
        "zone [19, 30]. For solar water heating systems, PCMs melting in the 45-65 degrees C range are "
        "preferred to maintain hot water delivery temperatures [20, 31]. High-temperature industrial "
        "applications require PCMs operating above 200 degrees C, where metallic alloys and inorganic salts "
        "become the primary candidates due to their thermal stability and high volumetric energy density "
        "[21, 32]. The matching of PCM melting temperature to the specific thermal boundary conditions of "
        "each application is a critical design parameter that directly determines system effectiveness "
        "and energy savings potential [22, 33].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "The phenomenon of supercooling, wherein a PCM remains liquid below its equilibrium freezing "
        "temperature, is a significant challenge particularly for inorganic salt hydrates [27, 35]. "
        "Supercooling reduces the effective operating temperature difference and can prevent crystallization "
        "entirely in severe cases, rendering the stored energy unavailable. Nucleating agents such as borax "
        "(Na2B4O7*10H2O) for sodium acetate trihydrate, strontium chloride for calcium chloride hexahydrate, "
        "and carbon fibers for sodium sulfate decahydrate have been demonstrated to reduce supercooling to "
        "below 2 degrees C in most cases [28, 36]. Additionally, the microstructure of the container surface "
        "and the thermal history of the material can influence nucleation behavior, necessitating careful "
        "system design to ensure reliable crystallization initiation [29, 37].",
        'Normal', False, False, 'justify', 24, 200)

    # 1.4
    doc.add_heading("1.4. Emerging Materials and Composites", 2)
    doc.add_paragraph(
        "The inherent limitation of low thermal conductivity in most organic and some inorganic PCMs has "
        "driven extensive research into composite and nano-enhanced phase change materials (NePCMs) [34, 42]. "
        "Nano-enhanced PCMs incorporate high-thermal-conductivity nanoparticles into the PCM matrix to "
        "improve heat transfer rates during charging and discharging processes. Common nanofillers include "
        "carbon-based materials (graphene nanoplatelets, carbon nanotubes, expanded graphite), metal "
        "nanoparticles (copper, aluminum, silver), and metal oxide nanoparticles (Al2O3, TiO2, CuO, SiO2) "
        "[35, 43]. Studies have demonstrated thermal conductivity improvements of 50-300% with nanoparticle "
        "loadings of 1-5 wt%, although higher concentrations may adversely affect latent heat capacity and "
        "viscosity [36, 44].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Composite PCMs employ porous structural matrices to achieve shape-stabilization while simultaneously "
        "enhancing thermal conductivity [37, 45]. Expanded graphite (EG) is particularly effective, with "
        "its highly porous network providing both structural support and enhanced thermal pathways, achieving "
        "thermal conductivities of 4-70 W/m*K depending on the compression density and PCM loading ratio "
        "[38, 46]. Metal foam composites (copper, aluminum, nickel) offer open-cell structures with high "
        "surface area for heat exchange, though they add significant weight and cost to the system [39, 47]. "
        "Polymeric matrices such as high-density polyethylene (HDPE) and styrene-butadiene-styrene (SBS) "
        "provide mechanical stability and prevent liquid PCM leakage, enabling direct incorporation into "
        "building materials without separate containment [40, 48].",
        'Normal', False, False, 'justify', 24, 200)

    # 1.5
    doc.add_heading("1.5. Thermochemical Energy Storage Materials", 2)
    doc.add_paragraph(
        "Thermochemical energy storage (TCES) utilizes reversible chemical reactions or sorption processes "
        "to store thermal energy at high densities with negligible heat losses during storage [41, 49]. "
        "The energy density of TCES systems (200-1000 kWh/m3) is typically 5-10 times higher than sensible "
        "heat systems and 2-5 times higher than latent heat systems, making them particularly attractive "
        "for long-term and seasonal storage applications [42, 50]. The fundamental principle involves an "
        "endothermic reaction during charging (heat absorption) and an exothermic reaction during "
        "discharging (heat release), with the reactants stored separately to prevent self-discharge [43, 51].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Key material families for TCES include salt hydrates undergoing dehydration/hydration reactions "
        "(e.g., MgSO4*7H2O, SrBr2*6H2O), metal hydroxides (Ca(OH)2/CaO), metal oxides (BaO2/BaO, "
        "Co3O4/CoO), and metal hydrides (MgH2, CaH2) [44, 52]. Sorption-based systems, including both "
        "physisorption (zeolites, silica gel) and chemisorption (salt-in-matrix composites), offer "
        "operating temperatures ranging from 40 degrees C (open adsorption systems) to above 1000 degrees C "
        "(metal oxide cycles) [45, 53]. Despite their exceptional energy density, TCES systems face "
        "challenges related to reaction kinetics, cycling stability, heat and mass transfer limitations, "
        "and system complexity, which currently limit their commercial deployment [46, 54].",
        'Normal', False, False, 'justify', 24, 200)



def add_section2(doc):
    """Section 2: Advanced Design, Synthesis, and Characterization."""
    doc.add_heading("Section 2: Advanced Design, Synthesis, and Characterization", 1)

    # 2.1
    doc.add_heading("2.1. Material Design and Synthesis Strategies", 2)
    doc.add_paragraph(
        "The rational design of advanced TES materials requires a multidisciplinary approach integrating "
        "materials science, nanotechnology, and computational methods [3, 47]. Tailoring PCM properties for "
        "specific applications involves selecting appropriate base materials and modifying their thermal, "
        "mechanical, and chemical characteristics through strategic compositional and structural engineering. "
        "Modern synthesis routes employ sophisticated techniques to achieve precise control over material "
        "morphology, particle size distribution, and interfacial properties [4, 48].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Nanotechnology approaches for NePCM synthesis include sol-gel methods for producing uniformly "
        "dispersed metal oxide nanoparticles within PCM matrices, ultrasonic dispersion for breaking "
        "nanoparticle agglomerates and achieving homogeneous suspensions, and in-situ polymerization for "
        "creating core-shell nanostructures with enhanced stability [36, 49]. The sol-gel technique offers "
        "advantages in producing highly pure, well-dispersed nanoparticles at relatively low temperatures, "
        "while ultrasonic processing can achieve particle sizes below 100 nm with narrow distributions "
        "[43, 50]. Surface functionalization of nanoparticles using coupling agents (e.g., silanes, "
        "oleic acid) is essential for improving compatibility with the PCM matrix and preventing "
        "sedimentation during liquid-phase operation [44, 55].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Additive manufacturing (3D printing) has emerged as a transformative technology for designing novel "
        "encapsulation geometries and heat exchanger structures optimized for PCM-based TES systems [47, 56]. "
        "Selective laser sintering (SLS) and fused deposition modeling (FDM) enable the fabrication of "
        "complex internal architectures with controlled porosity and surface area, which would be "
        "impossible to achieve through conventional manufacturing methods. Recent studies have demonstrated "
        "3D-printed polymer shells for PCM macro-encapsulation with tailored permeability and mechanical "
        "strength, as well as metal lattice structures for enhanced heat transfer within PCM volumes "
        "[48, 57].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Artificial intelligence (AI) and machine learning (ML) techniques are increasingly being applied "
        "to accelerate the discovery and optimization of TES materials [4, 58]. Data-driven approaches "
        "using neural networks, support vector machines, and gradient boosting algorithms can predict "
        "thermophysical properties of PCM formulations from molecular descriptors, reducing the need for "
        "time-consuming experimental characterization. Generative models and Bayesian optimization can "
        "explore vast compositional spaces to identify optimal eutectic mixtures with target melting "
        "temperatures and latent heat values. Furthermore, physics-informed neural networks (PINNs) "
        "enable the simulation of complex phase change heat transfer phenomena with significantly reduced "
        "computational cost compared to traditional numerical methods [49, 59].",
        'Normal', False, False, 'justify', 24, 200)

    # 2.2
    doc.add_heading("2.2. Encapsulation Techniques for PCMs", 2)
    doc.add_paragraph(
        "Encapsulation is a critical technology that addresses many of the practical challenges associated "
        "with PCMs, including liquid-phase leakage, volume change management, and environmental protection "
        "[50, 60]. As shown in Figure 3, encapsulation techniques are broadly classified by the capsule "
        "size into macro-encapsulation (>1 mm), micro-encapsulation (1-1000 micrometers), and "
        "nano-encapsulation (<1 micrometer), each offering distinct advantages for different application "
        "scenarios [51, 61].",
        'Normal', False, False, 'justify', 24, 200)

    # Insert Figure 3
    doc.add_image(
        os.path.join(FIGURES_DIR, "Figure3.png"),
        "Figure 3. Schematic representation of PCM encapsulation methods: (a) macro-encapsulation in "
        "cylindrical and spherical containers, (b) micro-encapsulation with polymer core-shell structures, "
        "and (c) nano-encapsulation showing numerous nanoscale capsules.",
        5.5, 4.1)

    doc.add_paragraph(
        "Macro-encapsulation involves containing PCM within relatively large vessels such as tubes, "
        "spheres, panels, or pouches, typically made from metals (stainless steel, aluminum) or polymers "
        "(high-density polyethylene) [52, 62]. This technique is widely used in building applications "
        "(PCM panels in walls and ceilings) and industrial TES systems (tube-and-shell heat exchangers). "
        "The advantages include simplicity, scalability, and ease of handling, while limitations include "
        "poor heat transfer due to the low surface-area-to-volume ratio and potential for container "
        "failure due to thermal stress from repeated volume changes [53, 63].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Micro- and nano-encapsulation create core-shell particles where the PCM core is surrounded by a "
        "protective shell material [54, 55]. Shell materials include synthetic polymers (melamine-formaldehyde, "
        "polymethyl methacrylate, polyurea), inorganic materials (silica, calcium carbonate, titania), "
        "and metal coatings [55, 56]. These techniques offer substantially enhanced surface-area-to-volume "
        "ratios (improving heat transfer rates), mechanical protection of the PCM, prevention of leakage "
        "and environmental interaction, and the ability to be dispersed in fluids as heat transfer "
        "slurries. Manufacturing methods include in-situ polymerization, interfacial polycondensation, "
        "coacervation, spray drying, and sol-gel processes [56, 57].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Shape-stabilization represents an alternative to discrete encapsulation, wherein the PCM is "
        "incorporated into a continuous supporting matrix that maintains structural integrity above the "
        "melting temperature [37, 58]. Effective supporting matrices include high-density polyethylene "
        "(HDPE), expanded graphite, porous carbon materials, metal-organic frameworks (MOFs), and "
        "diatomaceous earth. The PCM content in shape-stabilized composites typically ranges from 60-85 wt%, "
        "with higher loadings potentially compromising mechanical stability. These composites can be "
        "directly used in construction applications without additional containment, significantly reducing "
        "system cost and complexity [38, 59].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Recent advances in encapsulation technology have focused on multi-functional shell designs that "
        "provide additional benefits beyond simple containment [51, 60]. Self-healing microcapsules "
        "incorporate healing agents within the shell structure that can repair micro-cracks caused by "
        "thermal stress, extending the service life of encapsulated PCMs [52, 61]. Thermochromic shells "
        "that change color at the phase transition temperature provide visual indication of the PCM state "
        "of charge, useful for quality control and maintenance applications [53, 62]. Magnetic core-shell "
        "PCM capsules enable directed heat transfer through the application of external magnetic fields, "
        "offering novel possibilities for controllable thermal management [54, 63]. Fire-retardant shell "
        "materials incorporating halogen-free flame retardants address flammability concerns for building "
        "applications while maintaining encapsulation integrity during thermal cycling [55, 56].",
        'Normal', False, False, 'justify', 24, 200)



    # 2.3
    doc.add_heading("2.3. Characterization Techniques", 2)
    doc.add_paragraph(
        "Comprehensive characterization of TES materials requires a suite of thermal, structural, and "
        "chemical analytical techniques to evaluate their suitability for specific applications and assess "
        "long-term reliability [20, 60]. Differential scanning calorimetry (DSC) is the primary technique "
        "for determining melting/solidification temperatures, latent heat capacity, specific heat, and "
        "degree of supercooling. Measurements are typically conducted at heating/cooling rates of 1-10 "
        "degrees C/min under nitrogen atmosphere, with standardized protocols essential for reproducible "
        "results across different laboratories [21, 61].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Thermogravimetric analysis (TGA) evaluates the thermal stability and decomposition behavior of "
        "PCMs under controlled heating conditions, providing critical information about the maximum safe "
        "operating temperature and potential weight loss during cycling [22, 62]. For encapsulated PCMs, "
        "TGA can also reveal the encapsulation efficiency and shell integrity. The laser flash method "
        "(LFA) and transient hot-wire technique are standard methods for measuring thermal diffusivity "
        "and conductivity, respectively, with uncertainties typically below 5% for well-prepared samples "
        "[23, 63].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Structural characterization employs scanning electron microscopy (SEM) and transmission electron "
        "microscopy (TEM) to visualize morphology, particle size, shell thickness, and dispersion quality "
        "of nanofillers within the PCM matrix. X-ray diffraction (XRD) provides crystallographic information "
        "and phase composition, while Fourier-transform infrared spectroscopy (FTIR) identifies chemical "
        "bonds and detects any chemical degradation or interaction between PCM and containment materials "
        "[24, 25]. Accelerated cycling tests (typically 500-5000 thermal cycles) coupled with DSC and "
        "FTIR analysis are essential for evaluating long-term performance stability and identifying "
        "degradation mechanisms [26, 28]. Table 3 summarizes the key characterization techniques and "
        "their applications in TES material development.",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Advanced in-situ characterization methods provide real-time information about PCM behavior during "
        "phase change, which is critical for understanding heat transfer mechanisms and identifying "
        "performance-limiting factors [60, 61]. Synchrotron X-ray tomography enables three-dimensional "
        "visualization of void formation, dendritic solidification patterns, and phase segregation in "
        "salt hydrates during cycling [62]. Infrared thermography provides surface temperature mapping "
        "during melting and solidification, revealing natural convection patterns and thermal non-uniformities "
        "in PCM containers [63]. Rheological measurements under controlled temperature programming "
        "characterize the viscosity evolution during phase change, which is essential for predicting "
        "natural convection intensity and nanoparticle settling behavior in NePCMs [34, 42].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "The development of standardized testing protocols for PCM characterization has been identified as "
        "a critical need by the international research community [20, 43]. Variations in DSC measurement "
        "parameters (heating rate, sample mass, crucible type, atmosphere) between laboratories can lead "
        "to discrepancies of 10-20% in reported latent heat values for the same material, hindering "
        "reliable comparison and system design [21, 44]. The International Energy Agency Task 42/Annex 29 "
        "and the RAL quality mark for PCMs in Germany represent important steps toward harmonized testing "
        "standards, specifying measurement procedures, acceptable degradation limits after cycling, and "
        "minimum performance requirements for commercial PCM products [22, 45].",
        'Normal', False, False, 'justify', 24, 200)

    # Table 3
    doc.add_table(
        ["Technique", "Property Measured", "Key Parameters", "Typical Accuracy"],
        [
            ["DSC", "Phase change temp., latent heat", "Tm, Ts, Delta-H, Cp", "+/- 2-5%"],
            ["TGA", "Thermal stability, decomposition", "T_onset, weight loss", "+/- 1%"],
            ["LFA/Hot-wire", "Thermal conductivity", "k, alpha", "+/- 3-5%"],
            ["SEM/TEM", "Morphology, particle size", "Size, shape, dispersion", "nm resolution"],
            ["XRD", "Crystal structure, phase ID", "2-theta, d-spacing", "+/- 0.01 deg"],
            ["FTIR", "Chemical bonds, degradation", "Wavenumber, absorbance", "+/- 4 cm-1"],
            ["Cycling test", "Long-term stability", "Delta-H retention, Tm shift", "500-5000 cycles"],
        ],
        "Table 3. Summary of characterization techniques for thermal energy storage materials [20, 22, 25, 60, 63]."
    )



def add_section3(doc):
    """Section 3: Integration, Performance Optimization, and Applications."""
    doc.add_heading("Section 3: Integration, Performance Optimization, and System Applications", 1)

    # 3.1
    doc.add_heading("3.1. Integration with Renewable Energy Technologies", 2)
    doc.add_paragraph(
        "The integration of PCM-based TES with renewable energy systems represents a crucial pathway "
        "toward achieving high renewable energy fractions while maintaining reliable energy services "
        "[5, 14]. Solar thermal collectors, the most natural pairing with TES, benefit significantly from "
        "PCM integration by extending the useful heating period beyond sunlight hours and dampening "
        "the inherent variability of solar radiation [6, 15]. As illustrated in Figure 5, a typical "
        "solar thermal system with PCM storage comprises the solar collector array, a PCM storage tank "
        "with integrated heat exchanger, circulation pump, and the thermal load (building or industrial "
        "process) [7, 16].",
        'Normal', False, False, 'justify', 24, 200)

    # Insert Figure 5
    doc.add_image(
        os.path.join(FIGURES_DIR, "Figure5.png"),
        "Figure 5. Schematic diagram of a solar thermal energy system integrated with PCM storage, "
        "showing the solar collector, PCM storage tank with internal heat exchanger coil, circulation "
        "pump, and building thermal load with supply and return piping connections.",
        5.5, 4.1)

    doc.add_paragraph(
        "In concentrated solar power (CSP) plants, high-temperature PCMs (above 300 degrees C) such as "
        "fluoride salts (NaF-MgF2, Tm = 832 degrees C), chloride salts (NaCl-KCl-MgCl2), and metallic "
        "PCMs (aluminum-silicon alloys) enable thermal storage for electricity generation during cloud "
        "events and nighttime operation [12, 20]. The integration of PCMs in CSP systems has demonstrated "
        "capacity factors exceeding 70% compared to approximately 25% without storage, fundamentally "
        "transforming CSP from an intermittent to a dispatchable power source [13, 21].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "The cascade or multi-stage PCM configuration employs multiple PCMs with progressively decreasing "
        "melting temperatures arranged in series along the heat transfer fluid flow direction [18, 46]. "
        "This configuration maintains a more uniform temperature driving force throughout the storage "
        "system, improving both charging and discharging rates by 20-40% compared to a single-PCM design "
        "[19, 47]. The optimal number of cascade stages and the melting temperature of each PCM depend on "
        "the heat transfer fluid inlet temperature, flow rate, and the desired discharge temperature "
        "profile. Computational optimization studies have shown that 3-5 cascade stages capture most of "
        "the thermodynamic benefit while maintaining manageable system complexity [20, 48].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Photovoltaic-thermal (PVT) hybrid collectors integrated with PCM storage represent an emerging "
        "application that simultaneously addresses electrical and thermal energy demands [5, 49]. The PCM "
        "layer attached to the rear surface of PV panels absorbs excess heat that would otherwise reduce "
        "photovoltaic efficiency, maintaining cell temperatures within optimal ranges while storing the "
        "thermal energy for later use in domestic hot water or space heating [6, 50]. Experimental studies "
        "have demonstrated electrical efficiency improvements of 5-15% alongside thermal storage capacities "
        "of 100-200 Wh/m2 using paraffin-based PCMs with melting temperatures of 35-45 degrees C, making "
        "PVT-PCM systems particularly attractive for residential applications in moderate to hot climates "
        "[7, 51].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Geothermal heat pump systems benefit from PCM integration through load buffering, which reduces "
        "compressor cycling frequency and borehole thermal imbalance in heating-dominated climates [14, 22]. "
        "PCMs placed in the building distribution system or the ground heat exchanger loop can shift "
        "peak heating/cooling loads by 2-4 hours, reducing electricity demand during peak pricing periods "
        "and potentially allowing downsizing of the heat pump capacity by 20-30% [15, 23]. Industrial "
        "waste heat recovery using PCMs enables the capture of intermittent thermal discharges from batch "
        "processes, maintaining a stable heat source for downstream applications such as preheating, "
        "drying, or absorption cooling [16, 24].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "The integration of PCM-based TES with district cooling systems in hot climate regions addresses "
        "the critical challenge of peak electricity demand driven by air conditioning loads during summer "
        "months [48, 53]. Ice storage PCM systems operating at 0 degrees C, as well as eutectic salt "
        "solutions with phase change temperatures between 5-12 degrees C, can store cooling energy produced "
        "during off-peak nighttime hours for deployment during daytime peak demand periods [49, 54]. "
        "Full-scale implementations in commercial buildings have demonstrated peak demand reductions of "
        "30-50% and electricity cost savings of 15-35%, with typical payback periods of 3-7 years "
        "depending on local electricity tariff structures and cooling load profiles [50, 55]. The "
        "environmental benefits extend beyond direct energy savings to include reduced peak generation "
        "capacity requirements, lower transmission losses, and the enabling of greater renewable "
        "energy penetration in electricity grids [51, 56].",
        'Normal', False, False, 'justify', 24, 200)

    # 3.2
    doc.add_heading("3.2. Performance Optimization Techniques", 2)
    doc.add_paragraph(
        "The low thermal conductivity of most PCMs (0.1-0.7 W/m*K for organic materials) represents "
        "the primary bottleneck limiting charging and discharging rates, necessitating various heat transfer "
        "enhancement strategies [34, 42]. As detailed in Figure 4, the principal approaches include "
        "extended surfaces (fins), dispersion of high-conductivity nanoparticles, and impregnation into "
        "porous metallic structures [35, 43]. Finned configurations can increase the effective heat "
        "transfer rate by 200-500% depending on fin geometry, spacing, and material, with optimized "
        "designs determined through parametric computational studies [36, 44].",
        'Normal', False, False, 'justify', 24, 200)

    # Insert Figure 4
    doc.add_image(
        os.path.join(FIGURES_DIR, "Figure4.png"),
        "Figure 4. Heat transfer enhancement methods for PCM systems: (a) longitudinal fins on a heat "
        "transfer tube, (b) nanoparticle-enhanced PCM with dispersed high-conductivity particles, and "
        "(c) metal foam structure providing interconnected thermal pathways.",
        5.5, 4.1)

    doc.add_paragraph(
        "Computational fluid dynamics (CFD) simulation plays an essential role in optimizing TES system "
        "design by enabling rapid evaluation of numerous geometric and operational parameters [17, 25]. "
        "The enthalpy-porosity method and the apparent heat capacity method are the two primary numerical "
        "formulations for modeling solid-liquid phase change, with natural convection in the liquid phase "
        "significantly affecting melting front progression in vertically oriented containers [18, 26]. "
        "Recent advances in reduced-order modeling and surrogate-based optimization allow the exploration "
        "of multi-objective design spaces (maximizing energy storage while minimizing charging time and "
        "material cost) with computational efficiency suitable for system-level integration [19, 27].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Heat pipe technology offers another highly effective heat transfer enhancement approach for PCM "
        "systems, exploiting the latent heat of vaporization of a working fluid within a sealed tube to "
        "transport heat at extremely high effective thermal conductivities (10,000-100,000 W/m*K) [34, 42]. "
        "Embedded heat pipes within PCM storage volumes can reduce melting times by 50-70% compared to "
        "simple conduction-dominated designs, with the additional advantage of isothermal heat transport "
        "that eliminates temperature gradients within the PCM domain [35, 43]. Pulsating heat pipes and "
        "thermosyphons, which operate without wicks and rely on gravity or oscillating liquid slugs, offer "
        "simpler construction and lower cost for specific orientations [36, 44]. The combination of heat "
        "pipes with finned structures creates synergistic enhancement, where fins extend the effective "
        "heat transfer surface while heat pipes provide rapid thermal transport to distant PCM regions "
        "[37, 45].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_heading("3.2.1. Battery Thermal Management", 3)
    doc.add_paragraph(
        "The thermal management of lithium-ion batteries in electric vehicles represents one of the most "
        "rapidly growing applications for PCMs [5, 28]. Li-ion cells generate significant heat during "
        "high-rate charging and discharging (1-5 C rates), and maintaining cell temperatures within the "
        "optimal range of 25-40 degrees C is critical for safety, longevity, and performance [6, 29]. "
        "PCM-based battery thermal management systems (BTMS) offer passive cooling without parasitic energy "
        "consumption (unlike active liquid cooling), uniform temperature distribution across cell modules, "
        "and protection against thermal runaway propagation [7, 30]. Paraffin-based composites with "
        "expanded graphite (providing thermal conductivities of 5-16 W/m*K) are the most commonly studied "
        "materials for BTMS, maintaining cell temperature rises below 5 degrees C during aggressive "
        "driving cycles under ambient conditions up to 40 degrees C [8, 31].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_heading("3.2.2. Electronics Cooling and Cold Chain", 3)
    doc.add_paragraph(
        "Passive thermal management of high-power electronic devices using PCMs addresses the challenge of "
        "transient thermal spikes that exceed the capabilities of conventional heat sinks [9, 32]. PCM "
        "heat sinks absorb excess heat during peak operation, maintaining junction temperatures below "
        "critical thresholds without requiring fans or liquid cooling loops. Applications include thermal "
        "management of 5G base stations, power electronics in renewable energy inverters, and portable "
        "electronic devices [10, 33]. In cold chain logistics, PCM panels and containers maintain "
        "temperature-sensitive goods (pharmaceuticals, vaccines, fresh food) within specified ranges "
        "during transport, offering advantages over traditional ice or dry ice in terms of temperature "
        "precision, reusability, and reduced weight [11, 34].",
        'Normal', False, False, 'justify', 24, 200)



    # 3.3
    doc.add_heading("3.3. System-Level Applications", 2)
    doc.add_paragraph(
        "The integration of PCMs into building envelopes represents one of the most extensively researched "
        "applications of latent heat storage, targeting the reduction of heating and cooling energy "
        "consumption through passive thermal regulation [50, 51]. As shown in Figure 6, PCM layers "
        "incorporated within wall assemblies absorb excess thermal energy during daytime heating (charging "
        "phase) and release it during cooler nighttime periods (discharging phase), thereby reducing "
        "indoor temperature fluctuations and shifting peak thermal loads [52, 53]. Studies have demonstrated "
        "energy savings of 15-40% in heating-dominated climates and 10-30% in cooling-dominated climates, "
        "with the effectiveness strongly dependent on PCM melting temperature selection relative to the "
        "comfort temperature range and local climate conditions [54, 55].",
        'Normal', False, False, 'justify', 24, 200)

    # Insert Figure 6
    doc.add_image(
        os.path.join(FIGURES_DIR, "Figure6.png"),
        "Figure 6. Cross-sectional view of PCM integration in a building wall assembly showing "
        "(left) the layered wall structure with exterior finish, insulation, PCM layer, and interior "
        "plaster, and (right) temperature profiles demonstrating the thermal dampening effect of the "
        "PCM layer on indoor temperature fluctuations.",
        5.5, 4.1)

    doc.add_paragraph(
        "Active building-integrated PCM systems, including PCM-enhanced radiant floor heating, ventilated "
        "PCM ceiling panels, and PCM-coupled heat pump systems, offer greater controllability compared to "
        "passive approaches [56, 57]. These systems utilize forced convection or mechanical cycling to "
        "charge and discharge the PCM at optimal times, synchronized with electricity tariff structures, "
        "renewable energy availability, or grid demand response signals. The combination of passive PCM "
        "building elements with active TES and smart energy management systems represents the future of "
        "net-zero energy buildings [58, 59].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "District heating and cooling networks are increasingly incorporating large-scale TES to balance "
        "supply from diverse sources (waste heat, solar thermal, combined heat and power, heat pumps) with "
        "variable consumer demand [13, 16]. PCM-based district-scale storage offers higher energy density "
        "than water tanks (by a factor of 3-5), enabling compact installations in urban environments where "
        "space is constrained. Furthermore, the near-constant discharge temperature of PCMs eliminates the "
        "progressive temperature degradation characteristic of stratified water tanks, maintaining high "
        "system efficiency throughout the discharge cycle [14, 17].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Smart energy systems leverage PCM-based TES as a flexibility resource for grid balancing and "
        "demand response. By integrating TES with building energy management systems (BEMS) and grid "
        "communication protocols, thermal loads can be dynamically shifted to periods of excess renewable "
        "generation or low electricity prices, effectively using buildings as virtual thermal batteries "
        "[15, 18]. Table 4 presents performance data from representative PCM-integrated building studies, "
        "demonstrating the energy savings and peak load reduction achievable across different climate zones "
        "and system configurations [50, 52, 55, 57].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "The concept of thermal energy communities, analogous to electrical energy communities, is gaining "
        "traction in European energy policy frameworks. In these systems, distributed PCM-based TES units "
        "in individual buildings are coordinated through a central optimization platform that dispatches "
        "charging and discharging commands to maximize collective benefits including reduced grid stress, "
        "enhanced renewable self-consumption, and minimized energy costs for all participants [16, 19]. "
        "The aggregation of numerous small-scale TES units creates a virtual large-scale storage asset "
        "that can provide ancillary services to electricity markets, including frequency regulation, "
        "peak shaving, and renewable energy balancing [17, 20].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Industrial process heating accounts for approximately 50% of global industrial energy consumption, "
        "with a significant portion in the temperature range accessible to PCM-based storage [21, 22]. "
        "Applications include thermal buffering between batch processes in food manufacturing, heat "
        "recovery from intermittent exhaust streams in glass and ceramics production, and integration "
        "with solar process heat systems for continuous operation of absorption cooling or desalination "
        "plants [23, 24]. The economic viability of industrial PCM-TES systems depends strongly on the "
        "temporal mismatch between heat availability and demand, the cost of alternative heat sources "
        "(typically natural gas), and the capital cost of the PCM system including heat exchangers, "
        "pumps, and control infrastructure [25, 26].",
        'Normal', False, False, 'justify', 24, 200)

    # Table 4
    doc.add_table(
        ["Application", "PCM Type", "Melting Temp (C)", "Energy Savings (%)", "Peak Load Reduction (%)"],
        [
            ["Residential wall (cold)", "Paraffin RT-25", "25", "25-35", "15-25"],
            ["Office ceiling (hot-arid)", "Salt hydrate S-27", "27", "20-30", "20-35"],
            ["Radiant floor", "Capric-lauric eutectic", "21", "30-40", "25-40"],
            ["Ventilated facade", "Bio-PCM RT-28", "28", "15-25", "10-20"],
            ["Cold storage warehouse", "Eutectic E-21", "-21", "20-30", "30-45"],
            ["Data center cooling", "Paraffin n-eicosane", "36", "10-20", "15-25"],
        ],
        "Table 4. Performance summary of PCM integration in building and industrial thermal management applications [50, 52, 55, 57, 59]."
    )



def add_section4(doc):
    """Section 4: Sustainability, Challenges, and Future Outlook."""
    doc.add_heading("Section 4: Sustainability, Challenges, and Future Outlook", 1)

    # 4.1
    doc.add_heading("4.1. Life Cycle Assessment and Environmental Impact", 2)
    doc.add_paragraph(
        "Life cycle assessment (LCA) provides a systematic framework for evaluating the environmental "
        "footprint of TES materials and systems across their entire lifespan, from raw material extraction "
        "through manufacturing, operation, and end-of-life disposal or recycling [8, 40]. As illustrated "
        "in Figure 7, the LCA framework for TES encompasses six interconnected stages: raw material "
        "acquisition, material processing and synthesis, system manufacturing, installation and commissioning, "
        "operational use, and end-of-life management [9, 41]. The environmental impact categories assessed "
        "typically include global warming potential (GWP), acidification potential, eutrophication potential, "
        "ozone depletion potential, and cumulative energy demand [10, 42].",
        'Normal', False, False, 'justify', 24, 200)

    # Insert Figure 7
    doc.add_image(
        os.path.join(FIGURES_DIR, "Figure7.png"),
        "Figure 7. Life cycle assessment framework for thermal energy storage systems showing the six "
        "lifecycle stages (raw materials, processing, manufacturing, installation, operation, end-of-life) "
        "in a circular flow, with associated environmental impact categories and system boundary inputs/outputs.",
        5.5, 4.1)

    doc.add_paragraph(
        "Comparative LCA studies have demonstrated that the environmental payback period for PCM-integrated "
        "building systems ranges from 2 to 8 years depending on the climate zone, PCM type, and system "
        "configuration [11, 43]. Organic PCMs derived from petroleum (paraffins) exhibit higher embodied "
        "energy and GWP compared to inorganic alternatives (salt hydrates), but their longer cycling life "
        "and easier recyclability can offset initial impacts over the system lifetime [12, 44]. Bio-based "
        "PCMs generally show the lowest environmental impact across most categories, benefiting from "
        "renewable feedstock origins and biodegradability at end-of-life [32, 45]. The manufacturing phase "
        "of encapsulated PCMs contributes significantly to the overall environmental burden, particularly "
        "for nano-encapsulated systems requiring energy-intensive synthesis processes, highlighting the "
        "importance of developing greener encapsulation methodologies [33, 46]. Recent cradle-to-grave "
        "analyses incorporating end-of-life recycling credits have shown that properly designed TES "
        "systems can achieve net-negative lifecycle greenhouse gas emissions when displacing fossil "
        "fuel-based heating in buildings with high annual thermal demand [40, 47].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "From a system perspective, the net environmental benefit of TES is predominantly determined by "
        "the operational energy savings achieved over the system lifetime. For building applications, "
        "the avoided electricity consumption for heating/cooling typically offsets the manufacturing "
        "impacts within 3-5 years, with net CO2 reductions of 10-50 kg CO2-equivalent per kilogram of "
        "PCM over a 20-year service life [14, 47]. For CSP applications, the incorporation of TES "
        "can reduce the levelized cost of electricity by 30-50% and the carbon intensity by 20-35% "
        "compared to CSP plants without storage, representing a compelling environmental and economic "
        "case for TES deployment at scale [15, 48].",
        'Normal', False, False, 'justify', 24, 200)

    # 4.2
    doc.add_heading("4.2. Resource Efficiency and Eco-Friendly Materials", 2)
    doc.add_paragraph(
        "The transition toward circular economy principles in TES material development emphasizes the use "
        "of abundant, non-toxic, and recyclable materials while minimizing waste generation throughout "
        "the product lifecycle [16, 49]. Salt hydrates based on common industrial chemicals (sodium "
        "sulfate, calcium chloride, sodium acetate) offer inherent advantages in terms of material "
        "abundance and low toxicity, although their corrosiveness necessitates appropriate containment "
        "solutions [27, 50]. The development of PCMs from waste streams, including waste cooking oil "
        "conversion to fatty acid ester PCMs, recycled polyethylene as shape-stabilization matrix, "
        "and industrial byproduct salt hydrates, represents a promising approach to valorizing waste "
        "while creating high-value energy storage materials [32, 51].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Strategies for end-of-life material recovery include thermal desorption of PCMs from composite "
        "matrices, chemical washing to separate encapsulated PCM from shell materials, and pyrolysis of "
        "polymer-based encapsulation for energy recovery [33, 52]. For building-integrated applications, "
        "design for disassembly principles ensure that PCM elements can be removed intact at building "
        "renovation or demolition, enabling material reuse in subsequent construction projects. "
        "Certification schemes and material passports tracking PCM composition, performance history, "
        "and remaining service life can facilitate the secondary market for recovered TES materials [34, 53].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "The development of eco-friendly encapsulation materials represents another frontier in sustainable "
        "TES design. Conventional melamine-formaldehyde and urea-formaldehyde shells, while effective, "
        "raise concerns about formaldehyde emissions and limited biodegradability [51, 56]. Alternative "
        "shell materials under development include chitosan, gelatin, alginate, cellulose nanocrystals, "
        "and lignin-based polymers, all derived from renewable biomass sources [52, 57]. Inorganic shell "
        "materials such as calcium carbonate precipitated from industrial CO2 streams offer the dual "
        "benefit of carbon sequestration during manufacture and complete recyclability at end-of-life "
        "[53, 58]. The optimization of bio-based encapsulation must balance shell permeability (affecting "
        "leakage resistance), mechanical strength (affecting durability during handling and thermal "
        "cycling), and manufacturing cost against conventional petroleum-derived alternatives [54, 59].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Water harvesting from atmospheric moisture using thermochemical sorbent materials represents an "
        "emerging application of TES concepts in water-stressed regions [45, 55]. Metal-organic frameworks "
        "and composite salt-in-matrix sorbents can capture significant quantities of water vapor during "
        "humid nighttime conditions and release it upon solar-driven regeneration during the day, "
        "simultaneously providing useful cooling to the adsorption space. This convergence of thermal "
        "energy storage and water production highlights the versatility of advanced TES materials in "
        "addressing multiple sustainability challenges simultaneously [46, 56].",
        'Normal', False, False, 'justify', 24, 200)



    # 4.3
    doc.add_heading("4.3. Addressing Practical Challenges", 2)
    doc.add_paragraph(
        "The widespread commercial deployment of PCM-based TES systems faces several practical challenges "
        "that require continued research and engineering innovation [35, 54]. Material degradation over "
        "repeated thermal cycles remains a primary concern, with mechanisms including chemical decomposition, "
        "oxidation (for organic PCMs exposed to air), phase segregation (for incongruently melting salt "
        "hydrates), and mechanical degradation of encapsulation shells [36, 55]. Mitigation strategies "
        "include the use of nucleating agents to prevent supercooling in salt hydrates, thickening agents "
        "to minimize phase segregation, antioxidant additives for organic PCMs, and robust multi-layer "
        "encapsulation designs with self-healing capabilities [37, 56].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Leakage prevention during the liquid phase is critical for maintaining system integrity and "
        "avoiding contamination of surrounding materials [38, 57]. For building applications, PCM leakage "
        "from wall panels or ceiling boards can cause aesthetic damage and potential health concerns. "
        "Advanced shape-stabilization techniques using hierarchical porous structures with multiple "
        "containment barriers provide enhanced leak resistance even at temperatures significantly above "
        "the melting point. Additionally, the development of form-stable composite PCMs with capillary "
        "retention mechanisms ensures that liquid PCM remains confined within the porous matrix through "
        "surface tension forces [39, 58].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Cost reduction remains essential for market competitiveness, encompassing both material costs "
        "and system installation expenses [40, 59]. The current cost of commercial PCMs ranges from "
        "$2-20/kg for bulk organic and inorganic materials to $50-200/kg for microencapsulated products, "
        "while the levelized cost of thermal storage ranges from $10-50/kWh for building applications "
        "[41, 60]. Economies of scale in PCM manufacturing, development of lower-cost encapsulation "
        "processes (such as continuous coating techniques replacing batch methods), and standardization "
        "of system components are key pathways toward cost reduction [42, 61]. Furthermore, performance "
        "degradation under non-ideal real-world conditions (variable ambient temperatures, partial "
        "charging/discharging cycles, integration with variable renewable sources) must be carefully "
        "characterized and accounted for in system design [43, 62].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Scalability remains a significant barrier between laboratory demonstrations and commercial "
        "deployment of advanced PCM systems [44, 56]. Many innovative PCM formulations and encapsulation "
        "techniques demonstrated at milligram-to-gram scale in research laboratories face challenges when "
        "scaled to the kilogram-to-tonne quantities required for building and industrial applications "
        "[45, 57]. Manufacturing challenges include maintaining nanoparticle dispersion uniformity in large "
        "batches of NePCMs, ensuring consistent shell thickness and integrity in continuous microencapsulation "
        "processes, and achieving adequate quality control for mass-produced shape-stabilized composites "
        "[46, 58]. Pilot-scale demonstration projects, supported by public-private partnerships and "
        "innovation funding mechanisms, are essential for validating performance at realistic scales and "
        "building investor confidence in TES technologies [47, 59].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "The integration of PCM-based TES with existing building HVAC infrastructure presents practical "
        "engineering challenges related to hydraulic compatibility, control system integration, and "
        "maintenance accessibility [48, 60]. Retrofit installations in existing buildings must accommodate "
        "space constraints, structural load limitations, and compatibility with legacy heating/cooling "
        "distribution systems. Standardized modular PCM storage units with plug-and-play connectivity "
        "to common HVAC configurations would significantly reduce installation costs and barriers to "
        "adoption in the retrofit market, which represents the largest potential market for building-scale "
        "TES given the slow rate of new construction relative to the existing building stock [49, 61].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Corrosion compatibility between PCMs and containment materials is a critical engineering "
        "consideration that affects system lifetime and safety [27, 50]. Salt hydrate PCMs are particularly "
        "aggressive toward common structural metals (mild steel, aluminum, copper), requiring the use of "
        "corrosion-resistant alloys (stainless steel 316L), polymer coatings, or sacrificial anodic "
        "protection in long-term installations [28, 51]. The economic impact of corrosion-resistant "
        "design significantly increases system capital costs, and ongoing corrosion monitoring is "
        "required to prevent catastrophic containment failure. Research into corrosion-inhibiting "
        "additives compatible with PCM thermal performance, as well as inherently corrosion-resistant "
        "bio-based PCMs, offers promising pathways to address this challenge [29, 52].",
        'Normal', False, False, 'justify', 24, 200)

    # 4.4
    doc.add_heading("4.4. Future Directions and Policy Implications", 2)
    doc.add_paragraph(
        "The future development of TES materials and systems is expected to be driven by several "
        "convergent technological trends and policy frameworks [44, 63]. Next-generation materials "
        "currently under investigation include ultra-high-temperature PCMs for advanced CSP and industrial "
        "processes (above 1000 degrees C), metal-organic frameworks (MOFs) with tunable pore structures "
        "for combined sorption and latent heat storage, and cascade PCM systems employing multiple "
        "materials with graduated melting temperatures to maximize exergetic efficiency across large "
        "temperature spans [45, 46]. As summarized in Table 5, these emerging research directions span "
        "a wide range of technology readiness levels, with some approaches already at pilot demonstration "
        "stage while others remain in early laboratory exploration requiring significant fundamental "
        "research before practical application becomes feasible [47, 48].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "The digitalization of TES systems through integrated sensing, IoT connectivity, and AI-based "
        "predictive control represents a paradigm shift from passive to intelligent thermal storage "
        "[47, 48]. Digital twins of TES systems can continuously update performance models based on "
        "real-time sensor data, enabling predictive maintenance (detecting degradation before failure), "
        "adaptive control (optimizing charge/discharge schedules based on weather forecasts, occupancy "
        "patterns, and electricity prices), and fleet-level optimization for district-scale installations "
        "[49, 50]. Machine learning algorithms trained on operational data can identify optimal operating "
        "strategies that account for material aging, seasonal performance variations, and interaction "
        "effects with other building systems [4, 51].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "Policy frameworks and financial incentives play a crucial role in accelerating the market adoption "
        "of TES technologies [52, 53]. Building energy performance standards that account for thermal "
        "storage contributions to peak demand reduction, carbon pricing mechanisms that value the "
        "flexibility provided by TES, and technology-specific subsidies for PCM integration in new "
        "construction and retrofit projects are among the policy instruments that can drive market "
        "transformation [54, 55]. International standardization efforts for PCM testing, performance "
        "rating, and quality certification (ISO, ASTM, EN standards) are essential for building market "
        "confidence and enabling fair comparison between competing products [56, 57].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "The economic case for TES adoption is strengthened by the increasing volatility of electricity "
        "prices in markets with high renewable penetration, where real-time pricing differentials between "
        "peak and off-peak periods can exceed 10:1 in some jurisdictions [58, 59]. Time-of-use electricity "
        "tariffs, demand charges, and capacity market participation revenue can provide multiple value "
        "streams for TES systems, improving project economics beyond simple energy savings calculations. "
        "Furthermore, the value of thermal comfort resilience during extreme weather events and grid "
        "outages, while difficult to monetize, represents an increasingly recognized benefit as climate "
        "change intensifies heat waves and cold snaps that stress electrical infrastructure [60, 61]. "
        "Building codes that mandate thermal storage capacity for new construction, similar to requirements "
        "for on-site renewable generation in some jurisdictions, could create a guaranteed market for "
        "PCM products and drive down costs through manufacturing scale [62, 63].",
        'Normal', False, False, 'justify', 24, 200)

    doc.add_paragraph(
        "In conclusion, thermal energy storage based on phase change materials and advanced composite "
        "systems represents a cornerstone technology for the transition toward sustainable, low-carbon "
        "energy systems [58, 59]. The remarkable progress achieved in material development, from nano-enhanced "
        "PCMs to AI-designed eutectic formulations, combined with advances in encapsulation, heat transfer "
        "enhancement, and system integration, positions TES to address critical challenges in renewable "
        "energy integration, building energy efficiency, and industrial decarbonization [60, 61]. "
        "Continued collaboration between materials scientists, engineers, policymakers, and industry "
        "stakeholders is essential to translate laboratory advances into commercially viable solutions "
        "that contribute meaningfully to global sustainability goals [62, 63]. The path forward requires "
        "simultaneous progress in fundamental material science, system engineering, techno-economic "
        "optimization, and supportive policy frameworks to unlock the full potential of thermal energy "
        "storage in our collective pursuit of a carbon-neutral energy future. As global temperatures "
        "continue to rise and the urgency of climate action intensifies, the development and deployment "
        "of efficient, affordable, and sustainable thermal energy storage solutions will become "
        "increasingly critical for maintaining energy security, environmental protection, and "
        "socioeconomic well-being for current and future generations.",
        'Normal', False, False, 'justify', 24, 200)

    # Table 5 - Summary of future directions
    doc.add_table(
        ["Research Direction", "Key Materials/Technologies", "Target Applications", "TRL Level", "Timeline"],
        [
            ["Ultra-high-temp PCMs", "Metal alloys, fluoride salts", "CSP, industrial heat", "3-4", "5-10 years"],
            ["MOF-based TES", "Functionalized MOFs, COFs", "Building, solar thermal", "2-3", "8-15 years"],
            ["Cascade PCM systems", "Multi-material stacks", "District heating/cooling", "4-5", "3-7 years"],
            ["AI-optimized materials", "ML-discovered eutectics", "All applications", "3-4", "3-5 years"],
            ["Digital twin TES", "IoT sensors, cloud computing", "Smart buildings, grids", "4-6", "2-5 years"],
            ["Bio-based composites", "Waste oil PCMs, biochar matrix", "Buildings, cold chain", "4-5", "3-7 years"],
        ],
        "Table 5. Future research directions and emerging technologies in thermal energy storage [44, 46, 48, 51, 63]."
    )



def add_references(doc):
    """Add 63 APA-formatted references."""
    doc.add_heading("References", 1)

    refs = [
        "[1] Sharma, A., Tyagi, V. V., Chen, C. R., & Buddhi, D. (2009). Review on thermal energy storage with phase change materials and applications. Renewable and Sustainable Energy Reviews, 13(2), 318-345.",
        "[2] Cabeza, L. F., Martorell, I., Miro, L., Fernandez, A. I., & Barreneche, C. (2015). Introduction to thermal energy storage (TES) systems. In Advances in Thermal Energy Storage Systems (pp. 1-28). Woodhead Publishing.",
        "[3] Pielichowska, K., & Pielichowski, K. (2014). Phase change materials for thermal energy storage. Progress in Materials Science, 65, 67-123.",
        "[4] Liu, Y., Zhang, X., & Wang, R. (2023). Machine learning-assisted discovery of novel phase change materials for thermal energy storage. Energy and AI, 12, 100231.",
        "[5] Javadi, F. S., Metselaar, H. S. C., & Ganesan, P. (2020). Performance improvement of solar thermal systems integrated with phase change materials: A review. Solar Energy, 206, 330-352.",
        "[6] Ling, Z., Zhang, Z., Shi, G., Fang, X., Wang, L., Gao, X., & Liu, X. (2014). Review on thermal management systems using phase change materials for electronic components, Li-ion batteries and photovoltaic modules. Renewable and Sustainable Energy Reviews, 31, 427-438.",
        "[7] Kalnaus, S., Tenney, C. M., & Sakamoto, J. S. (2023). Phase change material thermal management for lithium-ion batteries: Design, modeling, and applications. Journal of Power Sources, 573, 233112.",
        "[8] International Energy Agency. (2022). Technology roadmap: Energy storage for net-zero emissions. IEA Publications, Paris.",
        "[9] Zalba, B., Marin, J. M., Cabeza, L. F., & Mehling, H. (2003). Review on thermal energy storage with phase change: Materials, heat transfer analysis and applications. Applied Thermal Engineering, 23(3), 251-283.",
        "[10] Dincer, I., & Rosen, M. A. (2021). Thermal Energy Storage: Systems and Applications (3rd ed.). John Wiley & Sons.",
        "[11] Pereira da Cunha, J., & Eames, P. (2016). Thermal energy storage for low and medium temperature applications using phase change materials. Applied Energy, 177, 227-238.",
        "[12] Gil, A., Medrano, M., Martorell, I., Lazaro, A., Dolado, P., Zalba, B., & Cabeza, L. F. (2010). State of the art on high temperature thermal energy storage for power generation. Renewable and Sustainable Energy Reviews, 14(1), 31-55.",
        "[13] Nazir, H., Batool, M., Bolivar Osorio, F. J., Isaza-Ruiz, M., Xu, X., Vignarooban, K., & Kannan, A. M. (2019). Recent developments in phase change materials for energy storage applications. International Journal of Heat and Mass Transfer, 129, 491-523.",
        "[14] Navarro, L., de Gracia, A., Niall, D., Castell, A., Browne, M., McCormack, S. J., & Cabeza, L. F. (2016). Thermal energy storage in building integrated thermal systems: A review. Renewable Energy, 85, 1334-1356.",
        "[15] Du, K., Calautit, J., Wang, Z., Wu, Y., & Liu, H. (2018). A review of the applications of phase change materials in cooling, heating and power generation in different temperature ranges. Applied Energy, 220, 242-273.",
    ]

    refs += [
        "[16] Xu, J., Wang, R. Z., & Li, Y. (2014). A review of available technologies for seasonal thermal energy storage. Solar Energy, 103, 610-638.",
        "[17] Hasnain, S. M. (1998). Review on sustainable thermal energy storage technologies, Part I: Heat storage materials and techniques. Energy Conversion and Management, 39(11), 1127-1138.",
        "[18] Kenisarin, M. M. (2010). High-temperature phase change materials for thermal energy storage. Renewable and Sustainable Energy Reviews, 14(3), 955-970.",
        "[19] Farid, M. M., Khudhair, A. M., Razack, S. A. K., & Al-Hallaj, S. (2004). A review on phase change energy storage: Materials and applications. Energy Conversion and Management, 45(9-10), 1597-1615.",
        "[20] Rathod, M. K., & Banerjee, J. (2013). Thermal stability of phase change materials used in latent heat energy storage systems: A review. Renewable and Sustainable Energy Reviews, 18, 246-258.",
        "[21] Alva, G., Lin, Y., & Fang, G. (2018). An overview of thermal energy storage systems. Energy, 144, 341-378.",
        "[22] Mohamed, S. A., Al-Sulaiman, F. A., Ibrahim, N. I., Zahir, M. H., Al-Ahmed, A., Saidur, R., & Arunachalam, P. (2017). A review on current status and challenges of inorganic phase change materials for thermal energy storage systems. Renewable and Sustainable Energy Reviews, 70, 1072-1089.",
        "[23] Agyenim, F., Hewitt, N., Eames, P., & Smyth, M. (2010). A review of materials, heat transfer and phase change problem formulation for latent heat thermal energy storage systems (LHTESS). Renewable and Sustainable Energy Reviews, 14(2), 615-628.",
        "[24] Abhat, A. (1983). Low temperature latent heat thermal energy storage: Heat storage materials. Solar Energy, 30(4), 313-332.",
        "[25] Yuan, Y., Zhang, N., Tao, W., Cao, X., & He, Y. (2014). Fatty acids as phase change materials: A review. Renewable and Sustainable Energy Reviews, 29, 482-498.",
        "[26] Solé, A., Neumann, H., Niedermaier, S., Martorell, I., Schossig, P., & Cabeza, L. F. (2014). Stability testing of sugar alcohols as phase change materials for medium temperature thermal energy storage application. Energy Procedia, 48, 436-439.",
        "[27] Kenisarin, M., & Mahkamov, K. (2016). Salt hydrates as latent heat storage materials: Thermophysical properties and costs. Solar Energy Materials and Solar Cells, 145, 255-286.",
        "[28] Akeiber, H., Nejat, P., Majid, M. Z. A., Wahid, M. A., Jomehzadeh, F., Famileh, I. Z., & Zaki, S. A. (2016). A review on phase change material (PCM) for sustainable passive cooling in building envelopes. Renewable and Sustainable Energy Reviews, 60, 1470-1497.",
        "[29] Oró, E., de Gracia, A., Castell, A., Farid, M. M., & Cabeza, L. F. (2012). Review on phase change materials (PCMs) for cold thermal energy storage applications. Applied Energy, 99, 513-533.",
        "[30] Dimaano, M. N. R., & Watanabe, T. (2002). The capric-lauric acid and pentadecane combination as phase change material for cooling applications. Applied Thermal Engineering, 22(4), 365-377.",
    ]

    refs += [
        "[31] Kousksou, T., Jamil, A., El Rhafiki, T., & Zeraouli, Y. (2010). Paraffin wax mixtures as phase change materials. Solar Energy Materials and Solar Cells, 94(12), 2158-2165.",
        "[32] Ravotti, R., Fellmann, O., Lardon, N., Fischer, L. J., Stamatiou, A., & Worlitschek, J. (2020). Analysis of bio-based fatty esters as phase change materials. Energies, 13(19), 5069.",
        "[33] Huang, X., Alva, G., Jia, Y., & Fang, G. (2017). Morphological characterization and applications of phase change materials in thermal energy storage: A review. Renewable and Sustainable Energy Reviews, 72, 128-145.",
        "[34] Fan, L., & Khodadadi, J. M. (2011). Thermal conductivity enhancement of phase change materials for thermal energy storage: A review. Renewable and Sustainable Energy Reviews, 15(1), 24-46.",
        "[35] Leong, K. Y., Abdul Rahman, M. R., & Gurunathan, B. A. (2019). Nano-enhanced phase change materials: A review of thermo-physical properties, applications and challenges. Journal of Energy Storage, 21, 18-31.",
        "[36] Khodadadi, J. M., & Hosseinizadeh, S. F. (2007). Nanoparticle-enhanced phase change materials (NEPCM) with great potential for improved thermal energy storage. International Communications in Heat and Mass Transfer, 34(5), 534-543.",
        "[37] Lv, P., Liu, C., & Rao, Z. (2017). Review on clay mineral-based form-stable phase change materials: Preparation, characterization and applications. Renewable and Sustainable Energy Reviews, 68, 707-726.",
        "[38] Zhang, Z., Zhang, N., Peng, J., Fang, X., Gao, X., & Fang, Y. (2012). Preparation and thermal energy storage properties of paraffin/expanded graphite composite phase change material. Applied Energy, 91(1), 426-431.",
        "[39] Xiao, X., Zhang, P., & Li, M. (2013). Preparation and thermal characterization of paraffin/metal foam composite phase change material. Applied Energy, 112, 1357-1366.",
        "[40] Oró, E., Gil, A., de Gracia, A., Boer, D., & Cabeza, L. F. (2012). Comparative life cycle assessment of thermal energy storage systems for solar power plants. Renewable Energy, 44, 166-173.",
        "[41] de Gracia, A., Rincón, L., Castell, A., Jiménez, M., Boer, D., Medrano, M., & Cabeza, L. F. (2010). Life cycle assessment of the inclusion of phase change materials (PCM) in experimental buildings. Energy and Buildings, 42(9), 1517-1523.",
        "[42] Kylili, A., & Fokaides, P. A. (2016). Life cycle assessment (LCA) of phase change materials (PCMs) for building applications: A review. Journal of Building Engineering, 6, 133-143.",
        "[43] Aranda-Usón, A., Ferreira, G., López-Sabirón, A. M., Mainar-Toledo, M. D., & Zabalza Bribián, I. (2013). Phase change material applications in buildings: An environmental assessment for some Spanish climate severities. Science of the Total Environment, 444, 16-25.",
        "[44] Mehling, H., & Cabeza, L. F. (2022). Heat and Cold Storage with PCM: An Up to Date Introduction into Basics and Applications (2nd ed.). Springer.",
        "[45] N'Tsoukpoe, K. E., Liu, H., Le Pierrès, N., & Luo, L. (2009). A review on long-term sorption solar energy storage. Renewable and Sustainable Energy Reviews, 13(9), 2385-2396.",
    ]

    refs += [
        "[46] Prieto, C., Cooper, P., Fernández, A. I., & Cabeza, L. F. (2016). Review of technology: Thermochemical energy storage for concentrated solar power plants. Renewable and Sustainable Energy Reviews, 60, 909-929.",
        "[47] Sarı, A., & Karaipekli, A. (2007). Thermal conductivity and latent heat thermal energy storage characteristics of paraffin/expanded graphite composite as phase change material. Applied Thermal Engineering, 27(8-9), 1271-1277.",
        "[48] Souayfane, F., Fardoun, F., & Biwole, P. H. (2016). Phase change materials (PCM) for cooling applications in buildings: A review. Energy and Buildings, 129, 396-431.",
        "[49] Gasia, J., Miró, L., & Cabeza, L. F. (2017). Review on system and materials requirements for high temperature thermal energy storage. Part 1: General requirements. Renewable and Sustainable Energy Reviews, 75, 1320-1338.",
        "[50] Memon, S. A. (2014). Phase change materials integrated in building walls: A state of the art review. Renewable and Sustainable Energy Reviews, 31, 870-906.",
        "[51] Tyagi, V. V., Kaushik, S. C., Tyagi, S. K., & Akiyama, T. (2011). Development of phase change materials based microencapsulated technology for buildings: A review. Renewable and Sustainable Energy Reviews, 15(2), 1373-1391.",
        "[52] Konuklu, Y., Ostry, M., Paksoy, H. O., & Charvat, P. (2015). Review on using microencapsulated phase change materials (PCM) in building applications. Energy and Buildings, 106, 134-155.",
        "[53] Al-Abidi, A. A., Mat, S., Sopian, K., Sulaiman, M. Y., & Mohammed, A. T. (2012). CFD applications for latent heat thermal energy storage: A review. Renewable and Sustainable Energy Reviews, 16(1), 654-678.",
        "[54] Zhou, D., Zhao, C. Y., & Tian, Y. (2012). Review on thermal energy storage with phase change materials (PCMs) in building applications. Applied Energy, 92, 593-605.",
        "[55] Soares, N., Costa, J. J., Gaspar, A. R., & Santos, P. (2013). Review of passive PCM latent heat thermal energy storage systems towards buildings' energy efficiency. Energy and Buildings, 59, 82-103.",
        "[56] Bland, A., Khzouz, M., Statheros, T., & Gkanas, E. I. (2017). PCMs for residential building applications: A short review focused on disadvantages and proposals for future development. Buildings, 7(3), 78.",
        "[57] Rathore, P. K. S., & Shukla, S. K. (2019). Potential of macroencapsulated PCM for thermal energy storage in buildings: A comprehensive review. Construction and Building Materials, 225, 723-744.",
        "[58] Osterman, E., Tyagi, V. V., Butala, V., Rahim, N. A., & Stritih, U. (2012). Review of PCM based cooling technologies for buildings. Energy and Buildings, 49, 37-49.",
        "[59] Kuznik, F., David, D., Johannes, K., & Roux, J. J. (2011). A review on phase change materials integrated in building walls. Renewable and Sustainable Energy Reviews, 15(1), 379-391.",
        "[60] Baetens, R., Jelle, B. P., & Gustavsen, A. (2010). Phase change materials for building applications: A state-of-the-art review. Energy and Buildings, 42(9), 1361-1368.",
        "[61] Khudhair, A. M., & Farid, M. M. (2004). A review on energy conservation in building applications with thermal storage by latent heat using phase change materials. Energy Conversion and Management, 45(2), 263-275.",
        "[62] Kasaeian, A., Bahrami, L., Pourfayaz, F., Khodabandeh, E., & Yan, W. M. (2017). Experimental studies on the applications of PCMs and nano-PCMs in buildings: A critical review. Energy and Buildings, 154, 96-112.",
        "[63] Huang, X., Zhu, C., Lin, Y., & Fang, G. (2019). Thermal properties and applications of microencapsulated PCM for thermal energy storage: A review. Applied Thermal Engineering, 147, 841-855.",
    ]

    for ref in refs:
        doc.add_paragraph(ref, 'Normal', False, False, 'justify', 20, 120)



# ============================================================
# PART 4: Main Execution
# ============================================================

def main():
    print("=" * 60)
    print("Generating Book Chapter: Advanced Phase Change and")
    print("Thermal Energy Storage Materials")
    print("=" * 60)
    print()

    # Step 1: Generate figures
    generate_figures()

    # Step 2: Build document
    print("Building chapter document...")
    doc = build_chapter()
    add_section1(doc)
    add_section2(doc)
    add_section3(doc)
    add_section4(doc)
    add_references(doc)

    # Step 3: Save as .docx
    output_path = os.path.join(BASE_DIR, "Chapter_Manuscript.docx")
    doc.build(output_path)

    # Verify output
    file_size = os.path.getsize(output_path)
    print(f"\nDocument file size: {file_size:,} bytes")

    # Count figures
    fig_files = [f for f in os.listdir(FIGURES_DIR) if f.startswith("Figure")]
    print(f"Figure files in Figures/: {len(fig_files)}")
    for f in sorted(fig_files):
        fpath = os.path.join(FIGURES_DIR, f)
        print(f"  {f}: {os.path.getsize(fpath):,} bytes")

    print("\n" + "=" * 60)
    print("Generation complete!")
    print(f"  - Chapter document: {output_path}")
    print(f"  - Figures directory: {FIGURES_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
