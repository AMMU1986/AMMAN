#!/usr/bin/env python3
"""
Generate 4 high-resolution conceptual figure images (PNG) for the chapter
"Biofouling, Maintenance, and Device Longevity" of the book
"Water Purification by 3D-Printing Devices".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies (matplotlib / PIL are unavailable
in the sandbox). Canvases are rendered at a large pixel size so that, when
embedded at a 6-inch print width, the effective resolution is high (>200 dpi).

Figures:
  Figure 1 - Stages of biofilm formation on a 3D-printed surface
  Figure 2 - Surface / material / geometric / operational determinants of
             microbial colonization
  Figure 3 - Closed-loop AI + sensor predictive-maintenance framework
  Figure 4 - Circular lifecycle and end-of-life framework
"""

import os
import math

from generate_figures import (
    PNGCanvas,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE,
    RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE,
    GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY,
    BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/biofouling_figures'

# Global scale factor for high-resolution output. All coordinates below are
# written in a 1x "design" space and multiplied by S at draw time.
S = 2


def _sc(*vals):
    return tuple(int(round(v * S)) for v in vals)


class HiCanvas(PNGCanvas):
    """PNGCanvas wrapper that scales a 1x design space up by factor S."""

    def __init__(self, w, h, bg=WHITE):
        super().__init__(int(w * S), int(h * S), bg)

    def R(self, x1, y1, x2, y2, outline, fill=None):
        self.rect(*_sc(x1, y1, x2, y2), outline, fill)

    def FR(self, x1, y1, x2, y2, color):
        self.fill_rect(*_sc(x1, y1, x2, y2), color)

    def L(self, x1, y1, x2, y2, color, thick=1):
        self.line(*_sc(x1, y1, x2, y2), color, max(1, thick * S))

    def A(self, x1, y1, x2, y2, color, thick=2, hs=8):
        self.arrow(*_sc(x1, y1, x2, y2), color, max(1, thick * S), int(hs * S))

    def C(self, cx, cy, r, color, fill=None):
        self.circle(*_sc(cx, cy), int(r * S), color, fill)

    def T(self, x, y, s, color, scale=1):
        self.text(*_sc(x, y), s, color, scale * S)

    def TC(self, cx, y, s, color, scale=1):
        self.text_c(int(cx * S), int(y * S), s, color, scale * S)

    def VL(self, x, y1, y2, color):
        self.vline(int(x * S), int(y1 * S), int(y2 * S), color)

    def HL(self, x1, x2, y, color):
        self.hline(int(x1 * S), int(x2 * S), int(y * S), color)


def _wrap(text, width):
    """Greedy word-wrap into lines of at most `width` characters."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def _print_bed(c, x0, x1, y_top, layers=6, lh=6, col=LIGHT_GRAY, line=GRAY):
    """Draw a side view of a layered 3D-printed substrate with ridged top."""
    y_bot = y_top + layers * lh
    c.FR(x0, y_top, x1, y_bot, col)
    for i in range(layers + 1):
        c.HL(x0, x1, y_top + i * lh, line)
    # ridged (wavy) top surface to suggest layer-line roughness
    x = x0
    up = True
    while x < x1:
        if up:
            c.L(x, y_top, x + 5, y_top - 4, line, 1)
        else:
            c.L(x, y_top - 4, x + 5, y_top, line, 1)
        up = not up
        x += 5
    return y_top - 4


def gen_fig1():
    """Figure 1: Stages of biofilm formation on a 3D-printed surface."""
    c = HiCanvas(900, 480)
    c.TC(450, 12, "Stages of Biofilm Formation on a 3D-Printed Surface", BLACK, 2)

    stages = [
        ("1. Conditioning", "film adsorbs", MED_BLUE, PALE_BLUE),
        ("2. Reversible", "adhesion", LIGHT_BLUE, PALE_BLUE),
        ("3. Irreversible", "adhesion (EPS)", MED_GREEN, LIGHT_GREEN),
        ("4. Proliferation", "microcolonies", ORANGE, LIGHT_ORANGE),
        ("5. Mature", "biofilm", PURPLE, LIGHT_PURPLE),
        ("6. Dispersion", "/ sloughing", RED, LIGHT_RED),
    ]
    n = len(stages)
    panel_w = 135
    gap = 7
    x0 = 20
    top = 70
    bed_y = 300
    for i, (l1, l2, col, fill) in enumerate(stages):
        px = x0 + i * (panel_w + gap)
        # panel frame + header
        c.R(px, top, px + panel_w, 360, col, WHITE)
        c.FR(px, top, px + panel_w, top + 26, fill)
        c.TC(px + panel_w / 2, top + 4, l1, BLACK, 1)
        c.TC(px + panel_w / 2, top + 15, l2, GRAY, 1)
        # printed substrate (side view)
        surf = _print_bed(c, px + 8, px + panel_w - 8, bed_y)
        # conditioning film grows across the stages
        if i >= 0:
            c.HL(px + 8, px + panel_w - 8, surf - 2, GOLD)
        # cells / community per stage
        cx0 = px + 20
        if i == 0:
            c.T(px + 14, surf - 16, "organics", GRAY, 1)
        elif i == 1:
            for k in range(2):
                c.C(cx0 + k * 40, surf - 10, 5, MED_BLUE, LIGHT_BLUE)
            c.A(px + panel_w / 2, surf - 34, px + panel_w / 2, surf - 18, GRAY, 2, 6)
        elif i == 2:
            for k in range(3):
                c.C(cx0 + k * 32, surf - 9, 6, DARK_GREEN, LIGHT_GREEN)
            c.HL(px + 10, px + panel_w - 10, surf - 1, DARK_GREEN)
        elif i == 3:
            for k in range(4):
                c.C(cx0 - 4 + k * 28, surf - 12, 7, ORANGE, LIGHT_ORANGE)
                c.C(cx0 + 6 + k * 28, surf - 24, 6, ORANGE, LIGHT_ORANGE)
        elif i == 4:
            # thick matrix dome with embedded cells + water channels
            for yy in range(0, 38, 4):
                c.HL(px + 12, px + panel_w - 12, surf - yy, LIGHT_PURPLE)
            for k in range(5):
                c.C(cx0 - 6 + k * 24, surf - 12, 5, PURPLE, LIGHT_PURPLE)
                c.C(cx0 + 2 + k * 24, surf - 28, 5, PURPLE, LIGHT_PURPLE)
        elif i == 5:
            for yy in range(0, 24, 4):
                c.HL(px + 12, px + panel_w - 12, surf - yy, LIGHT_RED)
            for k in range(3):
                c.C(cx0 + k * 32, surf - 10, 5, RED, LIGHT_RED)
            # detaching cells
            c.C(px + panel_w / 2, surf - 48, 5, RED, LIGHT_RED)
            c.A(px + panel_w / 2 - 6, surf - 40, px + panel_w - 14, surf - 58, GRAY, 2, 6)
        c.T(px + 10, 345, "printed", GRAY, 1)
        # progression arrow between panels
        if i < n - 1:
            c.A(px + panel_w - 2, top + 150, px + panel_w + gap + 2, top + 150, GRAY, 2, 7)

    # time axis
    c.A(20, 395, 880, 395, DARK_BLUE, 2, 10)
    c.T(20, 402, "seconds", GRAY, 1)
    c.TC(450, 402, "time / residence", GRAY, 1)
    c.T(820, 402, "days-weeks", GRAY, 1)

    # interpretive note
    c.R(20, 425, 880, 462, GRAY, (250, 250, 250))
    c.TC(450, 433, "Interlayer grooves and low-shear valleys accelerate the transition from reversible to", BLACK, 1)
    c.TC(450, 447, "irreversible attachment; the mature EPS matrix resists both shear and chemical cleaning", GRAY, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Biofilm_Formation_Stages.png'))
    print("  Figure_1_Biofilm_Formation_Stages.png done")


def gen_fig2():
    """Figure 2: Determinants of microbial colonization."""
    c = HiCanvas(900, 620)
    c.TC(450, 12, "Determinants of Microbial Colonization on 3D-Printed Surfaces", BLACK, 2)

    # central node
    cx, cy = 450, 290
    c.C(cx, cy, 62, DARK_BLUE, PALE_BLUE)
    c.TC(cx, cy - 16, "Microbial", BLACK, 1)
    c.TC(cx, cy - 2, "Colonization", BLACK, 1)
    c.TC(cx, cy + 14, "& Biofouling", GRAY, 1)

    # six determinant nodes arranged radially
    dets = [
        ("Surface roughness", "grooves shelter cells", MED_BLUE, LIGHT_BLUE, "Design"),
        ("Pore geometry", "dead zones, tortuosity", MED_GREEN, LIGHT_GREEN, "Design"),
        ("Print resolution", "staircase microtexture", DARK_GREEN, LIGHT_GREEN, "Design"),
        ("Material chemistry", "surface energy & charge", PURPLE, LIGHT_PURPLE, "Material"),
        ("Wettability", "hydration barrier", GOLD, LIGHT_GOLD, "Material"),
        ("Operating conditions", "flux, shear, nutrients", ORANGE, LIGHT_ORANGE, "Operational"),
    ]
    n = len(dets)
    Rr = 195
    for i, (label, sub, col, fill, group) in enumerate(dets):
        ang = -math.pi / 2 + i * (2 * math.pi / n)
        bx = cx + Rr * math.cos(ang)
        by = cy + Rr * math.sin(ang)
        c.R(bx - 94, by - 30, bx + 94, by + 30, col, fill)
        c.TC(bx, by - 20, label, BLACK, 1)
        c.TC(bx, by - 6, sub, GRAY, 1)
        c.TC(bx, by + 12, "[" + group + "]", col, 1)
        # bidirectional connector to center
        dx, dy = cx - bx, cy - by
        d = math.sqrt(dx * dx + dy * dy)
        sx = bx + dx / d * 96
        sy = by + dy / d * 32
        ex = cx - dx / d * 66
        ey = cy - dy / d * 66
        c.A(sx, sy, ex, ey, GRAY, 2, 8)

    # legend of the three control levers
    c.R(20, 560, 880, 605, GRAY, (250, 250, 250))
    c.FR(40, 574, 60, 590, LIGHT_BLUE); c.T(66, 577, "Design / fabrication levers", BLACK, 1)
    c.FR(330, 574, 350, 590, LIGHT_PURPLE); c.T(356, 577, "Material / surface-chemistry levers", BLACK, 1)
    c.FR(650, 574, 670, 590, LIGHT_ORANGE); c.T(676, 577, "Operational levers", BLACK, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Colonization_Determinants.png'))
    print("  Figure_2_Colonization_Determinants.png done")


def gen_fig3():
    """Figure 3: Closed-loop AI + sensor predictive-maintenance framework."""
    c = HiCanvas(920, 560)
    c.TC(460, 12, "Closed-Loop Predictive-Maintenance Framework", BLACK, 2)

    # Device box (left)
    c.R(40, 70, 230, 230, DARK_BLUE, PALE_BLUE)
    c.TC(135, 80, "3D-Printed", BLACK, 1)
    c.TC(135, 94, "Purification Device", BLACK, 1)
    c.TC(135, 112, "(embedded sensors)", GRAY, 1)
    # mini layered membrane with sensor dots
    _print_bed(c, 60, 210, 150, layers=5, lh=7)
    for sx, scol in [(80, RED), (120, MED_GREEN), (160, ORANGE), (195, PURPLE)]:
        c.C(sx, 145, 4, scol, scol)

    # Sensors list box
    c.R(40, 255, 230, 420, MED_BLUE, LIGHT_BLUE)
    c.TC(135, 262, "Sensing layer", BLACK, 1)
    sensors = ["- Transmembrane pressure", "- Permeate flux", "- Conductivity", "- Optical / OCT", "- Impedance (EIS)", "- Fluorescence / EPS"]
    for k, s in enumerate(sensors):
        c.T(52, 282 + k * 21, s, BLACK, 1)
    c.A(135, 230, 135, 255, GRAY, 2, 7)

    # Data acquisition
    c.R(300, 110, 470, 190, MED_GREEN, LIGHT_GREEN)
    c.TC(385, 128, "Data Acquisition", BLACK, 1)
    c.TC(385, 146, "& Pre-processing", BLACK, 1)
    c.TC(385, 164, "(streaming, cleaning)", GRAY, 1)

    # ML models
    c.R(300, 230, 470, 330, PURPLE, LIGHT_PURPLE)
    c.TC(385, 240, "Machine-Learning", BLACK, 1)
    c.TC(385, 254, "Models", BLACK, 1)
    c.T(312, 272, "- Fouling classification", BLACK, 1)
    c.T(312, 290, "- Flux / TMP forecasting", BLACK, 1)
    c.T(312, 308, "- Remaining useful life", BLACK, 1)

    # Digital twin
    c.R(300, 365, 470, 430, GOLD, LIGHT_GOLD)
    c.TC(385, 378, "Digital Twin", BLACK, 1)
    c.TC(385, 396, "(virtual state model)", GRAY, 1)

    # Decision / optimization
    c.R(540, 180, 720, 300, ORANGE, LIGHT_ORANGE)
    c.TC(630, 196, "Decision &", BLACK, 1)
    c.TC(630, 210, "Optimization", BLACK, 1)
    c.T(552, 230, "- When to clean", BLACK, 1)
    c.T(552, 248, "- Which method", BLACK, 1)
    c.T(552, 266, "- Operating set-points", BLACK, 1)

    # Actions
    c.R(770, 110, 900, 185, MED_GREEN, LIGHT_GREEN)
    c.TC(835, 126, "Backwash /", BLACK, 1)
    c.TC(835, 142, "CIP cleaning", BLACK, 1)
    c.R(770, 210, 900, 285, MED_BLUE, LIGHT_BLUE)
    c.TC(835, 226, "Adjust flux /", BLACK, 1)
    c.TC(835, 242, "shear", BLACK, 1)
    c.R(770, 310, 900, 385, RED, LIGHT_RED)
    c.TC(835, 326, "Replace", BLACK, 1)
    c.TC(835, 342, "module", BLACK, 1)

    # arrows of the loop
    c.A(230, 150, 300, 150, GRAY, 2, 8)
    c.A(385, 190, 385, 230, GRAY, 2, 8)
    c.A(385, 330, 385, 365, GRAY, 2, 8)
    c.A(470, 270, 540, 240, GRAY, 2, 8)      # ML -> decision
    c.A(470, 395, 540, 290, GRAY, 2, 8)      # twin -> decision
    c.A(720, 150, 770, 147, ORANGE, 2, 8)
    c.A(720, 240, 770, 245, ORANGE, 2, 8)
    c.A(720, 345, 770, 347, ORANGE, 2, 8)

    # feedback loop back to the device (actions change device state)
    c.L(835, 385, 835, 470, RED, 2)
    c.L(835, 470, 135, 470, RED, 2)
    c.A(135, 470, 135, 420, RED, 2, 9)
    c.TC(470, 476, "closed-loop feedback: actions update device state and sensor stream", RED, 1)

    # note
    c.R(40, 505, 900, 545, GRAY, (250, 250, 250))
    c.TC(470, 513, "Early-warning signals (optical, impedance, fluorescence) enable intervention while biofilm is", BLACK, 1)
    c.TC(470, 527, "immature, maximizing useful life while conserving chemicals, energy, and material", GRAY, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Predictive_Maintenance.png'))
    print("  Figure_3_Predictive_Maintenance.png done")


def gen_fig4():
    """Figure 4: Circular lifecycle and end-of-life framework."""
    c = HiCanvas(860, 560)
    c.TC(430, 12, "Circular Lifecycle of a 3D-Printed Water Purification Device", BLACK, 2)

    cx, cy = 430, 300
    R = 175
    stages = [
        ("Material Sourcing", "bio-based / recycled feedstock", MED_GREEN, LIGHT_GREEN),
        ("Fabrication", "optimized design, low waste", MED_BLUE, LIGHT_BLUE),
        ("Use & Maintenance", "antifouling, mild cleaning", ORANGE, LIGHT_ORANGE),
        ("Replacement", "modular, targeted swap", PURPLE, LIGHT_PURPLE),
        ("End of Life", "recycle / recover / biodegrade", GOLD, LIGHT_GOLD),
    ]
    n = len(stages)
    pts = []
    for i, (label, sub, col, fill) in enumerate(stages):
        ang = -math.pi / 2 + i * (2 * math.pi / n)
        bx = cx + R * math.cos(ang)
        by = cy + R * math.sin(ang)
        pts.append((bx, by, col))
        c.C(bx, by, 66, col, fill)
        c.TC(bx, by - 14, label.split()[0], BLACK, 1)
        if len(label.split()) > 1:
            c.TC(bx, by, " ".join(label.split()[1:]), BLACK, 1)
        sub_lines = _wrap(sub, 16)
        for li, sl in enumerate(sub_lines[:2]):
            c.TC(bx, by + 16 + li * 12, sl, GRAY, 1)

    # curved loop arrows connecting the stages clockwise
    for i in range(n):
        x1, y1, _ = pts[i]
        x2, y2, _ = pts[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        d = math.sqrt(dx * dx + dy * dy)
        sx = x1 + dx / d * 70
        sy = y1 + dy / d * 70
        ex = x2 - dx / d * 70
        ey = y2 - dy / d * 70
        c.A(sx, sy, ex, ey, GRAY, 2, 9)

    # central hub
    c.C(cx, cy, 58, DARK_BLUE, PALE_BLUE)
    c.TC(cx, cy - 16, "Durability +", BLACK, 1)
    c.TC(cx, cy - 2, "Modularity +", BLACK, 1)
    c.TC(cx, cy + 12, "Recyclability", BLACK, 1)

    # recovery feedback arrow (end-of-life back to sourcing) highlighted
    x_eol = pts[4][0]; y_eol = pts[4][1]
    x_src = pts[0][0]; y_src = pts[0][1]
    c.TC(cx, cy + 34, "closed loop", GRAY, 1)

    # note
    c.R(30, 500, 830, 545, GRAY, (250, 250, 250))
    c.TC(430, 508, "Fouling-resistant, long-lived, modular designs reduce replacement frequency and waste;", BLACK, 1)
    c.TC(430, 522, "recyclable or biodegradable materials return value to the loop, aligning cost and sustainability", GRAY, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Lifecycle_Framework.png'))
    print("  Figure_4_Lifecycle_Framework.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating biofouling chapter figures (high resolution)...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print(f"\nAll figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz / 1024:.1f} KB")


if __name__ == '__main__':
    main()
