#!/usr/bin/env python3
"""
Generate professional figures for 'AI for Electric Vehicles and Charging Infrastructure' chapter.
All figures are created programmatically using pure Python (no AI-generated content).
Output: PNG files at 300 DPI resolution.
Optimized for speed using array-based pixel manipulation.
"""

import struct
import zlib
import math
import os
import array

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ev_chapter_figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)


class FastPNG:
    """Fast RGB PNG image writer using bytearray for pixel storage."""

    def __init__(self, width, height, bg=(255, 255, 255)):
        self.w = width
        self.h = height
        # Store as flat bytearray: row-major, 3 bytes per pixel
        self.data = bytearray(bg * (width * height))


    def _idx(self, x, y):
        return (y * self.w + x) * 3

    def pixel(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = self._idx(x, y)
            self.data[i] = c[0]
            self.data[i+1] = c[1]
            self.data[i+2] = c[2]

    def fill_rect(self, x, y, w, h, c):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        row_bytes = bytes(c) * (x1 - x0)
        for row in range(y0, y1):
            start = self._idx(x0, row)
            end = start + (x1 - x0) * 3
            self.data[start:end] = row_bytes

    def hline(self, x, y, length, c, thickness=1):
        for t in range(thickness):
            self.fill_rect(x, y + t, length, 1, c)

    def vline(self, x, y, length, c, thickness=1):
        for t in range(thickness):
            self.fill_rect(x + t, y, 1, length, c)

    def rect_outline(self, x, y, w, h, c, t=2):
        self.hline(x, y, w, c, t)
        self.hline(x, y + h - t, w, c, t)
        self.vline(x, y, h, c, t)
        self.vline(x + w - t, y, h, c, t)

    def line(self, x1, y1, x2, y2, c, thickness=2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        steps = max(dx, dy, 1)
        for i in range(steps + 1):
            t = i / steps
            px = int(x1 + (x2 - x1) * t)
            py = int(y1 + (y2 - y1) * t)
            for tx in range(-(thickness//2), (thickness+1)//2):
                for ty in range(-(thickness//2), (thickness+1)//2):
                    self.pixel(px + tx, py + ty, c)


    def arrow(self, x1, y1, x2, y2, c, thickness=2, head=6):
        self.line(x1, y1, x2, y2, c, thickness)
        angle = math.atan2(y2 - y1, x2 - x1)
        a1 = angle + 2.5
        a2 = angle - 2.5
        hx1 = int(x2 - head * math.cos(a1))
        hy1 = int(y2 - head * math.sin(a1))
        hx2 = int(x2 - head * math.cos(a2))
        hy2 = int(y2 - head * math.sin(a2))
        self.line(x2, y2, hx1, hy1, c, thickness)
        self.line(x2, y2, hx2, hy2, c, thickness)

    def save(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)  # filter byte
            start = y * self.w * 3
            raw.extend(self.data[start:start + self.w * 3])

        sig = b'\x89PNG\r\n\x1a\n'

        def chunk(ctype, data):
            c = ctype + data
            crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
            return struct.pack('>I', len(data)) + c + crc

        ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0))
        phys = chunk(b'pHYs', struct.pack('>IIB', 11811, 11811, 1))  # 300 DPI
        idat = chunk(b'IDAT', zlib.compress(bytes(raw), 6))
        iend = chunk(b'IEND', b'')

        with open(path, 'wb') as f:
            f.write(sig + ihdr + phys + idat + iend)
        print(f"  OK: {path} ({self.w}x{self.h})")


# ============================================================
# Bitmap font - 5x7 chars, drawn at configurable scale
# ============================================================
GLYPHS = {
    'A':[0x4,0xA,0x11,0x1F,0x11,0x11,0x11],'B':[0x1E,0x11,0x11,0x1E,0x11,0x11,0x1E],
    'C':[0xE,0x11,0x10,0x10,0x10,0x11,0xE],'D':[0x1C,0x12,0x11,0x11,0x11,0x12,0x1C],
    'E':[0x1F,0x10,0x10,0x1E,0x10,0x10,0x1F],'F':[0x1F,0x10,0x10,0x1E,0x10,0x10,0x10],
    'G':[0xE,0x11,0x10,0x17,0x11,0x11,0xF],'H':[0x11,0x11,0x11,0x1F,0x11,0x11,0x11],
    'I':[0xE,0x4,0x4,0x4,0x4,0x4,0xE],'J':[0x7,0x2,0x2,0x2,0x2,0x12,0xC],
    'K':[0x11,0x12,0x14,0x18,0x14,0x12,0x11],'L':[0x10,0x10,0x10,0x10,0x10,0x10,0x1F],
    'M':[0x11,0x1B,0x15,0x15,0x11,0x11,0x11],'N':[0x11,0x19,0x15,0x13,0x11,0x11,0x11],
    'O':[0xE,0x11,0x11,0x11,0x11,0x11,0xE],'P':[0x1E,0x11,0x11,0x1E,0x10,0x10,0x10],
    'Q':[0xE,0x11,0x11,0x11,0x15,0x12,0xD],'R':[0x1E,0x11,0x11,0x1E,0x14,0x12,0x11],
    'S':[0xF,0x10,0x10,0xE,0x1,0x1,0x1E],'T':[0x1F,0x4,0x4,0x4,0x4,0x4,0x4],
    'U':[0x11,0x11,0x11,0x11,0x11,0x11,0xE],'V':[0x11,0x11,0x11,0x11,0xA,0xA,0x4],
    'W':[0x11,0x11,0x11,0x15,0x15,0x15,0xA],'X':[0x11,0x11,0xA,0x4,0xA,0x11,0x11],
    'Y':[0x11,0x11,0xA,0x4,0x4,0x4,0x4],'Z':[0x1F,0x1,0x2,0x4,0x8,0x10,0x1F],
    '0':[0xE,0x11,0x13,0x15,0x19,0x11,0xE],'1':[0x4,0xC,0x4,0x4,0x4,0x4,0xE],
    '2':[0xE,0x11,0x1,0x2,0x4,0x8,0x1F],'3':[0x1F,0x2,0x4,0x2,0x1,0x11,0xE],
    '4':[0x2,0x6,0xA,0x12,0x1F,0x2,0x2],'5':[0x1F,0x10,0x1E,0x1,0x1,0x11,0xE],
    '6':[0x6,0x8,0x10,0x1E,0x11,0x11,0xE],'7':[0x1F,0x1,0x2,0x4,0x8,0x8,0x8],
    '8':[0xE,0x11,0x11,0xE,0x11,0x11,0xE],'9':[0xE,0x11,0x11,0xF,0x1,0x2,0xC],
    ' ':[0,0,0,0,0,0,0],'.':[0,0,0,0,0,0,0x4],',':[0,0,0,0,0,0x4,0x8],
    '-':[0,0,0,0x1F,0,0,0],'/':[0x1,0x2,0x2,0x4,0x8,0x8,0x10],
    '(':[0x2,0x4,0x8,0x8,0x8,0x4,0x2],')':[0x8,0x4,0x2,0x2,0x2,0x4,0x8],
    ':':[0,0x4,0x4,0,0x4,0x4,0],'%':[0x19,0x19,0x2,0x4,0x8,0x13,0x13],
    '|':[0x4,0x4,0x4,0x4,0x4,0x4,0x4],'+':[0,0x4,0x4,0x1F,0x4,0x4,0],
    '=':[0,0,0x1F,0,0x1F,0,0],'<':[0x2,0x4,0x8,0x10,0x8,0x4,0x2],
    '>':[0x8,0x4,0x2,0x1,0x2,0x4,0x8],'_':[0,0,0,0,0,0,0x1F],
}

def text(img, x, y, s, c=(0,0,0), sc=2):
    cx = x
    for ch in s:
        g = GLYPHS.get(ch.upper() if ch.isalpha() else ch)
        if g is None:
            cx += 6 * sc
            continue
        for ry, row in enumerate(g):
            for rx in range(5):
                if row & (0x10 >> rx):
                    img.fill_rect(cx + rx*sc, y + ry*sc, sc, sc, c)
        cx += 6 * sc

def tw(s, sc=2):
    return len(s) * 6 * sc

def text_c(img, cx, y, s, c=(0,0,0), sc=2):
    text(img, cx - tw(s, sc)//2, y, s, c, sc)


# ============================================================
# Colors
# ============================================================
C = {
    'db': (25, 55, 109), 'bl': (51, 102, 187), 'lb': (135, 175, 220), 'vlb': (200, 220, 245),
    'gn': (60, 150, 80), 'lg': (144, 200, 144), 'dg': (34, 100, 50),
    'or': (230, 140, 50), 'lo': (250, 200, 130),
    'rd': (200, 60, 60), 'lr': (240, 150, 150),
    'pu': (130, 70, 160), 'lp': (190, 160, 220),
    'gy': (128, 128, 128), 'lgy': (220, 220, 220), 'dgy': (64, 64, 64),
    'wh': (255, 255, 255), 'bk': (0, 0, 0),
    'tl': (0, 128, 128), 'gd': (200, 170, 50),
}


# ============================================================
# Figure 1: Hierarchical AI Architecture for Intelligent BMS
# ============================================================
def fig1():
    print("  Figure 1: BMS Architecture...")
    W, H = 900, 700
    img = FastPNG(W, H)

    text_c(img, W//2, 8, "HIERARCHICAL AI ARCHITECTURE FOR INTELLIGENT BMS", C['db'], 2)

    layers = [
        ("LAYER 5: FLEET ANALYTICS/CLOUD", C['lr'], C['rd'],
         ["Fleet Monitor", "Model Train", "Pred. Maint.", "Digital Twin"]),
        ("LAYER 4: DECISION AND CONTROL", C['lp'], C['pu'],
         ["Charge Ctrl", "Thermal Mgmt", "Cell Balance", "Safety Prot."]),
        ("LAYER 3: AI MODEL INFERENCE", C['lo'], C['or'],
         ["SOC Estim.", "SOH Predict", "RUL Forecast", "Fault Detect"]),
        ("LAYER 2: DATA PREPROCESSING", C['lg'], C['dg'],
         ["Signal Filt.", "Feature Ext.", "Data Norm.", "Outlier Rem."]),
        ("LAYER 1: PHYSICAL SENSING", C['vlb'], C['db'],
         ["Voltage", "Current", "Temperature", "Impedance"]),
    ]

    ly_h = 105
    mx = 40
    sy = 50

    for i, (title, bg, border, items) in enumerate(layers):
        y0 = sy + i * (ly_h + 12)
        lw = W - 2 * mx
        img.fill_rect(mx, y0, lw, ly_h, bg)
        img.rect_outline(mx, y0, lw, ly_h, border, 2)
        text(img, mx + 8, y0 + 5, title, border, 1)

        iw = (lw - 60) // 4
        for j, item in enumerate(items):
            ix = mx + 15 + j * (iw + 10)
            iy = y0 + 30
            img.fill_rect(ix, iy, iw, 60, C['wh'])
            img.rect_outline(ix, iy, iw, 60, border, 1)
            text_c(img, ix + iw//2, iy + 23, item, border, 1)

        # Arrow between layers
        if i > 0:
            for ax in range(mx + 100, W - mx - 50, 200):
                img.arrow(ax, y0 - 10, ax, y0 - 2, C['gy'], 1, 4)

    # Legend
    text(img, mx, H - 40, "Data flows upward from sensors to cloud", C['dgy'], 1)
    text(img, mx, H - 25, "Control flows downward from decisions to actuators", C['dgy'], 1)

    img.save(os.path.join(OUTPUT_DIR, "Figure_1_BMS_Architecture.png"))


# ============================================================
# Figure 2: SOC Estimation Accuracy Comparison (Bar Chart)
# ============================================================
def fig2():
    print("  Figure 2: SOC Estimation Comparison...")
    W, H = 900, 550
    img = FastPNG(W, H)

    text_c(img, W//2, 8, "SOC ESTIMATION ACCURACY COMPARISON", C['db'], 2)

    # Chart area
    cx, cy = 80, 50
    cw, ch = 780, 400
    cb = cy + ch  # chart bottom

    # Axes
    img.vline(cx, cy, ch, C['bk'], 2)
    img.hline(cx, cb, cw, C['bk'], 2)

    # Y axis: RMSE 0-6%
    text(img, 10, cy + ch//2 - 10, "RMSE(%)", C['bk'], 1)
    for i in range(7):
        yp = cb - int(i / 6.0 * ch)
        img.hline(cx - 3, yp, 6, C['bk'], 1)
        text(img, cx - 25, yp - 3, str(i), C['bk'], 1)
        if i > 0:
            for dotx in range(cx + 5, cx + cw, 6):
                img.pixel(dotx, yp, C['lgy'])

    methods = [
        ("CC", 5.2, C['lgy']), ("VB", 4.8, C['gy']),
        ("EKF", 3.5, C['lb']), ("UKF", 3.0, C['bl']),
        ("SVM", 2.8, C['lg']), ("RF", 2.4, C['gn']),
        ("CNN", 2.0, C['lo']), ("LSTM", 1.5, C['or']),
        ("Trans", 1.2, C['lp']), ("PINN", 1.0, C['pu']),
    ]

    bw = cw // (len(methods) + 1)
    for i, (name, val, color) in enumerate(methods):
        bx = cx + 20 + i * bw
        bh = int(val / 6.0 * ch)
        by = cb - bh
        img.fill_rect(bx, by, bw - 10, bh, color)
        img.rect_outline(bx, by, bw - 10, bh, C['dgy'], 1)
        # Value label
        vt = f"{val:.1f}"
        text_c(img, bx + (bw-10)//2, by - 12, vt, C['bk'], 1)
        # Name below
        text_c(img, bx + (bw-10)//2, cb + 5, name, C['bk'], 1)

    # Category brackets
    text(img, cx + 10, cb + 20, "Traditional", C['dgy'], 1)
    text(img, cx + 160, cb + 20, "Kalman", C['dgy'], 1)
    text(img, cx + 320, cb + 20, "ML", C['dgy'], 1)
    text(img, cx + 500, cb + 20, "Deep Learning", C['dgy'], 1)

    # Legend note
    text(img, cx, H - 20, "CC=Coulomb Count, VB=Voltage, EKF/UKF=Kalman, RF=Random Forest, Trans=Transformer, PINN=Physics-Informed NN", C['dgy'], 1)

    img.save(os.path.join(OUTPUT_DIR, "Figure_2_SOC_Estimation_Comparison.png"))


# ============================================================
# Figure 3: Smart Charging Network Architecture
# ============================================================
def fig3():
    print("  Figure 3: Charging Network Architecture...")
    W, H = 900, 680
    img = FastPNG(W, H)

    text_c(img, W//2, 8, "AI-ENABLED SMART CHARGING NETWORK ARCHITECTURE", C['db'], 2)

    # Three tiers
    tiers = [
        ("CLOUD LAYER", 45, C['vlb'], C['bl'],
         ["Model Training", "Fleet Analytics", "Market Trading", "Data Warehouse"]),
        ("EDGE LAYER", 250, C['lg'], C['dg'],
         ["Station Ctrl", "Load Forecast", "Queue Mgmt", "V2G Coord."]),
        ("DEVICE LAYER", 455, C['lo'], C['or'],
         ["Charger 1", "Charger 2", "Solar PV", "Battery ESS"]),
    ]

    tw_val = 820
    tx = 40

    for tname, ty, bg, border, comps in tiers:
        th = 175
        img.fill_rect(tx, ty, tw_val, th, bg)
        img.rect_outline(tx, ty, tw_val, th, border, 2)
        text(img, tx + 10, ty + 5, tname, border, 2)

        comp_w = 170
        comp_h = 80
        gap = (tw_val - 4 * comp_w) // 5
        for j, comp in enumerate(comps):
            ccx = tx + gap + j * (comp_w + gap)
            ccy = ty + 60
            img.fill_rect(ccx, ccy, comp_w, comp_h, C['wh'])
            img.rect_outline(ccx, ccy, comp_w, comp_h, border, 1)
            text_c(img, ccx + comp_w//2, ccy + 33, comp, border, 1)

    # Arrows between tiers
    for ax in [200, 400, 600, 750]:
        img.arrow(ax, 220, ax, 248, C['gy'], 1, 4)
        img.arrow(ax + 15, 248, ax + 15, 220, C['gy'], 1, 4)
        img.arrow(ax, 425, ax, 453, C['gy'], 1, 4)
        img.arrow(ax + 15, 453, ax + 15, 425, C['gy'], 1, 4)

    # Communication labels
    text_c(img, W//2, 232, "5G / FIBER LINK", C['dgy'], 1)
    text_c(img, W//2, 437, "LOCAL NETWORK", C['dgy'], 1)

    # External entities at bottom
    entities = [
        ("GRID", 80, C['lr'], C['rd']),
        ("USER APP", 350, C['lp'], C['pu']),
        ("RENEWABLES", 620, C['lg'], C['dg']),
    ]
    for name, ex, bg, border in entities:
        ey = 645
        ew = 180
        eh = 30
        img.fill_rect(ex, ey, ew, eh, bg)
        img.rect_outline(ex, ey, ew, eh, border, 1)
        text_c(img, ex + ew//2, ey + 9, name, border, 1)
        img.arrow(ex + ew//2, ey - 2, ex + ew//2, 632, border, 1, 4)

    img.save(os.path.join(OUTPUT_DIR, "Figure_3_Charging_Network_Architecture.png"))


# ============================================================
# Figure 4: V2G Energy Flow Optimization Framework
# ============================================================
def fig4():
    print("  Figure 4: V2G Framework...")
    W, H = 900, 620
    img = FastPNG(W, H)

    text_c(img, W//2, 8, "V2G ENERGY FLOW OPTIMIZATION FRAMEWORK", C['db'], 2)

    # Central optimizer
    ocx, ocy = W//2, H//2
    ow, oh = 200, 80
    img.fill_rect(ocx - ow//2, ocy - oh//2, ow, oh, C['vlb'])
    img.rect_outline(ocx - ow//2, ocy - oh//2, ow, oh, C['db'], 2)
    text_c(img, ocx, ocy - 10, "AI OPTIMIZATION", C['db'], 1)
    text_c(img, ocx, ocy + 5, "ENGINE", C['db'], 1)
    text_c(img, ocx, ocy + 20, "(Deep RL)", C['bl'], 1)

    # Surrounding nodes
    nodes = [
        ("EV FLEET", 100, 100, C['lg'], C['dg']),
        ("GRID", 700, 100, C['lr'], C['rd']),
        ("SOLAR/WIND", 100, 480, C['lo'], C['or']),
        ("BUILDINGS", 700, 480, C['lp'], C['pu']),
        ("MARKET", 100, 290, C['lgy'], C['dgy']),
        ("USER PREFS", 700, 290, C['lgy'], C['dgy']),
    ]

    nw, nh = 150, 50
    for name, nx, ny, bg, border in nodes:
        img.fill_rect(nx, ny, nw, nh, bg)
        img.rect_outline(nx, ny, nw, nh, border, 1)
        text_c(img, nx + nw//2, ny + 18, name, border, 1)

    # Arrows to/from optimizer
    # EV Fleet -> Optimizer
    img.arrow(250, 125, ocx - ow//2 - 5, ocy - 20, C['dg'], 2, 5)
    # Optimizer -> EV Fleet
    img.arrow(ocx - ow//2 - 5, ocy - 5, 250, 135, C['gn'], 1, 4)
    # Grid -> Optimizer
    img.arrow(700, 125, ocx + ow//2 + 5, ocy - 20, C['rd'], 2, 5)
    # Optimizer -> Grid
    img.arrow(ocx + ow//2 + 5, ocy - 5, 700, 135, C['lr'], 1, 4)
    # Solar -> Optimizer
    img.arrow(250, 495, ocx - ow//2 - 5, ocy + 20, C['or'], 2, 5)
    # Buildings <- Optimizer
    img.arrow(ocx + ow//2 + 5, ocy + 20, 700, 495, C['pu'], 2, 5)
    # Market -> Optimizer
    img.arrow(250, 310, ocx - ow//2 - 5, ocy, C['dgy'], 1, 4)
    # User -> Optimizer
    img.arrow(700, 310, ocx + ow//2 + 5, ocy, C['dgy'], 1, 4)

    # Flow labels
    text(img, 260, 85, "CHARGE/DISCHARGE", C['dg'], 1)
    text(img, 560, 85, "GRID SERVICES", C['rd'], 1)
    text(img, 260, 460, "GENERATION", C['or'], 1)
    text(img, 580, 460, "DEMAND RESP.", C['pu'], 1)

    # Objectives bar at bottom
    img.fill_rect(100, 570, 700, 35, C['vlb'])
    img.rect_outline(100, 570, 700, 35, C['bl'], 1)
    text_c(img, W//2, 580, "OBJECTIVES: Cost Min | Battery Health | Grid Stability | Renewable Max", C['db'], 1)

    img.save(os.path.join(OUTPUT_DIR, "Figure_4_V2G_Framework.png"))


# ============================================================
# Figure 5: Digital Twin Framework for EV Battery Systems
# ============================================================
def fig5():
    print("  Figure 5: Digital Twin Framework...")
    W, H = 900, 650
    img = FastPNG(W, H)

    text_c(img, W//2, 8, "DIGITAL TWIN FRAMEWORK FOR EV BATTERY SYSTEMS", C['db'], 2)

    # Two domains side by side
    dw = 380
    dh = 440
    dy = 45

    # Physical Domain (left)
    px = 30
    img.fill_rect(px, dy, dw, dh, (240, 248, 255))
    img.rect_outline(px, dy, dw, dh, C['bl'], 2)
    text_c(img, px + dw//2, dy + 8, "PHYSICAL DOMAIN", C['db'], 2)

    p_items = [("BATTERY PACK", C['lg'], C['dg']),
               ("SENSORS", C['lo'], C['or']),
               ("BMS HARDWARE", C['vlb'], C['bl']),
               ("VEHICLE ECU", C['lp'], C['pu'])]
    for i, (name, bg, border) in enumerate(p_items):
        bx = px + 20
        by = dy + 50 + i * 95
        bw = dw - 40
        bh = 75
        img.fill_rect(bx, by, bw, bh, bg)
        img.rect_outline(bx, by, bw, bh, border, 1)
        text_c(img, bx + bw//2, by + 30, name, border, 2)

    # Virtual Domain (right)
    vx = 490
    img.fill_rect(vx, dy, dw, dh, (255, 248, 240))
    img.rect_outline(vx, dy, dw, dh, C['or'], 2)
    text_c(img, vx + dw//2, dy + 8, "VIRTUAL DOMAIN", C['or'], 2)

    v_items = [("ELECTROCHEM MODEL", C['lo'], C['or']),
               ("AI SURROGATE", C['lr'], C['rd']),
               ("DEGRADATION SIM", C['lp'], C['pu']),
               ("OPTIM. ENGINE", C['vlb'], C['bl'])]
    for i, (name, bg, border) in enumerate(v_items):
        bx = vx + 20
        by = dy + 50 + i * 95
        bw = dw - 40
        bh = 75
        img.fill_rect(bx, by, bw, bh, bg)
        img.rect_outline(bx, by, bw, bh, border, 1)
        text_c(img, bx + bw//2, by + 30, name, border, 2)

    # Bidirectional arrows between domains
    labels = ["Sensor Data", "State Updates", "Control Signals", "Predictions"]
    for i, lbl in enumerate(labels):
        ay = dy + 80 + i * 95
        # Right arrow
        img.arrow(px + dw + 5, ay, vx - 5, ay, C['bl'], 2, 5)
        # Left arrow
        img.arrow(vx - 5, ay + 20, px + dw + 5, ay + 20, C['or'], 2, 5)
        text_c(img, W//2, ay - 10, lbl, C['dgy'], 1)

    # Bottom: feedback loop
    ly = 510
    img.fill_rect(80, ly, 740, 60, C['lgy'])
    img.rect_outline(80, ly, 740, 60, C['dgy'], 2)
    text_c(img, W//2, ly + 10, "CONTINUOUS LEARNING AND MODEL UPDATE LOOP", C['dgy'], 2)
    text_c(img, W//2, ly + 35, "Bayesian Opt. | Transfer Learning | Online Adaptation | Recalibration", C['dgy'], 1)

    # Arrows from loop to both domains
    img.arrow(200, ly, 200, dy + dh + 3, C['dgy'], 1, 4)
    img.arrow(700, ly, 700, dy + dh + 3, C['dgy'], 1, 4)

    img.save(os.path.join(OUTPUT_DIR, "Figure_5_Digital_Twin_Framework.png"))


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("Generating Chapter Figures...")
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    print("Done! All figures saved to:", OUTPUT_DIR)
