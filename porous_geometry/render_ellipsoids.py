#!/usr/bin/env python3
"""
Pure-stdlib software renderer for the packed-ELLIPSOID .dat files produced by
ellipsoid_geometry.f90.  No numpy / matplotlib / PIL required.

Each ellipsoid is defined by centre (x,y,z), semi-axes (a,b,c) and ZXZ Euler
angles (phi,theta,psi).  For each screen pixel we solve the ray-ellipsoid
intersection analytically, keep the nearest hit via a z-buffer, and apply
Lambert + specular shading.  Ellipsoids are coloured by height (z) with a
viridis-like map, matching the reference figure's left panels.

usage: python3 render_ellipsoids.py <ellipsoids.dat> <out.png>
"""
import sys, math, struct, zlib

W, H = 900, 820
BG = (255, 255, 255)
LDOM = 25.0

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

def euler_matrix(phi, theta, psi):
    c1, s1 = math.cos(phi), math.sin(phi)
    c2, s2 = math.cos(theta), math.sin(theta)
    c3, s3 = math.cos(psi), math.sin(psi)
    return [
        [ c1*c3 - s1*c2*s3, -c1*s3 - s1*c2*c3,  s1*s2],
        [ s1*c3 + c1*c2*s3, -s1*s3 + c1*c2*c3, -c1*s2],
        [ s2*s3,             s2*c3,             c2   ],
    ]

def read_ellipsoids(path):
    E = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            p = [float(v) for v in line.split()]
            E.append(p[:9])   # x y z a b c phi theta psi
    return E

def write_png(path, w, h, rgb):
    def chunk(tag, data):
        c = struct.pack('>I', len(data)) + tag + data
        return c + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw.extend(rgb[y * w * 3:(y + 1) * w * 3])
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)))
        f.write(chunk(b'IDAT', zlib.compress(bytes(raw), 9)))
        f.write(chunk(b'IEND', b''))

def render(ells, out):
    # camera basis: same isometric view as the sphere renderer
    az = math.radians(-35.0); el = math.radians(22.0)
    ca, sa = math.cos(az), math.sin(az)
    ce, se = math.cos(el), math.sin(el)
    c = LDOM / 2.0

    # world axes: screen-right (u), screen-up (v), view direction into screen (w)
    # from the sphere renderer's rot():
    #   sx = -sa*x + ca*y
    #   sy =  ce*z - se*(ca*x + sa*y)
    #   depth = se*z + ce*(ca*x + sa*y)
    u_ax = (-sa,        ca,        0.0)
    v_ax = (-se*ca,    -se*sa,     ce )
    w_ax = ( ce*ca,     ce*sa,     se )   # + = towards viewer

    def project(x, y, z):
        x -= c; y -= c; z -= c
        sx = u_ax[0]*x + u_ax[1]*y + u_ax[2]*z
        sy = v_ax[0]*x + v_ax[1]*y + v_ax[2]*z
        dp = w_ax[0]*x + w_ax[1]*y + w_ax[2]*z
        return sx, sy, dp

    # extents for scaling
    pts = [project(e[0], e[1], e[2]) for e in ells]
    maxax = max(max(e[3], e[4], e[5]) for e in ells)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    xmin, xmax = min(xs)-maxax, max(xs)+maxax
    ymin, ymax = min(ys)-maxax, max(ys)+maxax
    span = max(xmax-xmin, ymax-ymin)
    margin = 60
    scale = (min(W, H) - 2*margin) / span
    ox = (W - (xmax+xmin)*scale) / 2.0
    oy = (H - (ymax+ymin)*scale) / 2.0

    def to_px(sx, sy):
        return ox + sx*scale, H - (oy + sy*scale)

    zmin = min(e[2] for e in ells); zmax = max(e[2] for e in ells)

    fb = bytearray()
    for _ in range(W*H):
        fb += bytes(BG)
    zbuf = [-1e30]*(W*H)

    # light towards viewer, upper-left
    L = (-0.4, 0.5, 0.75)
    ln = math.sqrt(sum(v*v for v in L)); L = tuple(v/ln for v in L)

    order = sorted(range(len(ells)), key=lambda i: pts[i][2])

    for idx in order:
        x, y, z, a, b, cc, phi, th, psi = ells[idx]
        R = euler_matrix(phi, th, psi)      # body->world
        inv = (1.0/a, 1.0/b, 1.0/cc)
        pcx, pcy = to_px(*pts[idx][:2])
        rp = max(a, b, cc) * scale          # pixel bound (superset)
        base = colormap((z - zmin) / (zmax - zmin + 1e-12))

        i0 = max(0, int(pcx-rp)); i1 = min(W-1, int(pcx+rp)+1)
        j0 = max(0, int(pcy-rp)); j1 = min(H-1, int(pcy+rp)+1)

        for py in range(j0, j1+1):
            for px in range(i0, i1+1):
                # world-space ray: origin far behind along -w through this pixel
                su = (px - ox) / scale
                sv = (H - py - oy) / scale
                # point on the view plane (through domain centre) in world coords
                ox_w = c + su*u_ax[0] + sv*v_ax[0]
                oy_w = c + su*u_ax[1] + sv*v_ax[1]
                oz_w = c + su*u_ax[2] + sv*v_ax[2]
                # ray direction = -w (into the screen)
                dx, dy, dz = -w_ax[0], -w_ax[1], -w_ax[2]

                # translate to ellipsoid centre
                px0 = ox_w - x; py0 = oy_w - y; pz0 = oz_w - z
                # rotate origin & dir into body frame (u = R^T d)
                obx = R[0][0]*px0 + R[1][0]*py0 + R[2][0]*pz0
                oby = R[0][1]*px0 + R[1][1]*py0 + R[2][1]*pz0
                obz = R[0][2]*px0 + R[1][2]*py0 + R[2][2]*pz0
                dbx = R[0][0]*dx + R[1][0]*dy + R[2][0]*dz
                dby = R[0][1]*dx + R[1][1]*dy + R[2][1]*dz
                dbz = R[0][2]*dx + R[1][2]*dy + R[2][2]*dz
                # scale by inverse semi-axes -> unit sphere space
                oxs = obx*inv[0]; oys = oby*inv[1]; ozs = obz*inv[2]
                dxs = dbx*inv[0]; dys = dby*inv[1]; dzs = dbz*inv[2]

                Aq = dxs*dxs + dys*dys + dzs*dzs
                Bq = 2.0*(oxs*dxs + oys*dys + ozs*dzs)
                Cq = oxs*oxs + oys*oys + ozs*ozs - 1.0
                disc = Bq*Bq - 4.0*Aq*Cq
                if disc < 0.0:
                    continue
                sq = math.sqrt(disc)
                t = (-Bq - sq) / (2.0*Aq)          # nearest (towards viewer)
                # depth of the hit (world), + = closer
                hx = ox_w + t*dx; hy = oy_w + t*dy; hz = oz_w + t*dz
                depth = (w_ax[0]*(hx-c) + w_ax[1]*(hy-c) + w_ax[2]*(hz-c))
                k = py*W + px
                if depth <= zbuf[k]:
                    continue
                zbuf[k] = depth

                # surface normal (world): grad of implicit form
                #   body-frame point:
                bx = obx + t*dbx; by = oby + t*dby; bz = obz + t*dbz
                gx = 2.0*bx*inv[0]*inv[0]
                gy = 2.0*by*inv[1]*inv[1]
                gz = 2.0*bz*inv[2]*inv[2]
                # rotate gradient back to world (n = R g)
                nx = R[0][0]*gx + R[0][1]*gy + R[0][2]*gz
                ny = R[1][0]*gx + R[1][1]*gy + R[1][2]*gz
                nz = R[2][0]*gx + R[2][1]*gy + R[2][2]*gz
                nn = math.sqrt(nx*nx+ny*ny+nz*nz) + 1e-12
                nx/=nn; ny/=nn; nz/=nn
                # face the viewer
                if nx*w_ax[0]+ny*w_ax[1]+nz*w_ax[2] < 0:
                    nx,ny,nz = -nx,-ny,-nz
                diff = max(0.0, nx*L[0]+ny*L[1]+nz*L[2])
                shade = 0.30 + 0.70*diff
                spec = diff**24 * 0.5
                r8 = min(255, int(base[0]*shade + 255*spec))
                g8 = min(255, int(base[1]*shade + 255*spec))
                b8 = min(255, int(base[2]*shade + 255*spec))
                o = k*3
                fb[o]=r8; fb[o+1]=g8; fb[o+2]=b8

    for xx in range(W):
        for yy in (0,1,H-2,H-1):
            o=(yy*W+xx)*3; fb[o]=fb[o+1]=fb[o+2]=120
    for yy in range(H):
        for xx in (0,1,W-2,W-1):
            o=(yy*W+xx)*3; fb[o]=fb[o+1]=fb[o+2]=120

    write_png(out, W, H, fb)
    print(f"wrote {out}  ({len(ells)} ellipsoids)")

if __name__ == '__main__':
    render(read_ellipsoids(sys.argv[1]), sys.argv[2])
