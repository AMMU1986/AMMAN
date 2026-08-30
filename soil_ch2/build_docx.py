# -*- coding: utf-8 -*-
"""Pure-Python DOCX builder (no python-docx). Builds Chapter 2 with headings,
paragraphs, tables, and embedded PNG figures. Produces a valid .docx (OOXML)."""
import os
import struct
import zipfile
from xml.sax.saxutils import escape

import content as C
import body as B

HERE = os.path.dirname(__file__)
FIGDIR = os.path.join(HERE, "figures")
OUT_DOCX = os.path.join(os.path.dirname(HERE), "Chapter2_Soil_Pollution_Global_Scale.docx")

EMU_PER_PX = 9525  # 96 dpi


def png_size(path):
    with open(path, "rb") as f:
        data = f.read(33)
    w, h = struct.unpack(">II", data[16:24])
    return w, h


# collect images
images = []  # list of (relid, filename, mediapath)
media_index = {}


def register_image(path):
    if path in media_index:
        return media_index[path]
    idx = len(images) + 1
    fname = "image%d.png" % idx
    relid = "rIdImg%d" % idx
    images.append((relid, fname, path))
    media_index[path] = (relid, fname)
    return media_index[path]


# ---- XML fragment builders ----
def run(text, bold=False, italic=False, size=None, color=None):
    rpr = ""
    props = ""
    if bold:
        props += "<w:b/>"
    if italic:
        props += "<w:i/>"
    if size:
        props += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size)
    if color:
        props += '<w:color w:val="%s"/>' % color
    if props:
        rpr = "<w:rPr>%s</w:rPr>" % props
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, escape(text))


def para(runs_xml, style=None, align=None, spacing_after=160, spacing_before=0):
    ppr = "<w:pPr>"
    if style:
        ppr += '<w:pStyle w:val="%s"/>' % style
    ppr += '<w:spacing w:before="%d" w:after="%d" w:line="276" w:lineRule="auto"/>' % (spacing_before, spacing_after)
    if align:
        ppr += '<w:jc w:val="%s"/>' % align
    ppr += "</w:pPr>"
    return "<w:p>%s%s</w:p>" % (ppr, runs_xml)


def heading(text, level):
    sizes = {1: 32, 2: 28, 3: 24}
    colors = {1: "1F3864", 2: "2E5496", 3: "2E5496"}
    before = {1: 240, 2: 300, 3: 200}
    r = run(text, bold=True, size=sizes[level], color=colors[level])
    return para(r, spacing_after=120, spacing_before=before[level])


def image_para(path, caption_num, caption_text):
    relid, fname = register_image(path)
    w, h = png_size(path)
    # scale to max 5.8 inches wide (5.8*914400 EMU)
    max_w_emu = int(5.8 * 914400)
    cw = w * EMU_PER_PX
    ch = h * EMU_PER_PX
    if cw > max_w_emu:
        scale = max_w_emu / cw
        cw = int(cw * scale)
        ch = int(ch * scale)
    drawing = (
        '<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
        '<wp:extent cx="%d" cy="%d"/>' % (cw, ch) +
        '<wp:docPr id="%d" name="%s"/>' % (caption_num, fname) +
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr><pic:cNvPr id="%d" name="%s"/><pic:cNvPicPr/></pic:nvPicPr>' % (caption_num, fname) +
        '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>' % relid +
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>' % (cw, ch) +
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>'
    )
    img_p = para(drawing, align="center", spacing_after=60, spacing_before=160)
    cap_r = run("Figure %d. " % caption_num, bold=True, size=18) + run(caption_text, italic=True, size=18)
    cap_p = para(cap_r, align="center", spacing_after=200)
    return img_p + cap_p


def table_xml(num, caption, headers, rows):
    cap_r = run("Table %d. " % num, bold=True, size=18) + run(caption, italic=True, size=18)
    cap_p = para(cap_r, align="left", spacing_after=60, spacing_before=160)
    ncols = len(headers)
    total_w = 9360  # twips (~6.5in)
    col_w = total_w // ncols
    grid = "<w:tblGrid>" + "".join('<w:gridCol w:w="%d"/>' % col_w for _ in range(ncols)) + "</w:tblGrid>"

    def cell(text, header=False):
        shd = '<w:shd w:val="clear" w:color="auto" w:fill="1F3864"/>' if header else ""
        tcpr = '<w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s<w:tcMar><w:top w:w="40" w:type="dxa"/><w:left w:w="80" w:type="dxa"/><w:bottom w:w="40" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tcMar></w:tcPr>' % (col_w, shd)
        if header:
            r = run(text, bold=True, size=18, color="FFFFFF")
        else:
            r = run(text, size=18)
        p = para(r, spacing_after=0, spacing_before=0)
        return "<w:tc>%s%s</w:tc>" % (tcpr, p)

    borders = ('<w:tblBorders>'
               '<w:top w:val="single" w:sz="4" w:color="8090B0"/>'
               '<w:left w:val="single" w:sz="4" w:color="8090B0"/>'
               '<w:bottom w:val="single" w:sz="4" w:color="8090B0"/>'
               '<w:right w:val="single" w:sz="4" w:color="8090B0"/>'
               '<w:insideH w:val="single" w:sz="4" w:color="B0B8C8"/>'
               '<w:insideV w:val="single" w:sz="4" w:color="B0B8C8"/>'
               '</w:tblBorders>')
    tblpr = '<w:tblPr><w:tblW w:w="%d" w:type="dxa"/>%s<w:tblLook w:val="04A0"/></w:tblPr>' % (total_w, borders)
    header_row = "<w:tr>" + "".join(cell(h, True) for h in headers) + "</w:tr>"
    body_rows = ""
    for row in rows:
        body_rows += "<w:tr>" + "".join(cell(c) for c in row) + "</w:tr>"
    tbl = "<w:tbl>%s%s%s%s</w:tbl>" % (tblpr, grid, header_row, body_rows)
    spacer = para("", spacing_after=160)
    return cap_p + tbl + spacer


# ---- Build document body ----
parts = []

# Title block
parts.append(para(run(C.BOOK_TITLE, bold=True, size=40, color="1F3864"), align="center", spacing_after=40, spacing_before=200))
parts.append(para(run(C.BOOK_SUBTITLE, italic=True, size=24, color="2E5496"), align="center", spacing_after=240))
parts.append(heading(C.CHAPTER_TITLE, 1))

# Abstract (no citations)
parts.append(para(run("Abstract", bold=True, size=24, color="1F3864"), spacing_after=100, spacing_before=160))
parts.append(para(run(C.ABSTRACT, italic=False, size=20), align="both", spacing_after=200))
parts.append(para(
    run("Keywords: ", bold=True, size=20) +
    run("soil pollution; heavy metals; global mapping; pollution hotspots; "
        "remote sensing; risk assessment; remediation prioritization; Anthropocene", size=20),
    spacing_after=240))

# Body blocks
for kind, payload in B.BODY:
    if kind == "h2":
        parts.append(heading(payload, 2))
    elif kind == "h3":
        parts.append(heading(payload, 3))
    elif kind == "p":
        parts.append(para(run(payload, size=22), align="both", spacing_after=160))
    elif kind == "fig":
        img, num, cap = payload
        parts.append(image_para(os.path.join(FIGDIR, img), num, cap))
    elif kind == "table":
        num, cap, headers, rows = payload
        parts.append(table_xml(num, cap, headers, rows))

# References
parts.append(heading("References", 2))
for i, ref in enumerate(B.REFERENCES, 1):
    r = run("[%d] " % i, bold=True, size=20) + run(ref, size=20)
    parts.append(para(r, align="both", spacing_after=100))

sect = ('<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
        'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>')

document_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
    '<w:body>' + "".join(parts) + sect + '</w:body></w:document>'
)

# ---- Static parts ----
content_types = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Default Extension="png" ContentType="image/png"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
    '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
    '</Types>'
)

root_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
    '</Relationships>'
)

# document rels: styles + images
doc_rels_items = ['<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
for relid, fname, _ in images:
    doc_rels_items.append('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/%s"/>' % (relid, fname))
doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(doc_rels_items) + '</Relationships>')

styles_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>'
    '<w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
    '</w:styles>'
)

core_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
    'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    '<dc:title>Soil Pollution on a Global Scale</dc:title>'
    '<dc:subject>Soil Pollution in the Anthropocene - Chapter 2</dc:subject>'
    '<dc:creator>Kiro</dc:creator>'
    '<cp:keywords>soil pollution; global mapping; hotspots; remediation</cp:keywords>'
    '</cp:coreProperties>'
)

app_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
    '<Application>Kiro DOCX Builder</Application></Properties>'
)

# ---- Write ZIP ----
with zipfile.ZipFile(OUT_DOCX, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", root_rels)
    z.writestr("word/document.xml", document_xml)
    z.writestr("word/_rels/document.xml.rels", doc_rels)
    z.writestr("word/styles.xml", styles_xml)
    z.writestr("docProps/core.xml", core_xml)
    z.writestr("docProps/app.xml", app_xml)
    for relid, fname, path in images:
        with open(path, "rb") as f:
            z.writestr("word/media/%s" % fname, f.read())

print("Wrote", OUT_DOCX)

# ---- Word count (body text only, excluding XML) ----
def count_words():
    words = 0
    words += len(C.ABSTRACT.split())
    for kind, payload in B.BODY:
        if kind == "p":
            words += len(payload.split())
        elif kind == "h2" or kind == "h3":
            words += len(payload.split())
        elif kind == "fig":
            words += len(payload[2].split())
        elif kind == "table":
            words += len(payload[1].split())
            for h in payload[2]:
                words += len(h.split())
            for row in payload[3]:
                for cval in row:
                    words += len(cval.split())
    for ref in B.REFERENCES:
        words += len(ref.split())
    return words

print("Approx word count:", count_words())
print("References:", len(B.REFERENCES))
print("Figures:", len(images))
tables = sum(1 for k, _ in B.BODY if k == "table")
print("Tables:", tables)
