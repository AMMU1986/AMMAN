#!/usr/bin/env python3
"""
Dependency-free isometric renderer for the Battery/PCM pack geometry.

Reads the cell centres produced by battery_pcm_geometry.f90
(battery_centres.dat) and ray-casts a translucent PCM block with the
embedded cylindrical batteries, writing 'battery_pcm_render.png'.

Uses only the Python standard library (math, struct, zlib).
"""
import math, struct, zlib

# ---- block dimensions (must match the Fortran program) ----
Lx, Ly, Lz = 92.0, 92.0, 65.0

# ---- read cell centres ----
cyls = []
r_cell = 9.0
with open("battery_centres.dat") as fh:
    for line in fh:
        if line.startswith("#") or not line.strip():
            continue
        p = line.split()
        xc, yc, r = float(p[1]), float(p[2]), float(p[3])
        r_cell = r
        cyls.append((xc, yc, r))

# ---- image / camera ----
W, H = 620, 500
cx, cy, cz = Lx/2, Ly/2, Lz/2                       # scene centre
az, el = math.radians(48.0), math.radians(26.0)      # isometric-ish view

# camera direction (from centre towards camera)
cam = (math.cos(el)*math.cos(az), math.cos(el)*math.sin(az), math.sin(el))
def norm(v):
    m = math.sqrt(v[0]**2+v[1]**2+v[2]**2)
    return (v[0]/m, v[1]/m, v[2]/m)
def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def dot(a,b):
    return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]

f = norm((-cam[0], -cam[1], -cam[2]))                # forward (into scene)
r = norm(cross(f, (0,0,1)))                          # screen right
u = cross(r, f)                                      # screen up

HALF = 62.0                                          # ortho half-height (world units)
aspect = W/H
half_w, half_h = HALF*aspect, HALF
BIG = 1000.0
Lgt = norm((-0.4, -0.55, 0.9))                       # light direction

box_col  = (150, 205, 150)                           # PCM green
cyl_col  = (176, 214, 170)                           # battery green
bg       = (255, 255, 255)

def shade(base, n):
    d = max(0.0, dot(n, Lgt))
    k = 0.40 + 0.60*d
    return (base[0]*k, base[1]*k, base[2]*k)

def hit_cylinders(ox,oy,oz,dx,dy,dz):
    """nearest cylinder hit -> (t, normal, base_color) or None"""
    best_t = 1e18; best_n=None
    for (xcc,ycc,rr) in cyls:
        # side
        a = dx*dx+dy*dy
        if a > 1e-12:
            bx, by = ox-xcc, oy-ycc
            b = 2*(bx*dx+by*dy)
            c = bx*bx+by*by-rr*rr
            disc = b*b-4*a*c
            if disc >= 0:
                sq = math.sqrt(disc)
                for t in ((-b-sq)/(2*a), (-b+sq)/(2*a)):
                    if 1e-4 < t < best_t:
                        z = oz+t*dz
                        if 0.0 <= z <= Lz:
                            px, py = ox+t*dx, oy+t*dy
                            best_t = t
                            best_n = ((px-xcc)/rr, (py-ycc)/rr, 0.0)
        # top / bottom caps
        if abs(dz) > 1e-12:
            for (zc, nz) in ((Lz, 1.0), (0.0, -1.0)):
                t = (zc-oz)/dz
                if 1e-4 < t < best_t:
                    px, py = ox+t*dx, oy+t*dy
                    if (px-xcc)**2+(py-ycc)**2 <= rr*rr:
                        best_t = t; best_n = (0.0,0.0,nz)
    if best_n is None:
        return None
    return best_t, best_n

def box_slab(ox,oy,oz,dx,dy,dz):
    """entry/exit t through the axis-aligned block, plus entry face normal"""
    tmin, tmax = -1e18, 1e18
    nmin = (0,0,0)
    for (o,d,lo,hi,axis) in ((ox,dx,0,Lx,0),(oy,dy,0,Ly,1),(oz,dz,0,Lz,2)):
        if abs(d) < 1e-12:
            if o < lo or o > hi:
                return None
            continue
        t1, t2 = (lo-o)/d, (hi-o)/d
        n1 = [0,0,0]; n1[axis] = -1
        n2 = [0,0,0]; n2[axis] =  1
        if t1 > t2:
            t1,t2 = t2,t1; n1,n2 = n2,n1
        if t1 > tmin:
            tmin = t1; nmin = tuple(n1)
        if t2 < tmax:
            tmax = t2
    if tmax < max(tmin, 0):
        return None
    return tmin, tmax, nmin

def blend(fg, a, bgc):
    return (fg[0]*a+bgc[0]*(1-a), fg[1]*a+bgc[1]*(1-a), fg[2]*a+bgc[2]*(1-a))

pixels = bytearray(W*H*3)

for j in range(H):
    sy = (1 - (j+0.5)/H*2)*half_h
    for i in range(W):
        sx = ((i+0.5)/W*2 - 1)*half_w
        ox = cx + r[0]*sx + u[0]*sy - f[0]*BIG
        oy = cy + r[1]*sx + u[1]*sy - f[1]*BIG
        oz = cz + r[2]*sx + u[2]*sy - f[2]*BIG
        dx,dy,dz = f

        col = bg
        slab = box_slab(ox,oy,oz,dx,dy,dz)
        cyl  = hit_cylinders(ox,oy,oz,dx,dy,dz)

        if slab is None and cyl is None:
            pass
        else:
            if cyl is not None:
                tc, nc = cyl
                base = shade(cyl_col, nc)
                # purple rim on top cap edge
                if abs(nc[2]) > 0.5:
                    px, py = ox+tc*dx, oy+tc*dy
                    for (xcc,ycc,rr) in cyls:
                        dd = math.sqrt((px-xcc)**2+(py-ycc)**2)
                        if rr-1.1 <= dd <= rr:
                            base = (120, 70, 150)
                            break
                col = base
                # translucent PCM in front of the cylinder
                if slab is not None:
                    tin, tout, _ = slab
                    front = max(0.0, tc - max(tin, 0.0))
                    a = min(0.5, 1-math.exp(-0.010*front))
                    col = blend(box_col, a, col)
            else:
                tin, tout, nin = slab
                tin = max(tin, 0.0)
                thick = tout - tin
                a = min(0.72, 1-math.exp(-0.0075*thick))
                face = shade(box_col, nin)
                col = blend(face, a, bg)

        o = (j*W+i)*3
        pixels[o]   = max(0,min(255,int(col[0])))
        pixels[o+1] = max(0,min(255,int(col[1])))
        pixels[o+2] = max(0,min(255,int(col[2])))

# ---------- overlay: project box edges & cylinder top rims ----------
def project(P):
    rel = (P[0]-cx, P[1]-cy, P[2]-cz)
    sx = dot(rel, r); sy = dot(rel, u)
    px = (sx/half_w + 1)/2*W - 0.5
    py = (1 - sy/half_h)/2*H - 0.5
    return px, py

def setpx(x,y,c):
    xi,yi = int(round(x)), int(round(y))
    if 0<=xi<W and 0<=yi<H:
        o=(yi*W+xi)*3
        pixels[o],pixels[o+1],pixels[o+2]=c

def line(P,Q,c):
    x0,y0=project(P); x1,y1=project(Q)
    n=int(max(abs(x1-x0),abs(y1-y0)))+1
    for k in range(n+1):
        t=k/n
        setpx(x0+(x1-x0)*t, y0+(y1-y0)*t, c)
        setpx(x0+(x1-x0)*t+1, y0+(y1-y0)*t, c)

# box corners & 12 edges
C=[(0,0,0),(Lx,0,0),(Lx,Ly,0),(0,Ly,0),(0,0,Lz),(Lx,0,Lz),(Lx,Ly,Lz),(0,Ly,Lz)]
E=[(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
for a,b in E:
    line(C[a],C[b],(70,90,70))

# cylinder top rims (purple)
for (xcc,ycc,rr) in cyls:
    prev=None
    for s in range(0,73):
        ang=2*math.pi*s/72
        P=(xcc+rr*math.cos(ang), ycc+rr*math.sin(ang), Lz)
        if prev: line(prev,P,(120,70,150))
        prev=P

# ---------- write PNG ----------
def write_png(path, w, h, rgb):
    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ+data) & 0xffffffff)
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw.extend(rgb[y*w*3:(y+1)*w*3])
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    with open(path,"wb") as fp:
        fp.write(sig)
        fp.write(chunk(b"IHDR", ihdr))
        fp.write(chunk(b"IDAT", zlib.compress(bytes(raw),9)))
        fp.write(chunk(b"IEND", b""))

write_png("battery_pcm_render.png", W, H, pixels)
print("wrote battery_pcm_render.png  (%dx%d)  cells=%d  r=%.2f mm" % (W,H,len(cyls),r_cell))
