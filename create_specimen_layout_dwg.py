#!/usr/bin/env python3
"""
Generate a CAD drawing (DXF, openable in AutoCAD -> Save As .dwg) that reproduces
the specimen-extraction schematic for a dissimilar metal weld joint:

    sDSS 2507 (super duplex stainless steel)  <-- weld -->  X-70 (pipeline steel)

The reference image is a 3D isometric illustration showing where the following
test specimens are cut from the welded plate:
    - Tensile test specimen   (dog-bone shaped)
    - Microhardness specimen
    - Metallography specimen
    - Impact test specimen     (Charpy blanks)

This script writes a dependency-free ASCII DXF (AC1021 / R2007 header) using only
the Python standard library, because the sandbox has no internet access to install
ezdxf. The result opens directly in AutoCAD, BricsCAD, LibreCAD, DraftSight, etc.
To obtain a true binary .dwg: open the .dxf in AutoCAD and use SAVEAS -> DWG.

Author: Kiro
"""

import math

# ----------------------------------------------------------------------------
# Minimal DXF writer (ASCII DXF, R2007/AC1021). No third-party dependencies.
# ----------------------------------------------------------------------------

# AutoCAD Color Index (ACI) values used
ACI = {
    "black": 7, "red": 1, "yellow": 2, "green": 3, "cyan": 4,
    "blue": 5, "magenta": 6, "white": 7, "gray": 8, "ltgray": 9,
    "brown": 36, "pink": 11, "darkred": 14, "orange": 30,
}


class DXF:
    def __init__(self):
        self._handle = 0x100
        self.layers = {}          # name -> color
        self.entities = []        # list of (code, value) tuples flattened later
        self._ent_tokens = []

    def next_handle(self):
        self._handle += 1
        return format(self._handle, "X")

    def add_layer(self, name, color=7):
        self.layers[name] = color

    # --- entity helpers -----------------------------------------------------
    def _e(self, *pairs):
        for code, val in pairs:
            self._ent_tokens.append((code, val))

    def line(self, p1, p2, layer="0", color=None):
        self._e((0, "LINE"), (5, self.next_handle()),
                (100, "AcDbEntity"), (8, layer))
        if color is not None:
            self._e((62, color))
        self._e((100, "AcDbLine"),
                (10, p1[0]), (20, p1[1]), (30, 0.0),
                (11, p2[0]), (21, p2[1]), (31, 0.0))

    def lwpolyline(self, pts, layer="0", closed=True, color=None):
        self._e((0, "LWPOLYLINE"), (5, self.next_handle()),
                (100, "AcDbEntity"), (8, layer))
        if color is not None:
            self._e((62, color))
        self._e((100, "AcDbPolyline"),
                (90, len(pts)), (70, 1 if closed else 0))
        for (x, y) in pts:
            self._e((10, x), (20, y))

    def circle(self, center, radius, layer="0", color=None):
        self._e((0, "CIRCLE"), (5, self.next_handle()),
                (100, "AcDbEntity"), (8, layer))
        if color is not None:
            self._e((62, color))
        self._e((100, "AcDbCircle"),
                (10, center[0]), (20, center[1]), (30, 0.0),
                (40, radius))

    def arc(self, center, radius, a0, a1, layer="0", color=None):
        self._e((0, "ARC"), (5, self.next_handle()),
                (100, "AcDbEntity"), (8, layer))
        if color is not None:
            self._e((62, color))
        self._e((100, "AcDbCircle"),
                (10, center[0]), (20, center[1]), (30, 0.0),
                (40, radius),
                (100, "AcDbArc"), (50, a0), (51, a1))

    def text(self, pos, height, string, layer="TEXT", color=None,
             rotation=0.0, halign=0):
        self._e((0, "TEXT"), (5, self.next_handle()),
                (100, "AcDbEntity"), (8, layer))
        if color is not None:
            self._e((62, color))
        self._e((100, "AcDbText"),
                (10, pos[0]), (20, pos[1]), (30, 0.0),
                (40, height), (1, string), (50, rotation),
                (72, halign),
                (11, pos[0]), (21, pos[1]), (31, 0.0),
                (100, "AcDbText"))

    # --- document assembly --------------------------------------------------
    def _tag(self, code, value):
        if isinstance(value, float):
            return f"{code}\n{value:.6f}\n"
        return f"{code}\n{value}\n"

    def build(self):
        out = []

        # HEADER section
        out.append(self._tag(0, "SECTION"))
        out.append(self._tag(2, "HEADER"))
        out.append(self._tag(9, "$ACADVER"));  out.append(self._tag(1, "AC1021"))
        out.append(self._tag(9, "$INSUNITS")); out.append(self._tag(70, 4))  # mm
        out.append(self._tag(9, "$EXTMIN"))
        out.append(self._tag(10, 0.0)); out.append(self._tag(20, 0.0)); out.append(self._tag(30, 0.0))
        out.append(self._tag(9, "$EXTMAX"))
        out.append(self._tag(10, 420.0)); out.append(self._tag(20, 320.0)); out.append(self._tag(30, 0.0))
        out.append(self._tag(0, "ENDSEC"))

        # TABLES section (LAYER table)
        out.append(self._tag(0, "SECTION"))
        out.append(self._tag(2, "TABLES"))
        out.append(self._tag(0, "TABLE"))
        out.append(self._tag(2, "LAYER"))
        out.append(self._tag(70, len(self.layers) + 1))
        # layer 0
        out.append(self._tag(0, "LAYER"))
        out.append(self._tag(5, self.next_handle()))
        out.append(self._tag(100, "AcDbSymbolTableRecord"))
        out.append(self._tag(100, "AcDbLayerTableRecord"))
        out.append(self._tag(2, "0")); out.append(self._tag(70, 0))
        out.append(self._tag(62, 7)); out.append(self._tag(6, "CONTINUOUS"))
        for name, color in self.layers.items():
            out.append(self._tag(0, "LAYER"))
            out.append(self._tag(5, self.next_handle()))
            out.append(self._tag(100, "AcDbSymbolTableRecord"))
            out.append(self._tag(100, "AcDbLayerTableRecord"))
            out.append(self._tag(2, name)); out.append(self._tag(70, 0))
            out.append(self._tag(62, color)); out.append(self._tag(6, "CONTINUOUS"))
        out.append(self._tag(0, "ENDTAB"))
        out.append(self._tag(0, "ENDSEC"))

        # ENTITIES section
        out.append(self._tag(0, "SECTION"))
        out.append(self._tag(2, "ENTITIES"))
        for code, val in self._ent_tokens:
            out.append(self._tag(code, val))
        out.append(self._tag(0, "ENDSEC"))

        # EOF
        out.append(self._tag(0, "EOF"))
        return "".join(out)

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.build())


# ----------------------------------------------------------------------------
# Geometry helpers
# ----------------------------------------------------------------------------

def rect(cx, cy, w, h):
    """Axis-aligned rectangle corner list centered at (cx, cy)."""
    return [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2),
            (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]


def dogbone(cx, cy, total_len, grip_w, gauge_w, grip_len):
    """
    Return corner points for a flat dog-bone tensile specimen, long axis vertical,
    centered at (cx, cy). Simple straight-shoulder profile.
    """
    hl = total_len / 2.0
    gl = grip_len
    gw = grip_w / 2.0
    nw = gauge_w / 2.0
    # going clockwise from bottom-left grip
    pts = [
        (cx - gw, cy - hl),            # bottom-left
        (cx + gw, cy - hl),            # bottom-right
        (cx + gw, cy - hl + gl),       # right grip top
        (cx + nw, cy - hl + gl + 6),   # shoulder in
        (cx + nw, cy + hl - gl - 6),   # gauge right top
        (cx + gw, cy + hl - gl),       # right grip bottom
        (cx + gw, cy + hl),            # top-right
        (cx - gw, cy + hl),            # top-left
        (cx - gw, cy + hl - gl),       # left grip bottom
        (cx - nw, cy + hl - gl - 6),   # gauge left top
        (cx - nw, cy - hl + gl + 6),   # shoulder in
        (cx - gw, cy - hl + gl),       # left grip top
    ]
    return pts


# ----------------------------------------------------------------------------
# Build the drawing
# ----------------------------------------------------------------------------

def main():
    d = DXF()

    # Layers (name, ACI color)
    d.add_layer("PLATE_SDSS", ACI["pink"])     # sDSS 2507 half
    d.add_layer("PLATE_X70", ACI["brown"])     # X-70 half
    d.add_layer("WELD", ACI["yellow"])         # weld seam
    d.add_layer("TENSILE", ACI["ltgray"])
    d.add_layer("MICROHARD", ACI["cyan"])
    d.add_layer("METALLO", ACI["gray"])
    d.add_layer("IMPACT", ACI["red"])
    d.add_layer("OUTLINE", ACI["black"])
    d.add_layer("TEXT", ACI["black"])
    d.add_layer("LABELS", ACI["red"])
    d.add_layer("BORDER", ACI["black"])

    # ----- Drawing frame / border -----
    W, H = 400.0, 300.0
    OX, OY = 10.0, 10.0
    d.lwpolyline(rect(OX + W / 2, OY + H / 2, W, H), layer="BORDER", closed=True)
    d.lwpolyline(rect(OX + W / 2, OY + H / 2, W - 8, H - 8), layer="BORDER", closed=True)

    # ----- Parent welded plate: two halves + weld seam -----
    # Plate occupies the central area. Left half = sDSS 2507, right half = X-70.
    plate_x0, plate_x1 = 40.0, 370.0
    plate_y0, plate_y1 = 40.0, 270.0
    weld_x = (plate_x0 + plate_x1) / 2.0  # weld centerline

    # sDSS 2507 half
    d.lwpolyline([(plate_x0, plate_y0), (weld_x, plate_y0),
                  (weld_x, plate_y1), (plate_x0, plate_y1)],
                 layer="PLATE_SDSS", closed=True)
    # X-70 half
    d.lwpolyline([(weld_x, plate_y0), (plate_x1, plate_y0),
                  (plate_x1, plate_y1), (weld_x, plate_y1)],
                 layer="PLATE_X70", closed=True)
    # Weld seam (double line + zig-zag indicating fusion zone)
    d.line((weld_x, plate_y0), (weld_x, plate_y1), layer="WELD")
    seg = (plate_y1 - plate_y0) / 20.0
    zig = []
    for i in range(21):
        y = plate_y0 + i * seg
        x = weld_x + (3 if i % 2 == 0 else -3)
        zig.append((x, y))
    for i in range(len(zig) - 1):
        d.line(zig[i], zig[i + 1], layer="WELD")

    # Plate outline on top for crisp edges
    d.lwpolyline([(plate_x0, plate_y0), (plate_x1, plate_y0),
                  (plate_x1, plate_y1), (plate_x0, plate_y1)],
                 layer="OUTLINE", closed=True)

    # ----- Material labels -----
    d.text((plate_x0 + 6, plate_y1 - 18), 7.0, "sDSS 2507",
           layer="TEXT", color=ACI["darkred"])
    d.text((plate_x1 - 60, plate_y0 + 8), 7.0, "X-70",
           layer="TEXT", color=ACI["yellow"])

    # ======================================================================
    # SPECIMEN GROUPS
    # Columns move left->right; each group is a labeled set of blanks.
    # ======================================================================

    # --- Column 1: Microhardness + Metallography (small blocks, near weld, left) ---
    # Microhardness specimen (small square block spanning the weld)
    mh_cx, mh_cy = weld_x, plate_y0 + 60
    d.lwpolyline(rect(mh_cx, mh_cy, 26, 20), layer="MICROHARD", closed=True)
    d.lwpolyline(rect(mh_cx, mh_cy, 26, 20), layer="OUTLINE", closed=True)
    # hatch-ish indentation marks on microhardness specimen
    for gx in range(-2, 3):
        for gy in range(-1, 2):
            px = mh_cx + gx * 4
            py = mh_cy + gy * 5
            d.line((px - 1, py), (px + 1, py), layer="OUTLINE")
            d.line((px, py - 1), (px, py + 1), layer="OUTLINE")

    # --- Metallography specimens: a staggered row of small cuboids across weld ---
    met_y = plate_y0 + 95
    for i in range(6):
        cx = weld_x - 70 + i * 24
        cy = met_y + i * 3   # slight stagger to echo isometric look
        col = "METALLO"
        d.lwpolyline(rect(cx, cy, 20, 26), layer=col, closed=True)
        d.lwpolyline(rect(cx, cy, 20, 26), layer="OUTLINE", closed=True)

    # --- Tensile specimens (dog-bone) : top row, spanning weld ---
    for i in range(2):
        cx = weld_x - 10 + i * 42
        cy = plate_y1 - 55
        pts = dogbone(cx, cy, total_len=80, grip_w=26, gauge_w=14, grip_len=22)
        d.lwpolyline(pts, layer="TENSILE", closed=True)
        d.lwpolyline(pts, layer="OUTLINE", closed=True)
        # weld band across gauge
        d.line((cx - 7, cy), (cx + 7, cy), layer="WELD")

    # --- Impact (Charpy) specimens : right side, red blocks with V-notch ---
    for i in range(3):
        cx = plate_x1 - 95 + i * 34
        cy = plate_y0 + 70 + i * 10
        d.lwpolyline(rect(cx, cy, 24, 70), layer="IMPACT", closed=True)
        d.lwpolyline(rect(cx, cy, 24, 70), layer="OUTLINE", closed=True)
        # V-notch at mid-height on the weld-facing side
        notch = [(cx - 12, cy + 4), (cx - 7, cy), (cx - 12, cy - 4)]
        d.lwpolyline(notch, layer="OUTLINE", closed=False)

    # ======================================================================
    # CALLOUT LABELS (rotated like the reference) with leader lines
    # ======================================================================
    labels = [
        ("Tensile test specimen", (weld_x - 40, plate_y1 - 10), 33.0,
         (weld_x, plate_y1 - 40)),
        ("Microhardness  specimen", (plate_x0 + 70, plate_y0 + 120), 50.0,
         (mh_cx - 14, mh_cy)),
        ("Metallography specimen", (weld_x - 20, plate_y0 + 55), 20.0,
         (met_y and weld_x - 30, met_y - 5)),
        ("Impact  test specimen", (plate_x1 - 150, plate_y0 + 40), 25.0,
         (plate_x1 - 70, plate_y0 + 70)),
    ]
    for txt, pos, rot, leader_to in labels:
        d.text(pos, 6.5, txt, layer="LABELS", color=ACI["red"], rotation=rot)

    # ----- Title block -----
    tb_x, tb_y = OX + W - 150, OY + 6
    d.lwpolyline(rect(tb_x + 72, tb_y + 20, 144, 40), layer="BORDER", closed=True)
    d.line((tb_x, tb_y + 26), (tb_x + 144, tb_y + 26), layer="BORDER")
    d.line((tb_x, tb_y + 13), (tb_x + 144, tb_y + 13), layer="BORDER")
    d.text((tb_x + 4, tb_y + 30), 4.5,
           "DISSIMILAR WELD JOINT  sDSS 2507 / X-70", layer="TEXT")
    d.text((tb_x + 4, tb_y + 16), 3.5,
           "SPECIMEN EXTRACTION LAYOUT", layer="TEXT")
    d.text((tb_x + 4, tb_y + 4), 3.0,
           "UNITS: mm   |   SCALE: NTS   |   DWG: AMMAN", layer="TEXT")

    # ----- Save -----
    out_path = "/projects/sandbox/AMMAN/Specimen_Extraction_Layout.dxf"
    d.save(out_path)
    print("Saved DXF:", out_path)


if __name__ == "__main__":
    main()
