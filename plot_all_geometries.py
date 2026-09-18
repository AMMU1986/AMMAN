#!/usr/bin/env python3
"""
Compose the eight PCM-capsule arrangements (geom_a.dat ... geom_h.dat)
produced by pcm_geometry_all.f90 into a single 2x4 montage PNG that mimics
Fig. 14 of Athawale et al. (2021):

    top row    (a) 3x3  (b) 4x4  (c) 5x5  (d) 6x6   -- straight
    bottom row (e) 3x3  (f) 4x4  (g) 5x5  (h) 6x6   -- alternate

Capsules (phi=1) are drawn red on a blue HTF background, matching the
figure.  Uses only the Python standard library (zlib, struct) plus a tiny
hand-coded 5x7 bitmap font for the (a)-(h) labels.
"""
import struct
import zlib

CASES  = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
SCALE  = 2      # pixels per coarse cell
GAP    = 16     # gap between panels (px)
LABELH = 30     # label band height below each panel (px)
BORDER = 2      # panel border thickness (px)
OUT    = "pcm_geometry_all.png"

# ------------------------------------------------------------------ font ----
# 5x7 glyphs, top row first, '1' = ink.
FONT = {
    '(': ["00100","01000","01000","01000","01000","01000","00100"],
    ')': ["00100","00010","00010","00010","00010","00010","00100"],
    'a': ["00000","00000","01110","00001","01111","10001","01111"],
    'b': ["10000","10000","10000","11110","10001","10001","11110"],
    'c': ["00000","00000","01110","10000","10000","10001","01110"],
    'd': ["00001","00001","00001","01111","10001","10001","01111"],
    'e': ["00000","00000","01110","10001","11111","10000","01110"],
    'f': ["00110","01001","01000","11100","01000","01000","01000"],
    'g': ["00000","01111","10001","10001","01111","00001","01110"],
    'h': ["10000","10000","10000","11110","10001","10001","10001"],
    ' ': ["00000","00000","00000","00000","00000","00000","00000"],
}


def read_field(path):
    xs, ys, vals = [], [], []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            p = s.split()
            if len(p) < 3:
                continue
            xs.append(float(p[0])); ys.append(float(p[1])); vals.append(float(p[2]))
    ux = sorted(set(xs)); uy = sorted(set(ys))
    nx, ny = len(ux), len(uy)
    xi = {v: k for k, v in enumerate(ux)}
    yi = {v: k for k, v in enumerate(uy)}
    phi = [[0.0]*nx for _ in range(ny)]
    for x, y, v in zip(xs, ys, vals):
        phi[yi[y]][xi[x]] = v
    return nx, ny, phi


def colormap(v):
    """phi -> (r,g,b): red capsule (phi=1), blue HTF (phi=0), dark interface."""
    v = max(0.0, min(1.0, v))
    if 0.15 < v < 0.85:
        return (20, 20, 25)          # interface outline
    if v >= 0.85:
        return (220, 30, 25)          # PCM capsule (red)
    return (25, 45, 210)              # HTF (blue)


class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w, self.h = w, h
        self.buf = bytearray(bytes(bg) * (w * h))

    def set(self, x, y, rgb):
        if 0 <= x < self.w and 0 <= y < self.h:
            o = (y * self.w + x) * 3
            self.buf[o:o+3] = bytes(rgb)

    def rect(self, x0, y0, x1, y1, rgb):
        for y in range(y0, y1):
            for x in range(x0, x1):
                self.set(x, y, rgb)

    def frame(self, x0, y0, x1, y1, rgb, t):
        self.rect(x0, y0, x1, y0+t, rgb)
        self.rect(x0, y1-t, x1, y1, rgb)
        self.rect(x0, y0, x0+t, y1, rgb)
        self.rect(x1-t, y0, x1, y1, rgb)

    def text(self, x, y, s, rgb, px=3):
        cx = x
        for ch in s:
            g = FONT.get(ch, FONT[' '])
            for r in range(7):
                for c in range(5):
                    if g[r][c] == '1':
                        self.rect(cx + c*px, y + r*px,
                                  cx + (c+1)*px, y + (r+1)*px, rgb)
            cx += 6 * px          # advance (5 + 1 spacing)

    def write_png(self, path):
        def chunk(tag, data):
            c = tag + data
            return (struct.pack(">I", len(data)) + c +
                    struct.pack(">I", zlib.crc32(c) & 0xffffffff))
        raw = bytearray()
        stride = self.w * 3
        for y in range(self.h):
            raw.append(0)
            raw.extend(self.buf[y*stride:(y+1)*stride])
        with open(path, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")
            f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)))
            f.write(chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
            f.write(chunk(b"IEND", b""))


def main():
    fields = [read_field(f"geom_{c}.dat") for c in CASES]
    nx, ny, _ = fields[0]
    pw, ph = nx * SCALE, ny * SCALE          # panel pixel size

    cols, rows = 4, 2
    W = GAP + cols * (pw + GAP)
    H = GAP + rows * (ph + LABELH + GAP)
    cv = Canvas(W, H)

    for idx, (case, (fnx, fny, phi)) in enumerate(zip(CASES, fields)):
        r = idx // cols
        c = idx % cols
        x0 = GAP + c * (pw + GAP)
        y0 = GAP + r * (ph + LABELH + GAP)
        # paint field (image top = high y)
        for j in range(fny):
            yy = y0 + (fny - 1 - j) * SCALE
            for i in range(fnx):
                rgb = colormap(phi[j][i])
                cv.rect(x0 + i*SCALE, yy, x0 + (i+1)*SCALE, yy + SCALE, rgb)
        cv.frame(x0 - BORDER, y0 - BORDER, x0 + pw + BORDER, y0 + ph + BORDER,
                 (0, 0, 0), BORDER)
        # label "(x)" centred below the panel
        label = f"({case})"
        lw = len(label) * 6 * 3
        cv.text(x0 + (pw - lw)//2, y0 + ph + 8, label, (0, 0, 0), px=3)

    cv.write_png(OUT)
    print(f"Wrote {OUT}  ({W} x {H} px)")


if __name__ == "__main__":
    main()
