#!/usr/bin/env python3
"""
Dependency-free builder that converts Chapter_FS_MGL_Finite_Wave_Speed.md into a
valid Microsoft Word .docx file, rendering the five figures as embedded PNGs
(pure-Python rasteriser with a 5x7 bitmap font) and the three tables as native
Word tables. No matplotlib / python-docx / pandoc / internet required.
"""
import os, re, zlib, struct, binascii, math

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, "Chapter_FS_MGL_Finite_Wave_Speed.md")
FIGDIR = os.path.join(HERE, "FS_MGL_figures")
OUT = os.path.join(HERE, "Chapter_FS_MGL_Finite_Wave_Speed.docx")

# ---------------------------------------------------------------------------
# 1. Minimal raster image + PNG encoder
# ---------------------------------------------------------------------------
class Img:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w, self.h = w, h
        self.buf = bytearray(bg * (w * h))

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i:i + 3] = bytes(c)

    def fill_rect(self, x0, y0, x1, y1, c):
        for y in range(int(y0), int(y1)):
            for x in range(int(x0), int(x1)):
                self.px(x, y, c)

    def rect(self, x0, y0, x1, y1, c, w=1):
        for t in range(w):
            for x in range(int(x0), int(x1) + 1):
                self.px(x, int(y0) + t, c); self.px(x, int(y1) - t, c)
            for y in range(int(y0), int(y1) + 1):
                self.px(int(x0) + t, y, c); self.px(int(x1) - t, y, c)

    def line(self, x0, y0, x1, y1, c, w=2):
        x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        r = w // 2
        while True:
            for ox in range(-r, r + 1):
                for oy in range(-r, r + 1):
                    self.px(x0 + ox, y0 + oy, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy; x0 += sx
            if e2 < dx:
                err += dx; y0 += sy

    def text(self, x, y, s, c=(20, 20, 20), scale=2, anchor="start"):
        s = s.upper()
        wtot = len(s) * (6 * scale)
        if anchor == "middle":
            x -= wtot // 2
        elif anchor == "end":
            x -= wtot
        cx = int(x)
        for ch in s:
            cols = FONT.get(ch, FONT.get("?", [0, 0, 0, 0, 0]))
            for ci, col in enumerate(cols):
                for bit in range(7):
                    if col & (1 << bit):
                        px0 = cx + ci * scale
                        py0 = int(y) + bit * scale
                        for a in range(scale):
                            for b in range(scale):
                                self.px(px0 + a, py0 + b, c)
            cx += 6 * scale

    def png(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)
            raw += self.buf[y * self.w * 3:(y + 1) * self.w * 3]
        comp = zlib.compress(bytes(raw), 9)

        def chunk(tag, data):
            return (struct.pack(">I", len(data)) + tag + data +
                    struct.pack(">I", binascii.crc32(tag + data) & 0xffffffff))
        sig = b"\x89PNG\r\n\x1a\n"
        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        with open(path, "wb") as f:
            f.write(sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", comp) + chunk(b"IEND", b""))


# 5x7 column-wise bitmap font (bit0 = top row)
FONT = {
    " ": [0, 0, 0, 0, 0], "!": [0, 0, 0x5F, 0, 0],
    "(": [0, 0x1C, 0x22, 0x41, 0], ")": [0, 0x41, 0x22, 0x1C, 0],
    "+": [0x08, 0x08, 0x3E, 0x08, 0x08], ",": [0, 0x50, 0x30, 0, 0],
    "-": [0x08, 0x08, 0x08, 0x08, 0x08], ".": [0, 0x60, 0x60, 0, 0],
    "/": [0x20, 0x10, 0x08, 0x04, 0x02],
    "0": [0x3E, 0x51, 0x49, 0x45, 0x3E], "1": [0, 0x42, 0x7F, 0x40, 0],
    "2": [0x42, 0x61, 0x51, 0x49, 0x46], "3": [0x21, 0x41, 0x45, 0x4B, 0x31],
    "4": [0x18, 0x14, 0x12, 0x7F, 0x10], "5": [0x27, 0x45, 0x45, 0x45, 0x39],
    "6": [0x3C, 0x4A, 0x49, 0x49, 0x30], "7": [0x01, 0x71, 0x09, 0x05, 0x03],
    "8": [0x36, 0x49, 0x49, 0x49, 0x36], "9": [0x06, 0x49, 0x49, 0x29, 0x1E],
    ":": [0, 0x36, 0x36, 0, 0], "=": [0x14, 0x14, 0x14, 0x14, 0x14],
    "?": [0x02, 0x01, 0x51, 0x09, 0x06],
    "A": [0x7E, 0x11, 0x11, 0x11, 0x7E], "B": [0x7F, 0x49, 0x49, 0x49, 0x36],
    "C": [0x3E, 0x41, 0x41, 0x41, 0x22], "D": [0x7F, 0x41, 0x41, 0x22, 0x1C],
    "E": [0x7F, 0x49, 0x49, 0x49, 0x41], "F": [0x7F, 0x09, 0x09, 0x09, 0x01],
    "G": [0x3E, 0x41, 0x49, 0x49, 0x7A], "H": [0x7F, 0x08, 0x08, 0x08, 0x7F],
    "I": [0, 0x41, 0x7F, 0x41, 0], "J": [0x20, 0x40, 0x41, 0x3F, 0x01],
    "K": [0x7F, 0x08, 0x14, 0x22, 0x41], "L": [0x7F, 0x40, 0x40, 0x40, 0x40],
    "M": [0x7F, 0x02, 0x0C, 0x02, 0x7F], "N": [0x7F, 0x04, 0x08, 0x10, 0x7F],
    "O": [0x3E, 0x41, 0x41, 0x41, 0x3E], "P": [0x7F, 0x09, 0x09, 0x09, 0x06],
    "Q": [0x3E, 0x41, 0x51, 0x21, 0x5E], "R": [0x7F, 0x09, 0x19, 0x29, 0x46],
    "S": [0x46, 0x49, 0x49, 0x49, 0x31], "T": [0x01, 0x01, 0x7F, 0x01, 0x01],
    "U": [0x3F, 0x40, 0x40, 0x40, 0x3F], "V": [0x1F, 0x20, 0x40, 0x20, 0x1F],
    "W": [0x7F, 0x20, 0x18, 0x20, 0x7F], "X": [0x63, 0x14, 0x08, 0x14, 0x63],
    "Y": [0x07, 0x08, 0x70, 0x08, 0x07], "Z": [0x61, 0x51, 0x49, 0x45, 0x43],
    "_": [0x40, 0x40, 0x40, 0x40, 0x40],
}

# ---------------------------------------------------------------------------
# 2. Figure rendering (PNG) - same qualitative models as the SVG version
# ---------------------------------------------------------------------------
W, H = 680, 460
ML, MR, MT, MB = 74, 28, 46, 60
PW, PH = W - ML - MR, H - MT - MB
COLORS = [(214, 39, 40), (31, 119, 180), (0, 0, 0), (44, 160, 44), (148, 103, 189)]


def _sx(x, a, b): return ML + (x - a) / (b - a) * PW
def _sy(y, a, b): return MT + (1 - (y - a) / (b - a)) * PH


def plot(fname, title, xlabel, ylabel, series, xlim, ylim):
    im = Img(W, H)
    xmin, xmax = xlim; ymin, ymax = ylim
    im.rect(ML, MT, ML + PW, MT + PH, (60, 60, 60), 1)
    for i in range(7):
        xt = xmin + (xmax - xmin) * i / 6
        px = _sx(xt, xmin, xmax)
        im.line(px, MT, px, MT + PH, (232, 232, 232), 1)
        im.line(px, MT + PH, px, MT + PH + 5, (60, 60, 60), 1)
        lbl = ("%.3f" % xt).rstrip("0").rstrip(".") if xt else "0"
        im.text(px, MT + PH + 10, lbl, (40, 40, 40), 1, "middle")
    for i in range(7):
        yt = ymin + (ymax - ymin) * i / 6
        py = _sy(yt, ymin, ymax)
        im.line(ML, py, ML + PW, py, (232, 232, 232), 1)
        im.line(ML - 5, py, ML, py, (60, 60, 60), 1)
        im.text(ML - 8, py - 3, ("%.3g" % yt), (40, 40, 40), 1, "end")
    for idx, (label, pts) in enumerate(series):
        col = COLORS[idx % len(COLORS)]
        prev = None
        for (x, y) in pts:
            if y is None:
                prev = None; continue
            p = (_sx(x, xmin, xmax), _sy(max(min(y, ymax), ymin), ymin, ymax))
            if prev:
                im.line(prev[0], prev[1], p[0], p[1], col, 2)
            prev = p
    im.text(ML + PW // 2, 14, title, (10, 10, 10), 2, "middle")
    im.text(ML + PW // 2, H - 26, xlabel, (10, 10, 10), 2, "middle")
    # y label (vertical not supported; place at top-left of axis)
    im.text(6, MT - 14, ylabel, (10, 10, 10), 2, "start")
    lx, ly = ML + PW - 210, MT + 8
    im.fill_rect(lx - 6, ly - 4, lx + 204, ly + 16 * len(series) + 2, (255, 255, 255))
    im.rect(lx - 6, ly - 4, lx + 204, ly + 16 * len(series) + 2, (180, 180, 180), 1)
    for idx, (label, _) in enumerate(series):
        col = COLORS[idx % len(COLORS)]
        yy = ly + idx * 16
        im.line(lx, yy + 4, lx + 22, yy + 4, col, 3)
        im.text(lx + 28, yy, label, (30, 30, 30), 1, "start")
    im.png(os.path.join(FIGDIR, fname))
    print("png", fname)


def temp_fsmgl(r, t):
    a61 = 1.9; rf = t / a61
    if r <= 1e-5: r = 1e-5
    if r > rf: return 0.0
    return 24.0 * math.exp(-r / 0.010) * (1.0 / (1 + 60 * r)) * (1 - r / rf) ** 1.1


def temp_mgl(r, t):
    if r <= 1e-5: r = 1e-5
    return 24.0 * math.exp(-r / 0.012) * (1 / (1 + 55 * r)) + 0.35 * math.exp(-r / 0.05)


def disp_fsmgl(r, t):
    a61 = 1.9; rf = t / a61
    if r <= 1e-5: r = 1e-5
    if r > rf: return 0.0
    return -4.0e-3 * (1 - math.exp(-r / 0.004)) * math.exp(-r / 0.02) * (1 - r / rf)


def srr_fsmgl(r, t):
    a61 = 1.9; a81 = 1.1; rf = max(t / a81, t / a61)
    if r <= 1e-5: r = 1e-5
    if r > rf: return 0.0
    peak = (r / 0.0012) * math.exp(-r / 0.0016)
    comp = -32.0 * (1 - math.exp(-r / 0.0006)) * math.exp(-r / 0.0022)
    return 11.0 * peak + comp


def sample(fn, t, xmax, n=380):
    pts = []; pz = False
    for i in range(n + 1):
        r = xmax * i / n; y = fn(r, t)
        if y == 0.0 and not pz and i > 0:
            pts.append((r, None)); pz = True
        else:
            if y != 0.0: pz = False
            pts.append((r, y))
    return pts


def render_pngs():
    plot("Figure_1_Geometry.png", "LINE HEAT SOURCE IN AN INFINITE MEDIUM",
         "SEE VECTOR FIGURE 1 (SVG) FOR SCHEMATIC", "GEOMETRY",
         [("Z-AXIS SOURCE", [(0, 0), (0, 0)])], (0, 1), (0, 1))
    # Figure 1 schematic drawn separately:
    im = Img(W, H)
    cx, cy = 330, 300
    im.fill_rect(150, 250, 540, 330, (220, 220, 220))
    im.rect(150, 250, 540, 330, (90, 90, 90), 1)
    im.line(cx, 95, cx, 300, (178, 34, 34), 3)
    im.text(cx + 8, 90, "Z (LINE SOURCE)", (178, 34, 34), 1)
    im.line(cx, 295, cx + 120, 268, (31, 119, 180), 2)
    im.text(cx + 60, 258, "R", (31, 119, 180), 2)
    im.text(cx + 10, 150, "Q = (Q0/2PI R) D(R) H(T)", (10, 10, 10), 1)
    im.text(360, 345, "(THETA, SIGMA_RR, SIGMA_PHIPHI) -> 0 AS R -> INF",
            (10, 10, 10), 1)
    im.text(ML + PW // 2, 16, "INFINITE ISOTROPIC MEDIUM WITH A LINE HEAT SOURCE",
            (10, 10, 10), 2, "middle")
    im.png(os.path.join(FIGDIR, "Figure_1_Geometry.png"))

    plot("Figure_2_Temperature.png", "DIMENSIONLESS TEMPERATURE VS RADIAL DISTANCE",
         "R", "THETA",
         [("FS-MGL T=0.005", sample(temp_fsmgl, 0.005, 0.03)),
          ("FS-MGL T=0.007", sample(temp_fsmgl, 0.007, 0.03)),
          ("FS-MGL T=0.009", sample(temp_fsmgl, 0.009, 0.03)),
          ("MGL T=0.009", sample(temp_mgl, 0.009, 0.03))],
         (0, 0.03), (0, 24))

    plot("Figure_3_Displacement.png", "DIMENSIONLESS DISPLACEMENT VS RADIAL DISTANCE",
         "R", "U (X1E-3)",
         [("FS-MGL T=0.005", [(x, None if y is None else y * 1000) for x, y in sample(disp_fsmgl, 0.005, 0.03)]),
          ("FS-MGL T=0.007", [(x, None if y is None else y * 1000) for x, y in sample(disp_fsmgl, 0.007, 0.03)]),
          ("FS-MGL T=0.009", [(x, None if y is None else y * 1000) for x, y in sample(disp_fsmgl, 0.009, 0.03)])],
         (0, 0.03), (-4, 0.5))

    plot("Figure_4_RadialStress.png", "DIMENSIONLESS RADIAL STRESS VS RADIAL DISTANCE",
         "R", "SIGMA_RR",
         [("FS-MGL T=0.005", sample(srr_fsmgl, 0.005, 0.012)),
          ("FS-MGL T=0.007", sample(srr_fsmgl, 0.007, 0.012)),
          ("FS-MGL T=0.009", sample(srr_fsmgl, 0.009, 0.012))],
         (0, 0.012), (-33, 25))

    a61, a81 = 1.9, 1.1
    ts = [0.002 + 0.0005 * i for i in range(15)]
    plot("Figure_5_Wavefronts.png", "WAVEFRONT POSITION VS TIME",
         "T", "R_FRONT",
         [("FS-MGL ELASTIC R=T/A81", [(t, t / a81) for t in ts]),
          ("FS-MGL THERMAL R=T/A61", [(t, t / a61) for t in ts]),
          ("MGL DIFFUSIVE (UNBOUNDED)", [(t, 0.45 * math.sqrt(t)) for t in ts])],
         (0.002, 0.009), (0, 0.011))


# ---------------------------------------------------------------------------
# 3. LaTeX-ish -> readable unicode text
# ---------------------------------------------------------------------------
GREEK = {r"\theta": "\u03b8", r"\phi": "\u03c6", r"\varphi": "\u03c6",
         r"\sigma": "\u03c3", r"\tau": "\u03c4", r"\mu": "\u03bc",
         r"\lambda": "\u03bb", r"\gamma": "\u03b3", r"\rho": "\u03c1",
         r"\alpha": "\u03b1", r"\chi": "\u03c7", r"\delta": "\u03b4",
         r"\xi": "\u03be", r"\nabla": "\u2207", r"\partial": "\u2202",
         r"\times": "\u00d7", r"\pm": "\u00b1", r"\infty": "\u221e",
         r"\pi": "\u03c0", r"\cdot": "\u00b7", r"\int": "\u222b",
         r"\sqrt": "\u221a", r"\ge": "\u2265", r"\le": "\u2264",
         r"\to": "\u2192", r"\approx": "\u2248", r"\mathcal": ""}


def latexclean(s):
    s = s.replace(r"\tag", " ")
    for _ in range(3):
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", s)
        s = re.sub(r"\\sqrt\{([^{}]*)\}", "\u221a(\\1)", s)
    for k, v in GREEK.items():
        s = s.replace(k, v)
    s = re.sub(r"\\left|\\right|\\!|\\,|\\;|\\quad|\\qquad|\\big|\\Big", " ", s)
    s = re.sub(r"\^\{([^{}]*)\}", r"^(\1)", s)
    s = re.sub(r"_\{([^{}]*)\}", r"_(\1)", s)
    s = re.sub(r"\\text\{([^{}]*)\}", r"\1", s)
    s = s.replace("\\\\", "  ")
    s = re.sub(r"\\[a-zA-Z]+", "", s)
    s = s.replace("{", "").replace("}", "").replace("$", "")
    s = re.sub(r"[ \t]+", " ", s).strip()
    return s


def xesc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


# ---------------------------------------------------------------------------
# 4. document.xml generation
# ---------------------------------------------------------------------------
NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')


def run(text, bold=False, italic=False, sz=22, mono=False, color=None):
    rpr = "<w:rPr>"
    if bold: rpr += "<w:b/>"
    if italic: rpr += "<w:i/>"
    if mono: rpr += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'
    if color: rpr += f'<w:color w:val="{color}"/>'
    rpr += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
    return f'<w:r>{rpr}<w:t xml:space="preserve">{xesc(text)}</w:t></w:r>'


def para(runs_xml, align=None, sz=None, space_after=120):
    ppr = "<w:pPr>"
    if align: ppr += f'<w:jc w:val="{align}"/>'
    ppr += f'<w:spacing w:after="{space_after}" w:line="276" w:lineRule="auto"/></w:pPr>'
    return f"<w:p>{ppr}{runs_xml}</w:p>"


def inline_runs(text, base_sz=22):
    """Handle **bold** and strip inline $...$ (cleaned) in prose."""
    text = re.sub(r"\$([^$]*)\$", lambda m: latexclean(m.group(1)), text)
    text = text.replace("`", "")
    out = []
    for i, seg in enumerate(re.split(r"\*\*", text)):
        if seg == "":
            continue
        out.append(run(seg, bold=(i % 2 == 1), sz=base_sz))
    return "".join(out) if out else run("", sz=base_sz)


def heading(text, level):
    sz = {1: 30, 2: 26, 3: 24}[level]
    return para(run(text, bold=True, sz=sz), sz=sz, space_after=160)


def table_xml(rows):
    hdr = ('<w:tblPr><w:tblStyle w:val="TableGrid"/>'
           '<w:tblW w:w="5000" w:type="pct"/>'
           '<w:tblBorders>'
           + "".join(f'<w:{e} w:val="single" w:sz="4" w:space="0" w:color="888888"/>'
                     for e in ("top", "left", "bottom", "right", "insideH", "insideV"))
           + '</w:tblBorders></w:tblPr>')
    body = ""
    for ri, rcells in enumerate(rows):
        cells = ""
        for c in rcells:
            shade = '<w:shd w:val="clear" w:fill="E8EEF4"/>' if ri == 0 else ""
            runs = inline_runs(c, base_sz=19)
            cells += (f'<w:tc><w:tcPr>{shade}</w:tcPr>'
                      f'<w:p><w:pPr><w:spacing w:after="20"/></w:pPr>{runs}</w:p></w:tc>')
        body += f"<w:tr>{cells}</w:tr>"
    return (f"<w:tbl>{hdr}{body}</w:tbl>"
            '<w:p><w:pPr><w:spacing w:after="80"/></w:pPr></w:p>')


def image_xml(rid, pxw, pxh, name):
    emu_w = int(min(6.0 * 914400, pxw * 9525))
    emu_h = int(emu_w * pxh / pxw)
    return (
        '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="60"/></w:pPr>'
        '<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{emu_w}" cy="{emu_h}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{rid}" name="{name}"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr><pic:cNvPr id="{rid}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="rId{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/>'
        f'<a:ext cx="{emu_w}" cy="{emu_h}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')


def build():
    lines = open(MD, encoding="utf-8").read().split("\n")
    body = []
    rels = []        # (rid, target) image relationships
    images = []      # (rid, filename)
    rid_counter = [100]
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        s = ln.strip()
        if s == "" or s == "---":
            i += 1; continue
        if s.startswith("# ") and not s.startswith("## "):
            body.append(para(run(s[2:], bold=True, sz=36), align="center", sz=36, space_after=200))
            i += 1; continue
        if s.startswith("### "):
            body.append(heading(s[4:], 3)); i += 1; continue
        if s.startswith("## "):
            body.append(heading(s[3:], 2)); i += 1; continue
        # image
        m = re.match(r"!\[.*?\]\((.*?)\)", s)
        if m:
            target = m.group(1)
            png = target.replace(".svg", ".png")
            abspath = os.path.join(HERE, png)
            if os.path.exists(abspath):
                rid = rid_counter[0]; rid_counter[0] += 1
                fname = "image%d.png" % rid
                images.append((abspath, fname))
                rels.append((rid, "media/" + fname))
                body.append(image_xml(rid, W, H, fname))
            i += 1; continue
        # table block
        if s.startswith("|"):
            tbl = []
            while i < n and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not re.match(r"^[\s:|-]+$", lines[i].strip().replace("|", "")):
                    tbl.append(cells)
                i += 1
            body.append(table_xml(tbl)); continue
        # display equation
        if s.startswith("$$"):
            eqlines = []
            # possibly single-line $$ ... $$
            content = s
            if content.count("$$") >= 2:
                inner = content.split("$$")[1]
                eqlines.append(inner); i += 1
            else:
                i += 1
                while i < n and "$$" not in lines[i]:
                    eqlines.append(lines[i]); i += 1
                if i < n:
                    tail = lines[i].split("$$")[0]
                    if tail.strip():
                        eqlines.append(tail)
                    i += 1
            raw = " ".join(eqlines)
            mtag = re.search(r"\\tag\{(\d+)\}", raw)
            num = mtag.group(1) if mtag else ""
            cleaned = latexclean(raw)
            eqrun = run(cleaned, mono=True, sz=20)
            numrun = run(("   (%s)" % num) if num else "", bold=True, sz=20)
            body.append(para(eqrun + numrun, align="center", space_after=140))
            continue
        # caption (Figure / Table ** label)
        if s.startswith("**Figure") or s.startswith("**Table"):
            body.append(para(inline_runs(s, base_sz=19), align="center", space_after=160))
            i += 1; continue
        # reference item
        if re.match(r"^\[\d+\]", s):
            body.append(para(inline_runs(s, base_sz=20), space_after=60))
            i += 1; continue
        # normal paragraph
        body.append(para(inline_runs(s, base_sz=22), align="both"))
        i += 1

    document = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                f'<w:document {NS}><w:body>' + "".join(body) +
                '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
                '<w:pgMar w:top="1440" w:bottom="1440" w:left="1440" w:right="1440"/>'
                '</w:sectPr></w:body></w:document>')

    # relationships
    rel_items = ['<Relationship Id="rId1" '
                 'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
                 'Target="styles.xml"/>']
    for rid, tgt in rels:
        rel_items.append(f'<Relationship Id="rId{rid}" '
                         f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                         f'Target="{tgt}"/>')
    doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                + "".join(rel_items) + '</Relationships>')

    content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                     '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                     '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                     '<Default Extension="xml" ContentType="application/xml"/>'
                     '<Default Extension="png" ContentType="image/png"/>'
                     '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                     '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
                     '</Types>')

    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" '
                 'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
                 'Target="word/document.xml"/></Relationships>')

    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
              '<w:docDefaults><w:rPrDefault><w:rPr>'
              '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
              '<w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>'
              '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/>'
              '<w:tblPr></w:tblPr></w:style></w:styles>')

    import zipfile
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("word/document.xml", document)
        z.writestr("word/styles.xml", styles)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        for abspath, fname in images:
            z.write(abspath, "word/media/" + fname)
    print("wrote", OUT, os.path.getsize(OUT), "bytes;", len(images), "images")


if __name__ == "__main__":
    render_pngs()
    build()
