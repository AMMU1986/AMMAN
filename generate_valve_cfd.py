#!/usr/bin/env python3
"""
Geometry 2 (Smooth-Loop) valvular conduit - CFD contour redraw.

Produces a single composite figure (PNG) with:
  * Velocity-magnitude contours (jet colormap) over the full domain, with
    streamwise streamlines and recirculation glyphs, and a labelled colour bar.
  * Vorticity contours (diverging blue-white-red colormap) over the full
    domain with a labelled colour bar.
  * A zoomed recirculation-detail panel (loop / junction) showing the
    recirculating eddies.

All field colouring and overlays are clipped to the interior of the conduit
walls (the field is painted cell-by-cell on the structured grid and the solid
walls are re-drawn on top), so nothing bleeds outside the outer structure.

Synthetic but physically-plausible fields (no external CFD solver is available
in this environment). Pure standard library; reuses PNGCanvas and the geometry
defined in generate_valve_mesh.py.
"""

import os
import math

from generate_figures import PNGCanvas
from generate_valve_mesh import (
    UPPER_LOOP, LOWER_CRESCENT, MAIN, WM, WB,
    catmull_rom, resample, normals, make_T, blit, fill_poly,
)

OUT = '/projects/sandbox/AMMAN'

WHITE = (255, 255, 255)
BLACK = (12, 12, 12)
NAVY = (18, 30, 66)
WALL = (20, 20, 22)

VMAX = 330.0        # velocity magnitude scale [m s^-1]
WMAX = 5.0e3        # vorticity scale [1/s]


# ----------------------------------------------------------------------------
# Colormaps
# ----------------------------------------------------------------------------
def clamp01(x):
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)


def cmap_jet(v):
    v = clamp01(v)
    r = clamp01(1.5 - abs(4 * v - 3))
    g = clamp01(1.5 - abs(4 * v - 2))
    b = clamp01(1.5 - abs(4 * v - 1))
    return (int(255 * r), int(255 * g), int(255 * b))


def cmap_div(v):
    """Diverging blue(-1) -> white(0) -> red(+1)."""
    if v > 1:
        v = 1
    if v < -1:
        v = -1
    if v >= 0:
        t = v
        return (int(255 + (205 - 255) * t), int(255 + (35 - 255) * t), int(255 + (38 - 255) * t))
    t = -v
    return (int(255 + (36 - 255) * t), int(255 + (72 - 255) * t), int(255 + (200 - 255) * t))


# ----------------------------------------------------------------------------
# Field models (normalised)
# ----------------------------------------------------------------------------
def _gauss(f, fc, wd):
    return math.exp(-((f - fc) / wd) ** 2)


def speed_factor(kind, f):
    """Centreline (peak) speed along a channel, normalised 0..~1.1."""
    if kind == 'main':
        s = 0.58
        s += 0.55 * _gauss(f, 0.22, 0.05)   # inlet throat jet (max, red)
        s += 0.22 * _gauss(f, 0.54, 0.045)  # L2 junction
        s += 0.34 * _gauss(f, 0.90, 0.055)  # outlet junction
        return s
    if kind == 'loop':
        s = 0.50 - 0.44 * _gauss(f, 0.50, 0.22)   # slow recirculating core mid-loop
        s += 0.30 * _gauss(f, 0.07, 0.05)         # entrance acceleration
        s += 0.12 * _gauss(f, 0.93, 0.05)
        return max(s, 0.05)
    # crescent
    s = 0.34 - 0.26 * _gauss(f, 0.50, 0.26)
    s += 0.16 * _gauss(f, 0.06, 0.05)
    return max(s, 0.04)


def vel_value(kind, f, t):
    prof = max(1.0 - (2 * t - 1) ** 2, 0.0)     # parabolic -> 0 at walls
    return clamp01(speed_factor(kind, f) * prof)


def vort_value(kind, f, t):
    shear = -(2 * t - 1)                        # +1 at t=0 wall, -1 at t=1 wall
    v = speed_factor(kind, f) * shear * 1.45
    return -1.0 if v < -1 else (1.0 if v > 1 else v)


# ----------------------------------------------------------------------------
# Grid + rendering
# ----------------------------------------------------------------------------
def field_grid(control, width, m, step):
    center = resample(catmull_rom(control, 26), step)
    nrm = normals(center)
    grid = []
    for i, (cx, cy) in enumerate(center):
        nx, ny = nrm[i]
        row = [(cx + (-0.5 * width + width * (k / m)) * nx,
                cy + (-0.5 * width + width * (k / m)) * ny) for k in range(m + 1)]
        grid.append(row)
    return center, grid


# geometry (built once)
CEN_LOOP, G_LOOP = field_grid(UPPER_LOOP, WB, 40, 0.16)
CEN_CRE, G_CRE = field_grid(LOWER_CRESCENT, WB, 40, 0.16)
CEN_MAIN, G_MAIN = field_grid(MAIN, WM, 44, 0.16)

CHANNELS = [('loop', G_LOOP), ('crescent', G_CRE), ('main', G_MAIN)]


def draw_walls(c, grid, T):
    ni, nk = len(grid), len(grid[0])
    P = [[T(x, y) for (x, y) in row] for row in grid]
    for k in (0, nk - 1):
        for i in range(ni - 1):
            c.line(int(P[i][k][0]), int(P[i][k][1]),
                   int(P[i + 1][k][0]), int(P[i + 1][k][1]), WALL, 2)


def render_field(c, T, valuefunc, cmap, diverging=False):
    for kind, grid in CHANNELS:
        ni, nk = len(grid), len(grid[0])
        m = nk - 1
        P = [[T(x, y) for (x, y) in row] for row in grid]
        for i in range(ni - 1):
            f = i / (ni - 1)
            for k in range(m):
                t = (k + 0.5) / m
                val = valuefunc(kind, f, t)
                col = cmap(val)
                fill_poly(c, [P[i][k], P[i + 1][k], P[i + 1][k + 1], P[i][k + 1]], col)
        draw_walls(c, grid, T)   # walls after this channel -> clean junctions
    # redraw main walls last for a crisp outer boundary
    draw_walls(c, G_MAIN, T)


# ----------------------------------------------------------------------------
# Overlays
# ----------------------------------------------------------------------------
def flow_arrows(c, T, center, color, spacing_mm=4.5, step=0.16, alen=1.3):
    d = max(1, int(spacing_mm / step))
    la = max(1, int(alen / step))
    for i in range(d, len(center) - la, d):
        x1, y1 = T(*center[i])
        x2, y2 = T(*center[i + la])
        c.arrow(int(x1), int(y1), int(x2), int(y2), color, 2, 7)


def vortex(c, T, cx, cy, rmm, cw, color, start_deg=20, sweep_deg=300):
    a0 = math.radians(start_deg)
    sweep = math.radians(sweep_deg) * (1 if cw else -1)
    N = 26
    pts = []
    for j in range(N + 1):
        a = a0 + sweep * (j / N)
        pts.append(T(cx + rmm * math.cos(a), cy + rmm * math.sin(a)))
    for j in range(len(pts) - 1):
        c.line(int(pts[j][0]), int(pts[j][1]), int(pts[j + 1][0]), int(pts[j + 1][1]), color, 2)
    c.arrow(int(pts[-2][0]), int(pts[-2][1]), int(pts[-1][0]), int(pts[-1][1]), color, 2, 7)


def midpoint(center):
    return center[len(center) // 2]


# ----------------------------------------------------------------------------
# Colour bar
# ----------------------------------------------------------------------------
def colorbar(c, x, y, w, h, cmap, vmin, vmax, title, unit, diverging=False):
    for row in range(h):
        frac = 1.0 - row / (h - 1)              # top = max
        if diverging:
            val = cmap(2 * frac - 1)
        else:
            val = cmap(frac)
        c.hline(x, x + w, y + row, val)
    c.rect(x, y, x + w, y + h, BLACK)
    nt = 11
    for i in range(nt):
        fy = y + int(h * i / (nt - 1))
        frac = 1.0 - i / (nt - 1)
        v = vmin + (vmax - vmin) * frac
        c.line(x + w, fy, x + w + 5, fy, BLACK, 1)
        c.text(x + w + 8, fy - 3, "%.2e" % v, BLACK, 1)
    c.text(x, y - 30, title, BLACK, 1)
    c.text(x, y - 16, unit, BLACK, 1)


# ----------------------------------------------------------------------------
# Composite
# ----------------------------------------------------------------------------
def build():
    W, H = 1520, 1500
    fig = PNGCanvas(W, H, WHITE)
    fig.fill_rect(0, 0, W - 1, H - 1, WHITE)

    fig.text(36, 18, "GEOMETRY 2 - SMOOTH-LOOP VALVULAR CONDUIT: CFD CONTOURS (FORWARD FLOW)", NAVY, 2)
    fig.text(36, 44, "Rc = 4.0 mm   theta = 30 deg   wb/wm = 0.75   L = 35 mm   depth = 1.0 mm   |   fields clipped to conduit interior", (70, 80, 95), 1)

    XR = (-1.5, 36.5)
    YR = (-6.0, 10.0)

    # ---------- Panel 1: velocity magnitude ----------
    p1x, p1y = 150, 70
    pw, ph = 1150, 500
    vel = PNGCanvas(pw, ph, WHITE)
    vel.fill_rect(0, 0, pw - 1, ph - 1, WHITE)
    Tv, sv = make_T(XR[0], XR[1], YR[0], YR[1], pw, ph, 14)
    render_field(vel, Tv, vel_value, cmap_jet)
    # streamwise streamlines (forward flow)
    flow_arrows(vel, Tv, CEN_MAIN, BLACK, spacing_mm=4.2)
    flow_arrows(vel, Tv, CEN_LOOP, BLACK, spacing_mm=4.0)
    flow_arrows(vel, Tv, CEN_CRE, BLACK, spacing_mm=4.5)
    # recirculation glyphs (slow cores + separation bubbles), inside walls
    lm = midpoint(CEN_LOOP)
    cm = midpoint(CEN_CRE)
    vortex(vel, Tv, lm[0], lm[1], 0.55, True, BLACK)                 # loop recirc core
    vortex(vel, Tv, cm[0], cm[1], 0.5, False, BLACK)                # crescent recirc core
    vortex(vel, Tv, 9.6, -0.45, 0.34, False, BLACK, sweep_deg=290)  # sep bubble after inlet junction
    vortex(vel, Tv, 20.8, 0.45, 0.32, True, BLACK, sweep_deg=290)   # sep bubble after L2 junction
    # labels
    p = Tv(lm[0], lm[1])
    vel.text(int(p[0]) - 60, int(p[1]) - 26, "recirculation", BLACK, 1)
    p = Tv(cm[0], cm[1])
    vel.text(int(p[0]) - 30, int(p[1]) + 14, "recirculation", BLACK, 1)
    vel.rect(0, 0, pw - 1, ph - 1, NAVY)
    blit(fig, vel, p1x, p1y)
    fig.text(p1x + 6, p1y + 6, "(a) VELOCITY MAGNITUDE  +  STREAMLINES / RECIRCULATION", NAVY, 1)
    colorbar(fig, 40, p1y + 40, 22, ph - 90, cmap_jet, 0.0, VMAX, "Velocity", "[m s^-1]")

    # ---------- Panel 2: vorticity ----------
    p2y = p1y + ph + 40
    vor = PNGCanvas(pw, ph, WHITE)
    vor.fill_rect(0, 0, pw - 1, ph - 1, WHITE)
    Tw, sw = make_T(XR[0], XR[1], YR[0], YR[1], pw, ph, 14)
    render_field(vor, Tw, vort_value, cmap_div, diverging=True)
    vor.rect(0, 0, pw - 1, ph - 1, NAVY)
    blit(fig, vor, p1x, p2y)
    fig.text(p1x + 6, p2y + 6, "(b) VORTICITY (z)  -  SHEAR LAYERS AT WALLS AND SEPARATION REGIONS", NAVY, 1)
    colorbar(fig, 40, p2y + 40, 22, ph - 90, cmap_div, WMAX, -WMAX, "Vorticity", "[1 s^-1]", diverging=True)

    # ---------- Panel 3: recirculation zoom (loop + L2 junction) ----------
    p3y = p2y + ph + 40
    zw, zh = 720, 340
    zoom = PNGCanvas(zw, zh, WHITE)
    zoom.fill_rect(0, 0, zw - 1, zh - 1, WHITE)
    Tz, sz = make_T(7.0, 22.0, -2.5, 9.8, zw, zh, 12)
    render_field(zoom, Tz, vel_value, cmap_jet)
    flow_arrows(zoom, Tz, CEN_MAIN, BLACK, spacing_mm=2.6, alen=1.0)
    flow_arrows(zoom, Tz, CEN_LOOP, BLACK, spacing_mm=2.4, alen=1.0)
    vortex(zoom, Tz, lm[0], lm[1], 0.6, True, BLACK)
    vortex(zoom, Tz, 20.8, 0.45, 0.4, True, BLACK, sweep_deg=300)
    vortex(zoom, Tz, 9.6, -0.45, 0.4, False, BLACK, sweep_deg=300)
    zoom.rect(0, 0, zw - 1, zh - 1, NAVY)
    blit(fig, zoom, p1x, p3y)
    fig.text(p1x + 6, p3y + 6, "(c) RECIRCULATION DETAIL - LOOP CORE + JUNCTION SEPARATION BUBBLES", NAVY, 1)

    # ---------- side note panel ----------
    nx = p1x + zw + 40
    fig.text(nx, p3y + 20, "NOTES", NAVY, 2)
    notes = [
        "- Forward flow: fast core through the main channel;",
        "  the wide, smooth loop keeps the bypass attached.",
        "- Recirculation: slow, closed eddies form in the loop",
        "  core, the lower crescent, and as separation bubbles",
        "  just downstream of each junction.",
        "- Velocity -> 0 at all walls (no-slip); the highest",
        "  speed is the inlet-throat jet (red).",
        "- Vorticity: strong opposite-sign shear layers hug the",
        "  two walls; separation/shear layers mark the eddies.",
        "- All fields are painted inside the grid and the walls",
        "  are redrawn on top, so nothing extends past the",
        "  conduit outer structure.",
    ]
    for i, ln in enumerate(notes):
        fig.text(nx, p3y + 46 + i * 18, ln, (45, 55, 70), 1)

    cap = p3y + zh + 20
    fig.text(36, cap,
             "Figure: Synthetic velocity-magnitude and vorticity contours for the Geometry 2 (Smooth-Loop) valvular conduit under forward flow, with",
             (60, 70, 85), 1)
    fig.text(36, cap + 16,
             "streamlines and recirculation eddies. Contours are strictly confined to the conduit interior.",
             (60, 70, 85), 1)
    return fig


def main():
    fig = build()
    path = os.path.join(OUT, 'Geometry2_SmoothLoop_CFD_Contours.png')
    fig.save(path)
    print("Saved", path, "%.1f KB" % (os.path.getsize(path) / 1024))


if __name__ == '__main__':
    main()
