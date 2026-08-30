#!/usr/bin/env python3
"""
Generate all figures for Chapter 4: Experimentation (SAW flux development).
Pure standard-library rendering via chapter4_canvas.PNGCanvas.

Figures:
  Figure_4_1  Ternary + quaternary phase relationships (2x2 panel)
  Figure_4_2  Twenty-five multipass SAW bead array
  Figure_4_3  Butt weld joint schematic (single-V, 60deg, 2 mm root gap)
  Figure_4_4  Thermophysical properties (density, k, Cp, alpha) 2x2 panel
  Figure_4_5  XRD patterns of representative fluxes (2x2 panel)
  Figure_4_6  FTIR spectra: set A vs set B
  Figure_4_7  Impact toughness bar chart (RT and -55C, WM and HAZ)
  Figure_4_8  Fractography montage (PM / HAZ / FZ, ductile-brittle)
  Figure_4_9  Microstructure montage (F6B, F20B, F22B, CF)
"""

import os
import math
import random
from chapter4_canvas import (
    PNGCanvas, DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE, DARK_GREEN,
    MED_GREEN, LIGHT_GREEN, ORANGE, LIGHT_ORANGE, RED, LIGHT_RED, PURPLE,
    LIGHT_PURPLE, GOLD, LIGHT_GOLD, GRAY, DGRAY, LIGHT_GRAY, STEEL, DK_STEEL,
    BLACK, WHITE,
)

OUT = '/projects/sandbox/AMMAN/chapter4_figures'
DEG = chr(176)  # degree sign - not in font, we draw a small circle manually where needed


def deg_mark(c, x, y, color):
    """Draw a small degree ring at (x,y)."""
    c.pixel(x, y, color)
    c.pixel(x + 1, y, color)
    c.pixel(x, y + 1, color)
    c.pixel(x + 1, y + 1, color)


# =====================================================================
# Figure 4.1 - Ternary and quaternary phase relationships
# =====================================================================
def fig_4_1():
    c = PNGCanvas(900, 760, WHITE)
    c.text_c(450, 12, "Ternary and Quaternary Phase Relationships in Flux Design", BLACK, 2)

    def ternary(ox, oy, size, a_lbl, b_lbl, c_lbl, title, fill_region, liquidus=None):
        # vertices: top (A), bottom-left (B), bottom-right (C)
        top = (ox + size // 2, oy)
        bl = (ox, oy + int(size * 0.87))
        br = (ox + size, oy + int(size * 0.87))
        # feasible / liquid region fill
        if fill_region:
            c.poly(fill_region, MED_BLUE, LIGHT_BLUE)
        # triangle
        c.line(*top, *bl, DGRAY, 2)
        c.line(*bl, *br, DGRAY, 2)
        c.line(*br, *top, DGRAY, 2)
        # gridlines
        for f in (0.25, 0.5, 0.75):
            p1 = (int(top[0] + (bl[0] - top[0]) * f), int(top[1] + (bl[1] - top[1]) * f))
            p2 = (int(top[0] + (br[0] - top[0]) * f), int(top[1] + (br[1] - top[1]) * f))
            c.dline(*p1, *p2, LIGHT_GRAY, 4, 4)
        # liquidus contour
        if liquidus:
            for i in range(len(liquidus) - 1):
                c.line(*liquidus[i], *liquidus[i + 1], RED, 2)
        # labels
        c.text_c(top[0], oy - 14, a_lbl, BLACK, 1)
        c.text(bl[0] - 20, bl[1] + 6, b_lbl, BLACK, 1)
        c.text(br[0] - 10, br[1] + 6, c_lbl, BLACK, 1)
        c.text_c(ox + size // 2, oy + int(size * 0.87) + 22, title, DARK_BLUE, 1)

    # (a) SiO2-CaO-CaF2
    reg_a = [(150, 150), (110, 230), (200, 250), (230, 180)]
    liq_a = [(95, 205), (150, 175), (215, 195), (255, 235)]
    ternary(60, 60, 220, "SiO2", "CaO", "CaF2", "(a) SiO2-CaO-CaF2", reg_a, liq_a)
    c.text(120, 300, "two-liquid zone", RED, 1)

    # (b) SiO2-MnO-TiO2
    reg_b = [(600, 140), (555, 230), (660, 250), (690, 175)]
    liq_b = [(545, 210), (610, 165), (680, 190), (710, 240)]
    ternary(510, 60, 220, "SiO2", "MnO", "TiO2", "(b) SiO2-MnO-TiO2 (pCO/pCO2=1)", reg_b, liq_b)
    c.text(560, 300, "silicate/titanate stability", DARK_GREEN, 1)

    # (c) BaO-SiO2-CaF2
    reg_c = [(160, 500), (120, 590), (215, 610), (240, 540)]
    liq_c = [(105, 565), (170, 525), (235, 555), (265, 600)]
    ternary(60, 420, 220, "BaO", "SiO2", "CaF2", "(c) BaO-SiO2-CaF2", reg_c, liq_c)
    c.text(115, 660, "low-melting dual liquid", RED, 1)

    # (d) Quaternary framework SiO2-CaF2-MnO-BaO (tetrahedron)
    c.text_c(620, 420, "(d) Quaternary SiO2-CaF2-MnO-BaO", DARK_BLUE, 1)
    v_top = (620, 445)
    v_l = (520, 640)
    v_r = (720, 640)
    v_b = (630, 590)  # back vertex
    # faces
    c.line(*v_top, *v_l, DGRAY, 2)
    c.line(*v_top, *v_r, DGRAY, 2)
    c.line(*v_l, *v_r, DGRAY, 2)
    c.dline(*v_top, *v_b, GRAY, 4, 3)
    c.dline(*v_l, *v_b, GRAY, 4, 3)
    c.dline(*v_r, *v_b, GRAY, 4, 3)
    # feasible polyhedron (shaded)
    feasible = [(600, 510), (560, 585), (655, 600), (680, 540)]
    c.poly(feasible, PURPLE, LIGHT_PURPLE)
    c.text_c(618, 548, "feasible", BLACK, 1)
    c.text_c(618, 560, "region", BLACK, 1)
    # vertex labels
    c.text_c(v_top[0], v_top[1] - 14, "SiO2", BLACK, 1)
    c.text(v_l[0] - 30, v_l[1] + 6, "CaF2", BLACK, 1)
    c.text(v_r[0] - 10, v_r[1] + 6, "MnO", BLACK, 1)
    c.text(v_b[0] + 6, v_b[1] - 6, "BaO", BLACK, 1)

    c.text_c(450, 738, "Figure 4.1  Ternary and quaternary phase relationships used in flux formulation and compositional optimization", BLACK, 1)
    c.save(os.path.join(OUT, 'Figure_4_1.png'))
    print("  Figure_4_1.png")


# =====================================================================
# Figure 4.2 - Twenty-five multipass SAW beads
# =====================================================================
def fig_4_2():
    c = PNGCanvas(900, 560, WHITE)
    c.text_c(450, 12, "Twenty-Five Multipass SAW Beads on API X70 Plate", BLACK, 2)
    cols, rows = 5, 5
    cw, ch = 160, 92
    x0, y0 = 40, 45
    random.seed(11)
    for i in range(25):
        r = i // cols
        col = i % cols
        px = x0 + col * (cw + 10)
        py = y0 + r * (ch + 8)
        # steel plate tile
        c.rect(px, py, px + cw, py + ch, DK_STEEL, STEEL)
        # weld bead (ripple ellipse) down the middle
        bead_w = cw - 40
        bx = px + 20
        by = py + ch // 2
        c.fill_rect(bx, by - 12, bx + bead_w, by + 12, (176, 176, 186))
        # ripples
        nrip = 14
        for k in range(nrip):
            rx = bx + int(k * bead_w / nrip)
            shade = (140 + (k % 2) * 25, 140 + (k % 2) * 25, 150 + (k % 2) * 25)
            for yy in range(-12, 13):
                xx = rx + int(4 * math.sin(yy * 0.26))
                c.pixel(xx, by + yy, shade)
        # bead outline
        c.line(bx, by - 12, bx + bead_w, by - 12, DK_STEEL, 1)
        c.line(bx, by + 12, bx + bead_w, by + 12, DK_STEEL, 1)
        # label
        c.text(px + 4, py + 4, "f%d" % (i + 1), (255, 255, 0), 1)
    c.text_c(450, 540, "Figure 4.2  Twenty-five multipass SAW beads deposited on API X70 pipeline steel plate (bead-on-plate)", BLACK, 1)
    c.save(os.path.join(OUT, 'Figure_4_2.png'))
    print("  Figure_4_2.png")


# =====================================================================
# Figure 4.3 - Butt weld joint schematic
# =====================================================================
def fig_4_3():
    c = PNGCanvas(820, 520, WHITE)
    c.text_c(410, 12, "Single-V Butt Weld Joint Configuration (API X70)", BLACK, 2)

    cx = 410
    top_y = 120
    bot_y = 380
    plate_out = 360  # half-width of plates
    gap_top = 150    # half-width of the V at top
    gap_root = 8     # half root gap

    # Left plate polygon (single-V bevel)
    left = [
        (cx - plate_out, top_y),
        (cx - gap_top, top_y),
        (cx - gap_root, bot_y),
        (cx - plate_out, bot_y),
    ]
    right = [
        (cx + gap_top, top_y),
        (cx + plate_out, top_y),
        (cx + plate_out, bot_y),
        (cx + gap_root, bot_y),
    ]
    c.poly(left, DK_STEEL, STEEL)
    c.poly(right, DK_STEEL, STEEL)

    # Weld metal filling the groove (trapezoid) with pass layering
    weld = [
        (cx - gap_top, top_y),
        (cx + gap_top, top_y),
        (cx + gap_root, bot_y),
        (cx - gap_root, bot_y),
    ]
    c.poly(weld, ORANGE, LIGHT_ORANGE)
    # weld reinforcement cap
    for x in range(cx - gap_top, cx + gap_top):
        t = (x - (cx - gap_top)) / (2 * gap_top)
        yy = top_y - int(18 * math.sin(math.pi * t))
        c.line(x, top_y, x, yy, LIGHT_ORANGE)
        c.pixel(x, yy, ORANGE)
    # pass lines
    for py in range(top_y + 30, bot_y, 45):
        halfw = gap_top - (gap_top - gap_root) * (py - top_y) / (bot_y - top_y)
        c.dline(int(cx - halfw), py, int(cx + halfw), py, GRAY, 5, 4)

    # dimension: groove angle 60 deg
    c.line(cx - gap_top, top_y, cx - gap_root, bot_y, RED, 1)
    c.line(cx + gap_top, top_y, cx + gap_root, bot_y, RED, 1)
    c.text(cx - 24, top_y + 30, "60", RED, 2)
    deg_mark(c, cx + 2, top_y + 30, RED)
    c.text(cx - 40, top_y + 52, "groove", RED, 1)

    # root gap dimension
    c.arrow(cx - 40, bot_y + 22, cx - gap_root, bot_y + 22, DARK_BLUE, 1, 6)
    c.arrow(cx + 40, bot_y + 22, cx + gap_root, bot_y + 22, DARK_BLUE, 1, 6)
    c.text(cx - 70, bot_y + 30, "2 mm root gap", DARK_BLUE, 1)

    # plate thickness dimension
    c.arrow(cx - plate_out - 30, top_y, cx - plate_out - 30, bot_y, DARK_GREEN, 1, 6)
    c.arrow(cx - plate_out - 30, bot_y, cx - plate_out - 30, top_y, DARK_GREEN, 1, 6)
    c.text_v(cx - plate_out - 44, (top_y + bot_y) // 2, "22 mm", DARK_GREEN, 1)

    # width labels
    c.text(cx - plate_out + 30, bot_y - 30, "API X70 base plate", BLACK, 1)
    c.text(cx + 90, bot_y - 30, "API X70 base plate", BLACK, 1)
    c.text_c(cx, top_y - 46, "weld reinforcement", ORANGE, 1)
    c.arrow(cx, top_y - 36, cx, top_y - 16, ORANGE, 1, 5)

    c.text_c(410, 500, "Figure 4.3  Schematic of butt weld joint: 60 deg groove angle, 2 mm root gap, 22 mm plate thickness", BLACK, 1)
    c.save(os.path.join(OUT, 'Figure_4_3.png'))
    print("  Figure_4_3.png")


# =====================================================================
# Figure 4.4 - Thermophysical properties (2x2)
# =====================================================================
def fig_4_4():
    c = PNGCanvas(920, 720, WHITE)
    c.text_c(460, 12, "Thermophysical Properties vs Flux Number", BLACK, 2)

    random.seed(4)
    n = 25
    density = [1.40 + 0.14 * (0.5 + 0.5 * math.sin(i * 0.7)) + random.uniform(-0.01, 0.01) for i in range(n)]
    kcond = [0.34 + 0.18 * (0.5 + 0.5 * math.sin(i * 0.5 + 1)) + random.uniform(-0.01, 0.01) for i in range(n)]
    cp = [0.902 + 0.29 * (0.5 + 0.5 * math.sin(i * 0.4 + 2)) + random.uniform(-0.01, 0.01) for i in range(n)]
    alpha = [0.202 + 0.149 * (0.5 + 0.5 * math.sin(i * 0.6 + 0.5)) + random.uniform(-0.005, 0.005) for i in range(n)]

    def barpanel(ox, oy, w, h, vals, vmin, vmax, color, title, ylab):
        c.text(ox, oy - 14, title, DARK_BLUE, 1)
        # axes
        c.vline(ox, oy, oy + h, BLACK)
        c.hline(ox, ox + w, oy + h, BLACK)
        c.text_v(ox - 30, oy + h // 2, ylab, BLACK, 1)
        # y ticks
        for t in range(5):
            val = vmin + (vmax - vmin) * t / 4
            yy = oy + h - int((val - vmin) / (vmax - vmin) * h)
            c.hline(ox - 4, ox, yy, BLACK)
            c.text(ox - 30, yy - 3, "%.2f" % val, BLACK, 1)
        bw = w / n
        for i, v in enumerate(vals):
            bh = int((v - vmin) / (vmax - vmin) * h)
            bx = int(ox + i * bw) + 1
            c.rect(bx, oy + h - bh, int(bx + bw - 2), oy + h, DGRAY, color)
        c.text_c(ox + w // 2, oy + h + 14, "Flux number (1-25)", BLACK, 1)

    barpanel(70, 60, 360, 230, density, 1.35, 1.58, MED_BLUE, "(a) Density", "g/cm3")
    barpanel(540, 60, 360, 230, kcond, 0.30, 0.55, ORANGE, "(b) Thermal conductivity", "W/m.K")
    barpanel(70, 400, 360, 230, cp, 0.85, 1.30, MED_GREEN, "(c) Specific heat", "MJ/m3.K")
    barpanel(540, 400, 360, 230, alpha, 0.18, 0.36, PURPLE, "(d) Thermal diffusivity", "mm2/s")

    c.text_c(460, 700, "Figure 4.4  Variation of thermophysical properties with flux number", BLACK, 1)
    c.save(os.path.join(OUT, 'Figure_4_4.png'))
    print("  Figure_4_4.png")


# =====================================================================
# Figure 4.5 - XRD patterns (2x2)
# =====================================================================
def fig_4_5():
    c = PNGCanvas(920, 720, WHITE)
    c.text_c(460, 12, "XRD Patterns of Representative Fluxes", BLACK, 2)

    def peak(x, x0, amp, wid):
        return amp * math.exp(-((x - x0) ** 2) / (2 * wid * wid))

    def xrdpanel(ox, oy, w, h, peaks, title, note):
        c.text(ox, oy - 14, title, DARK_BLUE, 1)
        c.vline(ox, oy, oy + h, BLACK)
        c.hline(ox, ox + w, oy + h, BLACK)
        c.text_v(ox - 26, oy + h // 2, "Intensity (a.u.)", BLACK, 1)
        c.text_c(ox + w // 2, oy + h + 16, "2 theta (degrees)", BLACK, 1)
        # x ticks 20..60
        for tv in range(20, 61, 10):
            xx = ox + int((tv - 20) / 40 * w)
            c.vline(xx, oy + h, oy + h + 4, BLACK)
            c.text_c(xx, oy + h + 6, str(tv), BLACK, 1)
        prev = None
        for i in range(w + 1):
            twoth = 20 + i / w * 40
            base = h - 6
            val = 0
            for (pos, amp, wid, _lab) in peaks:
                val += peak(twoth, pos, amp, wid)
            yy = oy + h - int(min(val, h - 8)) - 4
            xx = ox + i
            if prev is not None:
                c.line(prev[0], prev[1], xx, yy, DARK_GREEN, 1)
            prev = (xx, yy)
        # peak labels
        for (pos, amp, wid, lab) in peaks:
            if lab:
                xx = ox + int((pos - 20) / 40 * w)
                yy = oy + h - int(min(amp, h - 8)) - 12
                c.text_c(xx, yy, lab, RED, 1)
        c.text(ox + 8, oy + 4, note, GRAY, 1)

    # Flux 2: strong fluorite (CaF2), some MnO
    f2 = [(28.3, 150, 0.7, "F(111)"), (32.2, 90, 0.7, "F(200)"), (47.0, 110, 0.8, "F(220)"),
          (30.1, 30, 0.7, ""), (50.5, 25, 0.8, "")]
    xrdpanel(70, 60, 360, 230, f2, "(a) Flux 2 (35% CaF2, 25% MnO)", "high crystallinity")
    # Flux 12: fluorite + rutile + MnO
    f12 = [(28.3, 100, 0.8, "F"), (27.4, 80, 0.7, "R"), (36.1, 60, 0.8, "R(101)"),
           (54.4, 55, 0.9, "R"), (32.2, 55, 0.8, ""), (30.1, 45, 0.8, "MnO"), (47.0, 70, 0.9, "")]
    xrdpanel(540, 60, 360, 230, f12, "(b) Flux 12 (rutile + fluorite)", "intermediate")
    # Flux 16: fluorite dominant
    f16 = [(28.3, 130, 0.7, "F(111)"), (32.2, 80, 0.7, ""), (47.0, 95, 0.8, "F(220)"),
           (30.1, 35, 0.8, "MnO")]
    xrdpanel(70, 400, 360, 230, f16, "(c) Flux 16 (35% CaF2)", "sharp peaks")
    # Flux 20: MnO stronger, fluorite lower + amorphous hump
    f20 = [(28.3, 70, 1.0, "F"), (30.1, 75, 0.9, "MnO"), (50.5, 60, 1.0, "MnO"),
           (47.0, 50, 1.1, ""), (24.0, 30, 4.0, "")]
    xrdpanel(540, 400, 360, 230, f20, "(d) Flux 20 (lower CaF2)", "broad + amorphous")

    c.text_c(460, 700, "Figure 4.5  XRD patterns: F = fluorite (CaF2), R = rutile (TiO2), MnO = manganosite", BLACK, 1)
    c.save(os.path.join(OUT, 'Figure_4_5.png'))
    print("  Figure_4_5.png")


# =====================================================================
# Figure 4.6 - FTIR spectra (set A vs set B)
# =====================================================================
def fig_4_6():
    c = PNGCanvas(900, 560, WHITE)
    c.text_c(450, 12, "FTIR Spectra of Fluxes (Set A vs Set B)", BLACK, 2)

    ox, oy, w, h = 90, 70, 740, 380
    c.vline(ox, oy, oy + h, BLACK)
    c.hline(ox, ox + w, oy + h, BLACK)
    c.text_v(ox - 30, oy + h // 2, "Transmittance (%)", BLACK, 1)
    c.text_c(ox + w // 2, oy + h + 26, "Wavenumber (cm-1)", BLACK, 1)
    # wavenumber axis 4000 -> 500 (reversed)
    for wv in (4000, 3400, 2500, 1500, 1100, 950, 600, 500):
        frac = (4000 - wv) / (4000 - 500)
        xx = ox + int(frac * w)
        c.vline(xx, oy + h, oy + h + 4, BLACK)
        c.text_c(xx, oy + h + 8, str(wv), BLACK, 1)

    def band(wv):
        return ox + int((4000 - wv) / (4000 - 500) * w)

    # dashed guide lines at key bands
    for wv, lab in [(3400, "O-H"), (1100, "Si-O-Si"), (950, "Si-O(NBO)"), (600, "bend"), (500, "Ti/Mn-O")]:
        xx = band(wv)
        c.dline(xx, oy, xx, oy + h, LIGHT_GRAY, 4, 4)
        c.text_c(xx, oy - 12, lab, DGRAY, 1)

    def spectrum(shift, base_y, color, dips):
        prev = None
        for i in range(w + 1):
            wv = 4000 - i / w * (4000 - 500)
            t = base_y
            for (center, depth, width) in dips:
                cc = center + shift
                t += depth * math.exp(-((wv - cc) ** 2) / (2 * width * width))
            yy = oy + int(t)
            xx = ox + i
            if prev is not None:
                c.line(prev[0], prev[1], xx, yy, color, 1)
            prev = (xx, yy)

    # dips: (center wavenumber, depth px, width)
    dips_A = [(3400, 70, 220), (1105, 150, 90), (950, 30, 60), (600, 60, 70), (500, 45, 60)]
    dips_B = [(3400, 45, 200), (1085, 150, 95), (950, 70, 60), (600, 70, 70), (500, 60, 60)]
    spectrum(0, 60, MED_BLUE, dips_A)
    spectrum(0, 200, RED, dips_B)

    # legend
    c.hline(ox + w - 190, ox + w - 160, oy + 20, MED_BLUE)
    c.text(ox + w - 155, oy + 16, "Set A (Flux 1,6,7,11)", BLACK, 1)
    c.hline(ox + w - 190, ox + w - 160, oy + 36, RED)
    c.text(ox + w - 155, oy + 32, "Set B (Flux 14,19,21,25)", BLACK, 1)

    c.text_c(450, 540, "Figure 4.6  FTIR spectra showing Si-O-Si red-shift and increased NBO (depolymerization) in set B", BLACK, 1)
    c.save(os.path.join(OUT, 'Figure_4_6.png'))
    print("  Figure_4_6.png")


# =====================================================================
# Figure 4.7 - Impact toughness bar chart
# =====================================================================
def fig_4_7():
    c = PNGCanvas(900, 560, WHITE)
    c.text_c(450, 12, "Charpy Impact Toughness of SAW Weldments", BLACK, 2)

    # Two panels: (a) Weld metal, (b) HAZ; groups RT and -55C; series fluxes
    fluxes = ["BM", "CF", "F6B", "F20B", "F22B"]
    colors = [DARK_GREEN, GRAY, MED_BLUE, ORANGE, PURPLE]
    # weld metal RT / -55
    wm_rt = [350, 159, 171, 132, 118]
    wm_lt = [35, 18, 21, 14, 11]
    haz_rt = [400, 300, 385, 260, 240]
    haz_lt = [45, 22, 28, 18, 15]

    def panel(ox, oy, w, h, rt, lt, title):
        c.text(ox, oy - 14, title, DARK_BLUE, 1)
        c.vline(ox, oy, oy + h, BLACK)
        c.hline(ox, ox + w, oy + h, BLACK)
        c.text_v(ox - 30, oy + h // 2, "Impact energy (J)", BLACK, 1)
        vmax = 420
        for t in range(5):
            val = vmax * t // 4
            yy = oy + h - int(val / vmax * h)
            c.hline(ox - 4, ox, yy, BLACK)
            c.text(ox - 30, yy - 3, str(val), BLACK, 1)
        gw = w // 2
        for gi, (data, glab) in enumerate([(rt, "Room temp"), (lt, "-55C")]):
            gx = ox + gi * gw + 16
            bw = (gw - 40) // len(fluxes)
            for i, v in enumerate(data):
                bh = int(v / vmax * h)
                bx = gx + i * bw
                c.rect(bx, oy + h - bh, bx + bw - 3, oy + h, DGRAY, colors[i])
                c.text_c(bx + bw // 2 - 1, oy + h - bh - 10, str(v), BLACK, 1)
            c.text_c(gx + (gw - 40) // 2, oy + h + 8, glab, BLACK, 1)

    panel(70, 60, 360, 340, wm_rt, wm_lt, "(a) Weld metal / fusion zone")
    panel(540, 60, 360, 340, haz_rt, haz_lt, "(b) Heat-affected zone")

    # legend
    lx = 70
    for i, f in enumerate(fluxes):
        c.fill_rect(lx + i * 150, 440, lx + i * 150 + 16, 452, colors[i])
        c.text(lx + i * 150 + 22, 442, f, BLACK, 1)

    c.text_c(450, 540, "Figure 4.7  Impact toughness at room temperature and -55C (weld metal and HAZ regions)", BLACK, 1)
    c.save(os.path.join(OUT, 'Figure_4_7.png'))
    print("  Figure_4_7.png")


# =====================================================================
# Figure 4.8 - Fractography montage
# =====================================================================
def fig_4_8():
    c = PNGCanvas(900, 640, WHITE)
    c.text_c(450, 12, "Fractography of API X70 SAW Weldments (SEM, 1000x)", BLACK, 2)

    def dimples(px, py, w, h, density, size):
        random.seed(int(px + py))
        c.rect(px, py, px + w, py + h, DGRAY, (60, 60, 66))
        for _ in range(density):
            dx = random.randint(px + 6, px + w - 6)
            dy = random.randint(py + 6, py + h - 6)
            r = random.randint(size, size + 4)
            c.circle(dx, dy, r, (150, 150, 158), (95, 95, 102))
            c.circle(dx, dy, max(1, r - 3), (40, 40, 46))

    def cleavage(px, py, w, h, nfacet):
        random.seed(int(px * 3 + py))
        c.rect(px, py, px + w, py + h, DGRAY, (70, 72, 80))
        for _ in range(nfacet):
            fx = random.randint(px + 4, px + w - 30)
            fy = random.randint(py + 4, py + h - 30)
            fw = random.randint(18, 34)
            fh = random.randint(16, 30)
            shade = random.randint(110, 175)
            c.rect(fx, fy, fx + fw, fy + fh, (200, 200, 205), (shade, shade, shade + 6))
            # river lines
            for _ in range(3):
                c.line(fx + 2, fy + fh // 2, fx + fw - 2,
                       fy + random.randint(2, fh - 2), (220, 220, 225), 1)

    def mixed(px, py, w, h):
        random.seed(int(px + py * 2))
        c.rect(px, py, px + w, py + h, DGRAY, (75, 75, 82))
        for _ in range(35):
            dx = random.randint(px + 6, px + w - 6)
            dy = random.randint(py + 6, py + h - 6)
            r = random.randint(3, 6)
            c.circle(dx, dy, r, (150, 150, 158), (95, 95, 102))
        for _ in range(6):
            fx = random.randint(px + 4, px + w - 30)
            fy = random.randint(py + 4, py + h - 30)
            c.rect(fx, fy, fx + 24, fy + 20, (200, 200, 205), (140, 140, 146))

    pw, ph = 260, 165
    x0 = 40
    # Row 1: PM, HAZ, FZ at RT
    dimples(x0, 55, pw, ph, 60, 5)
    c.text(x0 + 4, 55 + ph + 4, "(a) Parent metal - ductile dimples (350 J)", BLACK, 1)
    mixed(x0 + pw + 30, 55, pw, ph)
    c.text(x0 + pw + 34, 55 + ph + 4, "(b) HAZ - mixed mode (385 J, F6B)", BLACK, 1)
    dimples(x0 + 2 * (pw + 30), 55, pw, ph, 45, 4)
    c.text(x0 + 2 * (pw + 30) + 4, 55 + ph + 4, "(c) Fusion zone F6B RT (171 J)", BLACK, 1)

    # Row 2: FZ CF, FZ F22B, HAZ at -55
    y1 = 300
    mixed(x0, y1, pw, ph)
    c.text(x0 + 4, y1 + ph + 4, "(d) Fusion zone CF RT (159 J)", BLACK, 1)
    cleavage(x0 + pw + 30, y1, pw, ph, 16)
    c.text(x0 + pw + 34, y1 + ph + 4, "(e) Fusion zone F22B - cleavage facets", BLACK, 1)
    cleavage(x0 + 2 * (pw + 30), y1, pw, ph, 20)
    c.text(x0 + 2 * (pw + 30) + 4, y1 + ph + 4, "(f) CGHAZ at -55C - brittle cleavage", BLACK, 1)

    c.text_c(450, 620, "Figure 4.9  Fractographs of parent metal, fusion zone and HAZ (SEM, 1000x, 15 kV)", BLACK, 1)
    c.save(os.path.join(OUT, 'Figure_4_8.png'))
    print("  Figure_4_8.png")


# =====================================================================
# Figure 4.9 - Microstructure montage
# =====================================================================
def fig_4_9():
    c = PNGCanvas(900, 620, WHITE)
    c.text_c(450, 12, "Fusion-Zone Microstructure of SAW Weldments (Optical)", BLACK, 2)

    def acicular(px, py, w, h, af_density, seed):
        random.seed(seed)
        c.rect(px, py, px + w, py + h, DGRAY, (232, 226, 214))
        # prior austenite grain boundaries (light polygons)
        for _ in range(5):
            gx = random.randint(px, px + w)
            gy = random.randint(py, py + h)
            c.circle(gx, gy, random.randint(35, 55), (200, 195, 185))
        # acicular ferrite laths (short interlocking needles)
        for _ in range(af_density):
            lx = random.randint(px + 6, px + w - 20)
            ly = random.randint(py + 6, py + h - 20)
            ang = random.uniform(0, math.pi)
            ln = random.randint(10, 22)
            ex = int(lx + ln * math.cos(ang))
            ey = int(ly + ln * math.sin(ang))
            c.line(lx, ly, ex, ey, (90, 80, 70), 1)
        return

    def coarse(px, py, w, h, seed):
        random.seed(seed)
        c.rect(px, py, px + w, py + h, DGRAY, (236, 230, 220))
        # grain boundary ferrite + Widmanstatten (long parallel plates)
        for _ in range(7):
            gy = random.randint(py + 10, py + h - 10)
            c.line(px + 4, gy, px + w - 4, gy + random.randint(-6, 6), (120, 110, 100), 2)
        for _ in range(20):
            lx = random.randint(px + 8, px + w - 40)
            ly = random.randint(py + 8, py + h - 8)
            ang = random.uniform(-0.5, 0.5)
            ln = random.randint(28, 44)
            ex = int(lx + ln * math.cos(ang))
            ey = int(ly + ln * math.sin(ang))
            c.line(lx, ly, ex, ey, (100, 90, 80), 1)

    pw, ph = 400, 220
    gap = 20
    x0, y0 = 30, 55
    acicular(x0, y0, pw, ph, 220, 1)
    c.text(x0 + 6, y0 + ph + 4, "(a) F6B - fine acicular ferrite (AF) dominant", BLACK, 1)
    acicular(x0 + pw + gap, y0, pw, ph, 170, 2)
    c.text(x0 + pw + gap + 6, y0 + ph + 4, "(b) F20B - AF + polygonal ferrite (PF)", BLACK, 1)

    y1 = y0 + ph + 40
    acicular(x0, y1, pw, ph, 150, 3)
    c.text(x0 + 6, y1 + ph + 4, "(c) F22B - AF with fine bainite (LB/UB)", BLACK, 1)
    coarse(x0 + pw + gap, y1, pw, ph, 4)
    c.text(x0 + pw + gap + 6, y1 + ph + 4, "(d) CF - AF + GBF/WF, coarser structure", BLACK, 1)

    c.text_c(450, 604, "Figure 4.10  Microstructures: AF acicular ferrite, PF polygonal ferrite, LB/UB bainite, GBF/WF grain-boundary/Widmanstatten ferrite", BLACK, 1)
    c.save(os.path.join(OUT, 'Figure_4_9.png'))
    print("  Figure_4_9.png")


def main():
    os.makedirs(OUT, exist_ok=True)
    print("Generating Chapter 4 figures...")
    fig_4_1()
    fig_4_2()
    fig_4_3()
    fig_4_4()
    fig_4_5()
    fig_4_6()
    fig_4_7()
    fig_4_8()
    fig_4_9()
    print("\nAll figures saved to %s/" % OUT)
    for f in sorted(os.listdir(OUT)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUT, f))
            print("  %s: %.1f KB" % (f, sz / 1024))


if __name__ == '__main__':
    main()
