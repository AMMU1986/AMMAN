#!/usr/bin/env python3
"""
Minimal anti-aliased vector-to-PNG renderer written in pure standard-library
Python (no PIL / matplotlib available in this sandbox).

Features
--------
* TrueType (glyf) font parsing with cmap format 4/12, simple and composite
  glyphs, used to render real Noto Sans text.
* Exact-area-coverage polygon rasteriser (port of the accumulation algorithm
  used by font-rs) giving smooth, anti-aliased edges for text and shapes.
* Helpers for rectangles, rounded rectangles, circles, thick lines, arrows,
  wrapped/centred text.
* PNG writer that embeds a pHYs chunk so the image is tagged at 300 dpi.
"""

import math
import struct
import zlib

FONT_PATH = '/usr/share/fonts/google-noto-vf/NotoSans[wght].ttf'
DPI = 300


# ---------------------------------------------------------------------------
# TrueType parsing
# ---------------------------------------------------------------------------
class TTFont:
    def __init__(self, path):
        with open(path, 'rb') as f:
            self.d = f.read()
        d = self.d
        num_tables = struct.unpack('>H', d[4:6])[0]
        self.tables = {}
        for i in range(num_tables):
            rec = d[12 + 16 * i: 28 + 16 * i]
            tag = rec[:4].decode('latin-1')
            _, off, length = struct.unpack('>III', rec[4:16])
            self.tables[tag] = (off, length)
        head = self.tables['head'][0]
        self.units_per_em = struct.unpack('>H', d[head + 18: head + 20])[0]
        self.loc_format = struct.unpack('>h', d[head + 50: head + 52])[0]
        maxp = self.tables['maxp'][0]
        self.num_glyphs = struct.unpack('>H', d[maxp + 4: maxp + 6])[0]
        hhea = self.tables['hhea'][0]
        self.ascender, self.descender = struct.unpack('>hh', d[hhea + 4: hhea + 8])
        self.num_hmetrics = struct.unpack('>H', d[hhea + 34: hhea + 36])[0]
        self._parse_loca()
        self._parse_hmtx()
        self._parse_cmap()
        self._cache = {}

    def _parse_loca(self):
        d = self.d
        off = self.tables['loca'][0]
        n = self.num_glyphs + 1
        if self.loc_format == 0:
            self.loca = [v * 2 for v in struct.unpack('>%dH' % n, d[off: off + 2 * n])]
        else:
            self.loca = list(struct.unpack('>%dI' % n, d[off: off + 4 * n]))

    def _parse_hmtx(self):
        d = self.d
        off = self.tables['hmtx'][0]
        self.adv = []
        for i in range(self.num_hmetrics):
            aw, _ = struct.unpack('>Hh', d[off + 4 * i: off + 4 * i + 4])
            self.adv.append(aw)
        last = self.adv[-1]
        self.adv += [last] * (self.num_glyphs - self.num_hmetrics)

    def _parse_cmap(self):
        d = self.d
        base = self.tables['cmap'][0]
        n = struct.unpack('>H', d[base + 2: base + 4])[0]
        subtables = {}
        for i in range(n):
            pid, eid, off = struct.unpack('>HHI', d[base + 4 + 8 * i: base + 12 + 8 * i])
            subtables[(pid, eid)] = base + off
        self.cmap = {}
        if (3, 10) in subtables:
            o = subtables[(3, 10)]
            ngroups = struct.unpack('>I', d[o + 12: o + 16])[0]
            for g in range(ngroups):
                s, e, gid = struct.unpack('>III', d[o + 16 + 12 * g: o + 28 + 12 * g])
                for c in range(s, e + 1):
                    self.cmap[c] = gid + (c - s)
            return
        o = subtables.get((3, 1)) or subtables.get((0, 3))
        seg2 = struct.unpack('>H', d[o + 6: o + 8])[0]
        segs = seg2 // 2
        ends = struct.unpack('>%dH' % segs, d[o + 14: o + 14 + seg2])
        starts = struct.unpack('>%dH' % segs, d[o + 16 + seg2: o + 16 + 2 * seg2])
        deltas = struct.unpack('>%dh' % segs, d[o + 16 + 2 * seg2: o + 16 + 3 * seg2])
        ro_off = o + 16 + 3 * seg2
        ranges = struct.unpack('>%dH' % segs, d[ro_off: ro_off + seg2])
        for i in range(segs):
            for c in range(starts[i], ends[i] + 1):
                if c == 0xFFFF:
                    continue
                if ranges[i] == 0:
                    gid = (c + deltas[i]) & 0xFFFF
                else:
                    addr = ro_off + 2 * i + ranges[i] + 2 * (c - starts[i])
                    gid = struct.unpack('>H', d[addr: addr + 2])[0]
                    if gid:
                        gid = (gid + deltas[i]) & 0xFFFF
                self.cmap[c] = gid

    def glyph_id(self, ch):
        return self.cmap.get(ord(ch), 0)

    def advance(self, gid):
        return self.adv[gid]

    # -- outlines -----------------------------------------------------------
    def contours(self, gid):
        """Return list of flattened contours [(x, y), ...] in font units."""
        if gid in self._cache:
            return self._cache[gid]
        raw = self._raw_contours(gid, 0)
        flat = [_flatten(c) for c in raw if len(c) >= 2]
        self._cache[gid] = flat
        return flat

    def _raw_contours(self, gid, depth):
        d = self.d
        glyf = self.tables['glyf'][0]
        start, end = self.loca[gid], self.loca[gid + 1]
        if end <= start or depth > 8:
            return []
        o = glyf + start
        ncont = struct.unpack('>h', d[o: o + 2])[0]
        p = o + 10
        if ncont >= 0:
            end_pts = struct.unpack('>%dH' % ncont, d[p: p + 2 * ncont])
            p += 2 * ncont
            ilen = struct.unpack('>H', d[p: p + 2])[0]
            p += 2 + ilen
            npts = end_pts[-1] + 1 if ncont else 0
            flags = []
            while len(flags) < npts:
                f = d[p]
                p += 1
                flags.append(f)
                if f & 8:
                    r = d[p]
                    p += 1
                    flags.extend([f] * r)
            flags = flags[:npts]
            xs = []
            v = 0
            for f in flags:
                if f & 2:
                    dx = d[p]
                    p += 1
                    v += dx if f & 16 else -dx
                elif not f & 16:
                    v += struct.unpack('>h', d[p: p + 2])[0]
                    p += 2
                xs.append(v)
            ys = []
            v = 0
            for f in flags:
                if f & 4:
                    dy = d[p]
                    p += 1
                    v += dy if f & 32 else -dy
                elif not f & 32:
                    v += struct.unpack('>h', d[p: p + 2])[0]
                    p += 2
                ys.append(v)
            out = []
            s = 0
            for e in end_pts:
                out.append([(xs[i], ys[i], flags[i] & 1) for i in range(s, e + 1)])
                s = e + 1
            return out
        # composite glyph
        out = []
        while True:
            flags, cgid = struct.unpack('>HH', d[p: p + 4])
            p += 4
            if flags & 1:
                a1, a2 = struct.unpack('>hh', d[p: p + 4])
                p += 4
            else:
                a1, a2 = struct.unpack('>bb', d[p: p + 2])
                p += 2
            xx, xy, yx, yy = 1.0, 0.0, 0.0, 1.0
            if flags & 8:
                xx = yy = struct.unpack('>h', d[p: p + 2])[0] / 16384.0
                p += 2
            elif flags & 0x40:
                xx, yy = [v / 16384.0 for v in struct.unpack('>hh', d[p: p + 4])]
                p += 4
            elif flags & 0x80:
                xx, xy, yx, yy = [v / 16384.0 for v in struct.unpack('>hhhh', d[p: p + 8])]
                p += 8
            dx, dy = (a1, a2) if flags & 2 else (0, 0)
            for c in self._raw_contours(cgid, depth + 1):
                out.append([(x * xx + y * yx + dx, x * xy + y * yy + dy, on) for x, y, on in c])
            if not flags & 0x20:
                break
        return out


def _flatten(pts, steps=6):
    """Flatten a TrueType quadratic contour into a polyline."""
    n = len(pts)
    # find an on-curve starting point
    start = None
    for i, pt in enumerate(pts):
        if pt[2]:
            start = i
            break
    if start is None:
        # all off-curve: start at midpoint of first two
        a, b = pts[0], pts[1]
        pts = [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 1)] + pts[1:] + [pts[0]]
        start = 0
        n = len(pts)
    seq = pts[start:] + pts[:start]
    out = [(seq[0][0], seq[0][1])]
    cur = (seq[0][0], seq[0][1])
    ctrl = None
    for i in range(1, n + 1):
        x, y, on = seq[i % n]
        if on:
            if ctrl is None:
                out.append((x, y))
            else:
                _quad(out, cur, ctrl, (x, y), steps)
                ctrl = None
            cur = (x, y)
        else:
            if ctrl is not None:
                mid = ((ctrl[0] + x) / 2, (ctrl[1] + y) / 2)
                _quad(out, cur, ctrl, mid, steps)
                cur = mid
            ctrl = (x, y)
    if ctrl is not None:
        _quad(out, cur, ctrl, out[0], steps)
    return out


def _quad(out, p0, p1, p2, steps):
    for k in range(1, steps + 1):
        t = k / steps
        mt = 1 - t
        out.append((mt * mt * p0[0] + 2 * mt * t * p1[0] + t * t * p2[0],
                    mt * mt * p0[1] + 2 * mt * t * p1[1] + t * t * p2[1]))


_FONT = None


def font():
    global _FONT
    if _FONT is None:
        _FONT = TTFont(FONT_PATH)
    return _FONT


# ---------------------------------------------------------------------------
# Canvas
# ---------------------------------------------------------------------------
def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w, self.h = w, h
        self.data = bytearray(bytes(bg) * (w * h))

    # -- primitive fills ----------------------------------------------------
    def fill_rect(self, x1, y1, x2, y2, color):
        x1, x2 = int(round(min(x1, x2))), int(round(max(x1, x2)))
        y1, y2 = int(round(min(y1, y2))), int(round(max(y1, y2)))
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(self.w, x2), min(self.h, y2)
        if x2 <= x1 or y2 <= y1:
            return
        row = bytes(color) * (x2 - x1)
        for y in range(y1, y2):
            i = (y * self.w + x1) * 3
            self.data[i: i + len(row)] = row

    def polygon(self, polys, color, alpha=1.0):
        """Fill one or more closed polylines (non-zero, anti-aliased)."""
        pts = [p for poly in polys for p in poly]
        if not pts:
            return
        minx = min(p[0] for p in pts)
        maxx = max(p[0] for p in pts)
        miny = min(p[1] for p in pts)
        maxy = max(p[1] for p in pts)
        ox = int(math.floor(minx)) - 1
        oy = int(math.floor(miny))
        bw = int(math.ceil(maxx)) - ox + 3
        bh = int(math.ceil(maxy)) - oy + 1
        if bw <= 0 or bh <= 0:
            return
        acc = [0.0] * (bw * bh + 2)
        for poly in polys:
            n = len(poly)
            for i in range(n):
                xa, ya = poly[i]
                xb, yb = poly[(i + 1) % n]
                _draw_line(acc, bw, bh, xa - ox, ya - oy, xb - ox, yb - oy)
        r, g, b = color
        data = self.data
        W, H = self.w, self.h
        for yy in range(bh):
            cy = oy + yy
            if cy < 0 or cy >= H:
                continue
            a = 0.0
            base = yy * bw
            rowi = cy * W
            for xx in range(bw):
                a += acc[base + xx]
                cov = a if a >= 0 else -a
                if cov < 0.003:
                    continue
                cx = ox + xx
                if cx < 0 or cx >= W:
                    continue
                if cov > 1.0:
                    cov = 1.0
                cov *= alpha
                k = (rowi + cx) * 3
                if cov >= 0.999:
                    data[k] = r
                    data[k + 1] = g
                    data[k + 2] = b
                else:
                    ic = 1.0 - cov
                    data[k] = int(data[k] * ic + r * cov + 0.5)
                    data[k + 1] = int(data[k + 1] * ic + g * cov + 0.5)
                    data[k + 2] = int(data[k + 2] * ic + b * cov + 0.5)

    # -- shapes -------------------------------------------------------------
    def rect(self, x1, y1, x2, y2, fill=None, outline=None, width=3):
        if fill:
            self.fill_rect(x1, y1, x2, y2, fill)
        if outline:
            self.fill_rect(x1, y1, x2, y1 + width, outline)
            self.fill_rect(x1, y2 - width, x2, y2, outline)
            self.fill_rect(x1, y1, x1 + width, y2, outline)
            self.fill_rect(x2 - width, y1, x2, y2, outline)

    def round_rect(self, x1, y1, x2, y2, r, fill=None, outline=None, width=3):
        def path(a1, b1, a2, b2, rr):
            rr = max(0.5, min(rr, (a2 - a1) / 2, (b2 - b1) / 2))
            pts = []
            for cx, cy, a0 in ((a2 - rr, b1 + rr, -90), (a2 - rr, b2 - rr, 0),
                               (a1 + rr, b2 - rr, 90), (a1 + rr, b1 + rr, 180)):
                for k in range(11):
                    ang = math.radians(a0 + 9 * k)
                    pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
            return pts
        if outline:
            outer = path(x1, y1, x2, y2, r)
            self.polygon([outer], outline)
            if fill:
                self.polygon([path(x1 + width, y1 + width, x2 - width, y2 - width,
                                   r - width)], fill)
            else:
                pass
        elif fill:
            self.polygon([path(x1, y1, x2, y2, r)], fill)

    def circle(self, cx, cy, rad, fill=None, outline=None, width=3, seg=96):
        def ring(rr):
            return [(cx + rr * math.cos(2 * math.pi * k / seg),
                     cy + rr * math.sin(2 * math.pi * k / seg)) for k in range(seg)]
        if outline:
            self.polygon([ring(rad)], outline)
            if fill:
                self.polygon([ring(rad - width)], fill)
        elif fill:
            self.polygon([ring(rad)], fill)

    def line(self, x1, y1, x2, y2, color, width=3):
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        if L == 0:
            return
        nx, ny = -dy / L * width / 2, dx / L * width / 2
        self.polygon([[(x1 + nx, y1 + ny), (x2 + nx, y2 + ny),
                       (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)]], color)

    def dashed_line(self, x1, y1, x2, y2, color, width=3, dash=18, gap=12):
        L = math.hypot(x2 - x1, y2 - y1)
        if L == 0:
            return
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        t = 0.0
        while t < L:
            e = min(L, t + dash)
            self.line(x1 + ux * t, y1 + uy * t, x1 + ux * e, y1 + uy * e, color, width)
            t = e + gap

    def arrow(self, x1, y1, x2, y2, color, width=5, head=26, head_w=None):
        head_w = head_w or head * 0.8
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        if L == 0:
            return
        ux, uy = dx / L, dy / L
        bx, by = x2 - ux * head, y2 - uy * head
        self.line(x1, y1, bx + ux * 2, by + uy * 2, color, width)
        nx, ny = -uy, ux
        self.polygon([[(x2, y2), (bx + nx * head_w / 2, by + ny * head_w / 2),
                       (bx - nx * head_w / 2, by - ny * head_w / 2)]], color)

    def block_arrow(self, x1, y, x2, h, color):
        """Horizontal chevron-style block arrow from x1 to x2 centred on y."""
        tip = h * 0.6
        self.polygon([[(x1, y - h / 2), (x2 - tip, y - h / 2), (x2, y),
                       (x2 - tip, y + h / 2), (x1, y + h / 2)]], color)

    # -- text ---------------------------------------------------------------
    def text_width(self, s, size, bold=False):
        f = font()
        sc = size / f.units_per_em
        w = sum(f.advance(f.glyph_id(c)) for c in s) * sc
        if bold:
            w += size * 0.03 * len(s) * 0.5
        return w

    def text(self, x, y, s, size, color=(0, 0, 0), bold=False, anchor='l',
             valign='top'):
        """Draw a single line. y is the top of the line box by default."""
        f = font()
        sc = size / f.units_per_em
        w = self.text_width(s, size, bold)
        if anchor == 'c':
            x -= w / 2
        elif anchor == 'r':
            x -= w
        asc = f.ascender * sc
        if valign == 'top':
            base = y + asc * 0.92
        elif valign == 'middle':
            base = y + size * 0.36
        else:
            base = y
        polys = []
        pen = x
        emb = size * 0.035 if bold else 0.0
        for ch in s:
            gid = f.glyph_id(ch)
            for c in f.contours(gid):
                poly = [(pen + px * sc, base - py * sc) for px, py in c]
                polys.append(poly)
                if bold:
                    polys.append([(px + emb, py) for px, py in poly])
                    polys.append([(px + emb / 2, py - emb / 3) for px, py in poly])
            pen += f.advance(gid) * sc + (size * 0.015 if bold else 0)
        if polys:
            self.polygon(polys, color)
        return w

    def wrap(self, s, size, max_w, bold=False):
        lines = []
        for para in s.split('\n'):
            words = para.split(' ')
            cur = ''
            for wd in words:
                trial = (cur + ' ' + wd).strip()
                if self.text_width(trial, size, bold) <= max_w or not cur:
                    cur = trial
                else:
                    lines.append(cur)
                    cur = wd
            lines.append(cur)
        return lines

    def text_block(self, x, y, s, size, max_w, color=(0, 0, 0), bold=False,
                   anchor='l', line_gap=1.28):
        lines = self.wrap(s, size, max_w, bold)
        for i, ln in enumerate(lines):
            self.text(x, y + i * size * line_gap, ln, size, color, bold, anchor)
        return len(lines) * size * line_gap

    def text_box_centered(self, cx, cy, s, size, max_w, color=(0, 0, 0),
                          bold=False, line_gap=1.28):
        lines = self.wrap(s, size, max_w, bold)
        total = len(lines) * size * line_gap
        y0 = cy - total / 2 + size * (line_gap - 1) / 2
        for i, ln in enumerate(lines):
            self.text(cx, y0 + i * size * line_gap, ln, size, color, bold, 'c')
        return total

    # -- output -------------------------------------------------------------
    def save(self, path, dpi=DPI):
        raw = bytearray()
        stride = self.w * 3
        for y in range(self.h):
            raw.append(0)
            raw.extend(self.data[y * stride:(y + 1) * stride])
        comp = zlib.compress(bytes(raw), 9)

        def chunk(t, body):
            c = t + body
            return struct.pack('>I', len(body)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
        ppm = int(round(dpi / 0.0254))
        with open(path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0)))
            f.write(chunk(b'pHYs', struct.pack('>IIB', ppm, ppm, 1)))
            f.write(chunk(b'IDAT', comp))
            f.write(chunk(b'IEND', b''))


def _draw_line(a, w, h, x0, y0, x1, y1):
    """Accumulate signed area coverage of one edge (font-rs algorithm)."""
    if abs(y0 - y1) <= 1e-9:
        return
    if y0 < y1:
        d_ir = 1.0
    else:
        d_ir = -1.0
        x0, y0, x1, y1 = x1, y1, x0, y0
    dxdy = (x1 - x0) / (y1 - y0)
    x = x0
    if y0 < 0:
        x -= y0 * dxdy
        y0s = 0
    else:
        y0s = int(y0)
    yend = min(h, int(math.ceil(y1)))
    for y in range(y0s, yend):
        ls = y * w
        dy = min(y + 1.0, y1) - max(float(y), y0)
        xnext = x + dxdy * dy
        d = dy * d_ir
        if x < xnext:
            xa, xb = x, xnext
        else:
            xa, xb = xnext, x
        xaf = math.floor(xa)
        xai = int(xaf)
        xbc = math.ceil(xb)
        xbi = int(xbc)
        if xbi <= xai + 1:
            xmf = 0.5 * (x + xnext) - xaf
            a[ls + xai] += d - d * xmf
            a[ls + xai + 1] += d * xmf
        else:
            s = 1.0 / (xb - xa)
            x0f = xa - xaf
            a0 = 0.5 * s * (1.0 - x0f) * (1.0 - x0f)
            x1f = xb - xbc + 1.0
            am = 0.5 * s * x1f * x1f
            a[ls + xai] += d * a0
            if xbi == xai + 2:
                a[ls + xai + 1] += d * (1.0 - a0 - am)
            else:
                a1 = s * (1.5 - x0f)
                a[ls + xai + 1] += d * (a1 - a0)
                ds = d * s
                for xi in range(xai + 2, xbi - 1):
                    a[ls + xi] += ds
                a2 = a1 + (xbi - xai - 3) * s
                a[ls + xbi - 1] += d * (1.0 - a2 - am)
            a[ls + xbi] += d * am
        x = xnext
