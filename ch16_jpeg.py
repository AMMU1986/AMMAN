#!/usr/bin/env python3
"""
ch16_jpeg.py - A self-contained, pure-Python baseline (sequential DCT, Huffman)
JPEG encoder.

The publisher's guidelines for the edited volume require figures to be supplied
in JPEG format. The sandbox has no imaging libraries (PIL/Pillow, matplotlib)
and no network access to install them, so this module implements a minimal but
standards-compliant baseline JPEG encoder using only the Python standard
library. It takes a flat RGB byte buffer and writes a valid .jpg file that
opens in Microsoft Word, LibreOffice, and standard image viewers.

Reference: ITU-T T.81 (JPEG), Annex K (example tables) and Annex C/F
(Huffman coding procedures).

Public API:
    encode_rgb_to_jpeg(width, height, rgb_bytes, path, quality=92)
"""

import math
import struct

# --- Standard zig-zag ordering (T.81 Figure A.6) ---
ZIGZAG = [
    0, 1, 8, 16, 9, 2, 3, 10,
    17, 24, 32, 25, 18, 11, 4, 5,
    12, 19, 26, 33, 40, 48, 41, 34,
    27, 20, 13, 6, 7, 14, 21, 28,
    35, 42, 49, 56, 57, 50, 43, 36,
    29, 22, 15, 23, 30, 37, 44, 51,
    58, 59, 52, 45, 38, 31, 39, 46,
    53, 60, 61, 54, 47, 55, 62, 63,
]

# --- Standard quantization tables (T.81 Annex K.1) ---
STD_LUMA_QT = [
    16, 11, 10, 16, 24, 40, 51, 61,
    12, 12, 14, 19, 26, 58, 60, 55,
    14, 13, 16, 24, 40, 57, 69, 56,
    14, 17, 22, 29, 51, 87, 80, 62,
    18, 22, 37, 56, 68, 109, 103, 77,
    24, 35, 55, 64, 81, 104, 113, 92,
    49, 64, 78, 87, 103, 121, 120, 101,
    72, 92, 95, 98, 112, 100, 103, 99,
]

STD_CHROMA_QT = [
    17, 18, 24, 47, 99, 99, 99, 99,
    18, 21, 26, 66, 99, 99, 99, 99,
    24, 26, 56, 99, 99, 99, 99, 99,
    47, 66, 99, 99, 99, 99, 99, 99,
    99, 99, 99, 99, 99, 99, 99, 99,
    99, 99, 99, 99, 99, 99, 99, 99,
    99, 99, 99, 99, 99, 99, 99, 99,
    99, 99, 99, 99, 99, 99, 99, 99,
]

# --- Standard Huffman table specifications (T.81 Annex K.3) ---
# BITS[i] = number of codes of length (i+1), for i in 0..15
DC_LUMA_BITS = [0, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
DC_LUMA_VALS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

DC_CHROMA_BITS = [0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
DC_CHROMA_VALS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

AC_LUMA_BITS = [0, 2, 1, 3, 3, 2, 4, 3, 5, 5, 4, 4, 0, 0, 1, 0x7D]
AC_LUMA_VALS = [
    0x01, 0x02, 0x03, 0x00, 0x04, 0x11, 0x05, 0x12,
    0x21, 0x31, 0x41, 0x06, 0x13, 0x51, 0x61, 0x07,
    0x22, 0x71, 0x14, 0x32, 0x81, 0x91, 0xA1, 0x08,
    0x23, 0x42, 0xB1, 0xC1, 0x15, 0x52, 0xD1, 0xF0,
    0x24, 0x33, 0x62, 0x72, 0x82, 0x09, 0x0A, 0x16,
    0x17, 0x18, 0x19, 0x1A, 0x25, 0x26, 0x27, 0x28,
    0x29, 0x2A, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39,
    0x3A, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49,
    0x4A, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59,
    0x5A, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69,
    0x6A, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79,
    0x7A, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89,
    0x8A, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98,
    0x99, 0x9A, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7,
    0xA8, 0xA9, 0xAA, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6,
    0xB7, 0xB8, 0xB9, 0xBA, 0xC2, 0xC3, 0xC4, 0xC5,
    0xC6, 0xC7, 0xC8, 0xC9, 0xCA, 0xD2, 0xD3, 0xD4,
    0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0xDA, 0xE1, 0xE2,
    0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xEA,
    0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8,
    0xF9, 0xFA,
]

AC_CHROMA_BITS = [0, 2, 1, 2, 4, 4, 3, 4, 7, 5, 4, 4, 0, 1, 2, 0x77]
AC_CHROMA_VALS = [
    0x00, 0x01, 0x02, 0x03, 0x11, 0x04, 0x05, 0x21,
    0x31, 0x06, 0x12, 0x41, 0x51, 0x07, 0x61, 0x71,
    0x13, 0x22, 0x32, 0x81, 0x08, 0x14, 0x42, 0x91,
    0xA1, 0xB1, 0xC1, 0x09, 0x23, 0x33, 0x52, 0xF0,
    0x15, 0x62, 0x72, 0xD1, 0x0A, 0x16, 0x24, 0x34,
    0xE1, 0x25, 0xF1, 0x17, 0x18, 0x19, 0x1A, 0x26,
    0x27, 0x28, 0x29, 0x2A, 0x35, 0x36, 0x37, 0x38,
    0x39, 0x3A, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48,
    0x49, 0x4A, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58,
    0x59, 0x5A, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68,
    0x69, 0x6A, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78,
    0x79, 0x7A, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87,
    0x88, 0x89, 0x8A, 0x92, 0x93, 0x94, 0x95, 0x96,
    0x97, 0x98, 0x99, 0x9A, 0xA2, 0xA3, 0xA4, 0xA5,
    0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xB2, 0xB3, 0xB4,
    0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xC2, 0xC3,
    0xC4, 0xC5, 0xC6, 0xC7, 0xC8, 0xC9, 0xCA, 0xD2,
    0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0xDA,
    0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9,
    0xEA, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8,
    0xF9, 0xFA,
]


def _build_huff_table(bits, vals):
    """Build {symbol: (code, length)} from BITS/HUFFVAL per T.81 Annex C."""
    huffsize = []
    for i, count in enumerate(bits):
        huffsize.extend([i + 1] * count)
    codes = {}
    code = 0
    k = 0
    if not huffsize:
        return codes
    si = huffsize[0]
    while k < len(huffsize):
        while k < len(huffsize) and huffsize[k] == si:
            codes[vals[k]] = (code, si)
            code += 1
            k += 1
        code <<= 1
        si += 1
    return codes


def _scale_qt(base, quality):
    """Scale a base quantization table by a quality factor (1..100)."""
    quality = max(1, min(100, int(quality)))
    if quality < 50:
        scale = 5000 // quality
    else:
        scale = 200 - quality * 2
    out = []
    for q in base:
        v = (q * scale + 50) // 100
        out.append(max(1, min(255, v)))
    return out


# Precompute DCT cosine coefficients:  M[u][x] = 0.5 * C(u) * cos((2x+1)uPi/16)
_C = [1.0 / math.sqrt(2)] + [1.0] * 7
_DCT_M = [[0.5 * _C[u] * math.cos((2 * x + 1) * u * math.pi / 16.0)
           for x in range(8)] for u in range(8)]


def _forward_dct_block(block):
    """2D separable forward DCT of an 8x8 list (row-major, level-shifted)."""
    M = _DCT_M
    # Pass 1: transform along x (within each row y) -> A[y][u]
    tmp = [[0.0] * 8 for _ in range(8)]
    for y in range(8):
        row = block[y * 8:y * 8 + 8]
        for u in range(8):
            Mu = M[u]
            s = (row[0] * Mu[0] + row[1] * Mu[1] + row[2] * Mu[2] +
                 row[3] * Mu[3] + row[4] * Mu[4] + row[5] * Mu[5] +
                 row[6] * Mu[6] + row[7] * Mu[7])
            tmp[y][u] = s
    # Pass 2: transform along y -> F[v][u]
    out = [0.0] * 64
    for u in range(8):
        col = [tmp[y][u] for y in range(8)]
        for v in range(8):
            Mv = M[v]
            s = (col[0] * Mv[0] + col[1] * Mv[1] + col[2] * Mv[2] +
                 col[3] * Mv[3] + col[4] * Mv[4] + col[5] * Mv[5] +
                 col[6] * Mv[6] + col[7] * Mv[7])
            out[v * 8 + u] = s
    return out


class _BitWriter:
    """Accumulates bits MSB-first with JPEG 0xFF byte stuffing."""

    def __init__(self):
        self.out = bytearray()
        self.acc = 0
        self.nbits = 0

    def write(self, code, length):
        self.acc = (self.acc << length) | (code & ((1 << length) - 1))
        self.nbits += length
        while self.nbits >= 8:
            self.nbits -= 8
            b = (self.acc >> self.nbits) & 0xFF
            self.out.append(b)
            if b == 0xFF:
                self.out.append(0x00)  # byte stuffing

    def flush(self):
        if self.nbits > 0:
            # pad remaining bits with 1s
            pad = 8 - self.nbits
            self.acc = (self.acc << pad) | ((1 << pad) - 1)
            self.nbits += pad
            b = (self.acc >> (self.nbits - 8)) & 0xFF
            self.out.append(b)
            if b == 0xFF:
                self.out.append(0x00)
            self.nbits = 0
            self.acc = 0


def _category(value):
    t = value if value >= 0 else -value
    c = 0
    while t:
        c += 1
        t >>= 1
    return c


def _mantissa(value, size):
    if value < 0:
        value += (1 << size) - 1
    return value & ((1 << size) - 1)


def _encode_block(coeffs, qt, prev_dc, bw, dc_tab, ac_tab):
    """Quantize + entropy-code one 8x8 DCT block. Returns new prev_dc."""
    q = [0] * 64
    for i in range(64):
        f = coeffs[i] / qt[i]
        q[i] = int(math.floor(f + 0.5)) if f >= 0 else -int(math.floor(-f + 0.5))

    # DC (differential)
    dc = q[0]
    diff = dc - prev_dc
    size = _category(diff)
    code, length = dc_tab[size]
    bw.write(code, length)
    if size:
        bw.write(_mantissa(diff, size), size)

    # AC (run-length + Huffman) in zig-zag order
    run = 0
    for k in range(1, 64):
        coef = q[ZIGZAG[k]]
        if coef == 0:
            run += 1
        else:
            while run > 15:
                c, l = ac_tab[0xF0]  # ZRL
                bw.write(c, l)
                run -= 16
            s = _category(coef)
            sym = (run << 4) | s
            c, l = ac_tab[sym]
            bw.write(c, l)
            bw.write(_mantissa(coef, s), s)
            run = 0
    if run > 0:
        c, l = ac_tab[0x00]  # EOB
        bw.write(c, l)
    return dc


def _marker_dqt(qt, tq):
    body = bytearray()
    body.append(tq & 0x0F)  # 8-bit precision, table id
    for k in range(64):
        body.append(qt[ZIGZAG[k]])
    return b'\xff\xdb' + struct.pack('>H', len(body) + 2) + bytes(body)


def _marker_dht(cls, tid, bits, vals):
    body = bytearray()
    body.append(((cls & 0x0F) << 4) | (tid & 0x0F))
    body.extend(bits)          # 16 length counts
    body.extend(vals)          # symbol values
    return b'\xff\xc4' + struct.pack('>H', len(body) + 2) + bytes(body)


def encode_rgb_to_jpeg(width, height, rgb_bytes, path, quality=92):
    """Encode a flat RGB byte buffer (len = width*height*3) to a baseline JPEG."""
    luma_qt = _scale_qt(STD_LUMA_QT, quality)
    chroma_qt = _scale_qt(STD_CHROMA_QT, quality)

    dc_luma = _build_huff_table(DC_LUMA_BITS, DC_LUMA_VALS)
    ac_luma = _build_huff_table(AC_LUMA_BITS, AC_LUMA_VALS)
    dc_chroma = _build_huff_table(DC_CHROMA_BITS, DC_CHROMA_VALS)
    ac_chroma = _build_huff_table(AC_CHROMA_BITS, AC_CHROMA_VALS)

    # Convert to YCbCr planes (level-shifted by -128 later inside block build)
    n = width * height
    Y = [0.0] * n
    Cb = [0.0] * n
    Cr = [0.0] * n
    for i in range(n):
        r = rgb_bytes[i * 3]
        g = rgb_bytes[i * 3 + 1]
        b = rgb_bytes[i * 3 + 2]
        Y[i] = 0.299 * r + 0.587 * g + 0.114 * b
        Cb[i] = 128.0 - 0.168736 * r - 0.331264 * g + 0.5 * b
        Cr[i] = 128.0 + 0.5 * r - 0.418688 * g - 0.081312 * b

    def get_block(plane, bx, by):
        """Extract an 8x8, level-shifted block, replicating edge pixels."""
        blk = [0.0] * 64
        for yy in range(8):
            sy = by + yy
            if sy >= height:
                sy = height - 1
            base = sy * width
            for xx in range(8):
                sx = bx + xx
                if sx >= width:
                    sx = width - 1
                blk[yy * 8 + xx] = plane[base + sx] - 128.0
        return blk

    bw = _BitWriter()
    pdc_y = pdc_cb = pdc_cr = 0
    mcus_x = (width + 7) // 8
    mcus_y = (height + 7) // 8
    for my in range(mcus_y):
        for mx in range(mcus_x):
            bx, by = mx * 8, my * 8
            fy = _forward_dct_block(get_block(Y, bx, by))
            pdc_y = _encode_block(fy, luma_qt, pdc_y, bw, dc_luma, ac_luma)
            fcb = _forward_dct_block(get_block(Cb, bx, by))
            pdc_cb = _encode_block(fcb, chroma_qt, pdc_cb, bw, dc_chroma, ac_chroma)
            fcr = _forward_dct_block(get_block(Cr, bx, by))
            pdc_cr = _encode_block(fcr, chroma_qt, pdc_cr, bw, dc_chroma, ac_chroma)
    bw.flush()

    out = bytearray()
    out += b'\xff\xd8'  # SOI
    # APP0 JFIF
    app0 = b'JFIF\x00' + bytes([1, 1, 0]) + struct.pack('>HH', 72, 72) + bytes([0, 0])
    out += b'\xff\xe0' + struct.pack('>H', len(app0) + 2) + app0
    # DQT
    out += _marker_dqt(luma_qt, 0)
    out += _marker_dqt(chroma_qt, 1)
    # SOF0 (baseline)
    sof = bytearray()
    sof.append(8)                       # precision
    sof += struct.pack('>HH', height, width)
    sof.append(3)                       # components
    sof += bytes([1, 0x11, 0])          # Y:  id1, 1x1 sampling, qt0
    sof += bytes([2, 0x11, 1])          # Cb: id2, 1x1 sampling, qt1
    sof += bytes([3, 0x11, 1])          # Cr: id3, 1x1 sampling, qt1
    out += b'\xff\xc0' + struct.pack('>H', len(sof) + 2) + bytes(sof)
    # DHT
    out += _marker_dht(0, 0, DC_LUMA_BITS, DC_LUMA_VALS)
    out += _marker_dht(1, 0, AC_LUMA_BITS, AC_LUMA_VALS)
    out += _marker_dht(0, 1, DC_CHROMA_BITS, DC_CHROMA_VALS)
    out += _marker_dht(1, 1, AC_CHROMA_BITS, AC_CHROMA_VALS)
    # SOS
    sos = bytearray()
    sos.append(3)                       # components in scan
    sos += bytes([1, 0x00])             # Y:  dc0/ac0
    sos += bytes([2, 0x11])             # Cb: dc1/ac1
    sos += bytes([3, 0x11])             # Cr: dc1/ac1
    sos += bytes([0, 63, 0])            # Ss, Se, Ah/Al
    out += b'\xff\xda' + struct.pack('>H', len(sos) + 2) + bytes(sos)
    out += bw.out
    out += b'\xff\xd9'  # EOI

    with open(path, 'wb') as f:
        f.write(out)
    return len(out)
