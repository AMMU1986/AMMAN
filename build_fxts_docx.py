#!/usr/bin/env python3
"""
Build a genuine .docx from FXTS_Delayed_CGBAM_Manuscript.md using ONLY the
Python standard library (no pandoc / python-docx available offline).

Produces: headings, paragraphs (with bold), native Word tables, equations as
centered Cambria-Math paragraphs (LaTeX shown; convert in Word if desired),
and the 7 figures embedded as SVG (with a 1x1 PNG raster fallback so they
render in Word 2016+/365).
"""
import base64, os, re, zipfile, html

HERE = os.path.dirname(__file__)
MD = os.path.join(HERE, "FXTS_Delayed_CGBAM_Manuscript.md")
FIGDIR = os.path.join(HERE, "fxts_figures")
OUT = os.path.join(HERE, "FXTS_Delayed_CGBAM_Manuscript.docx")

EMU_IN = 914400
# 1x1 transparent PNG fallback
PNG1x1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")

NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')


def esc(s):
    return html.escape(s, quote=False)


def clean_inline(s):
    s = s.replace("\\\\", " ")
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = s.replace("$", "")
    return s


def runs_from_bold(text):
    """Split **bold** segments -> list of (text, bold)."""
    out, i = [], 0
    for m in re.finditer(r"\*\*(.+?)\*\*", text):
        if m.start() > i:
            out.append((text[i:m.start()], False))
        out.append((m.group(1), True))
        i = m.end()
    if i < len(text):
        out.append((text[i:], False))
    return out or [(text, False)]


def p_xml(text, style=None, center=False, mono=False, size=None):
    text = clean_inline(text)
    ppr = "<w:pPr>"
    if style:
        ppr += '<w:pStyle w:val="%s"/>' % style
    if center:
        ppr += '<w:jc w:val="center"/>'
    ppr += "</w:pPr>"
    runs = ""
    for seg, bold in runs_from_bold(text):
        rpr = "<w:rPr>"
        if bold:
            rpr += "<w:b/>"
        if mono:
            rpr += '<w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:i/>'
        if size:
            rpr += '<w:sz w:val="%d"/>' % size
        rpr += "</w:rPr>"
        runs += '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, esc(seg))
    return "<w:p>%s%s</w:p>" % (ppr, runs)


def table_xml(rows):
    # rows: list of list of cell strings; first row = header
    def cell(txt, bold):
        txt = clean_inline(txt)
        rpr = "<w:rPr><w:b/></w:rPr>" if bold else ""
        return ('<w:tc><w:tcPr><w:tcW w:w="0" w:type="auto"/></w:tcPr>'
                '<w:p><w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p></w:tc>'
                % (rpr, esc(txt)))
    body = ('<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
            '<w:tblW w:w="0" w:type="auto"/>'
            '<w:tblBorders>'
            + "".join('<w:%s w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
                      % b for b in ("top", "left", "bottom", "right", "insideH", "insideV"))
            + "</w:tblBorders></w:tblPr>")
    for ri, row in enumerate(rows):
        body += "<w:tr>" + "".join(cell(c, ri == 0) for c in row) + "</w:tr>"
    body += "</w:tbl><w:p/>"
    return body


def drawing_xml(fig_id, rid_png, rid_svg, cx, cy):
    return (
        '<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0">'
        '<wp:extent cx="%d" cy="%d"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
        '<wp:docPr id="%d" name="Figure %d"/>'
        '<wp:cNvGraphicFramePr/>'
        '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic><pic:nvPicPr><pic:cNvPr id="%d" name="Figure %d"/><pic:cNvPicPr/></pic:nvPicPr>'
        '<pic:blipFill><a:blip r:embed="%s">'
        '<a:extLst><a:ext uri="{28A0092B-C50C-407E-A947-70E740481C1C}">'
        '<asvg:svgBlip xmlns:asvg="http://schemas.microsoft.com/office/drawing/2016/SVG/main" r:embed="%s"/>'
        '</a:ext></a:extLst></a:blip><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'
        % (cx, cy, fig_id, fig_id, fig_id, fig_id, rid_png, rid_svg, cx, cy))


# ----------------------------------------------------------------------
# parse markdown
# ----------------------------------------------------------------------
lines = open(MD, encoding="utf-8").read().split("\n")
body = []
media = []          # (svg_filename, svg_bytes)
rels = []           # (rid, target, mode)
rel_counter = [100]
fig_counter = [0]


def add_figure(svgpath):
    fig_counter[0] += 1
    fid = fig_counter[0]
    name = os.path.basename(svgpath)
    svg_bytes = open(svgpath, "rb").read()
    png_name = "fig%d.png" % fid
    svg_name = "fig%d.svg" % fid
    media.append((png_name, PNG1x1))
    media.append((svg_name, svg_bytes))
    rel_counter[0] += 1
    rid_png = "rId%d" % rel_counter[0]
    rels.append((rid_png, "media/" + png_name))
    rel_counter[0] += 1
    rid_svg = "rId%d" % rel_counter[0]
    rels.append((rid_svg, "media/" + svg_name))
    w = int(5.6 * EMU_IN)
    h = int(w * 420 / 680)
    body.append(drawing_xml(fid, rid_png, rid_svg, w, h))


i = 0
while i < len(lines):
    ln = lines[i]
    s = ln.strip()
    # equation block
    if s.startswith("$$"):
        buf = []
        if s != "$$":
            buf.append(s[2:])
        i += 1
        while i < len(lines) and lines[i].strip() != "$$" and not lines[i].strip().endswith("$$"):
            buf.append(lines[i]); i += 1
        if i < len(lines):
            last = lines[i].strip()
            if last.endswith("$$") and last != "$$":
                buf.append(last[:-2])
        eq = " ".join(x.strip() for x in buf if x.strip())
        m = re.search(r"\\tag\{(\d+)\}", eq)
        num = m.group(1) if m else ""
        eq = re.sub(r"\\tag\{\d+\}", "", eq).strip()
        shown = eq + ("          (%s)" % num if num else "")
        body.append(p_xml(shown, center=True, mono=True, size=20))
        i += 1
        continue
    # image
    mimg = re.match(r"!\[.*?\]\((.+?)\)", s)
    if mimg:
        rel = mimg.group(1)
        fp = os.path.join(HERE, rel)
        if os.path.exists(fp):
            add_figure(fp)
        i += 1
        continue
    # table
    if s.startswith("|") and i + 1 < len(lines) and set(lines[i + 1].strip()) <= set("|-: "):
        rows = []
        hdr = [c.strip() for c in s.strip("|").split("|")]
        rows.append(hdr)
        i += 2
        while i < len(lines) and lines[i].strip().startswith("|"):
            rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
            i += 1
        body.append(table_xml(rows))
        continue
    # headings
    if s.startswith("#### "):
        body.append(p_xml(s[5:], style="Heading3")); i += 1; continue
    if s.startswith("### "):
        body.append(p_xml(s[4:], style="Heading2")); i += 1; continue
    if s.startswith("## "):
        body.append(p_xml(s[3:], style="Heading1")); i += 1; continue
    if s.startswith("# "):
        body.append(p_xml(s[2:], style="Title")); i += 1; continue
    if s == "---" or s == "":
        i += 1; continue
    # list item
    if s.startswith("- ") or re.match(r"^\d+\. ", s):
        body.append(p_xml(s)); i += 1; continue
    # normal paragraph
    body.append(p_xml(s))
    i += 1

document = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document %s><w:body>%s'
    '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
    'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
    '</w:body></w:document>' % (NS, "".join(body)))

# relationships (styles + figures)
rels_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>')
for rid, tgt in rels:
    rels_xml += ('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="%s"/>'
                 % (rid, tgt))
rels_xml += "</Relationships>"

styles_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr><w:rPr><w:b/><w:sz w:val="34"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:pPr><w:spacing w:before="200" w:after="100"/></w:pPr><w:rPr><w:b/><w:sz w:val="25"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:pPr><w:spacing w:before="160" w:after="80"/></w:pPr><w:rPr><w:b/><w:i/><w:sz w:val="23"/></w:rPr></w:style>'
    '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders>'
    + "".join('<w:%s w:val="single" w:sz="4" w:space="0" w:color="auto"/>' % b
              for b in ("top", "left", "bottom", "right", "insideH", "insideV"))
    + "</w:tblBorders></w:tblPr></w:style></w:styles>")

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

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", root_rels)
    z.writestr("word/document.xml", document)
    z.writestr("word/styles.xml", styles_xml)
    z.writestr("word/_rels/document.xml.rels", rels_xml)
    for name, data in media:
        z.writestr("word/media/" + name, data)

# validate XML well-formedness
import xml.dom.minidom as mdom
for frag in (document, styles_xml, rels_xml, content_types, root_rels):
    mdom.parseString(frag)
print("OK: wrote", OUT, "(%d figures embedded)" % fig_counter[0])
print("size:", os.path.getsize(OUT), "bytes")
