#!/usr/bin/env python3
"""
Create a Word (.docx) report compiling the weld mechanical-property analysis:
- Charpy V-notch (CVN) impact toughness (+20 C and -20 C)
- Room-temperature Vickers hardness (HV0.5)
- Vickers microhardness traverse across the weld (VHN vs distance)

for the X70-X70, S355-S355 and X70-S355 welds (E6018 filler).

Pure Python standard library only (zipfile, struct, zlib, csv, os) since
python-docx / matplotlib / cairosvg are not available in this sandbox.
This mirrors the repo's existing create_chapter_docx.py and
create_manuscript_docx.py scripts: the .docx is a ZIP of hand-written OOXML
parts, and the profile figures are PNGs generated from raw bytes.
"""

import zipfile
import os
import struct
import zlib
import csv

BASE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(BASE, 'weld_figures')

# ============================================================
# Part 1: PNG rendering (raw bytes, no external libs)
# ============================================================


def _png_bytes(w, h, pixels):
    """Encode an RGB pixel grid (list of rows of (r,g,b)) as PNG bytes."""
    def chunk(chunk_type, data):
        c = chunk_type + data
        crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
        return struct.pack('>I', len(data)) + c + crc

    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))

    raw = bytearray()
    for row in pixels:
        raw.append(0)  # filter: none
        for (r, g, b) in row:
            raw += struct.pack('BBB', r, g, b)
    idat = chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    iend = chunk(b'IEND', b'')
    return sig + ihdr + idat + iend


class Canvas:
    """Tiny RGB raster canvas with plotting primitives."""

    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w = w
        self.h = h
        self.px = [[bg for _ in range(w)] for _ in range(h)]

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = color

    def hline(self, x0, x1, y, color):
        if x0 > x1:
            x0, x1 = x1, x0
        for x in range(x0, x1 + 1):
            self.set(x, y, color)

    def vline(self, x, y0, y1, color):
        if y0 > y1:
            y0, y1 = y1, y0
        for y in range(y0, y1 + 1):
            self.set(x, y, color)

    def rect_fill(self, x0, y0, x1, y1, color):
        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.set(x, y, color)

    def line(self, x0, y0, x1, y1, color, width=1):
        """Bresenham line with optional thickness."""
        x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for ox in range(-(width // 2), width // 2 + 1):
                for oy in range(-(width // 2), width // 2 + 1):
                    self.set(x0 + ox, y0 + oy, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, radius, color):
        for y in range(-radius, radius + 1):
            for x in range(-radius, radius + 1):
                if x * x + y * y <= radius * radius:
                    self.set(cx + x, cy + y, color)

    def save(self, path):
        with open(path, 'wb') as f:
            f.write(_png_bytes(self.w, self.h, self.px))


# --- minimal 5x7 bitmap font for axis labels / annotations ---

_FONT = {
    '0': ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    '1': ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    '2': ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    '3': ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    '4': ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    '5': ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    '6': ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    '7': ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    '8': ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    '9': ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    '-': ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    '.': ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    '+': ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    ' ': ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    'V': ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    'x': ["00000", "00000", "10001", "01010", "00100", "01010", "10001"],
    'm': ["00000", "00000", "11010", "10101", "10101", "10101", "10101"],
    'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    'M': ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    'Z': ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    'C': ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    'N': ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    '(': ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ')': ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    '/': ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
}


def draw_text(canvas, x, y, text, color=(20, 20, 20), scale=1):
    """Draw text using the tiny bitmap font. x,y = top-left."""
    cx = x
    for ch in text:
        glyph = _FONT.get(ch, _FONT[' '])
        for ry, rowbits in enumerate(glyph):
            for rx, bit in enumerate(rowbits):
                if bit == '1':
                    for sx in range(scale):
                        for sy in range(scale):
                            canvas.set(cx + rx * scale + sx, y + ry * scale + sy, color)
        cx += (6 * scale)
    return cx


# ============================================================
# Part 2: read data
# ============================================================


def read_traverse():
    """Return {weld_type: [(x, mean, std, zone), ...]} sorted by x."""
    data = {}
    with open(os.path.join(BASE, 'weld_hardness_traverse.csv'), newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            wt = row['Weld_Type']
            data.setdefault(wt, []).append(
                (float(row['x_mm']), float(row['Mean_HV']),
                 float(row['StdDev_HV']), row['Zone'])
            )
    for wt in data:
        data[wt].sort(key=lambda t: t[0])
    return data


def read_toughness():
    rows = []
    with open(os.path.join(BASE, 'weld_toughness_data.csv'), newline='') as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def read_roomtemp():
    rows = []
    with open(os.path.join(BASE, 'weld_hardness_roomtemp.csv'), newline='') as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


# ============================================================
# Part 3: render one traverse profile plot per weld
# ============================================================


def render_profile(weld_type, series, out_path):
    """Render a Mean_HV vs x line chart with +-1 SD band and fusion lines."""
    W, H = 900, 560
    ML, MR, MT, MB = 90, 40, 60, 70   # margins
    plot_w = W - ML - MR
    plot_h = H - MT - MB

    c = Canvas(W, H, bg=(255, 255, 255))

    xs = [p[0] for p in series]
    means = [p[1] for p in series]
    stds = [p[2] for p in series]

    x_min, x_max = -8.0, 8.0
    y_min = 140.0
    y_max = 280.0

    def px(x):
        return ML + (x - x_min) / (x_max - x_min) * plot_w

    def py(y):
        return MT + (y_max - y) / (y_max - y_min) * plot_h

    # zone shading: HAZ bands (3.8..5.0 on each side) and fusion zone (|x|<3.8)
    haz = (233, 240, 250)
    fz = (245, 238, 228)
    c.rect_fill(int(px(-3.8)), MT, int(px(3.8)), MT + plot_h, fz)
    c.rect_fill(int(px(-5.0)), MT, int(px(-3.8)), MT + plot_h, haz)
    c.rect_fill(int(px(3.8)), MT, int(px(5.0)), MT + plot_h, haz)

    # grid + y ticks
    grid = (222, 222, 222)
    axis = (40, 40, 40)
    yt = int(y_min)
    while yt <= y_max:
        y = int(py(yt))
        c.hline(ML, ML + plot_w, y, grid)
        draw_text(c, 40, y - 3, str(yt), color=(60, 60, 60))
        yt += 20
    # x ticks every 2 mm
    xt = int(x_min)
    while xt <= x_max:
        x = int(px(xt))
        c.vline(x, MT, MT + plot_h, grid)
        label = ('+' if xt > 0 else '') + str(xt)
        draw_text(c, x - 6, MT + plot_h + 8, label, color=(60, 60, 60))
        xt += 2

    # axes
    c.vline(ML, MT, MT + plot_h, axis)
    c.hline(ML, ML + plot_w, MT + plot_h, axis)

    # +-1 SD band (light gray polygon approximated as vertical strips)
    band = (208, 208, 208)
    for i in range(len(series)):
        x = int(px(xs[i]))
        y_hi = int(py(means[i] + stds[i]))
        y_lo = int(py(means[i] - stds[i]))
        c.vline(x, y_hi, y_lo, band)

    # fusion lines at +-5 mm (dashed red)
    fusion = (200, 40, 40)
    for fx in (-5.0, 5.0):
        x = int(px(fx))
        yy = MT
        while yy < MT + plot_h:
            c.vline(x, yy, min(yy + 6, MT + plot_h), fusion)
            yy += 12

    # mean profile polyline
    curve = (20, 70, 160)
    for i in range(len(series) - 1):
        c.line(px(xs[i]), py(means[i]), px(xs[i + 1]), py(means[i + 1]), curve, width=2)

    # title + axis labels
    draw_text(c, ML, 20, weld_type + '  HV0.5 traverse', color=(20, 20, 20), scale=2)
    draw_text(c, ML + plot_w // 2 - 70, H - 22, 'x (mm) from centerline', color=(30, 30, 30))
    # y axis label (vertical-ish, drawn stacked)
    draw_text(c, 8, MT + plot_h // 2 - 30, 'HV0.5', color=(30, 30, 30))

    # annotate fusion lines
    draw_text(c, int(px(-5.0)) - 26, MT - 14, '-5 mm', color=fusion)
    draw_text(c, int(px(5.0)) - 20, MT - 14, '+5 mm', color=fusion)

    c.save(out_path)
    print("  Created {} ({}x{})".format(out_path, W, H))


def create_figures(traverse):
    os.makedirs(FIG_DIR, exist_ok=True)
    files = {}
    order = ['X70-X70', 'S355-S355', 'X70-S355']
    for wt in order:
        fname = 'traverse_{}.png'.format(wt.replace('-', '_'))
        path = os.path.join(FIG_DIR, fname)
        render_profile(wt, traverse[wt], path)
        # record image pixel size for the drawing XML
        files[wt] = (fname, 900, 560)
    return files


# ============================================================
# Part 4: OOXML assembly
# ============================================================

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults><w:rPrDefault><w:rPr>
    <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
    <w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/><w:pPr><w:jc w:val="both"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption"><w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="240"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption"><w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="160" w:after="60"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Note"><w:name w:val="Note"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="360" w:right="360"/><w:spacing w:before="120"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
</w:styles>'''


def esc(text):
    return (str(text).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def run(text, bold=False, italic=False, size=None):
    props = []
    if bold:
        props.append('<w:b/>')
    if italic:
        props.append('<w:i/>')
    if size:
        props.append('<w:sz w:val="{0}"/><w:szCs w:val="{0}"/>'.format(size))
    rpr = '<w:rPr>' + ''.join(props) + '</w:rPr>' if props else ''
    return '<w:r>{}<w:t xml:space="preserve">{}</w:t></w:r>'.format(rpr, esc(text))


def para(text, style='Normal', bold=False, italic=False):
    ppr = '<w:pPr><w:pStyle w:val="{}"/></w:pPr>'.format(style)
    return '<w:p>{}{}</w:p>'.format(ppr, run(text, bold=bold, italic=italic))


def table(headers, rows, col_widths=None, font_size=20):
    n = len(headers)
    total = 9200
    if col_widths is None:
        col_widths = [total // n] * n
    tbl = ['<w:tbl>']
    tbl.append('<w:tblPr><w:tblW w:w="{}" w:type="dxa"/><w:tblLayout w:type="fixed"/>'.format(total))
    tbl.append('<w:tblBorders>')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        tbl.append('<w:{} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'.format(edge))
    tbl.append('</w:tblBorders></w:tblPr>')
    tbl.append('<w:tblGrid>' + ''.join('<w:gridCol w:w="{}"/>'.format(w) for w in col_widths) + '</w:tblGrid>')

    # header
    tbl.append('<w:tr>')
    for i, h in enumerate(headers):
        tbl.append('<w:tc><w:tcPr><w:tcW w:w="{}" w:type="dxa"/>'.format(col_widths[i]))
        tbl.append('<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>')
        tbl.append('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="20"/></w:pPr>{}</w:p></w:tc>'.format(
            run(h, bold=True, size=font_size)))
    tbl.append('</w:tr>')

    for row in rows:
        tbl.append('<w:tr>')
        for i in range(n):
            cell = row[i] if i < len(row) else ''
            tbl.append('<w:tc><w:tcPr><w:tcW w:w="{}" w:type="dxa"/></w:tcPr>'.format(col_widths[i]))
            tbl.append('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="20"/></w:pPr>{}</w:p></w:tc>'.format(
                run(cell, size=font_size)))
        tbl.append('</w:tr>')
    tbl.append('</w:tbl>')
    tbl.append('<w:p/>')
    return ''.join(tbl)


def image_para(rel_id, px_w, px_h, doc_id):
    """Embed a PNG as an inline drawing. Convert pixels to EMU (96 dpi)."""
    emu_w = int(px_w * 9525)
    emu_h = int(px_h * 9525)
    # scale down to fit ~6.0 inch page width (5486400 EMU)
    max_w = 5486400
    if emu_w > max_w:
        scale = max_w / emu_w
        emu_w = int(emu_w * scale)
        emu_h = int(emu_h * scale)
    return (
        '<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        '<wp:extent cx="{ew}" cy="{eh}"/>'
        '<wp:docPr id="{did}" name="Picture {did}"/>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr><pic:cNvPr id="{did}" name="Picture {did}"/><pic:cNvPicPr/></pic:nvPicPr>'
        '<pic:blipFill><a:blip r:embed="{rid}" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
        '<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{ew}" cy="{eh}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'
    ).format(ew=emu_w, eh=emu_h, did=doc_id, rid=rel_id)


# ============================================================
# Part 5: build document body
# ============================================================


def cvn_rows(rows, temp):
    out = []
    for r in rows:
        if r['Test_Temp_C'] == temp:
            out.append([r['Weld_Type'], r['Notch_Location'],
                        '{} +/- {}'.format(r['Mean_J'], r['StdDev_J']),
                        r['COV_pct']])
    return out


def build_body(traverse, toughness, roomtemp, fig_files, fig_rel_ids):
    b = []
    b.append(para('Weld Mechanical Property Analysis: X70 and S355 Joints (E6018 Filler)', 'Title'))

    # 1. Intro
    b.append(para('1. Introduction', 'Heading1'))
    b.append(para(
        'This report compiles the mechanical-property characterisation of three '
        'arc-welded joints, all produced with an E6018 filler electrode: a similar '
        'X70-X70 joint (high-strength pipeline steel), a similar S355-S355 joint '
        '(structural steel), and a dissimilar X70-S355 joint. Three property sets are '
        'reported: Charpy V-notch (CVN) impact toughness at +20 C and -20 C, '
        'room-temperature Vickers hardness (HV0.5) by zone, and a full Vickers '
        'microhardness traverse across each weld.'))

    # 2. Materials & method
    b.append(para('2. Materials and Method', 'Heading1'))
    b.append(para(
        'CVN impact specimens were 10 x 10 x 55 mm and tested per ISO 148-1, with the '
        'notch located in the weld metal (WM), heat-affected zone (HAZ) or base metal '
        '(BM); five specimens (n = 5) were tested per condition. Vickers hardness was '
        'measured under an HV0.5 load per ISO 6507-1 at room temperature (~23 C). The '
        'microhardness traverse ran from x = -8.0 mm to +8.0 mm across the weld '
        'centerline at 0.1 mm intervals (161 points per weld), with n = 3 indentations '
        'per point. The fusion-line interfaces are located at x = -5 mm and x = +5 mm.'))

    # 3. CVN toughness
    b.append(para('3. Charpy V-Notch (CVN) Impact Toughness', 'Heading1'))
    b.append(para('Absorbed energy reported as Mean +/- StdDev in joules (J); COV is the '
                  'coefficient of variation. n = 5 per condition.'))
    cvn_headers = ['Weld Type', 'Notch Location', 'Mean +/- SD (J)', 'COV (%)']
    cvn_widths = [2400, 3000, 2400, 1400]

    b.append(para('Table 1. CVN impact energy at +20 C.', 'TableCaption'))
    b.append(table(cvn_headers, cvn_rows(toughness, '20'), cvn_widths))
    b.append(para('Table 2. CVN impact energy at -20 C.', 'TableCaption'))
    b.append(table(cvn_headers, cvn_rows(toughness, '-20'), cvn_widths))

    # 4. Room-temperature hardness
    b.append(para('4. Room-Temperature Vickers Hardness (HV0.5)', 'Heading1'))
    b.append(para('Average hardness per zone (HV0.5, ISO 6507-1, n = 5 per zone).'))
    rt_headers = ['Weld Type', 'Zone', 'Avg HV0.5', 'StdDev (HV)']
    rt_rows = [[r['Weld_Type'], r['Zone'], r['Avg_Hardness_HV0.5'], r['StdDev_HV']]
               for r in roomtemp]
    b.append(para('Table 3. Average room-temperature hardness by weld and zone.', 'TableCaption'))
    b.append(table(rt_headers, rt_rows, [2400, 3400, 1700, 1700]))

    # 5. Microhardness traverse
    b.append(para('5. Microhardness Traverse Across the Weld', 'Heading1'))
    b.append(para(
        'The Vickers microhardness traverse (HV0.5) is plotted below for each weld as '
        'Mean HV versus distance x from the weld centerline. The shaded central region '
        'is the E6018 fusion zone (|x| < 3.8 mm); the flanking bands are the HAZ '
        '(3.8 <= |x| < 5.0 mm); the dashed red lines mark the fusion-line interfaces at '
        'x = +/-5 mm; and the light gray vertical whiskers denote the +/-1 SD spread '
        '(n = 3 per point). A condensed numeric profile (every 0.5 mm) follows each plot.'))

    tr_headers = ['x (mm)', 'Mean (HV)', 'StdDev (HV)', 'Zone']
    tr_widths = [1500, 2000, 2000, 3700]
    order = ['X70-X70', 'S355-S355', 'X70-S355']
    fig_no = 1
    doc_id = 100
    for wt in order:
        b.append(para('5.{} {} weld'.format(fig_no, wt), 'Heading2'))
        # figure
        _, pw, ph = fig_files[wt]
        b.append(image_para(fig_rel_ids[wt], pw, ph, doc_id))
        doc_id += 1
        b.append(para('Figure {}. HV0.5 microhardness traverse for the {} weld. '
                      'Dashed red lines = fusion lines at x = +/-5 mm; whiskers = +/-1 SD.'
                      .format(fig_no, wt), 'FigureCaption'))
        # condensed table every 0.5 mm
        series = traverse[wt]
        cond = [(x, m, s, z) for (x, m, s, z) in series if abs(round(x * 10) % 5) == 0]
        rows = [['{:+.1f}'.format(x), '{:.1f}'.format(m), '{:.1f}'.format(s), z]
                for (x, m, s, z) in cond]
        b.append(para('Table {}. Condensed HV0.5 traverse (every 0.5 mm) for the {} weld.'
                      .format(fig_no + 3, wt), 'TableCaption'))
        b.append(table(tr_headers, rows, tr_widths))
        fig_no += 1

    # 6. Observations
    b.append(para('6. Observations and Trends', 'Heading1'))
    for line in [
        'For every weld the base metal is the toughest zone, followed by the HAZ, with '
        'the E6018 weld metal the lowest in CVN energy; all zones lose toughness from '
        '+20 C to -20 C.',
        'The X70 material is both harder and tougher than S355: X70 base metal is around '
        '215 HV versus around 165 HV for S355, and X70-X70 CVN energies exceed the '
        'S355-S355 values at both test temperatures.',
        'The dissimilar X70-S355 weld is asymmetric and intermediate: the stiffer, harder '
        'X70 base metal and HAZ sit on the left (x < 0) while the softer S355 side sits on '
        'the right (x > 0), and its properties fall between the two similar joints.',
        'A distinct HAZ hardness peak (about 250 HV on the X70 side, about 206 HV on the '
        'S355 side) appears just inside each fusion line, consistent with a hardened '
        'transformation microstructure.',
        'E6018 is a 60-ksi-class filler, so the weld metal undermatches X70: the fusion '
        'zone (about 190-196 HV) is softer than the X70 base metal, producing the '
        'characteristic dip at the weld centerline.',
    ]:
        b.append(para('- ' + line, 'Normal'))

    # 7. Closing note
    b.append(para('7. Note on Data Provenance', 'Heading1'))
    b.append(para(
        'The values in this report are representative, literature-consistent (synthetic) '
        'figures generated for illustration and analysis. They are not measured laboratory '
        'results and should not be cited as experimental data.', 'Note'))

    return '\n'.join(b)


def create_docx(output_path):
    traverse = read_traverse()
    toughness = read_toughness()
    roomtemp = read_roomtemp()

    print("Creating traverse profile figures...")
    fig_files = create_figures(traverse)

    # relationship ids: rId1 styles, rId2.. images
    order = ['X70-X70', 'S355-S355', 'X70-S355']
    fig_rel_ids = {}
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    rid = 2
    media = {}
    for wt in order:
        fname, _, _ = fig_files[wt]
        rel_id = 'rId{}'.format(rid)
        fig_rel_ids[wt] = rel_id
        rels.append('<Relationship Id="{}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{}"/>'.format(rel_id, fname))
        media[fname] = os.path.join(FIG_DIR, fname)
        rid += 1
    rels.append('</Relationships>')
    word_rels = '\n'.join(rels)

    body = build_body(traverse, toughness, roomtemp, fig_files, fig_rel_ids)

    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">\n'
                '<w:body>\n' + body +
                '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
                '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
                'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>\n'
                '</w:body></w:document>')

    print("Creating Word document...")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
        for fname, path in media.items():
            with open(path, 'rb') as f:
                zf.writestr('word/media/{}'.format(fname), f.read())

    size_kb = os.path.getsize(output_path) / 1024
    print("  Created {} ({:.1f} KB)".format(output_path, size_kb))


if __name__ == '__main__':
    create_docx(os.path.join(BASE, 'Weld_Mechanical_Property_Analysis.docx'))
    print("Done.")
