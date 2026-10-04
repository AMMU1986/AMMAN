#!/usr/bin/env python3
"""
Dependency-free DXF -> PNG rasterizer (stdlib only).
Parses the generated DXF (LINE, LWPOLYLINE, CIRCLE, ARC, TEXT) and draws it
into an RGB raster, then encodes a PNG by hand with zlib.

No external libraries required (no PIL, no matplotlib, no internet).
"""
import math, struct, zlib

ACI_RGB = {
    1: (255, 0, 0), 2: (230, 190, 0), 3: (0, 176, 80), 4: (0, 176, 240),
    5: (0, 0, 255), 6: (255, 0, 255), 7: (0, 0, 0), 8: (128, 128, 128),
    9: (191, 191, 191), 11: (244, 169, 160), 14: (139, 0, 0),
    30: (255, 140, 0), 36: (107, 66, 38),
}
LAYER_ACI = {
    "PLATE_SDSS": 11, "PLATE_X70": 36, "WELD": 2, "TENSILE": 9,
    "MICROHARD": 4, "METALLO": 8, "IMPACT": 1, "OUTLINE": 7,
    "TEXT": 7, "LABELS": 1, "BORDER": 7, "0": 7,
}
FILL_LAYERS = {"PLATE_SDSS", "PLATE_X70", "TENSILE", "MICROHARD",
               "METALLO", "IMPACT"}

# ---------------- DXF parse ----------------
def parse(path):
    toks = open(path).read().splitlines()
    pairs = [(toks[i].strip(), toks[i + 1]) for i in range(0, len(toks) - 1, 2)]
    ents, cur, in_ent = [], None, False
    for c, v in pairs:
        if c == '2' and v == 'ENTITIES':
            in_ent = True
        elif c == '2' and v == 'ENDSEC':
            in_ent = False
        if in_ent and c == '0' and v in ('LINE', 'LWPOLYLINE', 'CIRCLE', 'ARC', 'TEXT'):
            if cur:
                ents.append(cur)
            cur = {'type': v, 'raw': {}}
        elif cur is not None and in_ent:
            cur['raw'].setdefault(c, []).append(v)
    if cur:
        ents.append(cur)
    return ents

def ent_color(e):
    layer = e['raw'].get('8', ['0'])[0]
    aci = LAYER_ACI.get(layer, 7)
    if '62' in e['raw']:
        try:
            aci = int(e['raw']['62'][0])
        except Exception:
            pass
    return ACI_RGB.get(aci, (0, 0, 0)), layer

# ---------------- Raster canvas ----------------
class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w, self.h = w, h
        self.px = bytearray()
        for _ in range(w * h):
            self.px += bytes(bg)

    def set(self, x, y, rgb):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(rgb)

    def line(self, x0, y0, x1, y1, rgb, width=1):
        x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        r = width // 2
        while True:
            for ox in range(-r, r + 1):
                for oy in range(-r, r + 1):
                    self.set(x0 + ox, y0 + oy, rgb)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x0 += sx
            if e2 <= dx:
                err += dx; y0 += sy

    def fill_poly(self, pts, rgb):
        if len(pts) < 3:
            return
        ys = [p[1] for p in pts]
        ymin, ymax = int(math.floor(min(ys))), int(math.ceil(max(ys)))
        for y in range(ymin, ymax + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x1, y1 = pts[i]
                x2, y2 = pts[(i + 1) % n]
                if (y1 <= y < y2) or (y2 <= y < y1):
                    t = (y - y1) / (y2 - y1)
                    xs.append(x1 + t * (x2 - x1))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                for x in range(int(math.floor(xs[k])), int(math.ceil(xs[k + 1])) + 1):
                    self.set(x, y, rgb)

    def write_png(self, path):
        raw = bytearray()
        stride = self.w * 3
        for y in range(self.h):
            raw.append(0)  # filter type 0
            raw += self.px[y * stride:(y + 1) * stride]
        def chunk(typ, data):
            c = struct.pack(">I", len(data)) + typ + data
            return c + struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)
        png = b"\x89PNG\r\n\x1a\n"
        png += chunk(b"IHDR", struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0))
        png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        png += chunk(b"IEND", b"")
        open(path, "wb").write(png)

# ---------------- tiny 5x7 vector font for labels ----------------
# Minimal stroke font: each char -> list of (x0,y0,x1,y1) in a 5x7 grid.
FONT = {
    ' ': [], '-': [(0,3,4,3)], '/': [(0,6,4,0)], '.': [(2,6,2,6)],
    '|': [(2,0,2,6)], '(': [(3,0,1,3),(1,3,3,6)], ')': [(1,0,3,3),(3,3,1,6)],
    '0': [(0,0,4,0),(4,0,4,6),(4,6,0,6),(0,6,0,0),(0,6,4,0)],
    '1': [(2,0,2,6),(1,1,2,0),(1,6,3,6)],
    '2': [(0,1,2,0),(2,0,4,1),(4,1,0,6),(0,6,4,6)],
    '3': [(0,0,4,0),(4,0,2,3),(2,3,4,4),(4,4,2,6),(2,6,0,5)],
    '4': [(3,0,0,4),(0,4,4,4),(3,0,3,6)],
    '5': [(4,0,0,0),(0,0,0,3),(0,3,3,3),(3,3,4,4),(4,4,2,6),(2,6,0,5)],
    '6': [(4,0,1,2),(1,2,0,4),(0,4,2,6),(2,6,4,4),(4,4,2,3),(2,3,0,4)],
    '7': [(0,0,4,0),(4,0,1,6)],
    'A': [(0,6,2,0),(2,0,4,6),(1,4,3,4)],
    'C': [(4,1,2,0),(2,0,0,3),(0,3,2,6),(2,6,4,5)],
    'D': [(0,0,0,6),(0,0,3,1),(3,1,4,3),(4,3,3,5),(3,5,0,6)],
    'E': [(4,0,0,0),(0,0,0,6),(0,6,4,6),(0,3,3,3)],
    'G': [(4,1,2,0),(2,0,0,3),(0,3,2,6),(2,6,4,5),(4,5,4,3),(4,3,2,3)],
    'I': [(1,0,3,0),(2,0,2,6),(1,6,3,6)],
    'J': [(4,0,4,5),(4,5,2,6),(2,6,0,4)],
    'L': [(0,0,0,6),(0,6,4,6)],
    'M': [(0,6,0,0),(0,0,2,3),(2,3,4,0),(4,0,4,6)],
    'N': [(0,6,0,0),(0,0,4,6),(4,6,4,0)],
    'O': [(0,0,4,0),(4,0,4,6),(4,6,0,6),(0,6,0,0)],
    'P': [(0,6,0,0),(0,0,4,0),(4,0,4,3),(4,3,0,3)],
    'R': [(0,6,0,0),(0,0,4,0),(4,0,4,3),(4,3,0,3),(1,3,4,6)],
    'S': [(4,1,1,0),(1,0,0,2),(0,2,4,4),(4,4,3,6),(3,6,0,5)],
    'T': [(0,0,4,0),(2,0,2,6)],
    'U': [(0,0,0,5),(0,5,2,6),(2,6,4,5),(4,5,4,0)],
    'W': [(0,0,1,6),(1,6,2,3),(2,3,3,6),(3,6,4,0)],
    'X': [(0,0,4,6),(4,0,0,6)],
    'Y': [(0,0,2,3),(4,0,2,3),(2,3,2,6)],
    'a': [(0,2,4,2),(4,2,4,6),(4,6,0,6),(0,6,0,4),(0,4,4,4)],
    'c': [(4,3,1,2),(1,2,1,5),(1,5,4,5)],
    'd': [(4,0,4,6),(4,6,1,6),(1,6,0,4),(0,4,1,2),(1,2,4,3)],
    'e': [(0,4,4,4),(4,4,4,2),(4,2,1,2),(1,2,0,4),(0,4,1,6),(1,6,4,6)],
    'g': [(4,2,1,2),(1,2,0,4),(0,4,4,4),(4,2,4,7),(4,7,1,7)],
    'h': [(0,0,0,6),(0,3,3,2),(3,2,4,4),(4,4,4,6)],
    'i': [(2,2,2,6),(2,0,2,0)],
    'l': [(2,0,2,6)],
    'm': [(0,6,0,2),(0,2,2,2),(2,2,2,6),(2,2,4,2),(4,2,4,6)],
    'n': [(0,6,0,2),(0,2,3,2),(3,2,4,4),(4,4,4,6)],
    'o': [(1,2,4,2),(4,2,4,6),(4,6,1,6),(1,6,1,2)],
    'p': [(0,2,0,7),(0,2,4,2),(4,2,4,5),(4,5,0,5)],
    'r': [(0,6,0,2),(0,2,4,2)],
    's': [(4,3,1,2),(1,2,4,4),(4,4,1,6)],
    't': [(2,0,2,6),(0,2,4,2)],
    'y': [(0,2,2,5),(4,2,0,7)],
}

def draw_text(cv, x, y, s, h, rgb, rot=0.0):
    cw = h * 0.62
    gap = h * 0.25
    rad = math.radians(rot)
    cosr, sinr = math.cos(rad), math.sin(rad)
    penx = 0.0
    for ch in s:
        strokes = FONT.get(ch, FONT.get(ch.upper(), None))
        if strokes is None:
            penx += cw + gap
            continue
        for (gx0, gy0, gx1, gy1) in strokes:
            lx0 = penx + gx0 / 4.0 * cw
            lx1 = penx + gx1 / 4.0 * cw
            ly0 = (6 - gy0) / 6.0 * h
            ly1 = (6 - gy1) / 6.0 * h
            # rotate about glyph origin, then translate to (x,y) in screen coords
            rx0 = x + lx0 * cosr - ly0 * sinr
            ry0 = y - (lx0 * sinr + ly0 * cosr)
            rx1 = x + lx1 * cosr - ly1 * sinr
            ry1 = y - (lx1 * sinr + ly1 * cosr)
            cv.line(rx0, ry0, rx1, ry1, rgb, 1)
        penx += cw + gap

# ---------------- main render ----------------
def main():
    ents = parse("Specimen_Extraction_Layout.dxf")
    scale = 2.4
    pad = 16
    maxx, maxy = 420.0, 320.0
    W = int(maxx * scale + 2 * pad)
    H = int(maxy * scale + 2 * pad)
    cv = Canvas(W, H)

    def X(x): return x * scale + pad
    def Y(y): return (maxy - y) * scale + pad  # flip Y

    # Pass 1: filled polygons (plate + specimen blanks) first
    for e in ents:
        if e['type'] != 'LWPOLYLINE':
            continue
        rgb, layer = ent_color(e)
        if layer not in FILL_LAYERS:
            continue
        xs = [float(v) for v in e['raw'].get('10', [])]
        ys = [float(v) for v in e['raw'].get('20', [])]
        pts = [(X(x), Y(y)) for x, y in zip(xs, ys)]
        cv.fill_poly(pts, rgb)

    # Pass 2: strokes (outlines, lines, text)
    for e in ents:
        rgb, layer = ent_color(e)
        r = e['raw']
        if e['type'] == 'LINE':
            cv.line(X(float(r['10'][0])), Y(float(r['20'][0])),
                    X(float(r['11'][0])), Y(float(r['21'][0])), rgb, 1)
        elif e['type'] == 'LWPOLYLINE':
            xs = [float(v) for v in r.get('10', [])]
            ys = [float(v) for v in r.get('20', [])]
            closed = r.get('70', ['0'])[0] == '1'
            pts = list(zip(xs, ys))
            n = len(pts)
            lim = n if closed else n - 1
            lw = 2 if layer in ("OUTLINE", "BORDER") else 1
            for i in range(lim):
                x1, y1 = pts[i]
                x2, y2 = pts[(i + 1) % n]
                cv.line(X(x1), Y(y1), X(x2), Y(y2), rgb, lw)
        elif e['type'] == 'CIRCLE':
            cx, cy, rad = float(r['10'][0]), float(r['20'][0]), float(r['40'][0])
            steps = 48
            for i in range(steps):
                a0 = 2 * math.pi * i / steps
                a1 = 2 * math.pi * (i + 1) / steps
                cv.line(X(cx + rad * math.cos(a0)), Y(cy + rad * math.sin(a0)),
                        X(cx + rad * math.cos(a1)), Y(cy + rad * math.sin(a1)), rgb, 1)
        elif e['type'] == 'TEXT':
            x, y, h = float(r['10'][0]), float(r['20'][0]), float(r['40'][0])
            s = r['1'][0]
            rot = float(r.get('50', ['0'])[0])
            draw_text(cv, X(x), Y(y), s, h * scale, rgb, rot)

    cv.write_png("Specimen_Extraction_Layout_render.png")
    print(f"Wrote Specimen_Extraction_Layout_render.png ({W}x{H})")

if __name__ == "__main__":
    main()
