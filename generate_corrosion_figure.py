#!/usr/bin/env python3
"""
Generate the potentiodynamic polarization figure for Chapter 5 (Corrosion Analysis)
of API X70 SAW weldments in 3.5 wt.% NaCl (sea water) environment.

Single exposing environment (Sea water) shown for all four specimens:
    F6B, F20B, F22B and CF (commercial flux).

Corrosion-resistance ranking encoded in the curves:
    F6B > CF > F20B > F22B
(more noble E_corr and lower i_corr  =>  higher corrosion resistance)

Pure Python standard library only (no matplotlib) - reuses the PNGCanvas
drawing engine that the other figure scripts in this repo use.
"""

import math
import os

# Reuse the canvas + font engine already present in the repo.
from generate_figures import (
    PNGCanvas,
    BLACK, WHITE, GRAY, LIGHT_GRAY,
    DARK_BLUE, MED_BLUE, RED, DARK_GREEN, ORANGE, PURPLE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/figures'


# ---------------------------------------------------------------------------
# Electrochemical parameters for each weldment (Tafel model).
#   E_corr : corrosion potential (V vs SCE)  -> more positive = more noble
#   i_corr : corrosion current density (A/cm^2, log10 value) -> lower = better
#   ba, bc : anodic / cathodic Tafel slopes (V/decade)
#
# Ranking (best -> worst corrosion resistance): F6B > CF > F20B > F22B
# ---------------------------------------------------------------------------
SPECIMENS = [
    # name,  E_corr,  log10(i_corr[A/cm2]),  ba,    bc,    color
    ("F6B",  -0.610,  -6.55,                 0.075, 0.120, DARK_GREEN),  # most noble, lowest icorr
    ("CF",   -0.645,  -6.35,                 0.080, 0.125, MED_BLUE),    # close to F6B
    ("F20B", -0.700,  -6.05,                 0.085, 0.130, ORANGE),
    ("F22B", -0.740,  -5.85,                 0.090, 0.135, RED),         # least noble, highest icorr
]


def tafel_log_i(E, Ecorr, log_icorr, ba, bc):
    """Return log10(|i|) [A/cm^2] for potential E using the Butler-Volmer /
    Tafel mixed-potential model:  i = i_corr * (10^((E-Ecorr)/ba) - 10^(-(E-Ecorr)/bc))
    """
    icorr = 10.0 ** log_icorr
    eta = E - Ecorr
    ia = icorr * (10.0 ** (eta / ba))
    ic = icorr * (10.0 ** (-eta / bc))
    i = abs(ia - ic)
    if i < 1e-12:
        i = 1e-12
    return math.log10(i)


def gen_corrosion_figure():
    W, H = 820, 620
    c = PNGCanvas(W, H, WHITE)

    # ---- Titles ----
    c.text_c(W // 2, 14, "Potentiodynamic Polarization of API X70 SAW Weldments", BLACK, 2)
    c.text_c(W // 2, 40, "Sea water (3.5 wt.% NaCl)", BLACK, 1)

    # ---- Plot area (data coordinates) ----
    # X axis: log10(current density) in A/cm^2, from -8 to -3
    # Y axis: potential E (V vs SCE), from -1.0 to -0.3
    x_min, x_max = -8.0, -3.0
    y_min, y_max = -1.00, -0.30

    # Pixel frame
    px_left, px_right = 95, W - 175
    px_top, px_bot = 70, H - 90

    def sx(logi):
        return int(px_left + (logi - x_min) / (x_max - x_min) * (px_right - px_left))

    def sy(E):
        # higher potential -> higher on screen (smaller pixel y)
        return int(px_bot - (E - y_min) / (y_max - y_min) * (px_bot - px_top))

    # ---- Grid ----
    for gx in range(int(x_min), int(x_max) + 1):
        xpix = sx(gx)
        c.vline(xpix, px_top, px_bot, LIGHT_GRAY)
    for k in range(0, 8):
        E = y_min + k * (y_max - y_min) / 7.0
        ypix = sy(E)
        c.hline(px_left, px_right, ypix, LIGHT_GRAY)

    # ---- Axis frame ----
    c.rect(px_left, px_top, px_right, px_bot, BLACK)

    # ---- X ticks / labels (log decades) ----
    for gx in range(int(x_min), int(x_max) + 1):
        xpix = sx(gx)
        c.vline(xpix, px_bot, px_bot + 5, BLACK)
        c.text_c(xpix, px_bot + 10, "10" , BLACK, 1)
        c.text(xpix + 12, px_bot + 6, str(gx), BLACK, 1)  # exponent
    c.text_c((px_left + px_right) // 2, px_bot + 34,
             "Current Density  log i  (A/cm2)", BLACK, 1)

    # ---- Y ticks / labels ----
    for k in range(0, 8):
        E = y_min + k * (y_max - y_min) / 7.0
        ypix = sy(E)
        c.hline(px_left - 5, px_left, ypix, BLACK)
        c.text(px_left - 55, ypix - 3, f"{E:0.2f}", BLACK, 1)
    # Rotated-ish y title (draw stacked)
    ylabel = "E (V vs SCE)"
    for i, ch in enumerate(ylabel):
        c.text(18, px_top + 60 + i * 12, ch, BLACK, 1)

    # ---- Curves ----
    N = 360
    for name, Ecorr, log_icorr, ba, bc, color in SPECIMENS:
        prev = None
        for n in range(N + 1):
            E = y_min + n * (y_max - y_min) / N
            li = tafel_log_i(E, Ecorr, log_icorr, ba, bc)
            if li < x_min:
                li = x_min
            if li > x_max:
                li = x_max
            xpix, ypix = sx(li), sy(E)
            if prev is not None:
                c.line(prev[0], prev[1], xpix, ypix, color, 2)
            prev = (xpix, ypix)

        # Mark corrosion potential (E_corr) at the curve's vertex (i_corr)
        cx, cy = sx(log_icorr), sy(Ecorr)
        c.circle(cx, cy, 3, BLACK, color)

    # ---- Legend (ordered by corrosion resistance, best -> worst) ----
    lx, ly = px_right + 20, px_top + 10
    c.text(lx, ly - 16, "Specimen", BLACK, 1)
    for i, (name, Ecorr, log_icorr, ba, bc, color) in enumerate(SPECIMENS):
        yy = ly + i * 22
        c.hline(lx, lx + 24, yy + 3, color)
        c.line(lx, yy + 2, lx + 24, yy + 2, color, 2)
        c.line(lx, yy + 3, lx + 24, yy + 3, color, 2)
        c.text(lx + 30, yy, name, BLACK, 1)

    # ---- Corrosion-resistance trend annotation ----
    ty = ly + len(SPECIMENS) * 22 + 18
    c.text(lx, ty, "Corrosion", BLACK, 1)
    c.text(lx, ty + 12, "resistance:", BLACK, 1)
    c.text(lx, ty + 30, "F6B > CF >", BLACK, 1)
    c.text(lx, ty + 42, "F20B > F22B", BLACK, 1)

    # ---- Ecorr / icorr summary box ----
    by0 = ty + 70
    c.text(lx, by0, "Ecorr (V):", BLACK, 1)
    for i, (name, Ecorr, log_icorr, ba, bc, color) in enumerate(SPECIMENS):
        c.text(lx, by0 + 14 + i * 12, f"{name}: {Ecorr:0.3f}", color, 1)

    # ---- Footer caption ----
    c.text(px_left, H - 40,
           "Figure 5.7: Potentiodynamic polarization curves of F6B, F20B, F22B and CF",
           BLACK, 1)
    c.text(px_left, H - 26,
           "weldments in sea water (3.5 wt.% NaCl). Trend: F6B > CF > F20B > F22B.",
           BLACK, 1)

    out = os.path.join(OUTPUT_DIR, 'Figure_Corrosion_Polarization_SeaWater.png')
    c.save(out)
    print(f"  saved {out}")


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    gen_corrosion_figure()
    print("Done.")
