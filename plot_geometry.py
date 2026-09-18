#!/usr/bin/env python3
"""
Render the PCM-capsule geometry produced by pcm_geometry.f90 as a PNG.

Reads phi_field.dat (x  y  phi) and paints a raster image where the PCM
volume fraction phi is mapped from red (phi=0, HTF) to blue (phi=1, PCM),
reproducing the colouring of Fig. 1 of Athawale et al. (2021).

Uses only the Python standard library (zlib, struct) so it needs no
third-party packages (matplotlib / PIL are unavailable in this sandbox).
"""
import struct
import zlib

SRC   = "phi_field.dat"
OUT   = "pcm_geometry.png"
SCALE = 3          # pixels per coarse cell (upscales the image)


def read_field(path):
    """Return (nx, ny, phi[j][i]) from the gnuplot-style data file."""
    xs, ys, vals = [], [], []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            p = line.split()
            if len(p) < 3:
                continue
            xs.append(float(p[0]))
            ys.append(float(p[1]))
            vals.append(float(p[2]))
    # unique sorted coordinates
    ux = sorted(set(xs))
    uy = sorted(set(ys))
    nx, ny = len(ux), len(uy)
    xi = {v: k for k, v in enumerate(ux)}
    yi = {v: k for k, v in enumerate(uy)}
    phi = [[0.0] * nx for _ in range(ny)]
    for x, y, v in zip(xs, ys, vals):
        phi[yi[y]][xi[x]] = v
    return nx, ny, phi


def colormap(v):
    """phi in [0,1] -> (r,g,b). Red = HTF, Blue = PCM, with a thin dark rim."""
    v = max(0.0, min(1.0, v))
    if 0.15 < v < 0.85:            # interface band -> dark outline
        return (25, 25, 30)
    if v >= 0.85:                  # PCM capsule -> blue
        return (30, 60, 220)
    # HTF -> red (paper's background)
    return (225, 35, 30)


def write_png(path, width, height, rgb_rows):
    """Minimal PNG writer (truecolor, 8-bit) using zlib."""
    def chunk(tag, data):
        c = tag + data
        return (struct.pack(">I", len(data)) + c +
                struct.pack(">I", zlib.crc32(c) & 0xffffffff))

    raw = bytearray()
    for row in rgb_rows:                      # each row: bytes of length width*3
        raw.append(0)                          # filter type 0 (none)
        raw.extend(row)

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    with open(path, "wb") as f:
        f.write(sig)
        f.write(chunk(b"IHDR", ihdr))
        f.write(chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
        f.write(chunk(b"IEND", b""))


def main():
    nx, ny, phi = read_field(SRC)
    W, H = nx * SCALE, ny * SCALE
    rows = []
    # image top row = highest y  -> iterate j from ny-1 down to 0
    for j in range(ny - 1, -1, -1):
        base = bytearray()
        for i in range(nx):
            r, g, b = colormap(phi[j][i])
            base += bytes((r, g, b)) * SCALE     # horizontal upscale
        for _ in range(SCALE):                   # vertical upscale
            rows.append(bytes(base))
    write_png(OUT, W, H, rows)
    print(f"Wrote {OUT}  ({W} x {H} px) from {nx} x {ny} field")


if __name__ == "__main__":
    main()
