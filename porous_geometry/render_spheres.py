#!/usr/bin/env python3
"""
Pure-stdlib software renderer for the packed-sphere .dat files produced by
porous_geometry.f90.  No numpy / matplotlib / PIL required.

- reads sphere centres + radii (x y z r [overlap])
- orthographic 3-D projection with azimuth/elevation rotation
- per-pixel sphere rasterization with a z-buffer + Lambert shading
- coloured by original height (z) with a viridis-like map (blue -> yellow),
  matching the left panels of the reference figure
- writes a PNG (manual PNG encoding via zlib)

usage: python3 render_spheres.py <spheres.dat> <out.png> [title]
"""
import sys, math, struct, zlib

W, H = 900, 820          # image size
BG = (255, 255, 255)     # background
LDOM = 25.0              # domain edge (matches Fortran LDOM)

# ---- viridis-ish colormap (blue -> teal -> green -> yellow) ----------------
_CMAP = [
    (68, 1, 84), (72, 40, 120), (62, 74, 137), (49, 104, 142),
    (38, 130, 142), (31, 158, 137), (53, 183, 121), (110, 206, 88),
    (181, 222, 43), (253, 231, 37),
]
def colormap(t):
    t = max(0.0, min(1.0, t))
    x = t * (len(_CMAP) - 1)
    i = int(x); f = x - i
    if i >= len(_CMAP) - 1:
        return _CMAP[-1]
    a, b = _CMAP[i], _CMAP[i + 1]
    return tuple(a[k] + (b[k] - a[k]) * f for k in range(3))

def read_spheres(path):
    S = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            p = line.split()
            S.append((float(p[0]), float(p[1]), float(p[2]), float(p[3])))
    return S

def write_png(path, w, h, rgb):
    def chunk(tag, data):
        c = struct.pack('>I', len(data)) + tag + data
        return c + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    raw = bytearray()
    for y in range(h):
        raw.append(0)                       # filter type 0
        row = rgb[y * w * 3:(y + 1) * w * 3]
        raw.extend(row)
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    with open(path, 'wb') as f:
        f.write(sig)
        f.write(chunk(b'IHDR', ihdr))
        f.write(chunk(b'IDAT', zlib.compress(bytes(raw), 9)))
        f.write(chunk(b'IEND', b''))

def render(spheres, out, title=''):
    # camera rotation (azimuth, elevation) for the 3-D isometric look
    az = math.radians(-35.0)
    el = math.radians(22.0)
    ca, sa = math.cos(az), math.sin(az)
    ce, se = math.cos(el), math.sin(el)
    c = LDOM / 2.0

    def rot(x, y, z):
        x -= c; y -= c; z -= c
        # azimuth about the vertical (world z) axis
        sx = -sa * x + ca * y            # screen horizontal
        dh = ca * x + sa * y             # horizontal distance into the scene
        # elevation: tilt so world height (z) maps to screen-up
        sy = ce * z - se * dh            # screen vertical (up = +)
        depth = se * z + ce * dh         # into screen (+ = closer to viewer)
        return sx, sy, depth

    # project all centres to find extents for scaling into the image
    pts = [rot(sx, sy, sz) for (sx, sy, sz, r) in spheres]
    maxr = max(r for *_, r in spheres)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    xmin, xmax = min(xs) - maxr, max(xs) + maxr
    ymin, ymax = min(ys) - maxr, max(ys) + maxr
    span = max(xmax - xmin, ymax - ymin)
    margin = 60
    scale = (min(W, H) - 2 * margin) / span
    ox = (W - (xmax + xmin) * scale) / 2.0
    oy = (H - (ymax + ymin) * scale) / 2.0

    def to_px(sx, sy):
        return ox + sx * scale, H - (oy + sy * scale)   # flip y for image

    # height range for colouring
    zmin = min(sz for _, _, sz, _ in spheres)
    zmax = max(sz for _, _, sz, _ in spheres)

    # framebuffer + z-buffer
    fb = bytearray(BG[0:1] * 0)  # placeholder
    fb = bytearray()
    for _ in range(W * H):
        fb += bytes(BG)
    zbuf = [-1e30] * (W * H)

    # light direction (towards viewer, upper-left)
    lx, ly, lz = -0.4, 0.5, 0.75
    ln = math.sqrt(lx * lx + ly * ly + lz * lz)
    lx, ly, lz = lx / ln, ly / ln, lz / ln

    # painter's order: far -> near (depth ascending)
    order = sorted(range(len(spheres)), key=lambda i: pts[i][2])

    for idx in order:
        sx, sy, sz, r = spheres[idx]
        rxc, ryc, rzc = pts[idx]
        pcx, pcy = to_px(rxc, ryc)
        rp = r * scale
        base = colormap((sz - zmin) / (zmax - zmin + 1e-12))

        i0 = max(0, int(pcx - rp)); i1 = min(W - 1, int(pcx + rp) + 1)
        j0 = max(0, int(pcy - rp)); j1 = min(H - 1, int(pcy + rp) + 1)
        rp2 = rp * rp
        for py in range(j0, j1 + 1):
            dyp = py - pcy
            for px in range(i0, i1 + 1):
                dxp = px - pcx
                q = rp2 - dxp * dxp - dyp * dyp
                if q < 0:
                    continue
                dzp = math.sqrt(q)                 # towards viewer
                depth = rzc + dzp / scale          # sphere-front depth
                k = py * W + px
                if depth <= zbuf[k]:
                    continue
                zbuf[k] = depth
                # surface normal in screen space
                nx, ny, nz = dxp / rp, -dyp / rp, dzp / rp
                diff = max(0.0, nx * lx + ny * ly + nz * lz)
                shade = 0.30 + 0.70 * diff          # ambient + diffuse
                # small specular highlight
                spec = diff ** 24 * 0.5
                r8 = min(255, int(base[0] * shade + 255 * spec))
                g8 = min(255, int(base[1] * shade + 255 * spec))
                b8 = min(255, int(base[2] * shade + 255 * spec))
                o = k * 3
                fb[o] = r8; fb[o + 1] = g8; fb[o + 2] = b8

    # thin frame
    for x in range(W):
        for yy in (0, 1, H - 2, H - 1):
            o = (yy * W + x) * 3; fb[o] = fb[o+1] = fb[o+2] = 120
    for y in range(H):
        for xx in (0, 1, W - 2, W - 1):
            o = (y * W + xx) * 3; fb[o] = fb[o+1] = fb[o+2] = 120

    write_png(out, W, H, fb)
    print(f"wrote {out}  ({len(spheres)} spheres)")

if __name__ == '__main__':
    dat = sys.argv[1]
    out = sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else ''
    render(read_spheres(dat), out, title)
