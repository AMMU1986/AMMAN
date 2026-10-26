#!/usr/bin/env python3
"""Build a .docx for Chapter 22 (Smart Water Systems) using only the Python
standard library (no python-docx / pandoc needed).

Parses the chapter Markdown and emits a valid WordprocessingML package with
headings, body paragraphs, native Word tables, and the two figures embedded
(SVG with a PNG raster fallback so modern Word renders the vector art).
"""
import os, re, zlib, struct, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, "Chapter_Smart_Water_Systems_Future.md")
OUT = os.path.join(HERE, "Chapter_22_Smart_Water_Systems.docx")
FIGDIR = os.path.join(HERE, "smart_water_figures")

EMU_PER_INCH = 914400
PAGE_W_IN = 6.0  # usable content width

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))

def solid_png(path, w, h, rgb=(236, 242, 246)):
    """Write a minimal solid-colour PNG (raster fallback for the SVG)."""
    def chunk(typ, data):
        return (struct.pack(">I", len(data)) + typ + data +
                struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff))
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    row = bytes(rgb) * w
    raw = bytearray()
    for _ in range(h):
        raw.append(0)
        raw.extend(row)
    idat = zlib.compress(bytes(raw), 9)
    with open(path, "wb") as f:
        f.write(sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b""))

def runs(text):
    """Convert inline **bold** markup into a sequence of w:r runs."""
    out = []
    for i, part in enumerate(re.split(r"\*\*", text)):
        if part == "":
            continue
        bold = (i % 2 == 1)
        rpr = "<w:rPr><w:b/></w:rPr>" if bold else ""
        out.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, esc(part)))
    return "".join(out) or '<w:r><w:t xml:space="preserve"></w:t></w:r>'

def para(text, style=None, align=None, spacing_after=160):
    ppr = "<w:pPr>"
    if style:
        ppr += '<w:pStyle w:val="%s"/>' % style
    if align:
        ppr += '<w:jc w:val="%s"/>' % align
    ppr += '<w:spacing w:after="%d"/>' % spacing_after
    ppr += "</w:pPr>"
    return "<w:p>%s%s</w:p>" % (ppr, runs(text))

def table_xml(rows):
    header = rows[0]
    body = rows[1:]
    ncol = len(header)
    width = int(PAGE_W_IN * EMU_PER_INCH / 635)  # twips total (~ 1/20 pt); use dxa
    # use fixed table width in twips (6in = 8640 twips)
    total_tw = int(PAGE_W_IN * 1440)
    colw = total_tw // ncol
    grid = "".join('<w:gridCol w:w="%d"/>' % colw for _ in range(ncol))
    out = ['<w:tbl><w:tblPr><w:tblStyle w:val="TblGrid"/>'
           '<w:tblW w:w="%d" w:type="dxa"/>' % total_tw +
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:color="7A8B96"/>'
           '<w:left w:val="single" w:sz="4" w:color="7A8B96"/>'
           '<w:bottom w:val="single" w:sz="4" w:color="7A8B96"/>'
           '<w:right w:val="single" w:sz="4" w:color="7A8B96"/>'
           '<w:insideH w:val="single" w:sz="4" w:color="B9C6CE"/>'
           '<w:insideV w:val="single" w:sz="4" w:color="B9C6CE"/>'
           '</w:tblBorders></w:tblPr><w:tblGrid>%s</w:tblGrid>' % grid]
    def cell(txt, head=False):
        shd = '<w:shd w:val="clear" w:fill="0B3D5C"/>' if head else ""
        pr = ('<w:pPr><w:spacing w:after="40"/></w:pPr>')
        if head:
            r = '<w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % esc(txt)
        else:
            r = runs(txt)
        return ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s</w:tcPr>'
                '<w:p>%s%s</w:p></w:tc>' % (colw, shd, pr, r))
    out.append("<w:tr>" + "".join(cell(c, True) for c in header) + "</w:tr>")
    for row in body:
        row = row + [""] * (ncol - len(row))
        out.append("<w:tr>" + "".join(cell(c) for c in row[:ncol]) + "</w:tr>")
    out.append("</w:tbl>")
    out.append('<w:p><w:pPr><w:spacing w:after="160"/></w:pPr></w:p>')
    return "".join(out)

def image_para(rel_png, cx, cy, docpr_id, name):
    return ('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="80"/></w:pPr>'
            '<w:r><w:drawing>'
            '<wp:inline distT="0" distB="0" distL="0" distR="0" '
            'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
            '<wp:extent cx="%d" cy="%d"/>'
            '<wp:docPr id="%d" name="%s"/>'
            '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:nvPicPr><pic:cNvPr id="%d" name="%s"/><pic:cNvPicPr/></pic:nvPicPr>'
            '<pic:blipFill>'
            '<a:blip r:embed="%sp" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<a:extLst><a:ext uri="{96DAC541-7B7A-43D3-8B79-37D633B846F1}">'
            '<asvg:svgBlip xmlns:asvg="http://schemas.microsoft.com/office/drawing/2016/SVG/main" '
            'r:embed="%ss" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
            '</a:ext></a:extLst></a:blip>'
            '<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            '</pic:pic></a:graphicData></a:graphic></wp:inline>'
            '</w:drawing></w:r></w:p>'
            % (cx, cy, docpr_id, name, docpr_id, name, rel_png, rel_png, cx, cy))

# ---- parse markdown ----
with open(MD, encoding="utf-8") as f:
    lines = f.read().split("\n")

body = []
images = []  # (relbase, svgpath, w, h)
i = 0
fig_idx = 0
while i < len(lines):
    ln = lines[i].rstrip("\n")
    s = ln.strip()
    if s == "" or s == "---":
        i += 1
        continue
    # table block
    if s.startswith("|"):
        block = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            block.append(lines[i].strip())
            i += 1
        rows = []
        for r_i, r in enumerate(block):
            cells = [c.strip() for c in r.strip("|").split("|")]
            if r_i == 1 and all(set(c) <= set("-: ") for c in cells):
                continue  # separator
            rows.append(cells)
        if rows:
            body.append(table_xml(rows))
        continue
    # image
    m = re.match(r"!\[.*?\]\((.*?)\)", s)
    if m:
        fig_idx += 1
        path = m.group(1)
        svgpath = os.path.join(HERE, path)
        # read viewBox for aspect
        w, h = 900, 600
        try:
            with open(svgpath, encoding="utf-8") as sf:
                head = sf.read(400)
            wm = re.search(r'width="(\d+)"', head); hm = re.search(r'height="(\d+)"', head)
            if wm and hm:
                w, h = int(wm.group(1)), int(hm.group(1))
        except Exception:
            pass
        cx = int(PAGE_W_IN * EMU_PER_INCH)
        cy = int(cx * h / w)
        relbase = "rIdImg%d" % fig_idx
        images.append((relbase, svgpath, fig_idx))
        body.append(image_para(relbase, cx, cy, 100 + fig_idx, "Figure %d" % fig_idx))
        i += 1
        continue
    # headings
    if s.startswith("### "):
        body.append(para(s[4:], style="Heading2")); i += 1; continue
    if s.startswith("## "):
        body.append(para(s[3:], style="Heading1")); i += 1; continue
    if s.startswith("# "):
        body.append(para(s[2:], style="Title", align="center")); i += 1; continue
    # keywords / abstract label lines and normal paragraphs
    body.append(para(s))
    i += 1

document = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    '<w:body>' + "".join(body) +
    '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
    'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
    '</w:body></w:document>')

styles = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>'
    '<w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
    '<w:pPr><w:spacing w:after="240"/></w:pPr>'
    '<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:color w:val="0B3D5C"/><w:sz w:val="36"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
    '<w:pPr><w:spacing w:before="240" w:after="120"/><w:keepNext/></w:pPr>'
    '<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:color w:val="0B3D5C"/><w:sz w:val="28"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
    '<w:pPr><w:spacing w:before="180" w:after="100"/><w:keepNext/></w:pPr>'
    '<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:color w:val="1F7A9C"/><w:sz w:val="24"/></w:rPr></w:style>'
    '<w:style w:type="table" w:styleId="TblGrid"><w:name w:val="Table Grid"/></w:style>'
    '</w:styles>')

content_types = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Default Extension="png" ContentType="image/png"/>'
    '<Default Extension="svg" ContentType="image/svg+xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    '</Types>')

root_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '</Relationships>')

doc_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
media = []
for relbase, svgpath, idx in images:
    png_name = "media/image%d.png" % idx
    svg_name = "media/image%d.svg" % idx
    doc_rels.append('<Relationship Id="%sp" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="%s"/>' % (relbase, png_name))
    doc_rels.append('<Relationship Id="%ss" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="%s"/>' % (relbase, svg_name))
    media.append((png_name, svg_name, svgpath, idx))
doc_rels.append('</Relationships>')
doc_rels = "".join(doc_rels)

# generate fallback PNGs
tmp_pngs = {}
for png_name, svg_name, svgpath, idx in media:
    with open(svgpath, encoding="utf-8") as sf:
        head = sf.read(400)
    wm = re.search(r'width="(\d+)"', head); hm = re.search(r'height="(\d+)"', head)
    w = int(wm.group(1)) if wm else 900
    h = int(hm.group(1)) if hm else 600
    p = os.path.join(HERE, "_fallback_%d.png" % idx)
    solid_png(p, w, h)
    tmp_pngs[png_name] = p

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", root_rels)
    z.writestr("word/document.xml", document)
    z.writestr("word/styles.xml", styles)
    z.writestr("word/_rels/document.xml.rels", doc_rels)
    for png_name, svg_name, svgpath, idx in media:
        z.write(tmp_pngs[png_name], "word/" + png_name)
        z.write(svgpath, "word/" + svg_name)

for p in tmp_pngs.values():
    os.remove(p)

print("Wrote", OUT, "(%d bytes)" % os.path.getsize(OUT))
