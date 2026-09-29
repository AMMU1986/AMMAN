#!/usr/bin/env python3
"""
Convert the 7 manuscript PNG figures to baseline JPEG using ONLY the Python
standard library (zlib, struct) — no PIL/numpy.

Contains:
  - a minimal PNG decoder (8-bit RGB / RGBA, filter types 0-4)
  - a baseline sequential (Huffman) JPEG encoder (4:2:0 chroma subsampling)

Reads:  infiltration_figures/*.png
Writes: infiltration_figures_jpg/*.jpg
"""

import os
import zlib
import struct
import math

SRC = '/projects/sandbox/AMMAN/infiltration_figures'
DST = '/projects/sandbox/AMMAN/infiltration_figures_jpg'
QUALITY = 85

FILES = [
    'Figure_1_Conceptual_Framework.png',
    'Figure_2_Vegetation_Configurations.png',
    'Figure_3_Infiltration_Rate_Density.png',
    'Figure_4_Cumulative_Soil_Discharge.png',
    'Figure_5_Spatial_Distribution.png',
    'Figure_6_Dimensionless_Collapse.png',
    'Figure_7_Observed_vs_Predicted.png',
]


# =========================================================================
# PNG decoder (supports 8-bit color types 2 (RGB) and 6 (RGBA))
# =========================================================================
def _paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def decode_png(path):
    with open(path, 'rb') as f:
        data = f.read()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', 'not a PNG'
    pos = 8
    width = height = bit_depth = color_type = None
    idat = bytearray()
    while pos < len(data):
        (length,) = struct.unpack('>I', data[pos:pos+4])
        ctype = data[pos+4:pos+8]
        chunk = data[pos+8:pos+8+length]
        pos += 12 + length
        if ctype == b'IHDR':
            width, height, bit_depth, color_type = struct.unpack('>IIBB', chunk[:10])
        elif ctype == b'IDAT':
            idat.extend(chunk)
        elif ctype == b'IEND':
            break
    assert bit_depth == 8, 'only 8-bit PNG supported'
    channels = {2: 3, 6: 4, 0: 1}[color_type]
    raw = zlib.decompress(bytes(idat))
    stride = width * channels
    out = bytearray(width * height * 3)
    prev = bytearray(stride)
    rp = 0
    for y in range(height):
        ftype = raw[rp]; rp += 1
        line = bytearray(raw[rp:rp+stride]); rp += stride
        if ftype == 1:  # Sub
            for i in range(channels, stride):
                line[i] = (line[i] + line[i-channels]) & 0xff
        elif ftype == 2:  # Up
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xff
        elif ftype == 3:  # Average
            for i in range(stride):
                a = line[i-channels] if i >= channels else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 0xff
        elif ftype == 4:  # Paeth
            for i in range(stride):
                a = line[i-channels] if i >= channels else 0
                c = prev[i-channels] if i >= channels else 0
                line[i] = (line[i] + _paeth(a, prev[i], c)) & 0xff
        # write RGB (drop alpha if present)
        op = y * width * 3
        for x in range(width):
            sp = x * channels
            out[op] = line[sp]
            out[op+1] = line[sp+1] if channels >= 3 else line[sp]
            out[op+2] = line[sp+2] if channels >= 3 else line[sp]
            op += 3
        prev = line
    return width, height, out


# =========================================================================
# Baseline JPEG encoder (4:2:0)
# =========================================================================
STD_LUM_Q = [
    16, 11, 10, 16, 24, 40, 51, 61,
    12, 12, 14, 19, 26, 58, 60, 55,
    14, 13, 16, 24, 40, 57, 69, 56,
    14, 17, 22, 29, 51, 87, 80, 62,
    18, 22, 37, 56, 68, 109, 103, 77,
    24, 35, 55, 64, 81, 104, 113, 92,
    49, 64, 78, 87, 103, 121, 120, 101,
    72, 92, 95, 98, 112, 100, 103, 99,
]
STD_CHR_Q = [
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

# Standard Huffman tables (Annex K)
STD_DC_LUM_BITS = [0, 0, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
STD_DC_LUM_VALS = list(range(12))
STD_AC_LUM_BITS = [0, 0, 2, 1, 3, 3, 2, 4, 3, 5, 5, 4, 4, 0, 0, 1, 0x7d]
STD_AC_LUM_VALS = [
    0x01, 0x02, 0x03, 0x00, 0x04, 0x11, 0x05, 0x12, 0x21, 0x31, 0x41, 0x06, 0x13, 0x51, 0x61, 0x07,
    0x22, 0x71, 0x14, 0x32, 0x81, 0x91, 0xa1, 0x08, 0x23, 0x42, 0xb1, 0xc1, 0x15, 0x52, 0xd1, 0xf0,
    0x24, 0x33, 0x62, 0x72, 0x82, 0x09, 0x0a, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x25, 0x26, 0x27, 0x28,
    0x29, 0x2a, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3a, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49,
    0x4a, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69,
    0x6a, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7a, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89,
    0x8a, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9a, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7,
    0xa8, 0xa9, 0xaa, 0xb2, 0xb3, 0xb4, 0xb5, 0xb6, 0xb7, 0xb8, 0xb9, 0xba, 0xc2, 0xc3, 0xc4, 0xc5,
    0xc6, 0xc7, 0xc8, 0xc9, 0xca, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda, 0xe1, 0xe2,
    0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8,
    0xf9, 0xfa,
]
STD_DC_CHR_BITS = [0, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
STD_DC_CHR_VALS = list(range(12))
STD_AC_CHR_BITS = [0, 0, 2, 1, 2, 4, 4, 3, 4, 7, 5, 4, 4, 0, 1, 2, 0x77]
STD_AC_CHR_VALS = [
    0x00, 0x01, 0x02, 0x03, 0x11, 0x04, 0x05, 0x21, 0x31, 0x06, 0x12, 0x41, 0x51, 0x07, 0x61, 0x71,
    0x13, 0x22, 0x32, 0x81, 0x08, 0x14, 0x42, 0x91, 0xa1, 0xb1, 0xc1, 0x09, 0x23, 0x33, 0x52, 0xf0,
    0x15, 0x62, 0x72, 0xd1, 0x0a, 0x16, 0x24, 0x34, 0xe1, 0x25, 0xf1, 0x17, 0x18, 0x19, 0x1a, 0x26,
    0x27, 0x28, 0x29, 0x2a, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3a, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48,
    0x49, 0x4a, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68,
    0x69, 0x6a, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7a, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87,
    0x88, 0x89, 0x8a, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9a, 0xa2, 0xa3, 0xa4, 0xa5,
    0xa6, 0xa7, 0xa8, 0xa9, 0xaa, 0xb2, 0xb3, 0xb4, 0xb5, 0xb6, 0xb7, 0xb8, 0xb9, 0xba, 0xc2, 0xc3,
    0xc4, 0xc5, 0xc6, 0xc7, 0xc8, 0xc9, 0xca, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda,
    0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8,
    0xf9, 0xfa,
]


def build_huff(bits, vals):
    """Return dict value -> (code, length)."""
    codes = {}
    code = 0
    k = 0
    for length in range(1, 17):
        for _ in range(bits[length]):
            codes[vals[k]] = (code, length)
            code += 1
            k += 1
        code <<= 1
    return codes


def scale_quant(table, quality):
    if quality < 1:
        quality = 1
    if quality > 100:
        quality = 100
    scale = 5000 // quality if quality < 50 else 200 - quality * 2
    out = []
    for q in table:
        v = (q * scale + 50) // 100
        out.append(max(1, min(255, v)))
    return out


class BitWriter:
    def __init__(self):
        self.buf = bytearray()
        self.acc = 0
        self.nbits = 0

    def write(self, code, length):
        self.acc = (self.acc << length) | (code & ((1 << length) - 1))
        self.nbits += length
        while self.nbits >= 8:
            self.nbits -= 8
            b = (self.acc >> self.nbits) & 0xff
            self.buf.append(b)
            if b == 0xff:
                self.buf.append(0x00)  # byte stuffing

    def flush(self):
        if self.nbits > 0:
            b = (self.acc << (8 - self.nbits)) & 0xff
            b |= (1 << (8 - self.nbits)) - 1
            self.buf.append(b)
            if b == 0xff:
                self.buf.append(0x00)
            self.nbits = 0
            self.acc = 0


# Precompute DCT cosine table
_C = [[0.0]*8 for _ in range(8)]
for _u in range(8):
    for _x in range(8):
        cu = math.sqrt(1/8) if _u == 0 else math.sqrt(2/8)
        _C[_u][_x] = cu * math.cos((2*_x+1)*_u*math.pi/16)


def fdct8x8(block):
    # separable 2D DCT
    tmp = [[0.0]*8 for _ in range(8)]
    for y in range(8):
        row = block[y]
        for u in range(8):
            s = 0.0
            Cu = _C[u]
            for x in range(8):
                s += row[x] * Cu[x]
            tmp[y][u] = s
    out = [[0.0]*8 for _ in range(8)]
    for u in range(8):
        for v in range(8):
            s = 0.0
            Cu = _C[u]
            for y in range(8):
                s += tmp[y][v] * Cu[y]
            out[u][v] = s
    return out


def bit_size(v):
    if v == 0:
        return 0
    a = abs(v)
    n = 0
    while a:
        a >>= 1
        n += 1
    return n


def encode_block(block, q, prev_dc, bw, dc_huff, ac_huff):
    dct = fdct8x8(block)
    # quantize into zigzag order
    zz = [0]*64
    flat = [dct[i//8][i % 8] for i in range(64)]
    for i in range(64):
        pos = ZIGZAG[i]
        zz[i] = int(round(flat[pos] / q[pos]))
    # DC
    diff = zz[0] - prev_dc
    s = bit_size(diff)
    code, length = dc_huff[s]
    bw.write(code, length)
    if s:
        val = diff if diff >= 0 else (diff + (1 << s) - 1)
        bw.write(val & ((1 << s) - 1), s)
    # AC
    run = 0
    for i in range(1, 64):
        c = zz[i]
        if c == 0:
            run += 1
        else:
            while run > 15:
                code, length = ac_huff[0xF0]
                bw.write(code, length)
                run -= 16
            s = bit_size(c)
            rs = (run << 4) | s
            code, length = ac_huff[rs]
            bw.write(code, length)
            val = c if c >= 0 else (c + (1 << s) - 1)
            bw.write(val & ((1 << s) - 1), s)
            run = 0
    if run > 0:
        code, length = ac_huff[0x00]  # EOB
        bw.write(code, length)
    return zz[0]


def emit_dht(marker_bytes, tc_th, bits, vals):
    body = bytes([tc_th]) + bytes(bits[1:17]) + bytes(vals)
    return b'\xff\xc4' + struct.pack('>H', len(body)+2) + body


def encode_jpeg(width, height, rgb, quality=QUALITY):
    lq = scale_quant(STD_LUM_Q, quality)
    cq = scale_quant(STD_CHR_Q, quality)
    dc_l = build_huff(STD_DC_LUM_BITS, STD_DC_LUM_VALS)
    ac_l = build_huff(STD_AC_LUM_BITS, STD_AC_LUM_VALS)
    dc_c = build_huff(STD_DC_CHR_BITS, STD_DC_CHR_VALS)
    ac_c = build_huff(STD_AC_CHR_BITS, STD_AC_CHR_VALS)

    # Convert to YCbCr planes
    Y = [0.0]*(width*height)
    Cb = [0.0]*(width*height)
    Cr = [0.0]*(width*height)
    for i in range(width*height):
        r = rgb[i*3]; g = rgb[i*3+1]; b = rgb[i*3+2]
        Y[i] = 0.299*r + 0.587*g + 0.114*b - 128.0
        Cb[i] = -0.168736*r - 0.331264*g + 0.5*b
        Cr[i] = 0.5*r - 0.418688*g - 0.081312*b

    def sample(plane, px, py):
        px = min(px, width-1); py = min(py, height-1)
        return plane[py*width+px]

    bw = BitWriter()
    pdc_y = pdc_cb = pdc_cr = 0
    # 4:2:0 MCU = 16x16 (4 Y blocks + 1 Cb + 1 Cr)
    mcux = (width + 15) // 16
    mcuy = (height + 15) // 16
    for my in range(mcuy):
        for mx in range(mcux):
            # 4 luma blocks
            for by in range(2):
                for bx in range(2):
                    blk = [[0.0]*8 for _ in range(8)]
                    ox = mx*16 + bx*8
                    oy = my*16 + by*8
                    for yy in range(8):
                        for xx in range(8):
                            blk[yy][xx] = sample(Y, ox+xx, oy+yy)
                    pdc_y = encode_block(blk, lq, pdc_y, bw, dc_l, ac_l)
            # Cb (subsampled)
            for plane, q, pdc, dch, ach, which in (
                    (Cb, cq, pdc_cb, dc_c, ac_c, 'cb'),
                    (Cr, cq, pdc_cr, dc_c, ac_c, 'cr')):
                blk = [[0.0]*8 for _ in range(8)]
                for yy in range(8):
                    for xx in range(8):
                        sx = mx*16 + xx*2
                        sy = my*16 + yy*2
                        s = (sample(plane, sx, sy) + sample(plane, sx+1, sy) +
                             sample(plane, sx, sy+1) + sample(plane, sx+1, sy+1)) / 4.0
                        blk[yy][xx] = s
                dc = encode_block(blk, q, pdc, bw, dch, ach)
                if which == 'cb':
                    pdc_cb = dc
                else:
                    pdc_cr = dc
    bw.flush()

    # Assemble file
    out = bytearray()
    out += b'\xff\xd8'  # SOI
    # APP0 JFIF
    out += b'\xff\xe0' + struct.pack('>H', 16) + b'JFIF\x00' + bytes([1, 1, 0]) + struct.pack('>HH', 1, 1) + bytes([0, 0])
    # DQT luma
    out += b'\xff\xdb' + struct.pack('>H', 67) + bytes([0]) + bytes([lq[ZIGZAG[i]] for i in range(64)])
    # DQT chroma
    out += b'\xff\xdb' + struct.pack('>H', 67) + bytes([1]) + bytes([cq[ZIGZAG[i]] for i in range(64)])
    # SOF0
    sof = struct.pack('>BHHB', 8, height, width, 3)
    sof += bytes([1, 0x22, 0]) + bytes([2, 0x11, 1]) + bytes([3, 0x11, 1])
    out += b'\xff\xc0' + struct.pack('>H', len(sof)+2) + sof
    # DHTs
    out += emit_dht(None, 0x00, STD_DC_LUM_BITS, STD_DC_LUM_VALS)
    out += emit_dht(None, 0x10, STD_AC_LUM_BITS, STD_AC_LUM_VALS)
    out += emit_dht(None, 0x01, STD_DC_CHR_BITS, STD_DC_CHR_VALS)
    out += emit_dht(None, 0x11, STD_AC_CHR_BITS, STD_AC_CHR_VALS)
    # SOS
    sos = bytes([3, 1, 0x00, 2, 0x11, 3, 0x11, 0, 63, 0])
    out += b'\xff\xda' + struct.pack('>H', len(sos)+2) + sos
    out += bw.buf
    out += b'\xff\xd9'  # EOI
    return bytes(out)


def main():
    os.makedirs(DST, exist_ok=True)
    for fname in FILES:
        src = os.path.join(SRC, fname)
        w, h, rgb = decode_png(src)
        jpg = encode_jpeg(w, h, rgb, QUALITY)
        out_name = fname.rsplit('.', 1)[0] + '.jpg'
        with open(os.path.join(DST, out_name), 'wb') as f:
            f.write(jpg)
        print("  %s -> %s (%dx%d, %.1f KB)" % (fname, out_name, w, h, len(jpg)/1024))
    print("Done. JPEGs in %s/" % DST)


if __name__ == '__main__':
    main()
