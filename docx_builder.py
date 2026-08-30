#!/usr/bin/env python3
"""
Minimal pure-Python OOXML (.docx) builder - no external dependencies.
Supports headings, paragraphs, centered/justified text, bold/italic runs,
bordered tables, and embedded PNG images with captions.
"""

import zipfile
import os


def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


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
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
    <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="240" w:after="240"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="40"/><w:szCs w:val="40"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:keepNext/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="100"/><w:keepNext/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="80"/><w:keepNext/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading4">
    <w:name w:val="heading 4"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="160" w:after="60"/><w:keepNext/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/></w:style>
</w:styles>'''


class DocxBuilder:
    def __init__(self):
        self.body = []
        self.images = []  # list of (rid, path)
        self._img_counter = 0

    # ---- text runs ----
    def _run(self, text, bold=False, italic=False, size=24, sub=False, sup=False):
        rpr = ['<w:rPr>']
        if bold:
            rpr.append('<w:b/>')
        if italic:
            rpr.append('<w:i/>')
        if sub:
            rpr.append('<w:vertAlign w:val="subscript"/>')
        if sup:
            rpr.append('<w:vertAlign w:val="superscript"/>')
        rpr.append('<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>')
        rpr.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>')
        return f'<w:r>{"".join(rpr)}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'

    def para(self, text="", bold=False, italic=False, size=24, align="both", style=None, space_after=None):
        p = ['<w:p><w:pPr>']
        if style:
            p.append(f'<w:pStyle w:val="{style}"/>')
        p.append(f'<w:jc w:val="{align}"/>')
        if space_after is not None:
            p.append(f'<w:spacing w:after="{space_after}"/>')
        p.append('</w:pPr>')
        if text:
            p.append(self._run(text, bold=bold, italic=italic, size=size))
        p.append('</w:p>')
        self.body.append("".join(p))

    def title(self, text):
        self.body.append(f'<w:p><w:pPr><w:pStyle w:val="Title"/></w:pPr>{self._run(text, bold=True, size=40)}</w:p>')

    def heading(self, text, level=2):
        sizes = {1: 32, 2: 28, 3: 26, 4: 24}
        self.body.append(
            f'<w:p><w:pPr><w:pStyle w:val="Heading{level}"/></w:pPr>'
            f'{self._run(text, bold=True, italic=(level == 4), size=sizes.get(level, 24))}</w:p>')

    def caption(self, text):
        self.body.append(
            f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="200"/></w:pPr>'
            f'{self._run(text, bold=True, size=20)}</w:p>')

    def table_caption(self, text):
        self.body.append(
            f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="160" w:after="60"/><w:keepNext/></w:pPr>'
            f'{self._run(text, bold=True, size=22)}</w:p>')

    def equation(self, text):
        self.body.append(
            f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="80"/></w:pPr>'
            f'{self._run(text, italic=True, size=24)}</w:p>')

    def bullet(self, text):
        bullet_text = "\u2022  " + text
        self.body.append(
            f'<w:p><w:pPr><w:ind w:left="720" w:hanging="360"/><w:jc w:val="both"/></w:pPr>'
            f'{self._run(bullet_text, size=24)}</w:p>')

    # ---- table ----
    def table(self, headers, rows, cell_size=18, first_col_left=False):
        cols = len(headers)
        colw = int(9360 / cols)
        t = ['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
             '<w:tblW w:w="9360" w:type="dxa"/>'
             '<w:jc w:val="center"/>'
             '<w:tblBorders>'
             '<w:top w:val="single" w:sz="6" w:color="000000"/>'
             '<w:bottom w:val="single" w:sz="6" w:color="000000"/>'
             '<w:left w:val="single" w:sz="6" w:color="000000"/>'
             '<w:right w:val="single" w:sz="6" w:color="000000"/>'
             '<w:insideH w:val="single" w:sz="4" w:color="000000"/>'
             '<w:insideV w:val="single" w:sz="4" w:color="000000"/>'
             '</w:tblBorders></w:tblPr>']
        t.append('<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{colw}"/>' for _ in range(cols)) + '</w:tblGrid>')

        def cell(text, bold, align, shade=None):
            tcpr = f'<w:tcW w:w="{colw}" w:type="dxa"/><w:vAlign w:val="center"/>'
            if shade:
                tcpr += f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>'
            return (f'<w:tc><w:tcPr>{tcpr}</w:tcPr>'
                    f'<w:p><w:pPr><w:jc w:val="{align}"/><w:spacing w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>'
                    f'{self._run(text, bold=bold, size=cell_size)}</w:p></w:tc>')

        # header
        t.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
        for h in headers:
            t.append(cell(h, True, "center", shade="D9E2F3"))
        t.append('</w:tr>')
        # body
        for r in rows:
            t.append('<w:tr>')
            for ci, c in enumerate(r):
                al = "left" if (first_col_left and ci == 0) else "center"
                t.append(cell(c, False, al))
            t.append('</w:tr>')
        t.append('</w:tbl>')
        self.body.append("".join(t))
        # spacer
        self.body.append('<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>')

    # ---- image ----
    def image(self, path, width_emu=5486400, height_emu=None, ratio=0.72):
        if not os.path.exists(path):
            self.para(f"[missing image: {os.path.basename(path)}]", italic=True, align="center")
            return
        self._img_counter += 1
        rid = f"rIdImg{self._img_counter}"
        self.images.append((rid, path))
        if height_emu is None:
            height_emu = int(width_emu * ratio)
        did = self._img_counter
        drawing = (
            '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="20"/></w:pPr>'
            '<w:r><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
            f'<wp:extent cx="{width_emu}" cy="{height_emu}"/>'
            f'<wp:docPr id="{did}" name="Picture{did}"/>'
            '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:nvPicPr><pic:cNvPr id="{did}" name="Picture{did}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{width_emu}" cy="{height_emu}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')
        self.body.append(drawing)

    def page_break(self):
        self.body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    # ---- save ----
    def save(self, output_file):
        doc_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
                    '  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
        for i, (rid, _path) in enumerate(self.images):
            doc_rels.append(f'  <Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image{i+1}.png"/>')
        doc_rels.append('</Relationships>')
        doc_rels_xml = "\n".join(doc_rels)

        document_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
            'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<w:body>' + "".join(self.body) +
            '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
            '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>'
            '</w:sectPr></w:body></w:document>')

        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('[Content_Types].xml', CONTENT_TYPES)
            zf.writestr('_rels/.rels', RELS)
            zf.writestr('word/_rels/document.xml.rels', doc_rels_xml)
            zf.writestr('word/document.xml', document_xml)
            zf.writestr('word/styles.xml', STYLES)
            for i, (_rid, path) in enumerate(self.images):
                zf.write(path, f'word/media/image{i+1}.png')
        return output_file
