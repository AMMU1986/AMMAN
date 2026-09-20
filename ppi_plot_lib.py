#!/usr/bin/env python3
"""
Pure-standard-library plotting/drawing helper for the PPI manuscript figures.

No third-party dependencies (matplotlib/numpy/PIL are unavailable in the
sandbox). Provides:
  - Canvas: an RGB raster with rectangle/line/text primitives
  - a 5x7 bitmap font (upper/lower case, digits, punctuation)
  - viridis-like colormap for the heatmap
  - PNG writer (zlib + struct)
"""

import struct
import zlib

# ----------------------------------------------------------------------------
# 5x7 bitmap font.  Each glyph is 7 rows of 5-character strings ('#' = pixel).
# ----------------------------------------------------------------------------
_FONT = {
    ' ': ["     ", "     ", "     ", "     ", "     ", "     ", "     "],
    'A': [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    'B': ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    'C': [" ####", "#    ", "#    ", "#    ", "#    ", "#    ", " ####"],
    'D': ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    'E': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    'F': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    'G': [" ####", "#    ", "#    ", "#  ##", "#   #", "#   #", " ####"],
    'H': ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    'I': ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "#####"],
    'J': ["#####", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "],
    'K': ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    'L': ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    'M': ["#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"],
    'N': ["#   #", "##  #", "# # #", "# # #", "#  ##", "#   #", "#   #"],
    'O': [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    'P': ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    'Q': [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    'R': ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    'S': [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    'T': ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    'U': ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    'V': ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    'W': ["#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"],
    'X': ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    'Y': ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    'Z': ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    'a': ["     ", "     ", " ### ", "    #", " ####", "#   #", " ####"],
    'b': ["#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#### "],
    'c': ["     ", "     ", " ####", "#    ", "#    ", "#    ", " ####"],
    'd': ["    #", "    #", " ####", "#   #", "#   #", "#   #", " ####"],
    'e': ["     ", "     ", " ### ", "#   #", "#####", "#    ", " ####"],
    'f': ["  ## ", " #   ", "####", " #   ", " #   ", " #   ", " #   "],
    'g': ["     ", " ####", "#   #", "#   #", " ####", "    #", " ### "],
    'h': ["#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#   #"],
    'i': ["  #  ", "     ", " ##  ", "  #  ", "  #  ", "  #  ", " ### "],
    'j': ["   # ", "     ", "  ## ", "   # ", "   # ", "#  # ", " ##  "],
    'k': ["#    ", "#    ", "#  # ", "# #  ", "##   ", "# #  ", "#  # "],
    'l': [" ##  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    'm': ["     ", "     ", "## # ", "# # #", "# # #", "#   #", "#   #"],
    'n': ["     ", "     ", "#### ", "#   #", "#   #", "#   #", "#   #"],
    'o': ["     ", "     ", " ### ", "#   #", "#   #", "#   #", " ### "],
    'p': ["     ", "     ", "#### ", "#   #", "#### ", "#    ", "#    "],
    'q': ["     ", "     ", " ####", "#   #", " ####", "    #", "    #"],
    'r': ["     ", "     ", "# ## ", "##   ", "#    ", "#    ", "#    "],
    's': ["     ", "     ", " ####", "#    ", " ### ", "    #", "#### "],
    't': [" #   ", " #   ", "####", " #   ", " #   ", " #  #", "  ## "],
    'u': ["     ", "     ", "#   #", "#   #", "#   #", "#   #", " ####"],
    'v': ["     ", "     ", "#   #", "#   #", "#   #", " # # ", "  #  "],
    'w': ["     ", "     ", "#   #", "#   #", "# # #", "# # #", " # # "],
    'x': ["     ", "     ", "#   #", " # # ", "  #  ", " # # ", "#   #"],
    'y': ["     ", "     ", "#   #", "#   #", " ####", "    #", " ### "],
    'z': ["     ", "     ", "#####", "   # ", "  #  ", " #   ", "#####"],
    '0': [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    '1': ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    '2': [" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"],
    '3': ["#####", "   # ", "  #  ", "   # ", "    #", "#   #", " ### "],
    '4': ["   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "],
    '5': ["#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "],
    '6': ["  ## ", " #   ", "#    ", "#### ", "#   #", "#   #", " ### "],
    '7': ["#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "],
    '8': [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    '9': [" ### ", "#   #", "#   #", " ####", "    #", "   # ", " ##  "],
    '.': ["     ", "     ", "     ", "     ", "     ", " ##  ", " ##  "],
    ',': ["     ", "     ", "     ", "     ", " ##  ", " ##  ", "#    "],
    ':': ["     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "     "],
    ';': ["     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "#    "],
    '(': ["   # ", "  #  ", " #   ", " #   ", " #   ", "  #  ", "   # "],
    ')': [" #   ", "  #  ", "   # ", "   # ", "   # ", "  #  ", " #   "],
    '[': [" ### ", " #   ", " #   ", " #   ", " #   ", " #   ", " ### "],
    ']': [" ### ", "   # ", "   # ", "   # ", "   # ", "   # ", " ### "],
    '/': ["    #", "    #", "   # ", "  #  ", " #   ", "#    ", "#    "],
    '%': ["##  #", "## # ", "   # ", "  #  ", " #   ", " # ##", "#  ##"],
    '-': ["     ", "     ", "     ", "#####", "     ", "     ", "     "],
    '+': ["     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "],
    '=': ["     ", "     ", "#####", "     ", "#####", "     ", "     "],
    '<': ["   # ", "  #  ", " #   ", "#    ", " #   ", "  #  ", "   # "],
    '>': [" #   ", "  #  ", "   # ", "    #", "   # ", "  #  ", " #   "],
    '_': ["     ", "     ", "     ", "     ", "     ", "     ", "#####"],
    '#': [" # # ", " # # ", "#####", " # # ", "#####", " # # ", " # # "],
    '&': [" ##  ", "#  # ", "#  # ", " ##  ", "#  # ", "#   #", " ## #"],
    "'": ["  #  ", "  #  ", " #   ", "     ", "     ", "     ", "     "],
    '*': ["     ", "# # #", " ### ", "#####", " ### ", "# # #", "     "],
    '?': [" ### ", "#   #", "   # ", "  #  ", "  #  ", "     ", "  #  "],
    '!': ["  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "],
    # unicode approximations
    '≥': ["   # ", "  #  ", " #   ", "  #  ", "   # ", "     ", "#####"],
    '≤': [" #   ", "  #  ", "   # ", "  #  ", " #   ", "     ", "#####"],
    '±': ["  #  ", "  #  ", "#####", "  #  ", "  #  ", "     ", "#####"],
    '→': ["     ", "   # ", "    #", "#####", "    #", "   # ", "     "],
    '×': ["     ", "     ", "#   #", " # # ", "  #  ", " # # ", "#   #"],
    '†': ["  #  ", "  #  ", "#####", "  #  ", "  #  ", "  #  ", "  #  "],
}

_GLYPH_W = 5
_GLYPH_H = 7


def _glyph(ch):
    return _FONT.get(ch, _FONT['?'])


def text_width(s, scale=2, spacing=1):
    """Pixel width of a rendered string."""
    return len(s) * (_GLYPH_W * scale + spacing * scale) if s else 0


class Canvas:
    """A simple RGB raster canvas."""

    def __init__(self, width, height, bg=(255, 255, 255)):
        self.w = width
        self.h = height
        self.px = bytearray(bytes(bg) * (width * height))

    def _set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def fill_rect(self, x0, y0, x1, y1, color):
        x0, x1 = int(min(x0, x1)), int(max(x0, x1))
        y0, y1 = int(min(y0, y1)), int(max(y0, y1))
        for y in range(y0, y1):
            for x in range(x0, x1):
                self._set(x, y, color)

    def rect_outline(self, x0, y0, x1, y1, color, thickness=1):
        for t in range(thickness):
            self.hline(x0, x1, y0 + t, color)
            self.hline(x0, x1, y1 - 1 - t, color)
            self.vline(x0 + t, y0, y1, color)
            self.vline(x1 - 1 - t, y0, y1, color)

    def hline(self, x0, x1, y, color):
        for x in range(int(min(x0, x1)), int(max(x0, x1))):
            self._set(x, int(y), color)

    def vline(self, x, y0, y1, color):
        for y in range(int(min(y0, y1)), int(max(y0, y1))):
            self._set(int(x), y, color)

    def line(self, x0, y0, x1, y1, color, thickness=1):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for tx in range(thickness):
                for ty in range(thickness):
                    self._set(x0 + tx, y0 + ty, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def fill_circle(self, cx, cy, r, color):
        cx, cy, r = int(cx), int(cy), int(r)
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    self._set(x, y, color)

    def vtext(self, x, y, s, color=(0, 0, 0), scale=2, spacing=2):
        """Draw text stacked vertically (letters top-to-bottom)."""
        cy = int(y)
        step = _GLYPH_H * scale + spacing * scale
        for ch in s:
            self.text_center(x, cy, ch, color, scale, spacing=1)
            cy += step
        return cy

    def text(self, x, y, s, color=(0, 0, 0), scale=2, spacing=1):
        """Draw text with top-left origin at (x, y)."""
        cx = int(x)
        step = _GLYPH_W * scale + spacing * scale
        for ch in s:
            g = _glyph(ch)
            for ry in range(_GLYPH_H):
                row = g[ry]
                for rx in range(_GLYPH_W):
                    if rx < len(row) and row[rx] == '#':
                        px0 = cx + rx * scale
                        py0 = int(y) + ry * scale
                        for sxp in range(scale):
                            for syp in range(scale):
                                self._set(px0 + sxp, py0 + syp, color)
            cx += step
        return cx

    def text_center(self, cx, y, s, color=(0, 0, 0), scale=2, spacing=1):
        w = text_width(s, scale, spacing)
        return self.text(cx - w // 2, y, s, color, scale, spacing)

    def text_right(self, xr, y, s, color=(0, 0, 0), scale=2, spacing=1):
        w = text_width(s, scale, spacing)
        return self.text(xr - w, y, s, color, scale, spacing)

    def save_png(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)  # filter: none
            start = y * self.w * 3
            raw.extend(self.px[start:start + self.w * 3])
        compressed = zlib.compress(bytes(raw), 9)

        def chunk(ctype, data):
            c = ctype + data
            return (struct.pack('>I', len(data)) + c +
                    struct.pack('>I', zlib.crc32(c) & 0xffffffff))

        png = b'\x89PNG\r\n\x1a\n'
        png += chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0))
        png += chunk(b'IDAT', compressed)
        png += chunk(b'IEND', b'')
        with open(path, 'wb') as f:
            f.write(png)


# ----------------------------------------------------------------------------
# viridis-like colormap (sampled control points, linearly interpolated)
# ----------------------------------------------------------------------------
_VIRIDIS = [
    (68, 1, 84), (72, 40, 120), (62, 74, 137), (49, 104, 142),
    (38, 130, 142), (31, 158, 137), (53, 183, 121), (109, 205, 89),
    (180, 222, 44), (253, 231, 37),
]


def viridis(t):
    """Map t in [0,1] to an (r,g,b) viridis colour."""
    if t <= 0:
        return _VIRIDIS[0]
    if t >= 1:
        return _VIRIDIS[-1]
    n = len(_VIRIDIS) - 1
    pos = t * n
    i = int(pos)
    frac = pos - i
    a = _VIRIDIS[i]
    b = _VIRIDIS[min(i + 1, n)]
    return tuple(int(a[k] + (b[k] - a[k]) * frac) for k in range(3))


def text_color_for(bg):
    """Choose black/white text for contrast against bg."""
    lum = 0.299 * bg[0] + 0.587 * bg[1] + 0.114 * bg[2]
    return (0, 0, 0) if lum > 140 else (255, 255, 255)
