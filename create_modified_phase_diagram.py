#!/usr/bin/env python3
"""
Rebuilds the stainless-steel solidification phase diagram (Cr_eq/Ni_eq vs
Temperature) as a clean AutoCAD R12 ASCII DXF, applying a uniform ~30% change:

  * all geometry scaled by 1.30 (30% larger)
  * Temperature axis values increased 30%  (600..1600  ->  780..2080 degC)
  * Composition axis values increased 30%  (0.50..4.00 ->  0.65..5.20)

Greek phases are written in ASCII:  g = gamma (austenite),  d = delta (ferrite).
Only the Python standard library is used.
"""

import math

SCALE = 1.30                      # the 30% change factor
OUT = "Modified_Phase_Diagram.dxf"

# ---------------------------------------------------------------- DXF writer
_buf = []
def g(code, value):               # emit one group-code / value pair
    _buf.append(str(code))
    _buf.append(str(value))

def num(v):                       # tidy float formatting
    return ("%.6f" % v).rstrip("0").rstrip(".") if isinstance(v, float) else str(v)

def line(x1, y1, x2, y2, layer="0", color=None, ltype=None):
    g(0, "LINE"); g(8, layer)
    if color is not None: g(62, color)
    if ltype: g(6, ltype)
    g(10, num(x1)); g(20, num(y1)); g(30, 0)
    g(11, num(x2)); g(21, num(y2)); g(31, 0)

def polyline(points, layer="0", color=None, ltype=None):
    g(0, "POLYLINE"); g(8, layer)
    if color is not None: g(62, color)
    if ltype: g(6, ltype)
    g(66, 1); g(10, 0); g(20, 0); g(30, 0); g(70, 0)
    for (x, y) in points:
        g(0, "VERTEX"); g(8, layer)
        g(10, num(x)); g(20, num(y)); g(30, 0)
    g(0, "SEQEND"); g(8, layer)

def text(x, y, s, h=2.5, layer="TEXT", rot=0.0, color=None, halign=0):
    g(0, "TEXT"); g(8, layer)
    if color is not None: g(62, color)
    g(10, num(x)); g(20, num(y)); g(30, 0)
    g(40, num(h)); g(1, s); g(50, num(rot))
    g(72, halign)
    g(11, num(x)); g(21, num(y)); g(31, 0)

def solid(x1, y1, x2, y2, x3, y3, layer="0", color=None):
    # filled triangle (R12 SOLID: points 10,11,12,13 ; set 13 == 12)
    g(0, "SOLID"); g(8, layer)
    if color is not None: g(62, color)
    g(10, num(x1)); g(20, num(y1)); g(30, 0)
    g(11, num(x2)); g(21, num(y2)); g(31, 0)
    g(12, num(x3)); g(22, num(y3)); g(32, 0)
    g(13, num(x3)); g(23, num(y3)); g(33, 0)

def S(x, y):                      # apply the 30% scale to a point
    return (x * SCALE, y * SCALE)

def SL(x1, y1, x2, y2, **kw):     line(*S(x1, y1), *S(x2, y2), **kw)
def SP(pts, **kw):                polyline([S(x, y) for (x, y) in pts], **kw)
def ST(x, y, s, h=2.5, **kw):     text(*S(x, y), s, h * SCALE, **kw)

# ---------------------------------------------------------------- file header
g(0, "SECTION"); g(2, "HEADER")
g(9, "$ACADVER"); g(1, "AC1009")
g(9, "$INSUNITS"); g(70, 4)
g(9, "$EXTMIN"); g(10, num(-26)); g(20, num(-20)); g(30, 0)
g(9, "$EXTMAX"); g(10, num(135)); g(20, num(135)); g(30, 0)
g(0, "ENDSEC")

# tables: linetypes + layers
g(0, "SECTION"); g(2, "TABLES")
g(0, "TABLE"); g(2, "LTYPE"); g(70, 2)
g(0, "LTYPE"); g(2, "CONTINUOUS"); g(70, 0); g(3, "Solid line"); g(72, 65); g(73, 0); g(40, 0.0)
g(0, "LTYPE"); g(2, "DASHED"); g(70, 0); g(3, "Dashed __ __"); g(72, 65); g(73, 2)
g(40, 19.5); g(49, 15.6); g(49, -3.9)
g(0, "ENDTAB")

g(0, "TABLE"); g(2, "LAYER"); g(70, 6)
def layer(name, color):
    g(0, "LAYER"); g(2, name); g(70, 0); g(62, color); g(6, "CONTINUOUS")
layer("0", 7)
layer("AXES", 7)
layer("CURVE_LIQ", 7)     # black liquidus / solidus
layer("CURVE_MODE", 1)    # red solidification-mode boundaries
layer("BOUND", 5)         # blue dashed composition boundaries
layer("TEXT", 7)
g(0, "ENDTAB")
g(0, "ENDSEC")

# ---------------------------------------------------------------- entities
g(0, "SECTION"); g(2, "ENTITIES")

# ---- plot box
SL(0, 0, 100, 0, layer="AXES")
SL(100, 0, 100, 100, layer="AXES")
SL(100, 100, 0, 100, layer="AXES")
SL(0, 100, 0, 0, layer="AXES")

# ---- temperature axis (left): ticks + 30%-scaled values
for j in range(6):                       # 600..1600 -> 780..2080
    y = j * 20.0
    SL(0, y, -2.5, y, layer="AXES")
    val = int(round((600 + 200 * j) * SCALE))
    ST(-10.5, y - 1.3, str(val), h=2.5, layer="TEXT")

# ---- composition axis (bottom): ticks + 30%-scaled values
for i in range(8):                       # 0.5..4.0 -> 0.65..5.2
    x = i * (100.0 / 7.0)
    SL(x, 0, x, -2.5, layer="AXES")
    val = (0.5 + 0.5 * i) * SCALE
    ST(x - 2.2, -4.2, ("%.2f" % val).rstrip("0").rstrip("."), h=2.5, layer="TEXT")

# ---- composition boundaries (dashed) + their composition labels
def comp_at(x):                          # Cr_eq/Ni_eq at drawing-x, then +30%
    return (0.5 + (0.5 / (100.0 / 7.0)) * x) * SCALE
for xb, top in [(21.35, 100), (28.04, 100), (41.55, 100), (61.60, 100)]:
    SL(xb, 0, xb, top, layer="BOUND", ltype="DASHED")
    ST(xb + 0.6, 1.2, ("%.2f" % comp_at(xb)).rstrip("0").rstrip("."),
       h=2.0, layer="TEXT", color=5)

# ---- liquidus / solidus (black curves, from original spline fit points)
SP([(0, 83.52), (8.81, 70.53), (45.0, 82.0), (85.34, 88.52),
    (98.26, 95.49), (100, 95.67)], layer="CURVE_LIQ")
SP([(0, 96.04), (16.25, 85.78), (55.0, 93.0), (100, 100)], layer="CURVE_LIQ")

# ---- solidification-mode boundaries (red)
SP([(21.35, 76.14), (28.04, 91.76)], layer="CURVE_MODE")
SP([(28.04, 91.76), (56.92, 54.55), (63.99, 39.75), (66.20, 13.47)], layer="CURVE_MODE")
SP([(21.35, 76.14), (31.95, 60.29), (38.58, 30.03), (39.68, 13.47)], layer="CURVE_MODE")

# ---- region labels (g = gamma/austenite, d = delta/ferrite)
regions = [
    ("Liquid (L)", 5.0, 97.0, 2.5, 0),
    ("L + g",       3.3, 86.4, 3.0, 0),
    ("L + g",       6.5, 68.3, 3.0, 0),
    ("L + g + d",   22.0, 83.0, 2.5, 0),
    ("L + d",       66.7, 92.4, 3.0, 0),
    ("g + d",       29.6, 73.4, 3.0, 0),
    ("d",           76.1, 54.1, 3.0, 0),
    ("A",           7.0, 44.9, 3.0, 0),
    ("AF",          23.3, 44.4, 3.0, 0),
    ("FA",          35.9, 43.8, 3.0, 0),
    ("F",           48.4, 43.4, 3.0, 0),
    ("g solvus",    32.3, 48.9, 2.5, -78),
    ("d solvus",    64.0, 42.6, 2.5, -65),
    ("g + eutectic d",      22.8, 11.9, 2.3, 90),
    ("g + skeletal d",      30.7, 11.7, 2.3, 90),
    ("g + acicular d",      43.2, 11.3, 2.3, 90),
    ("d + Widmanstatten g", 48.3, 10.9, 2.3, 90),
]
for (s, x, y, h, rot) in regions:
    ST(x, y, s, h=h, layer="TEXT", rot=rot)

# ---- axis titles with arrows
# Temperature (vertical, left)
SL(-16.5, 69.6, -16.5, 84.0, layer="AXES")
solid(*S(-16.5, 84.0), *S(-15.87, 81.6), *S(-17.17, 81.6), layer="AXES")
ST(-18.0, 35.3, "Temperature (degC)", h=3.0, layer="TEXT", rot=90)
# Composition (horizontal, bottom)
SL(49.5, -12.0, 63.9, -12.0, layer="AXES")
solid(*S(63.9, -12.0), *S(61.5, -12.62), *S(61.5, -11.32), layer="AXES")
ST(31.9, -10.3, "Cr_eq / Ni_eq", h=3.0, layer="TEXT")

# ---- legend / change note
ST(2.0, -16.5, "g = austenite (gamma)   d = ferrite (delta)", h=1.8, layer="TEXT")
ST(2.0, -19.0, "Modified: all geometry +30%, axis values +30%", h=1.8, layer="TEXT")

g(0, "ENDSEC")
g(0, "EOF")

with open(OUT, "w", encoding="ascii", errors="replace") as f:
    f.write("\n".join(_buf) + "\n")

print("Wrote", OUT, "with", _buf.count("LINE") + _buf.count("POLYLINE") + _buf.count("TEXT"),
      "primary entities")
