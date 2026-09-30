#!/usr/bin/env python3
"""
Pure-standard-library baseline (sequential) JPEG encoder.

No third-party dependencies (no PIL / numpy). Encodes an RGB pixel buffer
(bytearray, 3 bytes per pixel, row-major) into a valid baseline JFIF JPEG so
that figures can be embedded as .jpg inside the manuscript .docx.

Implements: RGB->YCbCr, 8x8 block DCT-II, quantization (standard JPEG luma /
chroma tables scaled by quality), zig-zag ordering, standard Huffman tables,
and the JFIF/APP0 + DQT + SOF0 + DHT + SOS marker structure.
"""

import math
import struct

# ---- Standard JPEG quantization tables (Annex K) ----
STD_LUMA_Q = [
    16, 11, 10, 16, 24, 40, 51, 61,
    12, 12, 14, 19, 26, 58, 60, 55,
    14, 13, 16, 24, 40, 57, 69, 56,
    14, 17, 22, 29, 51, 87, 80, 62,
    18, 22, 37, 56, 68, 109, 103, 77,
    24, 35, 55, 64, 81, 104, 113, 92,
    49, 64, 78, 87, 103, 121, 120, 101,
    72, 92, 95, 98, 112, 100, 103, 99,
]
STD_CHROMA_Q = [
    17, 18, 24, 47, 99, 99, 99, 99,
    18, 21, 26, 66, 99, 99, 99, 99,
    24, 26, 56, 99, 99, 99, 99, 99,
    47, 66, 99, 99, 99, 99, 99, 99,
    99, 99, 99, 99, 99, 99, 99, 99,
    99, 99, 99, 99, 99, 99, 99, 99,
    99, 99, 99, 99, 99, 99, 99, 99,
    99, 99, 99, 99, 99, 99, 99, 99,
]

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

# ---- Standard Huffman tables (Annex K) ----
STD_DC_LUMA_BITS = [0, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
STD_DC_LUMA_VALS = list(range(12))
STD_DC_CHROMA_BITS = [0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
STD_DC_CHROMA_VALS = list(range(12))

STD_AC_LUMA_BITS = [0, 2, 1, 3, 3, 2, 4, 3, 5, 5, 4, 4, 0, 0, 1, 0x7d]
STD_AC_LUMA_VALS = [
    0x01, 0x02, 0x03, 0x00, 0x04, 0x11, 0x05, 0x12, 0x21, 0x31, 0x41, 0x06,
    0x13, 0x51, 0x61, 0x07, 0x22, 0x71, 0x14, 0x32, 0x81, 0x91, 0xa1, 0x08,
    0x23, 0x42, 0xb1, 0xc1, 0x15, 0x52, 0xd1, 0xf0, 0x24, 0x33, 0x62, 0x72,
    0x82, 0x09, 0x0a, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x25, 0x26, 0x27, 0x28,
    0x29, 0x2a, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3a, 0x43, 0x44, 0x45,
    0x46, 0x47, 0x48, 0x49, 0x4a, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59,
    0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 0x73, 0x74, 0x75,
    0x76, 0x77, 0x78, 0x79, 0x7a, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89,
    0x8a, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9a, 0xa2, 0xa3,
    0xa4, 0xa5, 0xa6, 0xa7, 0xa8, 0xa9, 0xaa, 0xb2, 0xb3, 0xb4, 0xb5, 0xb6,
    0xb7, 0xb8, 0xb9, 0xba, 0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7, 0xc8, 0xc9,
    0xca, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda, 0xe1, 0xe2,
    0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xf1, 0xf2, 0xf3, 0xf4,
    0xf5, 0xf6, 0xf7, 0xf8, 0xf9, 0xfa,
]

STD_AC_CHROMA_BITS = [0, 2, 1, 2, 4, 4, 3, 4, 7, 5, 4, 4, 0, 1, 2, 0x77]
STD_AC_CHROMA_VALS = [
    0x00, 0x01, 0x02, 0x03, 0x11, 0x04, 0x05, 0x21, 0x31, 0x06, 0x12, 0x41,
    0x51, 0x07, 0x61, 0x71, 0x13, 0x22, 0x32, 0x81, 0x08, 0x14, 0x42, 0x91,
    0xa1, 0xb1, 0xc1, 0x09, 0x23, 0x33, 0x52, 0xf0, 0x15, 0x62, 0x72, 0xd1,
    0x0a, 0x16, 0x24, 0x34, 0xe1, 0x25, 0xf1, 0x17, 0x18, 0x19, 0x1a, 0x26,
    0x27, 0x28, 0x29, 0x2a, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3a, 0x43, 0x44,
    0x45, 0x46, 0x47, 0x48, 0x49, 0x4a, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58,
    0x59, 0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 0x73, 0x74,
    0x75, 0x76, 0x77, 0x78, 0x79, 0x7a, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87,
    0x88, 0x89, 0x8a, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9a,
    0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7, 0xa8, 0xa9, 0xaa, 0xb2, 0xb3, 0xb4,
    0xb5, 0xb6, 0xb7, 0xb8, 0xb9, 0xba, 0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7,
    0xc8, 0xc9, 0xca, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda,
    0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xf2, 0xf3, 0xf4,
    0xf5, 0xf6, 0xf7, 0xf8, 0xf9, 0xfa,
]


def _build_huff_table(bits, vals):
    """Return dict: value -> (code, code_length)."""
    codes = {}
    code = 0
    k = 0
    for length in range(1, 17):
        for _ in range(bits[length - 1]):
            codes[vals[k]] = (code, length)
            code += 1
            k += 1
        code <<= 1
    return codes


def _scale_quant_table(table, quality):
    if quality <= 0:
        quality = 1
    if quality > 100:
        quality = 100
    scale = 5000 // quality if quality < 50 else 200 - quality * 2
    out = []
    for q in table:
        v = (q * scale + 50) // 100
        out.append(max(1, min(255, v)))
    return out


# Precompute DCT cosine coefficients
_COS = [[math.cos((2 * x + 1) * u * math.pi / 16) for x in range(8)] for u in range(8)]
_C = [1 / math.sqrt(2)] + [1.0] * 7


def _fdct_block(block):
    """Forward 8x8 DCT-II (separable). block: list of 64 floats. Returns 64 floats."""
    tmp = [0.0] * 64
    # rows
    for y in range(8):
        base = y * 8
        row = block[base:base + 8]
        for u in range(8):
            s = 0.0
            cu = _COS[u]
            for x in range(8):
                s += row[x] * cu[x]
            tmp[base + u] = 0.5 * _C[u] * s
    out = [0.0] * 64
    # cols
    for x in range(8):
        for v in range(8):
            s = 0.0
            cv = _COS[v]
            for y in range(8):
                s += tmp[y * 8 + x] * cv[y]
            out[v * 8 + x] = 0.5 * _C[v] * s
    return out


class _BitWriter:
    def __init__(self):
        self.buf = bytearray()
        self.acc = 0
        self.nbits = 0

    def write(self, code, length):
        self.acc = (self.acc << length) | (code & ((1 << length) - 1))
        self.nbits += length
        while self.nbits >= 8:
            self.nbits -= 8
            byte = (self.acc >> self.nbits) & 0xFF
            self.buf.append(byte)
            if byte == 0xFF:
                self.buf.append(0x00)  # byte stuffing

    def flush(self):
        if self.nbits > 0:
            byte = (self.acc << (8 - self.nbits)) & 0xFF
            byte |= (1 << (8 - self.nbits)) - 1  # pad with 1s
            self.buf.append(byte)
            if byte == 0xFF:
                self.buf.append(0x00)
            self.nbits = 0
            self.acc = 0


def _bit_size(value):
    if value == 0:
        return 0
    return value.bit_length()


def _amplitude_bits(value, size):
    if value >= 0:
        return value
    return value + (1 << size) - 1


def encode_jpeg(width, height, rgb, quality=85):
    """Encode RGB bytearray into a baseline JPEG (returns bytes)."""
    luma_q = _scale_quant_table(STD_LUMA_Q, quality)
    chroma_q = _scale_quant_table(STD_CHROMA_Q, quality)

    dc_luma = _build_huff_table(STD_DC_LUMA_BITS, STD_DC_LUMA_VALS)
    ac_luma = _build_huff_table(STD_AC_LUMA_BITS, STD_AC_LUMA_VALS)
    dc_chroma = _build_huff_table(STD_DC_CHROMA_BITS, STD_DC_CHROMA_VALS)
    ac_chroma = _build_huff_table(STD_AC_CHROMA_BITS, STD_AC_CHROMA_VALS)

    def get_px(x, y):
        if x >= width:
            x = width - 1
        if y >= height:
            y = height - 1
        i = (y * width + x) * 3
        return rgb[i], rgb[i + 1], rgb[i + 2]

    bw = _BitWriter()
    prev_dc = [0, 0, 0]  # Y, Cb, Cr

    def encode_block(samples, qtab, dc_tab, ac_tab, comp_idx):
        coeffs = _fdct_block(samples)
        quant = [0] * 64
        for i in range(64):
            quant[i] = int(round(coeffs[i] / qtab[i]))
        # DC
        dc = quant[0]
        diff = dc - prev_dc[comp_idx]
        prev_dc[comp_idx] = dc
        size = _bit_size(abs(diff)) if diff != 0 else 0
        code, clen = dc_tab[size]
        bw.write(code, clen)
        if size > 0:
            bw.write(_amplitude_bits(diff, size), size)
        # AC
        zz = [quant[ZIGZAG[i]] for i in range(64)]
        run = 0
        for i in range(1, 64):
            v = zz[i]
            if v == 0:
                run += 1
            else:
                while run > 15:
                    code, clen = ac_tab[0xF0]
                    bw.write(code, clen)
                    run -= 16
                s = _bit_size(abs(v))
                sym = (run << 4) | s
                code, clen = ac_tab[sym]
                bw.write(code, clen)
                bw.write(_amplitude_bits(v, s), s)
                run = 0
        if run > 0:
            code, clen = ac_tab[0x00]  # EOB
            bw.write(code, clen)

    # Process MCUs (4:4:4, 8x8 blocks)
    for by in range(0, height, 8):
        for bx in range(0, width, 8):
            yb = [0.0] * 64
            cbb = [0.0] * 64
            crb = [0.0] * 64
            for j in range(8):
                for i in range(8):
                    r, g, b = get_px(bx + i, by + j)
                    Y = 0.299 * r + 0.587 * g + 0.114 * b
                    Cb = -0.168736 * r - 0.331264 * g + 0.5 * b + 128
                    Cr = 0.5 * r - 0.418688 * g - 0.081312 * b + 128
                    idx = j * 8 + i
                    yb[idx] = Y - 128
                    cbb[idx] = Cb - 128
                    crb[idx] = Cr - 128
            encode_block(yb, luma_q, dc_luma, ac_luma, 0)
            encode_block(cbb, chroma_q, dc_chroma, ac_chroma, 1)
            encode_block(crb, chroma_q, dc_chroma, ac_chroma, 2)

    bw.flush()

    # ---- Assemble JFIF ----
    out = bytearray()
    out += b'\xFF\xD8'  # SOI

    # APP0 JFIF
    app0 = b'JFIF\x00' + bytes([1, 1, 0]) + struct.pack('>HH', 1, 1) + bytes([0, 0])
    out += b'\xFF\xE0' + struct.pack('>H', len(app0) + 2) + app0

    # DQT (luma id0, chroma id1)
    def dqt(qid, table):
        payload = bytes([qid]) + bytes(table[ZIGZAG[i]] for i in range(64))
        return b'\xFF\xDB' + struct.pack('>H', len(payload) + 2) + payload
    out += dqt(0, luma_q)
    out += dqt(1, chroma_q)

    # SOF0
    sof = bytes([8]) + struct.pack('>HH', height, width) + bytes([3])
    sof += bytes([1, 0x11, 0])   # Y  sampling 1x1, qtable 0
    sof += bytes([2, 0x11, 1])   # Cb
    sof += bytes([3, 0x11, 1])   # Cr
    out += b'\xFF\xC0' + struct.pack('>H', len(sof) + 2) + sof

    # DHT
    def dht(tc_th, bits, vals):
        payload = bytes([tc_th]) + bytes(bits) + bytes(vals)
        return b'\xFF\xC4' + struct.pack('>H', len(payload) + 2) + payload
    out += dht(0x00, STD_DC_LUMA_BITS, STD_DC_LUMA_VALS)
    out += dht(0x10, STD_AC_LUMA_BITS, STD_AC_LUMA_VALS)
    out += dht(0x01, STD_DC_CHROMA_BITS, STD_DC_CHROMA_VALS)
    out += dht(0x11, STD_AC_CHROMA_BITS, STD_AC_CHROMA_VALS)

    # SOS
    sos = bytes([3]) + bytes([1, 0x00, 2, 0x11, 3, 0x11]) + bytes([0, 63, 0])
    out += b'\xFF\xDA' + struct.pack('>H', len(sos) + 2) + sos

    out += bw.buf
    out += b'\xFF\xD9'  # EOI
    return bytes(out)


def save_jpeg(path, width, height, rgb, quality=85):
    data = encode_jpeg(width, height, rgb, quality)
    with open(path, 'wb') as f:
        f.write(data)
    return len(data)
