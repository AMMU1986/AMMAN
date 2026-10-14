#!/usr/bin/env python3
"""
Generate an AutoCAD DXF reproducing the welded-plate specimen-extraction
diagram (part b): a 3D plate showing the WELD, two HAZ bands and BASE metal,
with the extraction layout of the mechanical-test specimens
(Tensile-Weld, Tensile-HAZ, Impact-Weld, Impact-HAZ, Hardness, Metallographic),
plus the grooved cross-section (100 mm wide, 12 mm thick, 60 deg included angle).

Pure standard library - writes a minimal ASCII DXF (ENTITIES only) that opens
directly in AutoCAD / any DXF viewer. Colours use the AutoCAD Color Index (ACI).
"""

import math

OUT = '/projects/sandbox/AMMAN/Welding_Specimen_Extraction.dxf'

# AutoCAD Color Index
RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, MAGENTA = 1, 30, 2, 3, 4, 5, 6
PURPLE, BLACK, GRAY, WHITE = 214, 7, 8, 7

E = []  # entity strings


def _g(code, val):
    E.append(f"{code}\n{val}")


def line(x1, y1, x2, y2, color=BLACK, layer="OUTLINE"):
    _g(0, "LINE"); _g(8, layer); _g(62, color)
    _g(10, x1); _g(20, y1); _g(30, 0.0)
    _g(11, x2); _g(21, y2); _g(31, 0.0)


def solid(p1, p2, p3, p4, color, layer="FILL"):
    """Filled quad. AutoCAD fills p1->p2->p4->p3 (pass p3,p4 as the TOP edge)."""
    _g(0, "SOLID"); _g(8, layer); _g(62, color)
    _g(10, p1[0]); _g(20, p1[1]); _g(30, 0.0)
    _g(11, p2[0]); _g(21, p2[1]); _g(31, 0.0)
    _g(12, p3[0]); _g(22, p3[1]); _g(32, 0.0)
    _g(13, p4[0]); _g(23, p4[1]); _g(33, 0.0)


def fill_rect(x0, y0, x1, y1, color, layer="FILL"):
    solid((x0, y0), (x1, y0), (x0, y1), (x1, y1), color, layer)


def fill_quad(bl, br, tr, tl, color, layer="FILL"):
    solid(bl, br, tl, tr, color, layer)


def rect_outline(x0, y0, x1, y1, color=BLACK, layer="OUTLINE"):
    line(x0, y0, x1, y0, color, layer); line(x1, y0, x1, y1, color, layer)
    line(x1, y1, x0, y1, color, layer); line(x0, y1, x0, y0, color, layer)


def text(x, y, h, s, color=BLACK, layer="TEXT", center=True, rot=0):
    _g(0, "TEXT"); _g(8, layer); _g(62, color)
    _g(10, x); _g(20, y); _g(30, 0.0); _g(40, h); _g(1, s)
    if rot:
        _g(50, rot)
    _g(72, 1 if center else 0)
    _g(11, x); _g(21, y); _g(31, 0.0)


def arc(cx, cy, r, a0, a1, color=BLACK, layer="DIM"):
    _g(0, "ARC"); _g(8, layer); _g(62, color)
    _g(10, cx); _g(20, cy); _g(30, 0.0); _g(40, r); _g(50, a0); _g(51, a1)


def hatch_rect(x0, y0, x1, y1, color, layer, spacing=7.0):
    """45-degree hatch lines clipped to a rectangle (slope +1, x - y = k)."""
    k = x0 - y1
    kmax = x1 - y0
    while k <= kmax:
        xa = max(x0, y0 + k)
        xb = min(x1, y1 + k)
        if xb > xa:
            line(xa, xa - k, xb, xb - k, color, layer)
        k += spacing * math.sqrt(2)


def arrow(x, y, dx, dy, color=BLACK, layer="DIM", size=6):
    """Small filled triangular arrowhead pointing in direction (dx,dy)."""
    ang = math.atan2(dy, dx)
    a1 = ang + math.radians(160)
    a2 = ang - math.radians(160)
    p1 = (x, y)
    p2 = (x + size * math.cos(a1), y + size * math.sin(a1))
    p3 = (x + size * math.cos(a2), y + size * math.sin(a2))
    solid(p1, p2, p3, p3, color, layer)


def dogbone(x0, x1, cy, grip_h, waist_h, color, layer):
    """Horizontal tensile dog-bone filled with trapezoids + rectangles."""
    span = x1 - x0
    g = span * 0.22      # grip length
    t = span * 0.12      # taper length
    gh = grip_h / 2.0
    wh = waist_h / 2.0
    xa, xb = x0 + g, x0 + g + t
    xc, xd = x1 - g - t, x1 - g
    fill_rect(x0, cy - gh, xa, cy + gh, color, layer)          # left grip
    fill_quad((xa, cy - gh), (xb, cy - wh), (xb, cy + wh), (xa, cy + gh), color, layer)
    fill_rect(xb, cy - wh, xc, cy + wh, color, layer)          # waist
    fill_quad((xc, cy - wh), (xd, cy - gh), (xd, cy + gh), (xc, cy + wh), color, layer)
    fill_rect(xd, cy - gh, x1, cy + gh, color, layer)          # right grip
    # outline
    for (ax, ay, bx, by) in [
        (x0, cy - gh, xa, cy - gh), (xa, cy - gh, xb, cy - wh),
        (xb, cy - wh, xc, cy - wh), (xc, cy - wh, xd, cy - gh),
        (xd, cy - gh, x1, cy - gh), (x1, cy - gh, x1, cy + gh),
        (x1, cy + gh, xd, cy + gh), (xd, cy + gh, xc, cy + wh),
        (xc, cy + wh, xb, cy + wh), (xb, cy + wh, xa, cy + gh),
        (xa, cy + gh, x0, cy + gh), (x0, cy + gh, x0, cy - gh)]:
        line(ax, ay, bx, by, BLACK, layer)


# ======================================================================
#  TOP SCHEMATIC  (3D plate with weld / HAZ / base + specimen layout)
# ======================================================================
# front face
FX0, FY0, FX1, FY1 = 0.0, 60.0, 240.0, 360.0
OX, OY = 36.0, 28.0          # isometric offset to back face

# weld + HAZ geometry (vertical bands)
WX0, WX1 = 107.0, 133.0      # weld band
HZL0, HZL1 = 93.0, 107.0     # left HAZ
HZR0, HZR1 = 133.0, 147.0    # right HAZ

# --- weld & HAZ hatched fills (background) ---
hatch_rect(WX0, FY0, WX1, FY1, RED, "WELD", spacing=7)
hatch_rect(HZL0, FY0, HZL1, FY1, ORANGE, "HAZ", spacing=6)
hatch_rect(HZR0, FY0, HZR1, FY1, ORANGE, "HAZ", spacing=6)
rect_outline(WX0, FY0, WX1, FY1, RED, "WELD")
rect_outline(HZL0, FY0, HZL1, FY1, ORANGE, "HAZ")
rect_outline(HZR0, FY0, HZR1, FY1, ORANGE, "HAZ")

# weld cap peak at the top of the plate
solid((WX0, FY1), (WX1, FY1), (120.0, FY1 + 30), (120.0, FY1 + 30), RED, "WELD")
line(WX0, FY1, 120.0, FY1 + 30, RED, "WELD")
line(WX1, FY1, 120.0, FY1 + 30, RED, "WELD")

# --- plate 3D box edges (drawn over bands so the box reads clearly) ---
rect_outline(FX0, FY0, FX1, FY1, BLACK, "OUTLINE")
line(FX0, FY1, FX0 + OX, FY1 + OY)          # top-left pillar
line(FX1, FY1, FX1 + OX, FY1 + OY)          # top-right pillar
line(FX1, FY0, FX1 + OX, FY0 + OY)          # bottom-right pillar
line(FX0 + OX, FY1 + OY, FX1 + OX, FY1 + OY)   # back top edge
line(FX1 + OX, FY1 + OY, FX1 + OX, FY0 + OY)   # back right edge

# --- zone labels ---
text(45, 188, 9, "BASE", BLACK)
text(196, 188, 9, "BASE", BLACK)
text(120, 183, 8, "WELD", BLACK)
text(100, 150, 7, "HAZ", BLACK, rot=90)
text(140, 150, 7, "HAZ", BLACK, rot=90)

# ======================================================================
#  SPECIMENS  (top -> bottom), drawn on top of the zones
# ======================================================================
# Tensile (weld)  - waist centred over the weld
dogbone(30, 210, 335, 30, 15, GREEN, "TENSILE")
text(120, 342, 6, "WELD", BLACK, layer="TENSILE")
text(192, 335, 6, "TENSILE (WELD)", BLACK, layer="TENSILE")

# Tensile (HAZ)   - shifted so the waist sits over the right HAZ
dogbone(30, 228, 300, 28, 14, GREEN, "TENSILE")
text(120, 300, 6, "HAZ", BLACK, layer="TENSILE")
text(205, 293, 6, "TENSILE (HAZ)", BLACK, layer="TENSILE")

# Impact (weld)   - bar centred on the weld
fill_rect(68, 258, 172, 282, BLUE, "IMPACT")
rect_outline(68, 258, 172, 282, BLACK, "IMPACT")
text(120, 270, 6, "IMPACT (WELD)", WHITE, layer="IMPACT")

# Impact (HAZ)    - bar over the right HAZ
fill_rect(112, 228, 216, 250, BLUE, "IMPACT")
rect_outline(112, 228, 216, 250, BLACK, "IMPACT")
text(164, 239, 6, "IMPACT (HAZ)", WHITE, layer="IMPACT")

# Hardness        - long traverse bar
fill_rect(20, 122, 220, 144, CYAN, "HARDNESS")
rect_outline(20, 122, 220, 144, BLACK, "HARDNESS")
text(120, 133, 7, "Hardness", BLACK, layer="HARDNESS")

# Metallographic  - long bar
fill_rect(18, 88, 232, 114, PURPLE, "METALLO")
rect_outline(18, 88, 232, 114, BLACK, "METALLO")
text(125, 101, 8, "Metallographic", WHITE, layer="METALLO")

# panel label (b)
rect_outline(4, 348, 34, 374, BLACK, "OUTLINE")
text(19, 361, 10, "(b)", BLACK)

# ======================================================================
#  CROSS-SECTION (single-V groove, 60 deg, 100 mm wide, 12 mm thick)
# ======================================================================
SCALE = 2.4                       # drawing units per mm
CW = 100 * SCALE                  # 240 units
TH = 12 * SCALE                   # 28.8 units
cx0, cy_top = 0.0, -40.0
cx1, cy_bot = cx0 + CW, cy_top - TH
cxc = (cx0 + cx1) / 2.0           # centre
depth = TH * 0.82                 # groove depth
gw = depth * math.tan(math.radians(30))   # half opening at top
root = (cxc, cy_top - depth)
cham = 10.0                       # outer top chamfers

# outline polyline (as connected lines)
pts = [
    (cx0, cy_bot), (cx1, cy_bot),            # bottom edge
    (cx1, cy_top - cham), (cx1 - cham, cy_top),  # top-right chamfer
    (cxc + gw, cy_top), root, (cxc - gw, cy_top),  # V groove
    (cx0 + cham, cy_top), (cx0, cy_top - cham),  # top-left chamfer
    (cx0, cy_bot)]
for i in range(len(pts) - 1):
    line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], BLACK, "SECTION")

# 60-degree included-angle callout
arc(root[0], root[1], 22, 60, 120, BLACK, "DIM")
text(cxc, cy_top + 14, 9, "60%%d", BLACK)

# width dimension (100 mm)
dy = cy_bot - 20
line(cx0, dy, cx1, dy, BLACK, "DIM")
line(cx0, cy_bot, cx0, dy - 4, BLACK, "DIM")
line(cx1, cy_bot, cx1, dy - 4, BLACK, "DIM")
arrow(cx0, dy, 1, 0); arrow(cx1, dy, -1, 0)
text(cxc, dy - 12, 9, "100 mm", BLACK)

# thickness dimension (12 mm)
dx = cx1 + 24
line(dx, cy_top, dx, cy_bot, BLACK, "DIM")
line(cx1, cy_top, dx + 4, cy_top, BLACK, "DIM")
line(cx1, cy_bot, dx + 4, cy_bot, BLACK, "DIM")
arrow(dx, cy_top, 0, -1); arrow(dx, cy_bot, 0, 1)
text(dx + 26, (cy_top + cy_bot) / 2, 9, "12 mm", BLACK)


# ======================================================================
def write_dxf(path):
    header = ["0", "SECTION", "2", "HEADER",
              "9", "$ACADVER", "1", "AC1009",
              "9", "$INSBASE", "10", "0.0", "20", "0.0", "30", "0.0",
              "9", "$EXTMIN", "10", "-40.0", "20", "-120.0", "30", "0.0",
              "9", "$EXTMAX", "10", "320.0", "20", "400.0", "30", "0.0",
              "0", "ENDSEC"]
    out = header + ["0", "SECTION", "2", "ENTITIES"] + E + ["0", "ENDSEC", "0", "EOF"]
    with open(path, "w") as f:
        f.write("\n".join(str(x) for x in out) + "\n")
    n = sum(1 for e in E if e.startswith("0\n"))
    print("wrote", path, "with", n, "entities")


if __name__ == "__main__":
    write_dxf(OUT)
