#!/usr/bin/env python3
"""
Generate a Lidinoid triply-periodic minimal surface (TPMS) porous solid
with a target porosity of 95%, using ONLY the Python standard library.

Outputs
-------
- lidinoid_output/Lidinoid_porosity95.stl : binary STL of the porous sheet
- lidinoid_output/Lidinoid_porosity95.png : shaded 3D preview render

Method
------
The Lidinoid is defined by the implicit function (unit period, X = 2*pi*x, ...):

  F(x,y,z) = 0.5*( sin(2X)cos(Y)sin(Z) + sin(2Y)cos(Z)sin(X) + sin(2Z)cos(X)sin(Y) )
           - 0.5*( cos(2X)cos(2Y) + cos(2Y)cos(2Z) + cos(2Z)cos(2X) )
           + 0.15

A "sheet"/shell solid is defined as the region  |F(x,y,z)| <= t .
The half-thickness t is calibrated so the solid volume fraction is 5%
(=> porosity = 95%). The two bounding isosurfaces F = +t and F = -t are then
extracted with marching tetrahedra to build a watertight-ish triangle mesh.
"""

import math
import os
import struct
import zlib

# ----------------------------------------------------------------------------
# Parameters
# ----------------------------------------------------------------------------
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lidinoid_output")
TARGET_POROSITY = 0.95          # 95% void
N = 48                          # grid cells per unit cell (resolution)
UNIT_CELL_MM = 10.0             # physical size of one unit cell in mm (for STL scale)
TWO_PI = 2.0 * math.pi


# ----------------------------------------------------------------------------
# Lidinoid implicit function (period = 1 in x, y, z)
# ----------------------------------------------------------------------------
def lidinoid(x, y, z):
    X = TWO_PI * x
    Y = TWO_PI * y
    Z = TWO_PI * z
    sX, cX = math.sin(X), math.cos(X)
    sY, cY = math.sin(Y), math.cos(Y)
    sZ, cZ = math.sin(Z), math.cos(Z)
    s2X, c2X = math.sin(2 * X), math.cos(2 * X)
    s2Y, c2Y = math.sin(2 * Y), math.cos(2 * Y)
    s2Z, c2Z = math.sin(2 * Z), math.cos(2 * Z)
    term1 = 0.5 * (s2X * cY * sZ + s2Y * cZ * sX + s2Z * cX * sY)
    term2 = 0.5 * (c2X * c2Y + c2Y * c2Z + c2Z * c2X)
    return term1 - term2 + 0.15


# ----------------------------------------------------------------------------
# Sample the field on a regular grid (corner values)
# ----------------------------------------------------------------------------
def sample_field(n):
    """Return (values, coords) where values is a flat list indexed by
    idx(i,j,k) = (i*(n+1)+j)*(n+1)+k over i,j,k in [0..n]."""
    m = n + 1
    coords = [i / n for i in range(m)]  # 0..1 inclusive
    values = [0.0] * (m * m * m)
    lid = lidinoid
    for i in range(m):
        xi = coords[i]
        base_i = i * m
        for j in range(m):
            yj = coords[j]
            base_j = (base_i + j) * m
            for k in range(m):
                values[base_j + k] = lid(xi, yj, coords[k])
    return values, coords


# ----------------------------------------------------------------------------
# Calibrate half-thickness t so solid fraction (|F|<=t) == 1 - porosity
# ----------------------------------------------------------------------------
def calibrate_thickness(values, target_solid_fraction):
    absvals = sorted(abs(v) for v in values)
    idx = int(round(target_solid_fraction * (len(absvals) - 1)))
    idx = max(0, min(idx, len(absvals) - 1))
    t = absvals[idx]
    # measured solid fraction at this t
    solid = sum(1 for v in absvals if v <= t)
    return t, solid / len(absvals)


# ----------------------------------------------------------------------------
# Marching tetrahedra (no big lookup tables required)
# ----------------------------------------------------------------------------
# 8 cube corners -> offsets
CORNER = [
    (0, 0, 0),  # 0
    (1, 0, 0),  # 1
    (1, 1, 0),  # 2
    (0, 1, 0),  # 3
    (0, 0, 1),  # 4
    (1, 0, 1),  # 5
    (1, 1, 1),  # 6
    (0, 1, 1),  # 7
]
# decompose the cube into 6 tetrahedra sharing the main diagonal 0-6
TETS = [
    (0, 5, 1, 6),
    (0, 1, 2, 6),
    (0, 2, 3, 6),
    (0, 3, 7, 6),
    (0, 7, 4, 6),
    (0, 4, 5, 6),
]


def _interp(iso, pa, va, pb, vb):
    if abs(vb - va) < 1e-12:
        f = 0.5
    else:
        f = (iso - va) / (vb - va)
    return (pa[0] + f * (pb[0] - pa[0]),
            pa[1] + f * (pb[1] - pa[1]),
            pa[2] + f * (pb[2] - pa[2]))


def march_tet(iso, values, coords, n):
    """Extract triangles for isosurface F == iso. Returns list of (v0,v1,v2)."""
    m = n + 1
    tris = []

    def idx(i, j, k):
        return (i * m + j) * m + k

    for i in range(n):
        for j in range(n):
            for k in range(n):
                # gather 8 corner values + positions
                cv = [0.0] * 8
                cp = [None] * 8
                for c, (dx, dy, dz) in enumerate(CORNER):
                    ii, jj, kk = i + dx, j + dy, k + dz
                    cv[c] = values[idx(ii, jj, kk)]
                    cp[c] = (coords[ii], coords[jj], coords[kk])
                for (a, b, cc, d) in TETS:
                    _march_one_tet(iso, tris,
                                   cp[a], cv[a], cp[b], cv[b],
                                   cp[cc], cv[cc], cp[d], cv[d])
    return tris


def _march_one_tet(iso, tris, p0, v0, p1, v1, p2, v2, p3, v3):
    # inside == value < iso
    verts = [(p0, v0), (p1, v1), (p2, v2), (p3, v3)]
    inside = [i for i in range(4) if verts[i][1] < iso]
    outside = [i for i in range(4) if verts[i][1] >= iso]
    ni = len(inside)
    if ni == 0 or ni == 4:
        return
    if ni == 1:
        a = inside[0]
        pa, va = verts[a]
        e = [_interp(iso, pa, va, verts[o][0], verts[o][1]) for o in outside]
        tris.append((e[0], e[1], e[2]))
    elif ni == 3:
        a = outside[0]
        pa, va = verts[a]
        e = [_interp(iso, pa, va, verts[o][0], verts[o][1]) for o in inside]
        tris.append((e[0], e[1], e[2]))
    else:  # ni == 2 -> quad -> two triangles
        i0, i1 = inside
        o0, o1 = outside
        pA, vA = verts[i0]
        pB, vB = verts[i1]
        pC, vC = verts[o0]
        pD, vD = verts[o1]
        q0 = _interp(iso, pA, vA, pC, vC)
        q1 = _interp(iso, pA, vA, pD, vD)
        q2 = _interp(iso, pB, vB, pD, vD)
        q3 = _interp(iso, pB, vB, pC, vC)
        tris.append((q0, q1, q2))
        tris.append((q0, q2, q3))


# ----------------------------------------------------------------------------
# STL export (binary)
# ----------------------------------------------------------------------------
def write_binary_stl(path, triangles, scale):
    with open(path, "wb") as f:
        f.write(b"Lidinoid TPMS 95% porosity - stdlib generated".ljust(80, b" "))
        f.write(struct.pack("<I", len(triangles)))
        for (a, b, c) in triangles:
            ax, ay, az = a[0] * scale, a[1] * scale, a[2] * scale
            bx, by, bz = b[0] * scale, b[1] * scale, b[2] * scale
            cx, cy, cz = c[0] * scale, c[1] * scale, c[2] * scale
            # normal
            ux, uy, uz = bx - ax, by - ay, bz - az
            vx, vy, vz = cx - ax, cy - ay, cz - az
            nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
            ln = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
            f.write(struct.pack("<3f", nx / ln, ny / ln, nz / ln))
            f.write(struct.pack("<3f", ax, ay, az))
            f.write(struct.pack("<3f", bx, by, bz))
            f.write(struct.pack("<3f", cx, cy, cz))
            f.write(struct.pack("<H", 0))


# ----------------------------------------------------------------------------
# Minimal PNG writer + shaded rasterizer for a preview
# ----------------------------------------------------------------------------
class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w, self.h = w, h
        self.rgb = bytearray(w * h * 3)
        for i in range(w * h):
            self.rgb[i * 3] = bg[0]
            self.rgb[i * 3 + 1] = bg[1]
            self.rgb[i * 3 + 2] = bg[2]
        self.zbuf = [1e30] * (w * h)

    def put(self, x, y, z, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            p = y * self.w + x
            if z < self.zbuf[p]:
                self.zbuf[p] = z
                self.rgb[p * 3] = color[0]
                self.rgb[p * 3 + 1] = color[1]
                self.rgb[p * 3 + 2] = color[2]

    def save_png(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)
            raw.extend(self.rgb[y * self.w * 3:(y + 1) * self.w * 3])
        comp = zlib.compress(bytes(raw), 9)

        def chunk(tag, data):
            c = struct.pack("<I", len(data))[::-1] + tag + data
            crc = zlib.crc32(tag + data) & 0xffffffff
            return c + struct.pack("<I", crc)[::-1]

        with open(path, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")
            ihdr = struct.pack("<I", self.w)[::-1] + struct.pack("<I", self.h)[::-1] + bytes([8, 2, 0, 0, 0])
            f.write(chunk(b"IHDR", ihdr))
            f.write(chunk(b"IDAT", comp))
            f.write(chunk(b"IEND", b""))


def fill_triangle(cv, s0, s1, s2, color):
    (x0, y0, z0) = s0
    (x1, y1, z1) = s1
    (x2, y2, z2) = s2
    minx = max(0, int(math.floor(min(x0, x1, x2))))
    maxx = min(cv.w - 1, int(math.ceil(max(x0, x1, x2))))
    miny = max(0, int(math.floor(min(y0, y1, y2))))
    maxy = min(cv.h - 1, int(math.ceil(max(y0, y1, y2))))
    denom = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    if abs(denom) < 1e-9:
        return
    inv = 1.0 / denom
    for py in range(miny, maxy + 1):
        for px in range(minx, maxx + 1):
            a = ((y1 - y2) * (px - x2) + (x2 - x1) * (py - y2)) * inv
            b = ((y2 - y0) * (px - x2) + (x0 - x2) * (py - y2)) * inv
            c = 1.0 - a - b
            if a >= -1e-6 and b >= -1e-6 and c >= -1e-6:
                z = a * z0 + b * z1 + c * z2
                cv.put(px, py, z, color)


def render_preview(path, triangles, size=900):
    cv = Canvas(size, size, bg=(245, 247, 250))
    # rotation angles
    ax, ay = 0.55, 0.7
    ca, sa = math.cos(ax), math.sin(ax)
    cb, sb = math.cos(ay), math.sin(ay)
    light = (0.4, 0.5, 0.75)
    ln = math.sqrt(sum(v * v for v in light))
    light = (light[0] / ln, light[1] / ln, light[2] / ln)
    base = (46, 117, 182)
    scale = size * 0.62
    cx = cy = size / 2

    def project(p):
        x, y, z = p[0] - 0.5, p[1] - 0.5, p[2] - 0.5
        # rotate about X
        y2 = y * ca - z * sa
        z2 = y * sa + z * ca
        # rotate about Y
        x2 = x * cb + z2 * sb
        z3 = -x * sb + z2 * cb
        sx = cx + scale * x2
        sy = cy - scale * y2
        return (sx, sy, z3)

    for (p0, p1, p2) in triangles:
        # normal in world space
        ux, uy, uz = p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]
        vx, vy, vz = p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2]
        nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
        nl = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
        dot = abs((nx * light[0] + ny * light[1] + nz * light[2]) / nl)
        shade = 0.28 + 0.72 * dot
        color = (min(255, int(base[0] * shade)),
                 min(255, int(base[1] * shade)),
                 min(255, int(base[2] * shade)))
        s0, s1, s2 = project(p0), project(p1), project(p2)
        fill_triangle(cv, s0, s1, s2, color)
    cv.save_png(path)


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Sampling Lidinoid field on {N}^3 grid ...")
    values, coords = sample_field(N)

    target_solid = 1.0 - TARGET_POROSITY
    t, measured_solid = calibrate_thickness(values, target_solid)
    print(f"Calibrated half-thickness t = {t:.5f}")
    print(f"Target porosity  = {TARGET_POROSITY*100:.2f}%")
    print(f"Achieved porosity= {(1.0 - measured_solid)*100:.2f}%  "
          f"(solid fraction {measured_solid*100:.2f}%)")

    print("Extracting isosurfaces F = +t and F = -t (marching tetrahedra) ...")
    tris = march_tet(+t, values, coords, N)
    tris += march_tet(-t, values, coords, N)
    print(f"Triangles: {len(tris)}")

    stl_path = os.path.join(OUTPUT_DIR, "Lidinoid_porosity95.stl")
    write_binary_stl(stl_path, tris, scale=UNIT_CELL_MM)
    print(f"Wrote STL  -> {stl_path}  ({os.path.getsize(stl_path)} bytes)")

    png_path = os.path.join(OUTPUT_DIR, "Lidinoid_porosity95.png")
    render_preview(png_path, tris)
    print(f"Wrote PNG  -> {png_path}  ({os.path.getsize(png_path)} bytes)")

    # summary file
    with open(os.path.join(OUTPUT_DIR, "Lidinoid_porosity95_report.txt"), "w") as f:
        f.write("Lidinoid TPMS porous solid\n")
        f.write("==========================\n")
        f.write(f"Grid resolution      : {N}^3 cells per unit cell\n")
        f.write(f"Unit cell size       : {UNIT_CELL_MM} mm\n")
        f.write(f"Target porosity      : {TARGET_POROSITY*100:.2f}%\n")
        f.write(f"Achieved porosity    : {(1.0 - measured_solid)*100:.2f}%\n")
        f.write(f"Half-wall thickness t : {t:.6f} (iso-value units)\n")
        f.write(f"Triangles            : {len(tris)}\n")
    print("Done.")


if __name__ == "__main__":
    main()
