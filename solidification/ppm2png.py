#!/usr/bin/env python3
"""Dependency-free PPM (P6) -> PNG converter (uses only the Python stdlib).

Usage:
    python3 ppm2png.py file1.ppm [file2.ppm ...]      # -> file1.png, ...
    python3 ppm2png.py                                # converts *.ppm in cwd
"""
import sys, glob, struct, zlib


def read_ppm(path):
    with open(path, "rb") as f:
        data = f.read()
    # parse header: magic, width, height, maxval (whitespace separated)
    tokens, i = [], 0
    while len(tokens) < 4:
        while i < len(data) and data[i:i + 1].isspace():
            i += 1
        if data[i:i + 1] == b"#":                     # comment line
            while i < len(data) and data[i:i + 1] != b"\n":
                i += 1
            continue
        start = i
        while i < len(data) and not data[i:i + 1].isspace():
            i += 1
        tokens.append(data[start:i])
    i += 1                                             # skip single whitespace
    magic, w, h = tokens[0], int(tokens[1]), int(tokens[2])
    if magic != b"P6":
        raise ValueError("only binary PPM (P6) is supported")
    return w, h, data[i:i + w * h * 3]


def write_png(path, w, h, rgb):
    def chunk(tag, payload):
        c = tag + payload
        return struct.pack(">I", len(payload)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)

    # add the mandatory per-scanline filter byte (0 = none)
    raw = bytearray()
    stride = w * 3
    for y in range(h):
        raw.append(0)
        raw.extend(rgb[y * stride:(y + 1) * stride])
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)   # 8-bit truecolour RGB
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)


def main():
    files = sys.argv[1:] or sorted(glob.glob("*.ppm"))
    if not files:
        print("no .ppm files found")
        return
    for p in files:
        w, h, rgb = read_ppm(p)
        out = p.rsplit(".", 1)[0] + ".png"
        write_png(out, w, h, rgb)
        print(f"{p} -> {out}  ({w}x{h})")


if __name__ == "__main__":
    main()
