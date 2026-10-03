#!/usr/bin/env python3
"""
Build a Word (.docx) manuscript from Manuscript_ML_Hybrid_Nanofluid_Radiator.md.

Pure Python standard library only (zipfile for the OOXML package, struct for
reading PNG dimensions). Renders:
  - Title / headings / body paragraphs
  - Markdown pipe tables as native Word tables
  - Embedded PNG figures (scaled to page width)
  - Figure captions / bold lines
  - Numbered display equations (lines ending in a (n) tag) centered
"""

import os
import re
import struct
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(HERE, "Manuscript_ML_Hybrid_Nanofluid_Radiator.md")
OUT_PATH = os.path.join(HERE, "Manuscript_ML_Hybrid_Nanofluid_Radiator.docx")

EMU_PER_PX = 9525           # 1 px (96 dpi) = 9525 EMU
MAX_IMG_WIDTH_EMU = 5486400  # ~6.0 inch usable width (letter, 1in margins)


def escape_xml(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return (600, 400)
    w, h = struct.unpack(">II", head[16:24])
    return (w, h)


def clean_inline(text):
    """Strip markdown emphasis markers for plain runs."""
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return text


def para(text, style=None, bold=False, size=None, italic=False, center=False):
    text = escape_xml(text)
    rpr = ""
    inner = ""
    if bold:
        inner += "<w:b/>"
    if italic:
        inner += "<w:i/>"
    if size is not None:
        inner += '<w:sz w:val="{0}"/><w:szCs w:val="{0}"/>'.format(size)
    if inner:
        rpr = "<w:rPr>{}</w:rPr>".format(inner)
    ppr_bits = ""
    if style:
        ppr_bits += '<w:pStyle w:val="{}"/>'.format(style)
    if center:
        ppr_bits += '<w:jc w:val="center"/>'
    ppr = "<w:pPr>{}</w:pPr>".format(ppr_bits) if ppr_bits else ""
    return ('<w:p>{}<w:r>{}<w:t xml:space="preserve">{}</w:t></w:r></w:p>'
            .format(ppr, rpr, text))


class DocxBuilder:
    def __init__(self):
        self.body = []
        self.rels = []           # (rid, target) for images
        self.images = []         # (arcname, filepath)
        self._img_counter = 0

    def add_image(self, path):
        if not os.path.exists(path):
            self.body.append(para("[missing image: {}]".format(os.path.basename(path)),
                                  italic=True))
            return
        self._img_counter += 1
        rid = "rIdImg{}".format(self._img_counter)
        arc = "media/image{}.png".format(self._img_counter)
        self.rels.append((rid, arc))
        self.images.append((arc, path))

        w, h = png_size(path)
        cx = w * EMU_PER_PX
        cy = h * EMU_PER_PX
        if cx > MAX_IMG_WIDTH_EMU:
            scale = MAX_IMG_WIDTH_EMU / cx
            cx = int(cx * scale)
            cy = int(cy * scale)
        did = self._img_counter
        drawing = (
            '<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
            '<wp:inline distT="0" distB="0" distL="0" distR="0">'
            '<wp:extent cx="{cx}" cy="{cy}"/>'
            '<wp:docPr id="{did}" name="Figure{did}"/>'
            '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:nvPicPr><pic:cNvPr id="{did}" name="Figure{did}"/><pic:cNvPicPr/></pic:nvPicPr>'
            '<pic:blipFill><a:blip r:embed="{rid}"/>'
            '<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            '</pic:pic></a:graphicData></a:graphic></wp:inline>'
            '</w:drawing></w:r></w:p>'
        ).format(cx=cx, cy=cy, did=did, rid=rid)
        self.body.append(drawing)

    def add_table(self, rows):
        """rows: list of list-of-cell-strings; first row is header."""
        out = ['<w:tbl>',
               '<w:tblPr><w:tblStyle w:val="TableGrid"/>'
               '<w:tblW w:w="0" w:type="auto"/>'
               '<w:tblBorders>'
               '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
               '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
               '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
               '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
               '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
               '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
               '</w:tblBorders></w:tblPr>']
        for ri, row in enumerate(rows):
            out.append("<w:tr>")
            for cell in row:
                txt = escape_xml(clean_inline(cell.strip()))
                shade = ('<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>'
                         if ri == 0 else "")
                bold = "<w:b/>" if ri == 0 else ""
                out.append(
                    '<w:tc><w:tcPr>{shade}</w:tcPr>'
                    '<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>'
                    '<w:r><w:rPr>{bold}<w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
                    '<w:t xml:space="preserve">{txt}</w:t></w:r></w:p></w:tc>'
                    .format(shade=shade, bold=bold, txt=txt))
            out.append("</w:tr>")
        out.append("</w:tbl>")
        out.append("<w:p/>")
        self.body.append("".join(out))

    def add(self, xml):
        self.body.append(xml)


def is_image_line(line):
    return bool(re.match(r"^!\[.*\]\(.*\)\s*$", line.strip()))


def image_path_from_line(line):
    m = re.search(r"\(([^)]+)\)", line)
    return m.group(1) if m else None


def is_equation_line(line):
    """Lines wrapped in $$ ... $$ with a trailing \\tag{n}."""
    return line.strip().startswith("$$")


def strip_equation(line):
    s = line.strip().strip("$").strip()
    m = re.search(r"\\tag\{([^}]+)\}", s)
    tag = m.group(1) if m else ""
    s = re.sub(r"\\tag\{[^}]+\}", "", s).strip()
    # light LaTeX -> readable text
    s = s.replace("\\,", " ").replace("\\;", "  ")
    s = s.replace("\\left", "").replace("\\right", "")
    s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", s)
    s = re.sub(r"\\sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
    s = re.sub(r"\\sum_\{([^{}]*)\}\^\{([^{}]*)\}", r"SUM[\1..\2]", s)
    s = s.replace("\\rho", "rho").replace("\\phi", "phi").replace("\\mu", "mu")
    s = s.replace("\\varepsilon", "eps").replace("\\Delta", "Delta")
    s = s.replace("\\dot{m}", "m_dot").replace("\\approx", "~=")
    s = s.replace("\\cdot", "*").replace("\\times", "x")
    s = re.sub(r"_\{([^{}]*)\}", r"_\1", s)
    s = re.sub(r"\^\{([^{}]*)\}", r"^\1", s)
    s = re.sub(r"\\mathrm\{([^{}]*)\}", r"\1", s)
    s = s.replace("{", "").replace("}", "").replace("\\", "")
    return s, tag


def convert(md_text, builder):
    lines = md_text.split("\n")
    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("---"):
            i += 1
            continue

        # table block
        if stripped.startswith("|") and "|" in stripped[1:]:
            tbl = []
            while i < n and lines[i].strip().startswith("|"):
                row_line = lines[i].strip()
                if re.match(r"^\|[\s\-:|]+\|$", row_line):
                    i += 1
                    continue
                cells = [c for c in row_line.strip("|").split("|")]
                tbl.append(cells)
                i += 1
            if tbl:
                builder.add_table(tbl)
            continue

        # image
        if is_image_line(stripped):
            rel = image_path_from_line(stripped)
            builder.add_image(os.path.join(HERE, rel))
            i += 1
            continue

        # equation
        if is_equation_line(stripped):
            eqn, tag = strip_equation(stripped)
            disp = eqn if not tag else "{}      ({})".format(eqn, tag)
            builder.add(para(disp, italic=True, center=True, size=22))
            i += 1
            continue

        # headings
        if stripped.startswith("# ") and not stripped.startswith("## "):
            builder.add(para(stripped[2:].strip(), style="Title", bold=True, size=32, center=True))
        elif stripped.startswith("## "):
            builder.add(para(stripped[3:].strip(), style="Heading1", bold=True, size=28))
        elif stripped.startswith("### "):
            builder.add(para(stripped[4:].strip(), style="Heading2", bold=True, size=24))
        elif stripped.startswith("#### "):
            builder.add(para(stripped[5:].strip(), style="Heading3", bold=True, size=22, italic=True))
        elif stripped.startswith("**") and stripped.endswith("**"):
            builder.add(para(clean_inline(stripped), bold=True))
        else:
            builder.add(para(clean_inline(stripped)))
        i += 1


STYLES_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
    <w:pPr><w:spacing w:after="120" w:line="300" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
    <w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
    <w:pPr><w:spacing w:before="320" w:after="120"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
    <w:pPr><w:spacing w:before="160" w:after="80"/></w:pPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr><w:tblBorders>
      <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>
    </w:tblBorders></w:tblPr>
  </w:style>
</w:styles>'''

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

ROOT_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''


def build():
    with open(MD_PATH, "r") as f:
        md = f.read()

    b = DocxBuilder()
    convert(md, b)

    doc_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
                '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rid, target in b.rels:
        doc_rels.append('<Relationship Id="{}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{}"/>'.format(rid, target))
    doc_rels.append("</Relationships>")
    doc_rels_xml = "\n".join(doc_rels)

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<w:body>'
        + "".join(b.body) +
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
        '</w:sectPr></w:body></w:document>'
    )

    with zipfile.ZipFile(OUT_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", CONTENT_TYPES)
        zf.writestr("_rels/.rels", ROOT_RELS)
        zf.writestr("word/_rels/document.xml.rels", doc_rels_xml)
        zf.writestr("word/document.xml", document)
        zf.writestr("word/styles.xml", STYLES_XML)
        for arc, path in b.images:
            zf.write(path, "word/" + arc)

    print("Created {}".format(OUT_PATH))
    print("  Embedded {} figures".format(len(b.images)))


if __name__ == "__main__":
    build()
