#!/usr/bin/env python3
"""
Generate an AutoCAD DXF (R12 ASCII) pictorial of a single-V groove butt-weld
joint between two plates, reproducing the reference figure:

  - two plates, 6 mm thick, widths 75 / 12 / 75 mm across, 250 mm long
  - single-V groove: 60 deg included angle, 2 mm root gap, 1 mm root face
  - grey weld bead filling the groove and running along the joint
  - multi-pass electrode callouts  E6018 / E7018 / E9018
  - red "Weld bead" arrow,  "(a)" label
  - dimensions: 6 mm, 75 mm, 12 mm, 75 mm (bead), 250 mm, 60 deg

Pure standard library (writes DXF text directly). Opens in AutoCAD, BricsCAD,
LibreCAD, DraftSight, etc.
"""

import math

OUT = '/projects/sandbox/AMMAN/Weld_Joint_Drawing.dxf'

# ----- isometric-style projection: model (w across, l along, t thickness) -----
ALPHA = math.radians(26.0)
LX, LY = math.cos(ALPHA), math.sin(ALPHA)   # length axis (up-right)


def P(w, l, t=0.0):
    """Project model point to 2-D paper coordinates."""
    return (w + l * LX, l * LY - t)


# ------------------------------- DXF writer -----------------------------------
class DXF:
    def __init__(self):
        self.layers = []          # (name, color)
        self.e = []               # entity strings

    def layer(self, name, color):
        self.layers.append((name, color))

    def line(self, p1, p2, layer, w=0.0):
        s = ['0', 'LINE', '8', layer]
        if w:
            s += ['39', f'{w}']
        s += ['10', f'{p1[0]:.4f}', '20', f'{p1[1]:.4f}', '30', '0',
              '11', f'{p2[0]:.4f}', '21', f'{p2[1]:.4f}', '31', '0']
        self.e += s

    def pl(self, pts, layer):
        for a, b in zip(pts, pts[1:]):
            self.line(a, b, layer)

    def text(self, p, h, s, layer, rot=0.0, halign=0, valign=0):
        ent = ['0', 'TEXT', '8', layer,
               '10', f'{p[0]:.4f}', '20', f'{p[1]:.4f}', '30', '0',
               '40', f'{h:.4f}', '1', s, '50', f'{rot:.4f}', '7', 'STANDARD']
        if halign or valign:
            ent += ['72', str(halign), '73', str(valign),
                    '11', f'{p[0]:.4f}', '21', f'{p[1]:.4f}', '31', '0']
        self.e += ent

    def solid(self, pts, layer):
        # pts in order around the quad/triangle; DXF needs 3rd/4th swapped
        q = list(pts)
        if len(q) == 3:
            q = [q[0], q[1], q[2], q[2]]
        a, b, c, d = q[0], q[1], q[2], q[3]
        order = [a, b, d, c]   # swap for DXF SOLID fill
        s = ['0', 'SOLID', '8', layer]
        for i, pt in enumerate(order):
            s += [f'1{i}', f'{pt[0]:.4f}', f'2{i}', f'{pt[1]:.4f}', f'3{i}', '0']
        self.e += s

    def arc(self, c, r, a0, a1, layer):
        self.e += ['0', 'ARC', '8', layer,
                   '10', f'{c[0]:.4f}', '20', f'{c[1]:.4f}', '30', '0',
                   '40', f'{r:.4f}', '50', f'{a0:.4f}', '51', f'{a1:.4f}']

    def arrow(self, tip, ang, layer, size=4.0):
        """Filled triangular arrowhead; ang = direction tail->tip (deg)."""
        a = math.radians(ang)
        back = (tip[0] - size * math.cos(a), tip[1] - size * math.sin(a))
        pw = size * 0.38
        n = (math.cos(a + math.pi / 2), math.sin(a + math.pi / 2))
        b1 = (back[0] + pw * n[0], back[1] + pw * n[1])
        b2 = (back[0] - pw * n[0], back[1] - pw * n[1])
        self.solid([tip, b1, b2], layer)

    def dim_lin(self, p1, p2, layer, h=6.0, text=None, rot=0.0, toff=3.0):
        """Dimension line between p1,p2 with inward arrows and centred text."""
        ang = math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))
        self.line(p1, p2, layer)
        self.arrow(p1, ang + 180, layer)
        self.arrow(p2, ang, layer)
        if text:
            mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            pa = math.radians(ang + 90)
            self.text((mx + toff * math.cos(pa), my + toff * math.sin(pa)),
                      h, text, layer, rot=rot, halign=1, valign=0)

    def save(self, path):
        out = ['0', 'SECTION', '2', 'HEADER',
               '9', '$ACADVER', '1', 'AC1009',
               '9', '$INSUNITS', '70', '4',
               '0', 'ENDSEC',
               '0', 'SECTION', '2', 'TABLES',
               '0', 'TABLE', '2', 'LAYER', '70', str(len(self.layers))]
        for name, color in self.layers:
            out += ['0', 'LAYER', '2', name, '70', '0', '62', str(color), '6', 'CONTINUOUS']
        out += ['0', 'ENDTAB', '0', 'ENDSEC',
                '0', 'SECTION', '2', 'ENTITIES']
        out += self.e
        out += ['0', 'ENDSEC', '0', 'EOF']
        with open(path, 'w') as f:
            f.write('\n'.join(out) + '\n')


# --------------------------------- geometry -----------------------------------
d = DXF()
d.layer('OUTLINE', 7)      # black plate outline
d.layer('BEAD', 8)         # grey weld bead
d.layer('DIM', 7)          # black dimensions / leaders
d.layer('TEXT', 7)         # black annotation text
d.layer('ELEC', 7)         # electrode labels
d.layer('RED', 1)          # red weld-bead arrow / label

# plate / groove parameters (mm)
W1, GAP, W2 = 75.0, 12.0, 75.0           # across-widths
WL = W1                                   # left plate inner top edge
WR = W1 + GAP                             # right plate inner top edge
WT = W1 + GAP + W2                        # total width = 162
LEN = 250.0                               # length along joint
TH = 6.0                                  # thickness
RG = 2.0                                  # root gap
RF = 1.0                                  # root face
# groove root edges (bottom), centred
RL = (WL + WR) / 2 - RG / 2               # 80
RR = (WL + WR) / 2 + RG / 2               # 82
RD = TH - RF                              # bevel depth = 5 (root face from t=5..6)

# ---- grey weld-bead fills (draw first, under the outline) ----
# top strip of the groove running the full length
d.solid([P(WL, 0, 0), P(WR, 0, 0), P(WR, LEN, 0), P(WL, LEN, 0)], 'BEAD')
# front cross-section V-fill (two quads: bevel trapezoid + root rectangle)
d.solid([P(WL, 0, 0), P(WR, 0, 0), P(RR, 0, RD), P(RL, 0, RD)], 'BEAD')
d.solid([P(RL, 0, RD), P(RR, 0, RD), P(RR, 0, TH), P(RL, 0, TH)], 'BEAD')

# ---- left plate top face ----
d.pl([P(0, 0, 0), P(WL, 0, 0), P(WL, LEN, 0), P(0, LEN, 0), P(0, 0, 0)], 'OUTLINE')
# ---- right plate top face ----
d.pl([P(WR, 0, 0), P(WT, 0, 0), P(WT, LEN, 0), P(WR, LEN, 0), P(WR, 0, 0)], 'OUTLINE')

# ---- front thickness face (l = 0) ----
# left plate front
d.pl([P(0, 0, 0), P(0, 0, TH), P(RL, 0, TH)], 'OUTLINE')
# right plate front
d.pl([P(WT, 0, 0), P(WT, 0, TH), P(RR, 0, TH)], 'OUTLINE')
# groove V profile at the front
d.pl([P(WL, 0, 0), P(RL, 0, RD), P(RL, 0, TH), P(RR, 0, TH), P(RR, 0, RD), P(WR, 0, 0)], 'OUTLINE')

# ---- right side thickness face (w = WT) ----
d.pl([P(WT, 0, TH), P(WT, LEN, TH), P(WT, LEN, 0)], 'OUTLINE')

# ================================ DIMENSIONS ==================================
# 6 mm thickness (vertical, left of front-left edge)
xo = -16.0
d.line(P(0, 0, 0), (xo, 0), 'DIM')
d.line(P(0, 0, TH), (xo, -TH), 'DIM')
d.dim_lin((xo, 0), (xo, -TH), 'DIM', h=5.5, text='6 mm', toff=-14)

# bottom widths 75 / 12 / 75 along the front bottom edge
yb = -TH
ext = -14.0
for wv in (0, WL, WR, WT):
    d.line(P(wv, 0, TH), (P(wv, 0, TH)[0], yb + ext - 2), 'DIM')
yd = yb + ext
d.dim_lin((0, yd), (WL, yd), 'DIM', h=6.0, text='75 mm', toff=-9)
d.dim_lin((WL, yd), (WR, yd), 'DIM', h=5.0)
d.text(((WL + WR) / 2, yd - 20), 5.5, '12 mm', 'DIM', halign=1)
d.line(((WL + WR) / 2, yd - 2), ((WL + WR) / 2, yd - 13), 'DIM')
d.dim_lin((WR, yd), (WT, yd), 'DIM', h=6.0, text='75 mm', toff=-9)

# 250 mm along the right outer long edge
p0, p1 = P(WT, 0, 0), P(WT, LEN, 0)
perp = (LY, -LX)                 # outward (right-down)
o = 22.0
q0 = (p0[0] + perp[0] * o, p0[1] + perp[1] * o)
q1 = (p1[0] + perp[0] * o, p1[1] + perp[1] * o)
d.line(p0, q0, 'DIM'); d.line(p1, q1, 'DIM')
d.dim_lin(q0, q1, 'DIM', h=6.5, text='250 mm', rot=math.degrees(ALPHA), toff=8)

# 75 mm along the weld bead (near portion)
wb = (WL + WR) / 2
b0, b1 = P(wb, 0, 0), P(wb, 75.0, 0)
nb = (-LY, LX)                   # offset up-left of bead
ob = 10.0
c0 = (b0[0] + nb[0] * ob, b0[1] + nb[1] * ob)
c1 = (b1[0] + nb[0] * ob, b1[1] + nb[1] * ob)
d.dim_lin(c0, c1, 'DIM', h=6.5, text='75 mm', rot=math.degrees(ALPHA), toff=7)

# 60 deg groove angle at the front apex
apex = P(wb, 0, RD)
d.text((apex[0] - 26, apex[1] + 8), 6.0, '60%%d', 'TEXT')   # %%d -> degree in CAD
a_l = math.degrees(math.atan2(P(WL, 0, 0)[1] - apex[1], P(WL, 0, 0)[0] - apex[0]))
a_r = math.degrees(math.atan2(P(WR, 0, 0)[1] - apex[1], P(WR, 0, 0)[0] - apex[0]))
d.arc(apex, 14.0, a_r, a_l, 'DIM')

# root gap / root face notes (on the right plate top face)
d.text(P(96, 70, 0), 6.0, 'Root gap: 2 mm', 'TEXT')
d.text(P(96, 52, 0), 6.0, 'Root face: 1 mm', 'TEXT')

# ============================ ELECTRODE CALLOUTS ==============================
elec = [
    ('E6018', (-78, 92), P(WL + 1, 30, 0.3)),      # cap pass (top)
    ('E7018', (-78, 74), P(WL + 2, 16, 2.2)),      # fill pass (mid)
    ('E9018', (-78, 56), P(RL + 0.3, 4, 4.4)),     # root pass (deep)
]
for name, tp, tgt in elec:
    d.text(tp, 7.0, name, 'ELEC')
    start = (tp[0] + 46, tp[1] + 3)
    d.line(start, tgt, 'ELEC')
    ang = math.degrees(math.atan2(tgt[1] - start[1], tgt[0] - start[0]))
    d.arrow(tgt, ang, 'ELEC', size=4.5)

# ============================ WELD BEAD (red) =================================
beadpt = P(wb, 120, -1)
rtxt = (beadpt[0] + 6, beadpt[1] + 48)
d.text((rtxt[0] - 4, rtxt[1] + 2), 9.0, 'Weld bead', 'RED')
d.line((rtxt[0] + 20, rtxt[1] - 4), (beadpt[0] + 2, beadpt[1] + 6), 'RED')
d.arrow((beadpt[0] + 2, beadpt[1] + 6),
        math.degrees(math.atan2((beadpt[1] + 6) - (rtxt[1] - 4),
                                (beadpt[0] + 2) - (rtxt[0] + 20))), 'RED', size=7.0)

# figure label (a)
d.text((P(WT, LEN, 0)[0] - 20, P(WT, LEN, 0)[1] + 18), 12.0, '(a)', 'TEXT')

d.save(OUT)
print('DXF written:', OUT)
