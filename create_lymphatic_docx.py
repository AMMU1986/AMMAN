#!/usr/bin/env python3
"""
Build Manuscript_Lymphatic_Rerouting_Scar.docx from the markdown source using only the
Python standard library. Supports headings, inline bold/italic, numbered display equations,
GitHub-style pipe tables rendered as native Word tables, and embedded PNG figures.
"""
import os
import re
import struct
import zipfile

ROOT = "/projects/sandbox/AMMAN"
MD = os.path.join(ROOT, "Manuscript_Lymphatic_Rerouting_Scar.md")
OUT = os.path.join(ROOT, "Manuscript_Lymphatic_Rerouting_Scar.docx")

PAGE_W_EMU = 6.0 * 914400          # 6.0 inch usable content width
EMU_PER_PX = 9525                  # 96 dpi
RIGHT_TAB = 9360                   # twips, ~6.5 inch

media = []                         # list of (arcname, abspath)
rels = []                          # list of (rId, target, type)
_next = [1]


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def runs(text):
    """Convert inline **bold** / *italic* markup into a sequence of w:r runs."""
    out = []
    i = 0
    tokens = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            body, props = tok[2:-2], "<w:b/>"
        elif tok.startswith("*") and tok.endswith("*"):
            body, props = tok[1:-1], "<w:i/>"
        else:
            body, props = tok, ""
        rpr = f"<w:rPr>{props}</w:rPr>" if props else ""
        out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{esc(body)}</w:t></w:r>')
    return "".join(out)


def para(text, style=None, jc=None, size=None, bold=False, space_before=None):
    ppr = "<w:pPr>"
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if jc:
        ppr += f'<w:jc w:val="{jc}"/>'
    if space_before is not None:
        ppr += f'<w:spacing w:before="{space_before}"/>'
    ppr += "</w:pPr>"
    if bold or size:
        props = ""
        if bold:
            props += "<w:b/>"
        if size:
            props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        r = f'<w:r><w:rPr>{props}</w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r>'
    else:
        r = runs(text)
    return f"<w:p>{ppr}{r}</w:p>"


def equation(num, body):
    tabs = (f'<w:tabs><w:tab w:val="center" w:pos="{RIGHT_TAB//2}"/>'
            f'<w:tab w:val="right" w:pos="{RIGHT_TAB}"/></w:tabs>')
    ppr = f"<w:pPr>{tabs}<w:spacing w:before='80' w:after='80'/></w:pPr>"
    r = (f'<w:r><w:tab/><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">{esc(body)}</w:t></w:r>'
         f'<w:r><w:tab/><w:t xml:space="preserve">({num})</w:t></w:r>')
    return f"<w:p>{ppr}{r}</w:p>"


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(26)
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def image_para(relpath):
    abspath = os.path.join(ROOT, relpath)
    w, h = png_size(abspath)
    cx = int(min(PAGE_W_EMU, w * EMU_PER_PX))
    cy = int(cx * h / w)
    rid = f"rId{len(rels) + 10}"
    arc = f"media/image{_next[0]}.png"
    _next[0] += 1
    media.append((arc, abspath))
    rels.append((rid, arc, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"))
    did = _next[0]
    draw = (
        '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/></w:pPr><w:r><w:drawing>'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{did}" name="Figure{did}"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr><pic:cNvPr id="{did}" name="image{did}.png"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'
    )
    return draw


def table(rows):
    header, body = rows[0], rows[1:]
    ncol = len(header)
    colw = int(RIGHT_TAB / ncol)
    borders = ("<w:tblBorders>"
               + "".join(f'<w:{e} w:val="single" w:sz="4" w:space="0" w:color="888888"/>'
                         for e in ("top", "left", "bottom", "right", "insideH", "insideV"))
               + "</w:tblBorders>")
    tblpr = (f'<w:tblPr><w:tblW w:w="{RIGHT_TAB}" w:type="dxa"/>{borders}'
             '<w:tblLayout w:type="fixed"/></w:tblPr>')
    grid = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{colw}"/>' for _ in range(ncol)) + "</w:tblGrid>"
    trs = []
    for ri, row in enumerate([header] + body):
        cells = []
        shade = '<w:shd w:val="clear" w:fill="E7E7E7"/>' if ri == 0 else ""
        for c in row:
            c = c.strip()
            inner = (f'<w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">{esc(c)}</w:t></w:r>'
                     if ri == 0 else
                     re.sub(r'<w:r>', '<w:r><w:rPr><w:sz w:val="18"/></w:rPr>', runs(c)))
            if ri != 0 and "<w:rPr>" not in inner:
                inner = f'<w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">{esc(c)}</w:t></w:r>'
            cell = (f'<w:tc><w:tcPr><w:tcW w:w="{colw}" w:type="dxa"/>{shade}</w:tcPr>'
                    f'<w:p><w:pPr><w:spacing w:after="20"/></w:pPr>{inner}</w:p></w:tc>')
            cells.append(cell)
        header_mark = '<w:trPr><w:tblHeader/></w:trPr>' if ri == 0 else ""
        trs.append(f"<w:tr>{header_mark}{''.join(cells)}</w:tr>")
    return f"<w:tbl>{tblpr}{grid}{''.join(trs)}</w:tbl>"


def convert():
    with open(MD, encoding="utf-8") as f:
        lines = f.read().split("\n")
    body = []
    i = 0
    first_h1 = True
    while i < len(lines):
        ln = lines[i].rstrip()
        s = ln.strip()
        if not s:
            i += 1
            continue
        # tables
        if s.startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i].strip())
                i += 1
            parsed = []
            for r in block:
                if re.match(r"^\|[\s\-:|]+\|?$", r):
                    continue
                cells = [c for c in r.strip().strip("|").split("|")]
                parsed.append(cells)
            if parsed:
                body.append(table(parsed))
            continue
        i += 1
        if s == "---":
            continue
        m = re.match(r"!\[\]\(([^)]+)\)", s)
        if m:
            body.append(image_para(m.group(1)))
            continue
        me = re.match(r"\(EQ(\d+)\)\s+(.*)", s)
        if me:
            body.append(equation(me.group(1), me.group(2).strip()))
            continue
        if s.startswith("# "):
            body.append(para(s[2:].strip(), style="Title"))
            first_h1 = False
            continue
        if s.startswith("## "):
            body.append(para(s[3:].strip(), style="Heading1"))
            continue
        if s.startswith("### "):
            body.append(para(s[4:].strip(), style="Heading2"))
            continue
        body.append(para(s, jc="both"))
    return "\n".join(body)


def build():
    body = convert()
    # relationships: styles + images
    rel_items = ['<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rid, tgt, typ in rels:
        rel_items.append(f'<Relationship Id="{rid}" Type="{typ}" Target="{tgt}"/>')
    word_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 + "".join(rel_items) + "</Relationships>")
    content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                     '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                     '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                     '<Default Extension="xml" ContentType="application/xml"/>'
                     '<Default Extension="png" ContentType="image/png"/>'
                     '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                     '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
                     "</Types>")
    rels_root = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
                 "</Relationships>")
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
              '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Cambria" w:hAnsi="Cambria"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>'
              '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
              '<w:pPr><w:spacing w:after="140" w:line="276" w:lineRule="auto"/></w:pPr>'
              '<w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>'
              '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
              '<w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr>'
              '<w:rPr><w:b/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr></w:style>'
              '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
              '<w:pPr><w:spacing w:before="320" w:after="120"/><w:keepNext/></w:pPr>'
              '<w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>'
              '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
              '<w:pPr><w:spacing w:before="220" w:after="100"/><w:keepNext/></w:pPr>'
              '<w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>'
              "</w:styles>")
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<w:document '
                'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
                'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
                'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
                'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
                '<w:body>' + body +
                '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
                '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
                '</w:body></w:document>')
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels_root)
        z.writestr("word/_rels/document.xml.rels", word_rels)
        z.writestr("word/document.xml", document)
        z.writestr("word/styles.xml", styles)
        for arc, src in media:
            with open(src, "rb") as fh:
                z.writestr("word/" + arc, fh.read())
    print(f"wrote {OUT}")
    print(f"  figures embedded: {len(media)}")


if __name__ == "__main__":
    build()
