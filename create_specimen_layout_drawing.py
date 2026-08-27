"""
Generate a DXF drawing that reproduces the "test-specimen extraction layout" figure.

The figure is an ISOMETRIC (pictorial) drawing showing:
  1. A base plate (155 x 55 x 5 mm) with slots/specimen blanks laid out on it,
     including tensile-dogbone blanks (100 long, 30/32/30 zones, R6 fillet neck,
     10 wide) and rectangular coupons (55 x 10, 30 long features).
  2. A stand-alone "Tensile sample"  (dogbone: 30 + 32 + 30 = ~100 long, ~10 wide).
  3. A stand-alone "Coupon for Hardness study" (stepped block ~40 x 20 x 6/8).
  4. A stand-alone "Impact test sample" (Charpy bar: 55 long, 10 wide, 5 thick,
     with a V/U notch).

All dimensions are in millimetres.

This script has NO third-party dependencies: it writes the DXF (AutoCAD R12
ASCII) format directly, so it runs anywhere Python runs. The resulting .dxf
opens in AutoCAD, BricsCAD, LibreCAD, DraftSight, Fusion 360, etc. To obtain a
.dwg, open the .dxf in any CAD program and "Save As -> DWG".

Author: generated for the AMMAN repository.
"""

import math

# ----------------------------------------------------------------------------
# Minimal DXF (R12 ASCII) writer -- no external libraries required.
# ----------------------------------------------------------------------------


class DXF:
    """Tiny writer for AutoCAD R12 ASCII DXF entities (LINE, CIRCLE, ARC, TEXT)."""

    def __init__(self):
        self._body = []          # entity group codes
        self._layers = {}        # name -> color index

    # -- layer bookkeeping ---------------------------------------------------
    def add_layer(self, name, color=7):
        self._layers[name] = color

    # -- 2D entities ---------------------------------------------------------
    def line(self, p1, p2, layer="0"):
        self._body += [
            (0, "LINE"), (8, layer),
            (10, p1[0]), (20, p1[1]), (30, 0.0),
            (11, p2[0]), (21, p2[1]), (31, 0.0),
        ]

    def polyline(self, pts, layer="0", closed=False):
        seq = list(pts)
        if closed and seq:
            seq = seq + [seq[0]]
        for a, b in zip(seq[:-1], seq[1:]):
            self.line(a, b, layer=layer)

    def circle(self, center, radius, layer="0"):
        self._body += [
            (0, "CIRCLE"), (8, layer),
            (10, center[0]), (20, center[1]), (30, 0.0),
            (40, radius),
        ]

    def arc(self, center, radius, a0, a1, layer="0"):
        self._body += [
            (0, "ARC"), (8, layer),
            (10, center[0]), (20, center[1]), (30, 0.0),
            (40, radius), (50, a0), (51, a1),
        ]

    def text(self, insert, height, value, layer="0", rotation=0.0):
        self._body += [
            (0, "TEXT"), (8, layer),
            (10, insert[0]), (20, insert[1]), (30, 0.0),
            (40, height), (1, value), (50, rotation),
        ]

    # -- serialisation -------------------------------------------------------
    def _tables(self):
        out = [(0, "SECTION"), (2, "TABLES"),
               (0, "TABLE"), (2, "LAYER"), (70, max(1, len(self._layers)))]
        for name, color in self._layers.items():
            out += [(0, "LAYER"), (2, name), (70, 0), (62, color), (6, "CONTINUOUS")]
        out += [(0, "ENDTAB"), (0, "ENDSEC")]
        return out

    def tostring(self):
        groups = []
        groups += [(0, "SECTION"), (2, "HEADER"), (0, "ENDSEC")]
        groups += self._tables()
        groups += [(0, "SECTION"), (2, "ENTITIES")]
        groups += self._body
        groups += [(0, "ENDSEC"), (0, "EOF")]
        lines = []
        for code, val in groups:
            lines.append(str(code))
            if isinstance(val, float):
                lines.append("{:.4f}".format(val))
            else:
                lines.append(str(val))
        return "\n".join(lines) + "\n"

    def save(self, path):
        with open(path, "w") as f:
            f.write(self.tostring())


# ----------------------------------------------------------------------------
# Isometric projection helpers.
# ----------------------------------------------------------------------------
# Standard isometric: X axis to the right-down at -30 deg, Y axis to the
# right-up at +30 deg, Z axis vertical. This matches the pictorial look of
# the source figure.

COS30 = math.cos(math.radians(30))
SIN30 = math.sin(math.radians(30))


def iso(x, y, z, origin=(0.0, 0.0)):
    """Project a 3D model point (mm) onto the 2D isometric plane."""
    px = (x - y) * COS30
    py = (x + y) * SIN30 + z
    return (origin[0] + px, origin[1] + py)


def box(dxf, org, dx, dy, dz, layer="OUTLINE", origin=(0, 0)):
    """Draw the visible edges of an axis-aligned box in isometric view.

    org : (x, y, z) location of the near-bottom corner of the box.
    dx, dy, dz : box extents along model X, Y, Z.
    Returns the 8 projected corner points for reuse.
    """
    ox, oy, oz = org
    # 8 corners
    c = {
        "000": iso(ox,      oy,      oz,      origin),
        "100": iso(ox + dx, oy,      oz,      origin),
        "110": iso(ox + dx, oy + dy, oz,      origin),
        "010": iso(ox,      oy + dy, oz,      origin),
        "001": iso(ox,      oy,      oz + dz, origin),
        "101": iso(ox + dx, oy,      oz + dz, origin),
        "111": iso(ox + dx, oy + dy, oz + dz, origin),
        "011": iso(ox,      oy + dy, oz + dz, origin),
    }
    # top face
    dxf.polyline([c["001"], c["101"], c["111"], c["011"]], layer=layer, closed=True)
    # front-right visible vertical edges + bottom visible edges
    dxf.line(c["001"], c["000"], layer=layer)
    dxf.line(c["101"], c["100"], layer=layer)
    dxf.line(c["111"], c["110"], layer=layer)
    dxf.line(c["000"], c["100"], layer=layer)
    dxf.line(c["100"], c["110"], layer=layer)
    return c


def iso_dim_text(dxf, model_pt, value, origin=(0, 0), h=3.0, layer="DIM", dxo=2.0, dyo=2.0):
    """Place a dimension text near a projected model point."""
    p = iso(*model_pt, origin=origin)
    dxf.text((p[0] + dxo, p[1] + dyo), h, value, layer=layer)


# ----------------------------------------------------------------------------
# Build the drawing.
# ----------------------------------------------------------------------------

def build():
    dxf = DXF()
    dxf.add_layer("OUTLINE", color=7)    # white/black main geometry
    dxf.add_layer("SLOT", color=5)       # blue slot / specimen blanks
    dxf.add_layer("DIM", color=3)        # green dimensions / text
    dxf.add_layer("NOTE", color=1)       # red notes

    TXT = 3.0

    # ========================================================================
    # 1) BASE PLATE WITH SPECIMEN LAYOUT  (left / main view)
    # ========================================================================
    # Plate: 155 (X) x 55 (Y) x 5 (Z). Placed so its near corner is origin_A.
    origin_A = (0.0, 20.0)
    PL_L, PL_W, PL_T = 155.0, 55.0, 5.0
    plate = box(dxf, (0, 0, 0), PL_L, PL_W, PL_T, layer="OUTLINE", origin=origin_A)

    # --- slots / specimen blanks sitting on the top face (z = PL_T) ----------
    # A central band of parallel slots (the "combed" region in the figure)
    ztop = PL_T
    n_slots = 9
    slot_x0, slot_x1 = 35.0, 120.0
    band_y0, band_y1 = 8.0, 47.0
    for i in range(n_slots + 1):
        y = band_y0 + (band_y1 - band_y0) * i / n_slots
        p0 = iso(slot_x0, y, ztop, origin_A)
        p1 = iso(slot_x1, y, ztop, origin_A)
        dxf.line(p0, p1, layer="SLOT")

    # Tensile-dogbone blank laid across the top-left of the plate.
    # Simplified as a slim raised bar 100 long x 10 wide x 6 tall with a
    # necked centre (R6). Drawn as an isometric box plus neck marker lines.
    tb_org = (12.0, 40.0, ztop)
    box(dxf, tb_org, 100.0, 10.0, 6.0, layer="OUTLINE", origin=origin_A)
    # neck marks (two vertical break lines around mid-length)
    for xn in (48.0, 52.0):
        a = iso(12.0 + xn, 40.0, ztop, origin_A)
        b = iso(12.0 + xn, 40.0, ztop + 6.0, origin_A)
        dxf.line(a, b, layer="OUTLINE")

    # A short rectangular coupon blank on the right of the plate (55 x 10 x 6)
    box(dxf, (95.0, 8.0, ztop), 55.0, 10.0, 6.0, layer="OUTLINE", origin=origin_A)
    # A small 30-long coupon lower-right
    box(dxf, (110.0, 30.0, ztop), 30.0, 10.0, 6.0, layer="OUTLINE", origin=origin_A)

    # --- dimensions for the base plate ---------------------------------------
    iso_dim_text(dxf, (PL_L / 2, 0, 0), "155", origin_A, TXT, dyo=-8)
    iso_dim_text(dxf, (PL_L, PL_W / 2, 0), "55", origin_A, TXT, dxo=6)
    iso_dim_text(dxf, (0, 0, PL_T / 2), "5", origin_A, TXT, dxo=-9)
    iso_dim_text(dxf, (12, 40, ztop + 6), "100", origin_A, TXT, dyo=6)
    iso_dim_text(dxf, (30, 40, ztop + 6), "30", origin_A, TXT, dyo=2)
    iso_dim_text(dxf, (62, 40, ztop + 6), "10", origin_A, TXT, dyo=2)
    iso_dim_text(dxf, (42, 45, ztop + 3), "R6", origin_A, TXT)
    iso_dim_text(dxf, (95, 8, ztop + 6), "55", origin_A, TXT, dyo=4)
    iso_dim_text(dxf, (110, 30, ztop + 6), "30", origin_A, TXT, dyo=4)
    iso_dim_text(dxf, (140, 40, ztop + 6), "10", origin_A, TXT, dyo=4)

    dxf.text((iso(0, 0, 0, origin_A)[0] - 5, iso(0, 0, 0, origin_A)[1] - 22),
             4.0, "ALL DIMENSIONS ARE IN mm", layer="NOTE")

    # ========================================================================
    # 2) TENSILE SAMPLE  (top-right detail)  -- dogbone bar
    # ========================================================================
    org_T = (250.0, 150.0)
    # grip - reduced - grip:  30 + 32(neck zone incl. gauge) + 30, width 10,
    # thickness ~5, reduced width ~6 with R fillets.
    # Draw as two grip boxes and a slimmer central box.
    box(dxf, (0, 0, 0),  30.0, 10.0, 5.0, layer="OUTLINE", origin=org_T)      # left grip
    box(dxf, (30, 2, 0), 32.0, 6.0,  5.0, layer="OUTLINE", origin=org_T)      # reduced neck
    box(dxf, (62, 0, 0), 30.0, 10.0, 5.0, layer="OUTLINE", origin=org_T)      # right grip
    dxf.text((org_T[0] - 5, org_T[1] + 45), 4.0, "Tensile sample", layer="NOTE")
    iso_dim_text(dxf, (15, 10, 0), "30",  org_T, TXT, dyo=4)
    iso_dim_text(dxf, (46, 8, 0),  "32",  org_T, TXT, dyo=4)
    iso_dim_text(dxf, (77, 10, 0), "30",  org_T, TXT, dyo=4)
    iso_dim_text(dxf, (46, 0, 0),  "100", org_T, TXT, dyo=-8)
    iso_dim_text(dxf, (0, 0, 2.5), "5",   org_T, TXT, dxo=-8)

    # ========================================================================
    # 3) COUPON FOR HARDNESS STUDY  (middle-right detail) -- stepped block
    # ========================================================================
    org_H = (255.0, 80.0)
    # Lower/base part 40 x 20 x 6, with a raised step 20 x 20 x 2 on top-back.
    box(dxf, (0, 0, 0),   40.0, 20.0, 6.0, layer="OUTLINE", origin=org_H)
    box(dxf, (0, 0, 6.0), 20.0, 20.0, 2.0, layer="OUTLINE", origin=org_H)
    dxf.text((org_H[0] - 5, org_H[1] + 42), 4.0, "Coupon for Hardness study", layer="NOTE")
    iso_dim_text(dxf, (20, 0, 0), "40", org_H, TXT, dyo=-8)
    iso_dim_text(dxf, (40, 10, 0), "20", org_H, TXT, dxo=6)
    iso_dim_text(dxf, (0, 0, 3.0), "6", org_H, TXT, dxo=-8)

    # ========================================================================
    # 4) IMPACT TEST SAMPLE  (bottom-right detail) -- Charpy bar with notch
    # ========================================================================
    org_I = (255.0, 15.0)
    IL, IW, IT = 55.0, 10.0, 5.0
    box(dxf, (0, 0, 0), IL, IW, IT, layer="OUTLINE", origin=org_I)
    # V-notch at mid-length on the top face (drawn as two converging lines)
    xn = IL / 2.0
    top_front = iso(xn, 0, IT, org_I)
    top_back = iso(xn, IW, IT, org_I)
    dxf.line(top_front, top_back, layer="OUTLINE")
    n1 = iso(xn - 2, 0, IT, org_I)
    n2 = iso(xn + 2, 0, IT, org_I)
    nb = iso(xn, 0, IT - 3, org_I)
    dxf.line(n1, nb, layer="OUTLINE")
    dxf.line(n2, nb, layer="OUTLINE")
    dxf.text((org_I[0] - 5, org_I[1] + 40), 4.0, "Impact test sample", layer="NOTE")
    iso_dim_text(dxf, (IL / 2, 0, 0), "55", org_I, TXT, dyo=-8)
    iso_dim_text(dxf, (IL, IW / 2, 0), "10", org_I, TXT, dxo=6)
    iso_dim_text(dxf, (0, 0, IT / 2), "5", org_I, TXT, dxo=-8)

    return dxf


if __name__ == "__main__":
    dxf = build()
    out = "/projects/sandbox/AMMAN/Specimen_Layout_Drawing.dxf"
    dxf.save(out)
    print("DXF written to:", out)
    print("Open in any CAD app (AutoCAD/BricsCAD/LibreCAD/DraftSight/Fusion360).")
    print("To get a .dwg: open the .dxf and 'Save As' -> DWG.")
