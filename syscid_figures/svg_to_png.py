#!/usr/bin/env python3
"""
Minimal, dependency-free rasteriser for the restricted SVG primitive set used by
gen_syscid_figures.py (rect/rrect, line, circle, text).  Produces 8-bit RGB PNGs
using only the Python standard library (zlib + struct).

This is deliberately simple: it supports solid fills, opacity compositing onto a
white canvas, basic stroked lines/rects/circles, dashed strokes (approximated as
solid for raster), and a compact built-in 5x7 bitmap font scaled to the requested
size so that figure labels remain legible in the Word document.  It is NOT a
general SVG engine; it only needs to handle what we emit.
"""
import math
import re
import struct
import zlib

# ---------------------------------------------------------------------------
# 5x7 uppercase/lowercase/digit/punctuation bitmap font (column-major bits).
# Each glyph is 5 columns x 7 rows. Good enough for crisp small captions.
# ---------------------------------------------------------------------------
FONT5x7 = {
    ' ': [0,0,0,0,0], '!': [0,0,0x5f,0,0], '"': [0,7,0,7,0],
    '#': [0x14,0x7f,0x14,0x7f,0x14], '$': [0x24,0x2a,0x7f,0x2a,0x12],
    '%': [0x23,0x13,0x08,0x64,0x62], '&': [0x36,0x49,0x55,0x22,0x50],
    "'": [0,5,3,0,0], '(': [0,0x1c,0x22,0x41,0], ')': [0,0x41,0x22,0x1c,0],
    '*': [0x14,0x08,0x3e,0x08,0x14], '+': [0x08,0x08,0x3e,0x08,0x08],
    ',': [0,0x50,0x30,0,0], '-': [0x08,0x08,0x08,0x08,0x08],
    '.': [0,0x60,0x60,0,0], '/': [0x20,0x10,0x08,0x04,0x02],
    '0': [0x3e,0x51,0x49,0x45,0x3e], '1': [0,0x42,0x7f,0x40,0],
    '2': [0x42,0x61,0x51,0x49,0x46], '3': [0x21,0x41,0x45,0x4b,0x31],
    '4': [0x18,0x14,0x12,0x7f,0x10], '5': [0x27,0x45,0x45,0x45,0x39],
    '6': [0x3c,0x4a,0x49,0x49,0x30], '7': [0x01,0x71,0x09,0x05,0x03],
    '8': [0x36,0x49,0x49,0x49,0x36], '9': [0x06,0x49,0x49,0x29,0x1e],
    ':': [0,0x36,0x36,0,0], ';': [0,0x56,0x36,0,0],
    '<': [0x08,0x14,0x22,0x41,0], '=': [0x14,0x14,0x14,0x14,0x14],
    '>': [0,0x41,0x22,0x14,0x08], '?': [0x02,0x01,0x51,0x09,0x06],
    '@': [0x32,0x49,0x79,0x41,0x3e], 'A': [0x7e,0x11,0x11,0x11,0x7e],
    'B': [0x7f,0x49,0x49,0x49,0x36], 'C': [0x3e,0x41,0x41,0x41,0x22],
    'D': [0x7f,0x41,0x41,0x22,0x1c], 'E': [0x7f,0x49,0x49,0x49,0x41],
    'F': [0x7f,0x09,0x09,0x09,0x01], 'G': [0x3e,0x41,0x49,0x49,0x7a],
    'H': [0x7f,0x08,0x08,0x08,0x7f], 'I': [0,0x41,0x7f,0x41,0],
    'J': [0x20,0x40,0x41,0x3f,0x01], 'K': [0x7f,0x08,0x14,0x22,0x41],
    'L': [0x7f,0x40,0x40,0x40,0x40], 'M': [0x7f,0x02,0x0c,0x02,0x7f],
    'N': [0x7f,0x04,0x08,0x10,0x7f], 'O': [0x3e,0x41,0x41,0x41,0x3e],
    'P': [0x7f,0x09,0x09,0x09,0x06], 'Q': [0x3e,0x41,0x51,0x21,0x5e],
    'R': [0x7f,0x09,0x19,0x29,0x46], 'S': [0x46,0x49,0x49,0x49,0x31],
    'T': [0x01,0x01,0x7f,0x01,0x01], 'U': [0x3f,0x40,0x40,0x40,0x3f],
    'V': [0x1f,0x20,0x40,0x20,0x1f], 'W': [0x7f,0x20,0x18,0x20,0x7f],
    'X': [0x63,0x14,0x08,0x14,0x63], 'Y': [0x03,0x04,0x78,0x04,0x03],
    'Z': [0x61,0x51,0x49,0x45,0x43], '[': [0,0x7f,0x41,0x41,0],
    '\\': [0x02,0x04,0x08,0x10,0x20], ']': [0,0x41,0x41,0x7f,0],
    '^': [0x04,0x02,0x01,0x02,0x04], '_': [0x40,0x40,0x40,0x40,0x40],
    '`': [0,1,2,4,0], 'a': [0x20,0x54,0x54,0x54,0x78],
    'b': [0x7f,0x48,0x44,0x44,0x38], 'c': [0x38,0x44,0x44,0x44,0x20],
    'd': [0x38,0x44,0x44,0x48,0x7f], 'e': [0x38,0x54,0x54,0x54,0x18],
    'f': [0x08,0x7e,0x09,0x01,0x02], 'g': [0x0c,0x52,0x52,0x52,0x3e],
    'h': [0x7f,0x08,0x04,0x04,0x78], 'i': [0,0x44,0x7d,0x40,0],
    'j': [0x20,0x40,0x44,0x3d,0], 'k': [0x7f,0x10,0x28,0x44,0],
    'l': [0,0x41,0x7f,0x40,0], 'm': [0x7c,0x04,0x18,0x04,0x78],
    'n': [0x7c,0x08,0x04,0x04,0x78], 'o': [0x38,0x44,0x44,0x44,0x38],
    'p': [0x7c,0x14,0x14,0x14,0x08], 'q': [0x08,0x14,0x14,0x18,0x7c],
    'r': [0x7c,0x08,0x04,0x04,0x08], 's': [0x48,0x54,0x54,0x54,0x20],
    't': [0x04,0x3f,0x44,0x40,0x20], 'u': [0x3c,0x40,0x40,0x20,0x7c],
    'v': [0x1c,0x20,0x40,0x20,0x1c], 'w': [0x3c,0x40,0x30,0x40,0x3c],
    'x': [0x44,0x28,0x10,0x28,0x44], 'y': [0x0c,0x50,0x50,0x50,0x3c],
    'z': [0x44,0x64,0x54,0x4c,0x44], '{': [0x08,0x36,0x41,0,0],
    '|': [0,0,0x7f,0,0], '}': [0,0,0x41,0x36,0x08], '~': [0x02,0x01,0x02,0x04,0x02],
}
# unicode punctuation we emit -> ascii fallbacks
UNI = {'–':'-','—':'-','×':'x','·':'.','≥':'>=','✔':'Y','✖':'N','→':'->',
       'α':'a','β':'b','γ':'g','κ':'k','’':"'",'‘':"'",'“':'"','”':'"',
       'é':'e','í':'i','ó':'o','á':'a','ú':'u','ñ':'n','•':'-','\u2022':'-'}


def _ascii(s):
    return ''.join(UNI.get(c, c if 32 <= ord(c) < 127 else '?') for c in s)


class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def _idx(self, x, y):
        return (y * self.w + x) * 3

    def blend(self, x, y, rgb, a=1.0):
        if x < 0 or y < 0 or x >= self.w or y >= self.h:
            return
        i = self._idx(x, y)
        if a >= 1.0:
            self.px[i:i+3] = bytes(rgb)
        else:
            for k in range(3):
                self.px[i+k] = int(self.px[i+k] * (1 - a) + rgb[k] * a)

    def fill_rect(self, x, y, w, h, rgb, a=1.0):
        x0, y0 = int(round(x)), int(round(y))
        for yy in range(y0, int(round(y + h))):
            for xx in range(x0, int(round(x + w))):
                self.blend(xx, yy, rgb, a)

    def stroke_rect(self, x, y, w, h, rgb, sw=1):
        self.fill_rect(x, y, w, sw, rgb)
        self.fill_rect(x, y + h - sw, w, sw, rgb)
        self.fill_rect(x, y, sw, h, rgb)
        self.fill_rect(x + w - sw, y, sw, h, rgb)

    def line(self, x1, y1, x2, y2, rgb, sw=1):
        x1, y1, x2, y2 = map(float, (x1, y1, x2, y2))
        dx, dy = x2 - x1, y2 - y1
        n = int(max(abs(dx), abs(dy))) + 1
        for i in range(n + 1):
            t = i / n
            cx, cy = x1 + dx * t, y1 + dy * t
            r = sw / 2.0
            for oy in range(-int(r), int(r) + 1):
                for ox in range(-int(r), int(r) + 1):
                    self.blend(int(round(cx + ox)), int(round(cy + oy)), rgb)

    def circle(self, cx, cy, rad, rgb, a=1.0, fill=True, sw=2):
        for yy in range(int(cy - rad - 1), int(cy + rad + 2)):
            for xx in range(int(cx - rad - 1), int(cx + rad + 2)):
                d = math.hypot(xx - cx, yy - cy)
                if fill and d <= rad:
                    self.blend(xx, yy, rgb, a)
                elif not fill and abs(d - rad) <= sw / 2.0:
                    self.blend(xx, yy, rgb)

    def text(self, x, y, s, size, rgb, anchor='start'):
        s = _ascii(s)
        scale = max(1, int(round(size / 7.0)))
        gw = 6 * scale  # 5 cols + 1 space
        tw = gw * len(s)
        if anchor == 'middle':
            x -= tw / 2
        elif anchor == 'end':
            x -= tw
        baseline = y - 7 * scale  # y is roughly baseline; shift up to top
        for ci, ch in enumerate(s):
            cols = FONT5x7.get(ch, FONT5x7['?'])
            for col in range(5):
                bits = cols[col]
                for row in range(7):
                    if bits & (1 << row):
                        px = x + ci * gw + col * scale
                        py = baseline + row * scale
                        for sy in range(scale):
                            for sx in range(scale):
                                self.blend(int(px + sx), int(py + sy), rgb)

    def png_bytes(self):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)
            raw += self.px[y * self.w * 3:(y + 1) * self.w * 3]
        comp = zlib.compress(bytes(raw), 9)

        def chunk(typ, data):
            c = struct.pack('>I', len(data)) + typ + data
            return c + struct.pack('>I', zlib.crc32(typ + data) & 0xffffffff)
        sig = b'\x89PNG\r\n\x1a\n'
        ihdr = struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0)
        return sig + chunk(b'IHDR', ihdr) + chunk(b'IDAT', comp) + chunk(b'IEND', b'')


# ---------------------------------------------------------------------------
# Tiny SVG parser for our restricted output
# ---------------------------------------------------------------------------
def _hex(c):
    if not c or c == 'none':
        return None
    c = c.strip()
    if c.startswith('#'):
        c = c[1:]
        if len(c) == 3:
            c = ''.join(ch * 2 for ch in c)
        return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))
    named = {'white': (255, 255, 255), 'black': (0, 0, 0)}
    return named.get(c, (0, 0, 0))


def _attr(tag, name, default=None):
    m = re.search(name + r"='([^']*)'", tag)
    return m.group(1) if m else default


def render_svg(path, png_path, supersample=2):
    with open(path) as f:
        svg = f.read()
    m = re.search(r"<svg[^>]*width='(\d+)'[^>]*height='(\d+)'", svg)
    W, H = int(m.group(1)), int(m.group(2))
    ss = supersample
    cv = Canvas(W * ss, H * ss)

    # process elements in document order
    for tag in re.findall(r"<(?:rect|line|circle|text)[^>]*?/?>(?:[^<]*</text>)?", svg):
        if tag.startswith('<rect'):
            x = float(_attr(tag, 'x', 0)); y = float(_attr(tag, 'y', 0))
            w = float(_attr(tag, 'width', 0)); h = float(_attr(tag, 'height', 0))
            fill = _hex(_attr(tag, 'fill'))
            op = float(_attr(tag, 'fill-opacity', '1') or 1)
            if fill:
                cv.fill_rect(x*ss, y*ss, w*ss, h*ss, fill, op)
            stroke = _hex(_attr(tag, 'stroke'))
            if stroke:
                sw = float(_attr(tag, 'stroke-width', '1') or 1) * ss
                cv.stroke_rect(x*ss, y*ss, w*ss, h*ss, stroke, max(1, int(sw)))
        elif tag.startswith('<line'):
            x1 = float(_attr(tag, 'x1', 0)); y1 = float(_attr(tag, 'y1', 0))
            x2 = float(_attr(tag, 'x2', 0)); y2 = float(_attr(tag, 'y2', 0))
            stroke = _hex(_attr(tag, 'stroke')) or (90, 107, 123)
            sw = float(_attr(tag, 'stroke-width', '1') or 1) * ss
            cv.line(x1*ss, y1*ss, x2*ss, y2*ss, stroke, max(1, int(round(sw))))
        elif tag.startswith('<circle'):
            cx = float(_attr(tag, 'cx', 0)); cy = float(_attr(tag, 'cy', 0))
            r = float(_attr(tag, 'r', 0))
            fill = _hex(_attr(tag, 'fill'))
            op = float(_attr(tag, 'fill-opacity', '1') or 1)
            if fill:
                cv.circle(cx*ss, cy*ss, r*ss, fill, op, fill=True)
            stroke = _hex(_attr(tag, 'stroke'))
            if stroke:
                sw = float(_attr(tag, 'stroke-width', '1') or 1) * ss
                cv.circle(cx*ss, cy*ss, r*ss, stroke, fill=False, sw=max(1, int(sw)))
        elif tag.startswith('<text'):
            x = float(_attr(tag, 'x', 0)); y = float(_attr(tag, 'y', 0))
            size = float(_attr(tag, 'font-size', '12') or 12)
            fill = _hex(_attr(tag, 'fill')) or (27, 39, 51)
            anchor = _attr(tag, 'text-anchor', 'start')
            tm = re.search(r">([^<]*)</text>", tag)
            s = tm.group(1) if tm else ''
            s = (s.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>'))
            cv.text(x*ss, y*ss, s, size*ss, fill, anchor)

    # downsample (box filter) back to WxH for anti-aliasing
    out = Canvas(W, H)
    for y in range(H):
        for x in range(W):
            r = g = b = 0
            for dy in range(ss):
                for dx in range(ss):
                    i = ((y*ss+dy) * cv.w + (x*ss+dx)) * 3
                    r += cv.px[i]; g += cv.px[i+1]; b += cv.px[i+2]
            n = ss*ss
            out.px[(y*W+x)*3:(y*W+x)*3+3] = bytes((r//n, g//n, b//n))
    with open(png_path, 'wb') as f:
        f.write(out.png_bytes())
    return W, H


if __name__ == '__main__':
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    for n in range(1, 7):
        import glob
        matches = glob.glob(os.path.join(here, f'Figure_{n}_*.svg'))
        if matches:
            svg = matches[0]
            png = svg[:-4] + '.png'
            w, h = render_svg(svg, png)
            print('rendered', os.path.basename(png), f'{w}x{h}')
