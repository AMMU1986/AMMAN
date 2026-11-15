#!/usr/bin/env python3
"""Build Manuscript_PMEDM_ML_Reanalysis.docx from the Markdown manuscript.

Standard library only. Equations are converted from LaTeX to native Word
equations (OMML) with right-aligned numbers, tables become Word tables, and
figures are embedded from pmedm_ml_figures/.
"""

import datetime
import os
import re
import struct
import sys
import zipfile
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "pmedm_ml_code"))
from latex2omml import latex_to_omml  # noqa: E402

MD = os.path.join(ROOT, "Manuscript_PMEDM_ML_Reanalysis.md")
OUT = os.path.join(ROOT, "Manuscript_PMEDM_ML_Reanalysis.docx")
TEXT_WIDTH_TWIPS = 9026          # A4 with 2.54 cm margins
FIG_WIDTH_EMU = int(16.0 * 360000)

NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')


def png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(24)
    w, h = struct.unpack(">II", head[16:24])
    return w, h


class Builder:
    def __init__(self):
        self.body = []
        self.images = []  # (rid, filename, path)

    # ------------------------------------------------------------------ runs
    def runs(self, text, size=None, bold=False, italic=False):
        """Inline Markdown (bold, italic, code) and $math$ to WordprocessingML runs."""
        out = []
        parts = re.split(r"(\$[^$]+\$)", text)
        for part in parts:
            if not part:
                continue
            if part.startswith("$") and part.endswith("$") and len(part) > 2:
                omml, _ = latex_to_omml(part[1:-1], display=False)
                out.append("<m:oMath>%s</m:oMath>" % omml)
                continue
            for tok in re.split(r"(\*\*[^*]+\*\*|\*[^*\s][^*]*\*|`[^`]+`)", part):
                if not tok:
                    continue
                b, it, code = bold, italic, False
                if tok.startswith("**") and tok.endswith("**"):
                    tok, b = tok[2:-2], True
                elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
                    tok, it = tok[1:-1], True
                elif tok.startswith("`") and tok.endswith("`"):
                    tok, code = tok[1:-1], True
                rpr = ""
                if code:
                    rpr += '<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/>'
                if b:
                    rpr += "<w:b/>"
                if it:
                    rpr += "<w:i/>"
                if size:
                    rpr += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size)
                out.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
                           % ("<w:rPr>%s</w:rPr>" % rpr if rpr else "", escape(tok)))
        return "".join(out)

    def para(self, text, style="Normal", align=None, size=None, bold=False, keep_next=False,
             indent=None):
        ppr = '<w:pStyle w:val="%s"/>' % style
        if keep_next:
            ppr += "<w:keepNext/>"
        if indent:
            ppr += indent
        if align:
            ppr += '<w:jc w:val="%s"/>' % align
        self.body.append("<w:p><w:pPr>%s</w:pPr>%s</w:p>" % (ppr, self.runs(text, size, bold)))

    def equation(self, latex):
        """Display equation in a borderless two-column table: centred equation, right number."""
        omml, tag = latex_to_omml(latex, display=True)
        w_num = 900
        w_eq = TEXT_WIDTH_TWIPS - w_num
        none = '<w:%s w:val="nil"/>'
        borders = "".join(none % s for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
        eq_cell = ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
                   '<w:p><w:pPr><w:pStyle w:val="Equation"/><w:jc w:val="center"/></w:pPr>'
                   '<m:oMathPara><m:oMathParaPr><m:jc m:val="center"/></m:oMathParaPr>'
                   '<m:oMath>%s</m:oMath></m:oMathPara></w:p></w:tc>' % (w_eq, omml))
        num_cell = ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
                    '<w:p><w:pPr><w:pStyle w:val="Equation"/><w:jc w:val="right"/></w:pPr>'
                    '<w:r><w:t>(%s)</w:t></w:r></w:p></w:tc>' % (w_num, tag or ""))
        self.body.append(
            '<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:tblBorders>%s</w:tblBorders>'
            '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="0" w:type="dxa"/>'
            '<w:right w:w="0" w:type="dxa"/></w:tblCellMar></w:tblPr>'
            '<w:tblGrid><w:gridCol w:w="%d"/><w:gridCol w:w="%d"/></w:tblGrid>'
            '<w:tr><w:trPr><w:cantSplit/></w:trPr>%s%s</w:tr></w:tbl>'
            % (borders, w_eq, w_num, eq_cell, num_cell))

    def figure(self, caption, rel_path):
        path = os.path.join(ROOT, rel_path)
        w, h = png_size(path)
        cx = FIG_WIDTH_EMU
        cy = int(cx * h / w)
        idx = len(self.images) + 1
        rid = "rIdImg%d" % idx
        self.images.append((rid, "image%d.png" % idx, path))
        drawing = (
            '<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
            '<wp:extent cx="%d" cy="%d"/><wp:docPr id="%d" name="Figure %d"/>'
            '<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic><pic:nvPicPr><pic:cNvPr id="%d" name="image%d.png"/><pic:cNvPicPr/></pic:nvPicPr>'
            '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
            '</a:graphicData></a:graphic></wp:inline></w:drawing></w:r>'
            % (cx, cy, idx, idx, idx, idx, rid, cx, cy))
        self.body.append('<w:p><w:pPr><w:pStyle w:val="FigureBox"/><w:keepNext/><w:jc w:val="center"/>'
                         '</w:pPr>%s</w:p>' % drawing)
        m = re.match(r"(Figure \d+\.)\s*(.*)", caption)
        text = "**%s** %s" % (m.group(1), m.group(2)) if m else caption
        self.para(text, style="Caption")

    def table(self, rows):
        header, body = rows[0], rows[1:]
        ncols = len(header)
        grid = "".join('<w:gridCol w:w="%d"/>' % (TEXT_WIDTH_TWIPS // ncols) for _ in range(ncols))
        xml = ['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="5000" w:type="pct"/>'
               '<w:tblBorders><w:top w:val="single" w:sz="10" w:space="0" w:color="000000"/>'
               '<w:bottom w:val="single" w:sz="10" w:space="0" w:color="000000"/></w:tblBorders>'
               '<w:tblCellMar><w:left w:w="60" w:type="dxa"/><w:right w:w="60" w:type="dxa"/>'
               '</w:tblCellMar></w:tblPr><w:tblGrid>%s</w:tblGrid>' % grid]

        def cell(text, head, col, merge_rest=False):
            tcpr = '<w:tcBorders><w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>' \
                   '</w:tcBorders>' if head else ""
            jc = "left" if col == 0 else "center"
            return ('<w:tc><w:tcPr>%s</w:tcPr><w:p><w:pPr><w:pStyle w:val="TableText"/><w:jc w:val="%s"/>'
                    '</w:pPr>%s</w:p></w:tc>' % (tcpr, jc, self.runs(text, 17, bold=head)))

        xml.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>%s</w:tr>'
                   % "".join(cell(t, True, i) for i, t in enumerate(header)))
        for r in body:
            r = (r + [""] * ncols)[:ncols]
            if all(not c for c in r[1:]) and r[0]:
                # full-width note row (e.g. fixed conditions)
                xml.append('<w:tr><w:tc><w:tcPr><w:gridSpan w:val="%d"/></w:tcPr><w:p><w:pPr>'
                           '<w:pStyle w:val="TableText"/></w:pPr>%s</w:p></w:tc></w:tr>'
                           % (ncols, self.runs(r[0], 17)))
                continue
            xml.append("<w:tr>%s</w:tr>" % "".join(cell(t, False, i) for i, t in enumerate(r)))
        xml.append("</w:tbl>")
        self.body.append("".join(xml))
        self.body.append('<w:p><w:pPr><w:pStyle w:val="Normal"/><w:spacing w:after="0"/></w:pPr></w:p>')


def merge_fixed_row(cells):
    """Turn '| Fixed | text | | | |' into a single full-width note."""
    if len(cells) > 2 and cells[0] and cells[1] and all(not c for c in cells[2:]):
        return ["%s: %s" % (cells[0], cells[1])] + [""] * (len(cells) - 1)
    return cells


def build():
    lines = open(MD, encoding="utf-8").read().splitlines()
    b = Builder()
    i = 0
    in_refs = False
    after_table = False
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.startswith("$$"):
            buf = line[2:]
            while not buf.rstrip().endswith("$$"):
                i += 1
                buf += " " + lines[i]
            b.equation(buf.rstrip()[:-2])
            i += 1
            after_table = False
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    rows.append(merge_fixed_row(cells))
                i += 1
            b.table(rows)
            after_table = True
            continue
        m = re.match(r"!\[(.*)\]\((.*)\)", line)
        if m:
            b.figure(m.group(1), m.group(2))
            i += 1
            after_table = False
            continue
        if line.startswith("# "):
            b.para(line[2:], style="Title", align="center")
        elif line.startswith("## "):
            title = line[3:]
            in_refs = title.strip() == "References"
            b.para(title, style="Heading1", keep_next=True)
        elif line.startswith("### "):
            b.para(line[4:], style="Heading2", keep_next=True)
        elif in_refs and re.match(r"^\d+\. ", line):
            num, rest = line.split(". ", 1)
            b.para("[%s] %s" % (num, rest), style="Reference")
        elif re.match(r"^\d+\. ", line):
            b.para(line, style="ListPara")
        elif line.startswith("**Table"):
            b.para(line, style="Caption", keep_next=True)
        elif after_table:
            b.para(line, style="TableNote")
        else:
            b.para(line)
        after_table = False
        i += 1
    return b


STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/><w:pPr><w:jc w:val="both"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="120" w:after="240" w:line="300" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="80"/><w:jc w:val="left"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Equation"><w:name w:val="Equation"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="120" w:after="120" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="60" w:after="200" w:line="260" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="FigureBox"><w:name w:val="Figure"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="200" w:after="60" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableText"><w:name w:val="Table Text"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="17"/><w:szCs w:val="17"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableNote"><w:name w:val="Table Note"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="40" w:after="200" w:line="240" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="ListPara"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="425" w:hanging="425"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="Reference"><w:name w:val="Reference"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="80" w:line="260" w:lineRule="auto"/><w:ind w:left="567" w:hanging="567"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
  <w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblCellMar><w:left w:w="60" w:type="dxa"/><w:right w:w="60" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>
</w:styles>"""


def write_docx(b):
    body = "".join(b.body)
    sect = ('<w:sectPr><w:footerReference w:type="default" r:id="rIdFooter"/>'
            '<w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" '
            'w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>'
            '<w:lnNumType w:countBy="1" w:restart="continuous"/></w:sectPr>')
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:document %s><w:body>%s%s'
                '</w:body></w:document>' % (NS, body, sect))
    footer = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
              '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
              '<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:fldChar w:fldCharType="begin"/></w:r>'
              '<w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
              '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r>'
              '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>')
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
            'relationships/styles" Target="styles.xml"/>',
            '<Relationship Id="rIdSettings" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
            'relationships/settings" Target="settings.xml"/>',
            '<Relationship Id="rIdFooter" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
            'relationships/footer" Target="footer1.xml"/>']
    for rid, name, _ in b.images:
        rels.append('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                    'relationships/image" Target="media/%s"/>' % (rid, name))
    rels.append("</Relationships>")
    settings = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
                '<w:defaultTabStop w:val="720"/><w:compat><w:compatSetting w:name="compatibilityMode" '
                'w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat>'
                '<m:mathPr><m:mathFont m:val="Cambria Math"/><m:dispDef/><m:wrapIndent m:val="1440"/>'
                '<m:intLim m:val="subSup"/><m:naryLim m:val="undOvr"/></m:mathPr></w:settings>')
    content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
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
    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                 'relationships/officeDocument" Target="word/document.xml"/>'
                 '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/'
                 'metadata/core-properties" Target="docProps/core.xml"/></Relationships>')
    now = datetime.datetime(2026, 11, 15).strftime("%Y-%m-%dT%H:%M:%SZ")
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>Cross-validated machine learning with uncertainty quantification for PM-EDM of WC-Co</dc:title>'
            '<dc:creator>[Author name(s)]</dc:creator>'
            '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created></cp:coreProperties>' % now)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("docProps/core.xml", core)
        z.writestr("word/document.xml", document)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/settings.xml", settings)
        z.writestr("word/footer1.xml", footer)
        z.writestr("word/_rels/document.xml.rels", "".join(rels))
        for _, name, path in b.images:
            z.write(path, "word/media/" + name)
    return OUT


if __name__ == "__main__":
    print(write_docx(build()))
