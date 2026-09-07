#!/usr/bin/env python3
"""
Render the Fortran FVM result (mid-plane slice CSV) to a PNG.
Pure Python standard library only.

Produces a two-panel figure:
  Left  : Lidinoid microstructure (solid vs void) on the slice
  Right : computed temperature field (jet colormap) with the solid
          walls outlined, plus a vertical colour bar.

Usage:
  python3 render_fvm_slice.py [csv_path] [png_path]
Defaults to the 95%-porosity slice.
"""

import csv
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    HERE, "lidinoid_output", "fvm_Tslice_por95.csv")
PNG_PATH = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
    HERE, "lidinoid_output", "fvm_temperature_field.png")

CELL = 6          # pixels per grid cell
MARGIN = 34
GAP = 46
CBAR_W = 26
CBAR_GAP = 20
TOP = 46          # header band

SOLID_RGB = (31, 78, 121)      # dark blue solid
VOID_RGB = (223, 232, 242)     # pale void


# ---------------------------------------------------------------- colormap
def jet(t):
    """Classic 'jet' colormap for t in [0,1] -> (r,g,b) 0..255."""
    t = 0.0 if t < 0 else (1.0 if t > 1 else t)

    def clamp(v):
        return int(255 * (0.0 if v < 0 else (1.0 if v > 1 else v)))
    r = clamp(1.5 - abs(4 * t - 3))
    g = clamp(1.5 - abs(4 * t - 2))
    b = clamp(1.5 - abs(4 * t - 1))
    return (r, g, b)


# ---------------------------------------------------------------- PNG writer
class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w, self.h = w, h
        self.px = bytearray(bg[0:1] * 0)  # placeholder
        self.px = bytearray([0]) * (w * h * 3)
        for i in range(w * h):
            self.px[i * 3] = bg[0]
            self.px[i * 3 + 1] = bg[1]
            self.px[i * 3 + 2] = bg[2]

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            p = (y * self.w + x) * 3
            self.px[p] = c[0]
            self.px[p + 1] = c[1]
            self.px[p + 2] = c[2]

    def rect(self, x0, y0, w, h, c):
        for yy in range(y0, y0 + h):
            for xx in range(x0, x0 + w):
                self.set(xx, yy, c)

    def frame(self, x0, y0, w, h, c):
        for xx in range(x0, x0 + w):
            self.set(xx, y0, c); self.set(xx, y0 + h - 1, c)
        for yy in range(y0, y0 + h):
            self.set(x0, yy, c); self.set(x0 + w - 1, yy, c)

    def save(self, path):
        raw = bytearray()
        row = self.w * 3
        for y in range(self.h):
            raw.append(0)
            raw.extend(self.px[y * row:(y + 1) * row])
        comp = zlib.compress(bytes(raw), 9)

        def be(n):
            return struct.pack(">I", n)

        def chunk(tag, data):
            return be(len(data)) + tag + data + struct.pack(
                ">I", zlib.crc32(tag + data) & 0xffffffff)

        with open(path, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")
            f.write(chunk(b"IHDR", be(self.w) + be(self.h) + bytes([8, 2, 0, 0, 0])))
            f.write(chunk(b"IDAT", comp))
            f.write(chunk(b"IEND", b""))


# ------------------------------------------------------- tiny 5x7 text font
FONT = {
    ' ': ["00000"] * 7,
    'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    'C': ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    'D': ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    'G': ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    'I': ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    'M': ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    'N': ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    'O': ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    'P': ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    'R': ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    'U': ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    'V': ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    'W': ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    'Y': ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    '%': ["11001", "11010", "00100", "01000", "10011", "00011", "00000"],
    '=': ["00000", "00000", "11111", "00000", "11111", "00000", "00000"],
    '.': ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    '0': ["01110", "10011", "10101", "10101", "11001", "10001", "01110"],
    '1': ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    '2': ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    '3': ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    '4': ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    '5': ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    '6': ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    '7': ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    '8': ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    '9': ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    ':': ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    '-': ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    '(': ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ')': ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    '/': ["00001", "00010", "00100", "00100", "01000", "10000", "10000"],
}


def text(cv, x, y, s, c, sc=2):
    cx = x
    for ch in s.upper():
        glyph = FONT.get(ch, FONT[' '])
        for r in range(7):
            for col in range(5):
                if glyph[r][col] == '1':
                    cv.rect(cx + col * sc, y + r * sc, sc, sc, c)
        cx += 6 * sc
    return cx


# ---------------------------------------------------------------- load CSV
def load(csv_path):
    n = 0
    rows = []
    with open(csv_path, newline="") as f:
        rd = csv.reader(f)
        next(rd)  # header
        for line in rd:
            i, j = int(line[0]), int(line[1])
            T = float(line[4]); phase = int(line[5])
            rows.append((i, j, T, phase))
            n = max(n, i, j)
    T = [[0.0] * n for _ in range(n)]
    P = [[0] * n for _ in range(n)]
    for (i, j, t, ph) in rows:
        T[j - 1][i - 1] = t
        P[j - 1][i - 1] = ph
    return n, T, P


def main():
    n, T, P = load(CSV_PATH)
    panel = n * CELL
    W = MARGIN + panel + GAP + panel + CBAR_GAP + CBAR_W + 60
    H = TOP + panel + MARGIN + 24
    cv = Canvas(W, H, bg=(250, 251, 253))

    ink = (30, 30, 30)
    # header
    text(cv, MARGIN, 14, "LIDINOID TPMS - FINITE VOLUME HEAT CONDUCTION", ink, sc=2)

    def is_edge(i, j):
        if P[j][i] != 1:
            return False
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ii, jj = i + di, j + dj
            if 0 <= ii < n and 0 <= jj < n and P[jj][ii] == 0:
                return True
        return False

    # y is flipped so row j=0 (y=0) sits at the bottom
    # ---- Panel A : microstructure ----
    ax0, ay0 = MARGIN, TOP
    for j in range(n):
        for i in range(n):
            c = SOLID_RGB if P[j][i] == 1 else VOID_RGB
            cv.rect(ax0 + i * CELL, ay0 + (n - 1 - j) * CELL, CELL, CELL, c)
    cv.frame(ax0 - 1, ay0 - 1, panel + 2, panel + 2, ink)
    text(cv, ax0, ay0 + panel + 8, "MICROSTRUCTURE (SOLID / VOID)", ink, sc=2)

    # ---- Panel B : temperature field ----
    bx0 = MARGIN + panel + GAP
    by0 = TOP
    for j in range(n):
        for i in range(n):
            col = jet(T[j][i])
            if is_edge(i, j):
                col = (10, 10, 10)          # outline solid walls in black
            cv.rect(bx0 + i * CELL, by0 + (n - 1 - j) * CELL, CELL, CELL, col)
    cv.frame(bx0 - 1, by0 - 1, panel + 2, panel + 2, ink)
    text(cv, bx0, by0 + panel + 8, "TEMPERATURE FIELD  (HOT LEFT - COLD RIGHT)", ink, sc=2)

    # ---- colour bar ----
    cbx = bx0 + panel + CBAR_GAP
    for r in range(panel):
        t = 1.0 - r / (panel - 1)
        cv.rect(cbx, by0 + r, CBAR_W, 1, jet(t))
    cv.frame(cbx - 1, by0 - 1, CBAR_W + 2, panel + 2, ink)
    text(cv, cbx - 2, by0 - 22, "T", ink, sc=2)
    text(cv, cbx + CBAR_W + 6, by0 - 2, "1.0", ink, sc=2)
    text(cv, cbx + CBAR_W + 6, by0 + panel - 14, "0.0", ink, sc=2)

    cv.save(PNG_PATH)
    print(f"grid = {n} x {n}")
    print(f"wrote {PNG_PATH}  ({os.path.getsize(PNG_PATH)} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
