#!/usr/bin/env python3
"""
Redraw of the "Geometry 2 - Smooth-Loop Configuration" valvular-conduit
computational mesh.

Produces a single composite figure (PNG) that shows:
  * the complete computational domain (main channel + smooth bypass loop
    + lower return crescent), rendered as a wall-clustered structured mesh
    on the usual blue CFD-viewer gradient background, and
  * four enlarged views of the branch junction, the curved loop passage,
    the narrow gap / recirculation region, and the near-wall / outlet
    junction, where strong gradients, flow separation and recirculation
    occur.

Geometry 2 parameters (Smooth-Loop):
    Rc = 4.0 mm   (bypass-loop radius of curvature)
    theta = 30 deg (branching angle)
    wb/wm = 0.75   (width ratio)   ->  wm = 2.0 mm, wb = 1.5 mm
    L  = 35 mm     (total valve length)
    depth = 1.0 mm (out-of-plane, rectangular cross-section)

Pure standard-library implementation (no matplotlib / numpy). Reuses the
PNGCanvas writer already present in this repository.
"""

import os
import math

from generate_figures import PNGCanvas, _FONT  # reuse PNG writer + font

OUT = '/projects/sandbox/AMMAN'

# ----------------------------------------------------------------------------
# Physical parameters (mm)
# ----------------------------------------------------------------------------
WM = 2.0            # main-channel width
WB = 0.75 * WM      # bypass width = 1.5 mm
L = 35.0            # total valve length

# ----------------------------------------------------------------------------
# Colours
# ----------------------------------------------------------------------------
BG_TOP = (96, 126, 205)     # gradient top (deep blue)
BG_BOT = (225, 233, 248)    # gradient bottom (pale blue)
CELL_FILL = (72, 78, 88)    # dark fill between mesh lines
MESH_LINE = (168, 177, 190) # fine interior mesh lines
WALL_LINE = (26, 30, 38)    # solid walls
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NAVY = (20, 34, 74)
RED = (200, 40, 40)
BOXCOL = (196, 30, 30)      # zoom-region markers
YELLOW = (250, 210, 60)


# ----------------------------------------------------------------------------
# Geometry helpers
# ----------------------------------------------------------------------------
def catmull_rom(pts, n=24):
    """Smooth Catmull-Rom spline through the given control points."""
    def cr(p0, p1, p2, p3, t):
        t2 = t * t
        t3 = t2 * t
        x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t +
                   (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                   (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
        y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t +
                   (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                   (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
        return (x, y)

    ext = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(ext) - 2):
        for j in range(n):
            out.append(cr(ext[i - 1], ext[i], ext[i + 1], ext[i + 2], j / n))
    out.append(pts[-1])
    return out


def resample(poly, step):
    """Resample a polyline at (approximately) uniform arc-length spacing."""
    out = [poly[0]]
    prev = poly[0]
    acc = 0.0
    for p in poly[1:]:
        seg = math.hypot(p[0] - prev[0], p[1] - prev[1])
        while seg > 0 and acc + seg >= step:
            r = (step - acc) / seg
            nx = prev[0] + (p[0] - prev[0]) * r
            ny = prev[1] + (p[1] - prev[1]) * r
            out.append((nx, ny))
            prev = (nx, ny)
            seg = math.hypot(p[0] - prev[0], p[1] - prev[1])
            acc = 0.0
        acc += seg
        prev = p
    if out[-1] != poly[-1]:
        out.append(poly[-1])
    return out


def normals(center):
    """Unit normals along a centreline (central differences)."""
    n = len(center)
    nrm = []
    for i in range(n):
        a = center[max(0, i - 1)]
        b = center[min(n - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        m = math.hypot(tx, ty) or 1.0
        nrm.append((-ty / m, tx / m))
    return nrm


def cluster_offsets(width, m, beta=1.7):
    """Cross-stream offsets clustered towards both walls (boundary layers)."""
    offs = []
    tb = math.tanh(beta)
    for k in range(m + 1):
        t = k / m
        s = math.tanh(beta * (2 * t - 1)) / tb    # -1 .. 1
        offs.append(0.5 * width * s)
    return offs


def build_grid(control, width, m, step=0.13, beta=1.7):
    """Return a structured grid G[i][k] (mm) for a channel."""
    center = resample(catmull_rom(control, 26), step)
    nrm = normals(center)
    offs = cluster_offsets(width, m, beta)
    grid = []
    for i, (cx, cy) in enumerate(center):
        nx, ny = nrm[i]
        row = [(cx + o * nx, cy + o * ny) for o in offs]
        grid.append(row)
    return grid


# ----------------------------------------------------------------------------
# Channel definitions (mm).  y = 0 is the main-channel axis.
# ----------------------------------------------------------------------------
MAIN = [(-1.5, 0.0), (36.5, 0.0)]

# Upper smooth bypass loop: leaves the main channel (junction L1), rises at
# ~30 deg, curves smoothly (Rc = 4 mm) up and over, and descends back to the
# main channel (junction L2) passing close above it (the "narrow gap").
UPPER_LOOP = [
    (7.0, 0.0),
    (8.7, 1.0),      # ~30 deg branching take-off
    (9.7, 3.3),
    (9.9, 6.1),
    (11.4, 8.4),     # crest region
    (14.4, 8.9),
    (17.0, 7.3),
    (18.5, 4.4),
    (18.9, 1.7),     # descending leg -> narrow gap with main-channel top wall
    (19.0, 0.0),     # junction L2
]

# Lower return crescent: departs near junction L2, sweeps in a long gentle arc
# below the main channel and rejoins it near the outlet (junction R).
LOWER_CRESCENT = [
    (18.6, 0.0),     # junction L2
    (19.6, -1.7),    # drop below
    (22.2, -3.2),
    (26.0, -3.8),    # crescent trough
    (30.0, -3.1),
    (32.3, -1.3),
    (33.2, 0.0),     # junction R (rejoin)
]

CHANNELS = [
    {'grid': build_grid(UPPER_LOOP, WB, 9, step=0.095, beta=1.7)},
    {'grid': build_grid(LOWER_CRESCENT, WB, 9, step=0.095, beta=1.7)},
    {'grid': build_grid(MAIN, WM, 12, step=0.11, beta=1.9)},  # drawn last (on top)
]


# ----------------------------------------------------------------------------
# Rendering primitives
# ----------------------------------------------------------------------------
def gradient_bg(c, top, bot):
    for y in range(c.h):
        t = y / (c.h - 1)
        col = (int(top[0] + (bot[0] - top[0]) * t),
               int(top[1] + (bot[1] - top[1]) * t),
               int(top[2] + (bot[2] - top[2]) * t))
        c.hline(0, c.w - 1, y, col)


def fill_poly(c, pts, color):
    if len(pts) < 3:
        return
    ys = [p[1] for p in pts]
    ymin = max(0, int(math.floor(min(ys))))
    ymax = min(c.h - 1, int(math.ceil(max(ys))))
    n = len(pts)
    for y in range(ymin, ymax + 1):
        xs = []
        yc = y + 0.5
        for i in range(n):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % n]
            if (y1 <= yc < y2) or (y2 <= yc < y1):
                xs.append(x1 + (x2 - x1) * (yc - y1) / (y2 - y1))
        xs.sort()
        for j in range(0, len(xs) - 1, 2):
            c.hline(int(round(xs[j])), int(round(xs[j + 1])), y, color)


def draw_channel(c, grid, T):
    """Fill + structured mesh for one channel, using transform T(x,y)->(px,py)."""
    ni = len(grid)
    nk = len(grid[0])
    # transform whole grid to pixels
    P = [[T(x, y) for (x, y) in row] for row in grid]

    # 1) solid fill between the two walls
    outline = [P[i][0] for i in range(ni)] + [P[i][nk - 1] for i in range(ni - 1, -1, -1)]
    fill_poly(c, outline, CELL_FILL)

    # 2) fine longitudinal mesh lines
    for k in range(nk):
        for i in range(ni - 1):
            x1, y1 = P[i][k]
            x2, y2 = P[i + 1][k]
            c.line(int(x1), int(y1), int(x2), int(y2), MESH_LINE, 1)

    # 3) fine transverse mesh lines
    for i in range(ni):
        for k in range(nk - 1):
            x1, y1 = P[i][k]
            x2, y2 = P[i][k + 1]
            c.line(int(x1), int(y1), int(x2), int(y2), MESH_LINE, 1)

    # 4) solid walls (k = 0 and k = nk-1)
    for k in (0, nk - 1):
        for i in range(ni - 1):
            x1, y1 = P[i][k]
            x2, y2 = P[i + 1][k]
            c.line(int(x1), int(y1), int(x2), int(y2), WALL_LINE, 2)


def render_domain(c, T):
    """Draw all channels (bypasses first, main channel on top) onto canvas c."""
    for ch in CHANNELS:
        draw_channel(c, ch['grid'], ch['grid'] and T)


def make_T(xmin, xmax, ymin, ymax, W, H, pad):
    sx = (W - 2 * pad) / (xmax - xmin)
    sy = (H - 2 * pad) / (ymax - ymin)
    s = min(sx, sy)
    ox = pad + (W - 2 * pad - s * (xmax - xmin)) / 2.0
    oy = pad + (H - 2 * pad - s * (ymax - ymin)) / 2.0

    def T(x, y):
        px = ox + (x - xmin) * s
        py = (H - oy) - (y - ymin) * s     # flip y so +y points up
        return (px, py)
    return T, s


def blit(dst, src, ox, oy):
    for y in range(src.h):
        dy = oy + y
        if dy < 0 or dy >= dst.h:
            continue
        di = (dy * dst.w + ox) * 3
        si = (y * src.w) * 3
        dst.data[di:di + src.w * 3] = src.data[si:si + src.w * 3]


def panel(w, h, xr, yr, pad=12):
    """Render one region into its own canvas and return it (with transform)."""
    c = PNGCanvas(w, h, BG_TOP)
    gradient_bg(c, BG_TOP, BG_BOT)
    T, s = make_T(xr[0], xr[1], yr[0], yr[1], w, h, pad)
    render_domain(c, T)
    # border
    c.rect(0, 0, w - 1, h - 1, NAVY)
    c.rect(1, 1, w - 2, h - 2, NAVY)
    return c, T, s


# ----------------------------------------------------------------------------
# Composite figure
# ----------------------------------------------------------------------------
def build_figure():
    W, H = 1500, 1320
    fig = PNGCanvas(W, H, WHITE)
    fig.fill_rect(0, 0, W - 1, H - 1, WHITE)

    # ---- Title ------------------------------------------------------------
    fig.text(40, 20, "GEOMETRY 2 - SMOOTH-LOOP VALVULAR CONDUIT: COMPUTATIONAL MESH", NAVY, 2)
    fig.text(40, 46, "Structured wall-clustered mesh  |  Rc = 4.0 mm   theta = 30 deg   wb/wm = 0.75   L = 35 mm   depth = 1.0 mm   (wm = 2.0 mm, wb = 1.5 mm)", (70, 80, 95), 1)

    # ---- Main domain view -------------------------------------------------
    mx, my = 30, 70
    mw, mh = W - 60, 600
    main = PNGCanvas(mw, mh, BG_TOP)
    gradient_bg(main, BG_TOP, BG_BOT)
    Tm, sm = make_T(-1.5, 36.5, -6.0, 10.0, mw, mh, 16)
    render_domain(main, Tm)
    main.rect(0, 0, mw - 1, mh - 1, NAVY)

    # zoom-region markers (mm boxes) + labels
    regions = [
        ("A", (5.0, 12.0, -2.5, 4.5), "Branch junction (inlet take-off)"),
        ("B", (8.5, 17.5, 4.5, 9.8), "Curved loop passage (crest)"),
        ("C", (15.5, 21.5, -2.5, 5.0), "Narrow gap / recirculation"),
        ("D", (28.5, 34.5, -4.6, 2.2), "Near-wall region (outlet junction)"),
    ]
    for tag, (x0, x1, y0, y1), _ in regions:
        p0 = Tm(x0, y1)
        p1 = Tm(x1, y0)
        rx0, ry0 = int(p0[0]), int(p0[1])
        rx1, ry1 = int(p1[0]), int(p1[1])
        main.rect(rx0, ry0, rx1, ry1, BOXCOL)
        main.rect(rx0 - 1, ry0 - 1, rx1 + 1, ry1 + 1, BOXCOL)
        main.fill_rect(rx0, ry0 - 18, rx0 + 16, ry0 - 2, BOXCOL)
        main.text(rx0 + 3, ry0 - 16, tag, WHITE, 2)

    # flow arrows
    ay = int(Tm(0, 0)[1])
    main.arrow(30, 40, 130, 40, NAVY, 3, 12)
    main.text(30, 20, "FORWARD FLOW (low resistance)", NAVY, 1)
    main.arrow(mw - 30, mh - 34, mw - 130, mh - 34, RED, 3, 12)
    main.text(mw - 300, mh - 54, "REVERSE FLOW (high resistance)", RED, 1)

    # scale bar (5 mm)
    sb = int(5 * sm)
    bx, by = 40, mh - 40
    main.fill_rect(bx, by, bx + sb, by + 6, NAVY)
    main.text(bx, by - 18, "5 mm", NAVY, 1)

    blit(fig, main, mx, my)
    fig.text(mx + 6, my + 6, "COMPLETE COMPUTATIONAL DOMAIN", WHITE, 1)

    # ---- Inset panels -----------------------------------------------------
    iy = my + mh + 26
    n = 4
    gap = 18
    iw = (W - 60 - (n - 1) * gap) // n
    ih = 300
    for idx, (tag, box, title) in enumerate(regions):
        pc, _, ps = panel(iw, ih, (box[0], box[1]), (box[2], box[3]), pad=10)
        px = 30 + idx * (iw + gap)
        blit(fig, pc, px, iy)
        # header bar
        fig.fill_rect(px, iy - 20, px + iw, iy - 2, NAVY)
        fig.fill_rect(px, iy - 20, px + 20, iy - 2, BOXCOL)
        fig.text(px + 5, iy - 18, tag, WHITE, 2)
        fig.text(px + 26, iy - 16, title.upper(), WHITE, 1)

    # ---- Parameter table --------------------------------------------------
    ty = iy + ih + 26
    fig.text(40, ty, "TABLE 1 - VALVULAR-CONDUIT CONFIGURATION PARAMETERS", NAVY, 2)
    ty += 26
    rows = [
        ("Parameter", "Symbol", "Geometry 2 (Smooth-Loop)"),
        ("Loop radius of curvature", "Rc", "4.0 mm"),
        ("Branching angle", "theta", "30 deg"),
        ("Width ratio", "wb / wm", "0.75"),
        ("Main-channel width", "wm", "2.0 mm"),
        ("Bypass width", "wb", "1.5 mm"),
        ("Total valve length", "L", "35 mm"),
        ("Channel depth", "d", "1.0 mm (rectangular section)"),
    ]
    col_x = [40, 430, 700]
    rh = 24
    tw = 1000
    for r, row in enumerate(rows):
        yy = ty + r * rh
        if r == 0:
            fig.fill_rect(40, yy - 2, 40 + tw, yy + rh - 4, NAVY)
        elif r % 2 == 0:
            fig.fill_rect(40, yy - 2, 40 + tw, yy + rh - 4, (235, 239, 246))
        for ci, cell in enumerate(row):
            col = WHITE if r == 0 else (30, 40, 60)
            fig.text(col_x[ci], yy + 4, cell, col, 1)
    # table outline
    fig.rect(40, ty - 2, 40 + tw, ty + len(rows) * rh - 4, NAVY)

    cap_y = ty + len(rows) * rh + 14
    fig.text(40, cap_y,
             "Figure: Geometry 2 (Smooth-Loop) valvular-conduit mesh. The gradual bypass curvature and wider passages (wb/wm = 0.75) suppress",
             (60, 70, 85), 1)
    fig.text(40, cap_y + 16,
             "flow separation in the forward direction while the recirculation set up in the loop and lower crescent resists reverse flow.",
             (60, 70, 85), 1)
    fig.text(40, cap_y + 32,
             "Insets A-D show the branch junction, curved loop passage, narrow gap/recirculation region and near-wall/outlet refinement.",
             (60, 70, 85), 1)

    return fig


def main():
    fig = build_figure()
    png_path = os.path.join(OUT, 'Geometry2_SmoothLoop_Mesh.png')
    fig.save(png_path)
    print("Saved", png_path, "%.1f KB" % (os.path.getsize(png_path) / 1024))


if __name__ == '__main__':
    main()
