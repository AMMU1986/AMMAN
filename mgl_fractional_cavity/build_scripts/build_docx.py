"""Assemble the manuscript .docx from content.py using raw OOXML (python-docx unavailable)."""
import os
import re
import struct
import zipfile
from xml.sax.saxutils import escape

import omml
from content import B

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(HERE, "figs")
OUT = os.path.join(os.path.dirname(HERE), "MGL_fractional_cavity_paper.docx")
TEXT_W = 9026  # twips, A4 with 1-inch margins
NS = ('xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
      'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
      'xmlns:o="urn:schemas-microsoft-com:office:office" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
      'xmlns:v="urn:schemas-microsoft-com:vml" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:w10="urn:schemas-microsoft-com:office:word" '
      'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')

rels = []      # (rId, type, target, external)
media = []     # (name, path)


def add_rel(typ, target, external=False):
    rid = "rId%d" % (len(rels) + 10)
    rels.append((rid, typ, target, external))
    return rid


def trun(text, bold=False, italic=False, size=None, highlight=None, color=None):
    if not text:
        return ""
    pr = ""
    if bold:
        pr += "<w:b/>"
    if italic:
        pr += "<w:i/>"
    if color:
        pr += '<w:color w:val="%s"/>' % color
    if size:
        pr += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size)
    if highlight:
        pr += '<w:highlight w:val="%s"/>' % highlight
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (
        "<w:rPr>%s</w:rPr>" % pr if pr else "", escape(text))


def inline(text, **kw):
    """Text with $...$ inline math."""
    parts = re.split(r"(\$[^$]+\$)", text)
    out = []
    for p in parts:
        if p.startswith("$") and p.endswith("$") and len(p) > 1:
            out.append(omml.omath(p[1:-1]))
        else:
            out.append(trun(p, **kw))
    return "".join(out)


def para(content, style=None, align=None, extra_ppr=""):
    ppr = ""
    if style:
        ppr += '<w:pStyle w:val="%s"/>' % style
    ppr += extra_ppr
    if align:
        ppr += '<w:jc w:val="%s"/>' % align
    return "<w:p><w:pPr>%s</w:pPr>%s</w:p>" % (ppr, content)


def png_size(path):
    with open(path, "rb") as fh:
        d = fh.read(32)
    return struct.unpack(">II", d[16:24])


def figure(fname, caption, idx):
    path = os.path.join(FIGS, fname)
    name = "image%d.png" % idx
    media.append((name, path))
    rid = add_rel("http://schemas.openxmlformats.org/officeDocument/2006/relationships/image", "media/" + name)
    w, h = png_size(path)
    cx = int(6.0 * 914400)
    cy = int(cx * h / w)
    if cy > int(7.6 * 914400):
        cy = int(7.6 * 914400)
        cx = int(cy * w / h)
    drawing = (
        '<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
        '<wp:extent cx="%d" cy="%d"/><wp:docPr id="%d" name="Figure %d"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
        '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic><pic:nvPicPr><pic:cNvPr id="%d" name="%s"/><pic:cNvPicPr/></pic:nvPicPr>'
        '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
        '</a:graphicData></a:graphic></wp:inline></w:drawing></w:r>') % (cx, cy, idx, idx, idx, name, rid, cx, cy)
    out = para(drawing, align="center", extra_ppr='<w:keepNext/><w:spacing w:before="200" w:after="60"/>')
    m = re.match(r"(Figure \d+\.)(.*)", caption, re.S)
    out += para(trun(m.group(1), bold=True) + inline(m.group(2)), style="Caption")
    return out


def table(caption, rows, widths):
    m = re.match(r"(Table \d+\.)(.*)", caption, re.S)
    out = para(trun(m.group(1), bold=True) + inline(m.group(2)), style="Caption",
               extra_ppr='<w:keepNext/><w:spacing w:before="240" w:after="80"/>')
    tw = sum(widths)
    grid = "".join('<w:gridCol w:w="%d"/>' % w for w in widths)
    t = ('<w:tbl><w:tblPr><w:tblW w:w="%d" w:type="dxa"/><w:jc w:val="center"/>'
         '<w:tblBorders><w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
         '<w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
         '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/></w:tblBorders>'
         '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar>'
         '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
         '</w:tblPr><w:tblGrid>%s</w:tblGrid>') % (tw, grid)
    for ri, row in enumerate(rows):
        hdr = ri == 0
        t += "<w:tr>%s" % ('<w:trPr><w:tblHeader/></w:trPr>' if hdr else "")
        for ci, cell in enumerate(row):
            border = ('<w:tcBorders><w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/></w:tcBorders>'
                      if hdr else "")
            shade = '<w:shd w:val="clear" w:color="auto" w:fill="EDEFF3"/>' if hdr else ""
            t += ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s%s<w:vAlign w:val="center"/></w:tcPr>%s</w:tc>'
                  % (widths[ci], border, shade,
                     para(inline(cell, bold=hdr, size=20), style="TableText")))
        t += "</w:tr>"
    t += "</w:tbl>"
    return out + t + para("", extra_ppr='<w:spacing w:before="0" w:after="120"/>')


def equation(latex, num):
    content = ("<w:r><w:tab/></w:r>" + omml.omath(latex) +
               "<w:r><w:tab/></w:r>" + trun("(%d)" % num))
    tabs = ('<w:tabs><w:tab w:val="center" w:pos="%d"/><w:tab w:val="right" w:pos="%d"/></w:tabs>'
            '<w:spacing w:before="120" w:after="120"/>') % (TEXT_W // 2, TEXT_W)
    return para(content, style="Equation", extra_ppr=tabs)


def build_body():
    out = []
    fig_i = 0
    eq_nums = []
    for blk in B:
        k = blk[0]
        if k == "title":
            out.append(para(trun(blk[1]), style="Title"))
        elif k == "authors":
            out.append(para(trun(blk[1], italic=True), style="Authors"))
        elif k == "h1":
            out.append(para(trun(blk[1]), style="Heading1"))
        elif k == "h1u":
            out.append(para(trun(blk[1]), style="Heading1"))
        elif k == "h2":
            out.append(para(inline(blk[1]), style="Heading2"))
        elif k == "p":
            out.append(para(inline(blk[1]), style="BodyText"))
        elif k == "abstract":
            out.append(para(inline(blk[1]), style="Abstract"))
        elif k == "kw":
            out.append(para(trun("Keywords: ", bold=True) + trun(blk[1], italic=True), style="Abstract"))
        elif k == "eq":
            eq_nums.append(blk[2])
            out.append(equation(blk[1], blk[2]))
        elif k == "fig":
            fig_i += 1
            out.append(figure(blk[1], blk[2], fig_i))
        elif k == "table":
            out.append(table(blk[1], blk[2], blk[3]))
        elif k == "ref":
            url = "https://doi.org/" + blk[2]
            rid = add_rel("http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", url, True)
            link = ('<w:hyperlink r:id="%s" w:history="1"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr>'
                    '<w:t xml:space="preserve">%s</w:t></w:r></w:hyperlink>') % (rid, escape(blk[2]))
            out.append(para(trun(blk[1]) + link, style="Reference"))
        elif k == "note":
            out.append(para(trun(blk[1], bold=True, highlight="yellow"), style="BodyText",
                            extra_ppr='<w:spacing w:before="240"/>'))
    assert eq_nums == list(range(1, 48)), eq_nums
    assert fig_i == 8
    return "".join(out)


STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="en-GB"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
<w:style w:type="paragraph" w:styleId="BodyText"><w:name w:val="Body Text"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:jc w:val="both"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="240" w:after="240"/><w:jc w:val="center"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Authors"><w:name w:val="Authors"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="360"/><w:jc w:val="center"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Abstract"><w:name w:val="Abstract"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="567" w:right="567"/><w:jc w:val="both"/></w:pPr><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="BodyText"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="360" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="BodyText"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:i/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Equation"><w:name w:val="Equation"/><w:basedOn w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:after="240"/><w:jc w:val="both"/></w:pPr><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="TableText"><w:name w:val="Table Text"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="40" w:after="40" w:line="240" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Reference"><w:name w:val="Reference"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="567" w:hanging="567"/><w:jc w:val="both"/></w:pPr><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Footer"><w:name w:val="footer"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/></w:pPr><w:rPr><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/><w:rPr><w:color w:val="0563C1"/><w:u w:val="single"/></w:rPr></w:style>
</w:styles>'''

FOOTER = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr %s><w:p><w:pPr><w:pStyle w:val="Footer"/></w:pPr>'
          '<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
          '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r>'
          '</w:p></w:ftr>') % NS

SETTINGS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
            '<w:defaultTabStop w:val="720"/><m:mathPr><m:mathFont m:val="Cambria Math"/><m:defJc m:val="centerGroup"/></m:mathPr>'
            '<w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat>'
            '</w:settings>')


def main():
    body = build_body()
    frid = add_rel("http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer", "footer1.xml")
    sect = ('<w:sectPr><w:footerReference w:type="default" r:id="%s"/><w:pgSz w:w="11906" w:h="16838"/>'
            '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>'
            '</w:sectPr>') % frid
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document %s><w:body>%s%s</w:body></w:document>'
           % (NS, body, sect))
    doc_rels = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
                '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>']
    for rid, typ, target, ext in rels:
        doc_rels.append('<Relationship Id="%s" Type="%s" Target="%s"%s/>' % (
            rid, typ, escape(target), ' TargetMode="External"' if ext else ""))
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Default Extension="png" ContentType="image/png"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
          '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
          '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '</Types>')
    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
                 '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                 '</Relationships>')
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>MGL Thermoelasticity of a Spherical Cavity and a Cylindrical Hole under Thermal Shock with Fractional-Order Heat Conduction</dc:title>'
            '</cp:coreProperties>')
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("docProps/core.xml", core)
        z.writestr("word/document.xml", doc)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/settings.xml", SETTINGS)
        z.writestr("word/footer1.xml", FOOTER)
        z.writestr("word/_rels/document.xml.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">%s</Relationships>'
                   % "".join(doc_rels))
        for name, path in media:
            z.write(path, "word/media/" + name)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
