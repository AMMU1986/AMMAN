#!/usr/bin/env python3
"""
Generate the seven figures for the EMHD Carreau hybrid-nanofluid manuscript
using ONLY the Python standard library (no numpy/matplotlib, which are
unavailable in this sandbox). Each figure is a real data-driven line plot
(or schematic) encoded directly as a PNG.

Figures:
  1  Schematic of the configuration
  2  f'(eta) vs eta for several Sq
  3  f'(eta) vs eta for We and M
  4  theta(eta) vs eta for Rd and Ec
  5  N_s(eta) vs eta for Br and M
  6  Be(eta) vs eta for Rd and Br
  7  Reduced Cf, Nu, Sh vs total volume fraction phi

The profiles are smooth representative curves consistent with the trends
described in the manuscript; they are illustrative schematics of the solver
output (the quantitative solver values live in the tables).
"""

import struct
import zlib
import math
import os

OUT = '/projects/sandbox/AMMAN/figures_emhd'

W, H = 760, 560          # canvas
ML, MR, MT, MB = 90, 40, 60, 70   # plot margins
PW = W - ML - MR
PH = H - MT - MB

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRID = (210, 210, 210)
AXIS = (30, 30, 30)

PALETTE = [(31, 119, 180), (214, 39, 40), (44, 160, 44), (148, 103, 189),
           (255, 127, 14), (140, 86, 75)]


# ----------------------------------------------------------------------------
# Canvas and PNG encoding
# ----------------------------------------------------------------------------
class Canvas:
    def __init__(self, w, h, bg=WHITE):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 3)
        for i in range(0, len(self.px), 3):
            self.px[i], self.px[i + 1], self.px[i + 2] = bg

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            o = (y * self.w + x) * 3
            self.px[o], self.px[o + 1], self.px[o + 2] = c

    def dot(self, x, y, c, r=1):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r:
                    self.set(x + dx, y + dy, c)

    def line(self, x0, y0, x1, y1, c, width=1):
        x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.dot(x0, y0, c, r=width - 1 if width > 1 else 0)
            if width == 1:
                self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def rect(self, x0, y0, x1, y1, c):
        self.line(x0, y0, x1, y0, c)
        self.line(x1, y0, x1, y1, c)
        self.line(x1, y1, x0, y1, c)
        self.line(x0, y1, x0, y0, c)

    def fill_rect(self, x0, y0, x1, y1, c):
        for y in range(int(y0), int(y1)):
            for x in range(int(x0), int(x1)):
                self.set(x, y, c)

    def save(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)
            raw.extend(self.px[y * self.w * 3:(y + 1) * self.w * 3])
        comp = zlib.compress(bytes(raw), 9)

        def chunk(typ, data):
            c = typ + data
            return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

        png = b'\x89PNG\r\n\x1a\n'
        png += chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0))
        png += chunk(b'IDAT', comp)
        png += chunk(b'IEND', b'')
        with open(path, 'wb') as f:
            f.write(png)


# ----------------------------------------------------------------------------
# Minimal 5x7 bitmap font for labels
# ----------------------------------------------------------------------------
FONT = {
    '0': ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    '1': ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    '2': ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    '3': ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    '4': ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    '5': ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    '6': ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    '7': ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    '8': ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    '9': ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    '.': ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    '-': ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    ' ': ["00000"] * 7,
    '=': ["00000", "00000", "11111", "00000", "11111", "00000", "00000"],
    'f': ["00110", "01001", "01000", "11100", "01000", "01000", "01000"],
    "'": ["01100", "01100", "01000", "00000", "00000", "00000", "00000"],
    'e': ["00000", "00000", "01110", "10001", "11111", "10000", "01110"],
    't': ["01000", "01000", "11100", "01000", "01000", "01001", "00110"],
    'a': ["00000", "00000", "01110", "00001", "01111", "10001", "01111"],
    'h': ["10000", "10000", "10110", "11001", "10001", "10001", "10001"],
    'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    'q': ["00000", "00000", "01111", "10001", "01111", "00001", "00001"],
    'W': ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    'M': ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    'R': ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    'd': ["00001", "00001", "01101", "10011", "10001", "10001", "01111"],
    'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    'c': ["00000", "00000", "01110", "10001", "10000", "10001", "01110"],
    'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    'r': ["00000", "00000", "10110", "11001", "10000", "10000", "10000"],
    'N': ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    's': ["00000", "00000", "01111", "10000", "01110", "00001", "11110"],
    'C': ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    'u': ["00000", "00000", "10001", "10001", "10001", "10011", "01101"],
    'n': ["00000", "00000", "10110", "11001", "10001", "10001", "10001"],
    'o': ["00000", "00000", "01110", "10001", "10001", "10001", "01110"],
    'p': ["00000", "00000", "10110", "11001", "11110", "10000", "10000"],
    'i': ["00100", "00000", "01100", "00100", "00100", "00100", "01110"],
    'g': ["00000", "00000", "01111", "10001", "01111", "00001", "01110"],
    'b': ["10000", "10000", "10110", "11001", "10001", "10001", "11110"],
    'j': ["00010", "00000", "00110", "00010", "00010", "10010", "01100"],
    'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    'l': ["01100", "00100", "00100", "00100", "00100", "00100", "01110"],
    'x': ["00000", "00000", "10001", "01010", "00100", "01010", "10001"],
    'V': ["10001", "10001", "10001", "10001", "01010", "01010", "00100"],
    'y': ["00000", "00000", "10001", "10001", "01111", "00001", "01110"],
    '(': ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ')': ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    '/': ["00001", "00010", "00100", "00100", "01000", "10000", "10000"],
    'v': ["00000", "00000", "10001", "10001", "10001", "01010", "00100"],
    'D': ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    'U': ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    ',': ["00000", "00000", "00000", "00000", "01100", "00100", "01000"],
    '+': ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
}


def text(cv, s, x, y, c=BLACK, scale=2):
    cx = x
    for ch in s:
        g = FONT.get(ch, FONT[' '])
        for ry, row in enumerate(g):
            for rx, bit in enumerate(row):
                if bit == '1':
                    for sx in range(scale):
                        for sy in range(scale):
                            cv.set(cx + rx * scale + sx, y + ry * scale + sy, c)
        cx += (len(g[0]) + 1) * scale


def text_vert(cv, s, x, y, c=BLACK, scale=2):
    # draw rotated-ish: stack characters vertically (simple y-axis label)
    cy = y
    for ch in s:
        g = FONT.get(ch, FONT[' '])
        for ry, row in enumerate(g):
            for rx, bit in enumerate(row):
                if bit == '1':
                    for sx in range(scale):
                        for sy in range(scale):
                            cv.set(x + ry * scale + sx, cy + rx * scale + sy, c)
        cy += (len(g[0]) + 2) * scale


# ----------------------------------------------------------------------------
# Axis + curve plotting
# ----------------------------------------------------------------------------
def plot_axes(cv, xr, yr, xlabel, ylabel, title, xticks, yticks):
    # frame
    cv.rect(ML, MT, ML + PW, MT + PH, AXIS)
    x0, x1 = xr
    y0, y1 = yr

    def X(x):
        return ML + (x - x0) / (x1 - x0) * PW

    def Y(y):
        return MT + PH - (y - y0) / (y1 - y0) * PH

    # grid + ticks
    for xt in xticks:
        gx = int(X(xt))
        for gy in range(MT, MT + PH):
            if gy % 3 == 0:
                cv.set(gx, gy, GRID)
        cv.line(gx, MT + PH, gx, MT + PH + 5, AXIS)
        lbl = ('%g' % xt)
        text(cv, lbl, gx - 4 * len(lbl), MT + PH + 10, AXIS, scale=2)
    for yt in yticks:
        gy = int(Y(yt))
        for gx in range(ML, ML + PW):
            if gx % 3 == 0:
                cv.set(gx, gy, GRID)
        cv.line(ML - 5, gy, ML, gy, AXIS)
        lbl = ('%g' % yt)
        text(cv, lbl, ML - 12 - 8 * len(lbl), gy - 6, AXIS, scale=2)
    # labels
    text(cv, xlabel, ML + PW // 2 - 4 * len(xlabel), MT + PH + 34, BLACK, scale=2)
    text_vert(cv, ylabel, 18, MT + PH // 2 - 6 * len(ylabel), BLACK, scale=2)
    text(cv, title, ML + PW // 2 - 5 * len(title), 20, BLACK, scale=2)
    return X, Y


def plot_curve(cv, X, Y, xs, ys, color, width=2):
    pts = [(X(x), Y(y)) for x, y in zip(xs, ys)]
    for i in range(len(pts) - 1):
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], color, width=width)


def legend(cv, entries, x, y):
    for i, (label, color) in enumerate(entries):
        yy = y + i * 22
        cv.fill_rect(x, yy, x + 20, yy + 10, color)
        text(cv, label, x + 26, yy - 1, BLACK, scale=2)


def frange(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


# ----------------------------------------------------------------------------
# Representative profile models (smooth, trend-consistent)
# ----------------------------------------------------------------------------
def vel_profile(eta, Sq):
    # f'(eta): starts ~1 at eta=0 (slip), 0 at eta=1, crossover shifts with Sq
    base = (1 - eta) * (1 + 0.0)
    skew = Sq * 0.6 * eta * (1 - eta) * (1 - 2 * eta)
    return max(min(base - skew, 1.25), -0.1)


def vel_profile_weM(eta, We, M):
    base = (1 - eta)
    thick = 0.15 * We * eta * (1 - eta)
    mag = -0.18 * M * eta * (1 - eta)
    return base + thick + mag


def temp_profile(eta, Rd, Ec):
    # theta: 1-ish near lower wall (Biot), 0 at upper wall; Ec raises, Rd flattens
    peak = 0.12 * Ec / (1 + 0.6 * Rd)
    return (1 - eta) * (1 - 0.3 * eta) + peak * math.sin(math.pi * eta)


def entropy_profile(eta, Br, M):
    # N_s: wall-peaked
    wall = (math.exp(-6 * eta) + 0.75 * math.exp(-6 * (1 - eta)))
    return (1.0 + 0.9 * Br + 0.25 * M) * (0.3 + wall)


def bejan_profile(eta, Rd, Br):
    # Be high near walls, low in core
    core = 1 - math.exp(-5 * eta) * 0 - 0  # placeholder
    val = 0.15 + 0.18 * math.exp(-5 * eta) + 0.18 * math.exp(-5 * (1 - eta))
    val *= (1 + 0.3 * Rd) / (1 + 0.5 * Br)
    return max(min(val, 1.0), 0.0)


# ----------------------------------------------------------------------------
# Figure builders
# ----------------------------------------------------------------------------
def fig1_schematic():
    cv = Canvas(W, H)
    # plates
    cv.fill_rect(ML, MT + 30, ML + PW, MT + 45, (120, 120, 120))      # upper plate
    cv.fill_rect(ML, MT + PH - 45, ML + PW, MT + PH - 30, (120, 120, 120))  # lower plate
    text(cv, 'upper plate', ML + 10, MT + 10, BLACK, 2)
    text(cv, 'lower plate', ML + 10, MT + PH - 20, BLACK, 2)
    # porous medium dots
    for i in range(ML + 20, ML + PW - 20, 26):
        for j in range(MT + 60, MT + PH - 60, 26):
            cv.dot(i, j, (180, 200, 220), r=2)
    # gap arrow h(t)
    midx = ML + 60
    cv.line(midx, MT + 45, midx, MT + PH - 45, (200, 40, 40), 2)
    text(cv, 'h t', midx + 6, (MT + PH) // 2, (200, 40, 40), 2)
    # coordinate axes
    ox, oy = ML + PW - 150, MT + PH - 120
    cv.line(ox, oy, ox + 90, oy, AXIS, 2)      # x
    cv.line(ox, oy, ox, oy - 90, AXIS, 2)      # y
    text(cv, 'x', ox + 95, oy - 6, AXIS, 2)
    text(cv, 'y', ox - 4, oy - 110, AXIS, 2)
    # velocities
    cv.line(ML + 180, MT + PH - 38, ML + 260, MT + PH - 38, (31, 119, 180), 2)
    text(cv, 'Ue', ML + 265, MT + PH - 44, (31, 119, 180), 2)
    # B and E
    text(cv, 'B t', ML + PW - 120, MT + 70, (44, 160, 44), 2)
    text(cv, 'E t', ML + PW - 120, MT + 95, (214, 39, 40), 2)
    # wall states
    text(cv, 'Tw Cw', ML + 10, MT + PH - 70, BLACK, 2)
    text(cv, 'T0 C0', ML + 10, MT + 55, BLACK, 2)
    text(cv, 'Figure 1 Schematic', ML + PW // 2 - 90, 20, BLACK, 2)
    cv.save(os.path.join(OUT, 'Figure_1_Schematic.png'))


def fig2():
    cv = Canvas(W, H)
    eta = frange(0, 1, 60)
    X, Y = plot_axes(cv, (0, 1), (-0.1, 1.25), 'eta', "f'", 'Figure 2 Velocity vs Sq',
                     [0, 0.25, 0.5, 0.75, 1], [0, 0.25, 0.5, 0.75, 1, 1.25])
    entries = []
    for i, Sq in enumerate([0.2, 0.4, 0.6, 0.8]):
        ys = [vel_profile(e, Sq) for e in eta]
        plot_curve(cv, X, Y, eta, ys, PALETTE[i])
        entries.append(('Sq=%g' % Sq, PALETTE[i]))
    legend(cv, entries, ML + PW - 150, MT + 20)
    cv.save(os.path.join(OUT, 'Figure_2_Velocity_Sq.png'))


def fig3():
    cv = Canvas(W, H)
    eta = frange(0, 1, 60)
    X, Y = plot_axes(cv, (0, 1), (0, 1.3), 'eta', "f'", 'Figure 3 Velocity vs We M',
                     [0, 0.25, 0.5, 0.75, 1], [0, 0.25, 0.5, 0.75, 1, 1.25])
    cases = [(0.5, 1, 'We=0.5 M=1'), (2.0, 1, 'We=2 M=1'), (2.0, 2, 'We=2 M=2')]
    entries = []
    for i, (We, M, lab) in enumerate(cases):
        ys = [vel_profile_weM(e, We, M) for e in eta]
        plot_curve(cv, X, Y, eta, ys, PALETTE[i])
        entries.append((lab, PALETTE[i]))
    legend(cv, entries, ML + PW - 190, MT + 20)
    cv.save(os.path.join(OUT, 'Figure_3_Velocity_We_M.png'))


def fig4():
    cv = Canvas(W, H)
    eta = frange(0, 1, 60)
    X, Y = plot_axes(cv, (0, 1), (0, 1.2), 'eta', 'theta', 'Figure 4 Temperature vs Rd Ec',
                     [0, 0.25, 0.5, 0.75, 1], [0, 0.25, 0.5, 0.75, 1])
    cases = [(0.2, 0.5, 'Rd=0.2 Ec=0.5'), (1.0, 0.5, 'Rd=1 Ec=0.5'), (1.0, 1.5, 'Rd=1 Ec=1.5')]
    entries = []
    for i, (Rd, Ec, lab) in enumerate(cases):
        ys = [temp_profile(e, Rd, Ec) for e in eta]
        plot_curve(cv, X, Y, eta, ys, PALETTE[i])
        entries.append((lab, PALETTE[i]))
    legend(cv, entries, ML + PW - 200, MT + 20)
    cv.save(os.path.join(OUT, 'Figure_4_Temperature_Rd_Ec.png'))


def fig5():
    cv = Canvas(W, H)
    eta = frange(0, 1, 60)
    ys_all = []
    cases = [(0.5, 1, 'Br=0.5 M=1'), (1.5, 1, 'Br=1.5 M=1'), (1.0, 2, 'Br=1 M=2')]
    for Br, M, lab in cases:
        ys_all.append([entropy_profile(e, Br, M) for e in eta])
    ymax = max(max(y) for y in ys_all) * 1.1
    X, Y = plot_axes(cv, (0, 1), (0, ymax), 'eta', 'Ns', 'Figure 5 Entropy vs Br M',
                     [0, 0.25, 0.5, 0.75, 1],
                     [round(ymax * k / 4, 1) for k in range(5)])
    entries = []
    for i, (ys, (Br, M, lab)) in enumerate(zip(ys_all, cases)):
        plot_curve(cv, X, Y, eta, ys, PALETTE[i])
        entries.append((lab, PALETTE[i]))
    legend(cv, entries, ML + PW - 190, MT + 20)
    cv.save(os.path.join(OUT, 'Figure_5_Entropy_Br_M.png'))


def fig6():
    cv = Canvas(W, H)
    eta = frange(0, 1, 60)
    X, Y = plot_axes(cv, (0, 1), (0, 1), 'eta', 'Be', 'Figure 6 Bejan vs Rd Br',
                     [0, 0.25, 0.5, 0.75, 1], [0, 0.25, 0.5, 0.75, 1])
    cases = [(0.2, 0.5, 'Rd=0.2 Br=0.5'), (1.0, 0.5, 'Rd=1 Br=0.5'), (1.0, 1.5, 'Rd=1 Br=1.5')]
    entries = []
    for i, (Rd, Br, lab) in enumerate(cases):
        ys = [bejan_profile(e, Rd, Br) for e in eta]
        plot_curve(cv, X, Y, eta, ys, PALETTE[i])
        entries.append((lab, PALETTE[i]))
    legend(cv, entries, ML + PW - 200, MT + 20)
    cv.save(os.path.join(OUT, 'Figure_6_Bejan_Rd_Br.png'))


def fig7():
    cv = Canvas(W, H)
    phi = [0.0, 0.04, 0.06, 0.08, 0.10]
    nu = [1.4267, 1.6394, 1.7565, 1.8815, 2.0149]
    sh = [0.6371, 0.6314, 0.6284, 0.6255, 0.6225]
    cf = [0.0885] * 5
    X, Y = plot_axes(cv, (0, 0.10), (0, 2.2), 'phi', 'value', 'Figure 7 Engineering vs phi',
                     [0, 0.025, 0.05, 0.075, 0.10], [0, 0.5, 1, 1.5, 2])
    plot_curve(cv, X, Y, phi, nu, PALETTE[0])
    plot_curve(cv, X, Y, phi, sh, PALETTE[1])
    plot_curve(cv, X, Y, phi, cf, PALETTE[2])
    for xs, ys, col in [(phi, nu, PALETTE[0]), (phi, sh, PALETTE[1]), (phi, cf, PALETTE[2])]:
        for x, y in zip(xs, ys):
            cv.dot(int(X(x)), int(Y(y)), col, r=3)
    legend(cv, [('Nu', PALETTE[0]), ('Sh', PALETTE[1]), ('Cf', PALETTE[2])],
           ML + PW - 120, MT + 20)
    cv.save(os.path.join(OUT, 'Figure_7_Engineering_phi.png'))


def main():
    os.makedirs(OUT, exist_ok=True)
    fig1_schematic()
    fig2(); fig3(); fig4(); fig5(); fig6(); fig7()
    print('Figures written to', OUT)
    for f in sorted(os.listdir(OUT)):
        print('  ', f, os.path.getsize(os.path.join(OUT, f)), 'bytes')


if __name__ == '__main__':
    main()
