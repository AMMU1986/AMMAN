"""
Minimal, dependency-free DOCX writer (stdlib only).
Builds a valid OOXML .docx package via zipfile.

Supports: headings, body paragraphs (with justified alignment), page breaks,
inline images (PNG) with captions, and simple grid tables with a header row.
"""
import zipfile
import os
import html
import struct


def _esc(s):
    return html.escape(s, quote=True)


class DocxBuilder:
    def __init__(self):
        self.body = []          # list of XML strings (paragraphs / tables)
        self.rels = []          # relationship entries
        self.media = []         # (rid, arcname, filepath)
        self._rid = 0
        self._img_id = 0

    def _next_rid(self):
        self._rid += 1
        return f"rId{self._rid}"

    # ---- content helpers -------------------------------------------------
    def heading(self, text, level=1):
        style = f"Heading{level}"
        self.body.append(
            f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{_esc(text)}</w:t></w:r></w:p>'
        )

    def title(self, text):
        self.body.append(
            '<w:p><w:pPr><w:pStyle w:val="Title"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{_esc(text)}</w:t></w:r></w:p>'
        )

    def subtitle(self, text):
        self.body.append(
            '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
            f'<w:r><w:rPr><w:i/><w:sz w:val="24"/></w:rPr>'
            f'<w:t xml:space="preserve">{_esc(text)}</w:t></w:r></w:p>'
        )

    def _runs_from_text(self, text, bold=False, italic=False):
        rpr = ""
        if bold or italic:
            rpr = "<w:rPr>" + ("<w:b/>" if bold else "") + ("<w:i/>" if italic else "") + "</w:rPr>"
        return f'<w:r>{rpr}<w:t xml:space="preserve">{_esc(text)}</w:t></w:r>'

    def paragraph(self, text, justify=True, bold=False, italic=False, size=None, spacing_after=120):
        jc = '<w:jc w:val="both"/>' if justify else ""
        sp = f'<w:spacing w:after="{spacing_after}"/>'
        rpr_parts = ""
        if size:
            rpr_parts += f'<w:sz w:val="{size}"/>'
        if bold:
            rpr_parts += "<w:b/>"
        if italic:
            rpr_parts += "<w:i/>"
        rpr = f"<w:rPr>{rpr_parts}</w:rPr>" if rpr_parts else ""
        self.body.append(
            f'<w:p><w:pPr>{sp}{jc}</w:pPr>'
            f'<w:r>{rpr}<w:t xml:space="preserve">{_esc(text)}</w:t></w:r></w:p>'
        )

    def bullet(self, text):
        self.body.append(
            '<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
            '<w:spacing w:after="60"/><w:jc w:val="both"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{_esc(text)}</w:t></w:r></w:p>'
        )

    def page_break(self):
        self.body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    def spacer(self):
        self.body.append('<w:p/>')

    # ---- image -----------------------------------------------------------
    def image(self, filepath, caption, max_width_in=6.0):
        # read PNG dimensions
        with open(filepath, "rb") as f:
            data = f.read()
        w_px, h_px = struct.unpack(">II", data[16:24])
        self._img_id += 1
        rid = self._next_rid()
        arc = f"media/image{self._img_id}.png"
        self.media.append((rid, arc, filepath))
        self.rels.append(
            f'<Relationship Id="{rid}" '
            f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            f'Target="{arc}"/>'
        )
        # EMU: 914400 per inch
        emu_per_in = 914400
        width_emu = int(max_width_in * emu_per_in)
        height_emu = int(width_emu * (h_px / w_px))
        docpr_id = self._img_id
        drawing = f'''<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/></w:pPr><w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0">
<wp:extent cx="{width_emu}" cy="{height_emu}"/>
<wp:effectExtent l="0" t="0" r="0" b="0"/>
<wp:docPr id="{docpr_id}" name="Picture {docpr_id}"/>
<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>
<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:nvPicPr><pic:cNvPr id="{docpr_id}" name="Picture {docpr_id}"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{width_emu}" cy="{height_emu}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''
        self.body.append(drawing)
        # caption
        self.body.append(
            '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="200"/></w:pPr>'
            f'<w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr>'
            f'<w:t xml:space="preserve">{_esc(caption)}</w:t></w:r></w:p>'
        )

    # ---- table -----------------------------------------------------------
    def table(self, caption, headers, rows, col_widths=None):
        # caption above table
        self.body.append(
            '<w:p><w:pPr><w:spacing w:before="160" w:after="60"/></w:pPr>'
            f'<w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr>'
            f'<w:t xml:space="preserve">{_esc(caption)}</w:t></w:r></w:p>'
        )
        ncol = len(headers)
        total = 9360
        if col_widths is None:
            col_widths = [total // ncol] * ncol
        grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in col_widths)

        def cell(text, is_header):
            shade = '<w:shd w:val="clear" w:color="auto" w:fill="1F4E79"/>' if is_header else ""
            rpr = "<w:rPr><w:b/><w:color w:val=\"FFFFFF\"/><w:sz w:val=\"18\"/></w:rPr>" if is_header \
                else "<w:rPr><w:sz w:val=\"18\"/></w:rPr>"
            width = col_widths[0]
            return (
                f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shade}'
                '<w:tcMar><w:top w:w="40" w:type="dxa"/><w:bottom w:w="40" w:type="dxa"/>'
                '<w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tcMar>'
                '<w:vAlign w:val="center"/></w:tcPr>'
                f'<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>'
                f'<w:r>{rpr}<w:t xml:space="preserve">{_esc(text)}</w:t></w:r></w:p></w:tc>'
            )

        def build_cell(text, is_header, width):
            shade = '<w:shd w:val="clear" w:color="auto" w:fill="1F4E79"/>' if is_header else ""
            rpr = "<w:rPr><w:b/><w:color w:val=\"FFFFFF\"/><w:sz w:val=\"18\"/></w:rPr>" if is_header \
                else "<w:rPr><w:sz w:val=\"18\"/></w:rPr>"
            return (
                f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shade}'
                '<w:tcMar><w:top w:w="40" w:type="dxa"/><w:bottom w:w="40" w:type="dxa"/>'
                '<w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tcMar>'
                '<w:vAlign w:val="center"/></w:tcPr>'
                f'<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>'
                f'<w:r>{rpr}<w:t xml:space="preserve">{_esc(text)}</w:t></w:r></w:p></w:tc>'
            )

        rows_xml = ""
        # header row
        hdr = "".join(build_cell(h, True, col_widths[i]) for i, h in enumerate(headers))
        rows_xml += f'<w:tr><w:trPr><w:tblHeader/></w:trPr>{hdr}</w:tr>'
        for r in rows:
            cells = "".join(build_cell(str(v), False, col_widths[i]) for i, v in enumerate(r))
            rows_xml += f"<w:tr>{cells}</w:tr>"

        tbl = (
            '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
            f'<w:tblW w:w="{total}" w:type="dxa"/>'
            '<w:tblBorders>'
            '<w:top w:val="single" w:sz="4" w:color="7F7F7F"/>'
            '<w:left w:val="single" w:sz="4" w:color="7F7F7F"/>'
            '<w:bottom w:val="single" w:sz="4" w:color="7F7F7F"/>'
            '<w:right w:val="single" w:sz="4" w:color="7F7F7F"/>'
            '<w:insideH w:val="single" w:sz="4" w:color="BFBFBF"/>'
            '<w:insideV w:val="single" w:sz="4" w:color="BFBFBF"/>'
            '</w:tblBorders><w:tblLook w:val="04A0"/></w:tblPr>'
            f'<w:tblGrid>{grid}</w:tblGrid>{rows_xml}</w:tbl>'
        )
        self.body.append(tbl)
        self.body.append('<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>')

    # ---- package assembly ------------------------------------------------
    def save(self, path):
        body_xml = "\n".join(self.body)
        document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<w:body>
{body_xml}
<w:sectPr>
<w:pgSz w:w="12240" w:h="15840"/>
<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
</w:sectPr>
</w:body>
</w:document>'''

        content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''

        root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rIdDoc" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

        doc_rels_items = (
            '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            '<Relationship Id="rIdNum" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
            + "".join(self.rels)
        )
        doc_rels = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
{doc_rels_items}
</Relationships>'''

        styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:pPr><w:spacing w:line="276" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="22"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="120"/></w:pPr><w:rPr><w:rFonts w:ascii="Cambria" w:hAnsi="Cambria"/><w:b/><w:color w:val="1F3864"/><w:sz w:val="40"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="280" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:rFonts w:ascii="Cambria" w:hAnsi="Cambria"/><w:b/><w:color w:val="1F4E79"/><w:sz w:val="30"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="220" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:rFonts w:ascii="Cambria" w:hAnsi="Cambria"/><w:b/><w:color w:val="2E74B5"/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="180" w:after="80"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:rFonts w:ascii="Cambria" w:hAnsi="Cambria"/><w:b/><w:color w:val="2E74B5"/><w:sz w:val="23"/></w:rPr></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4" w:color="auto"/><w:left w:val="single" w:sz="4" w:color="auto"/><w:bottom w:val="single" w:sz="4" w:color="auto"/><w:right w:val="single" w:sz="4" w:color="auto"/><w:insideH w:val="single" w:sz="4" w:color="auto"/><w:insideV w:val="single" w:sz="4" w:color="auto"/></w:tblBorders></w:tblPr></w:style>
</w:styles>'''

        numbering = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="&#8226;"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr><w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/></w:rPr></w:lvl></w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
</w:numbering>'''

        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", content_types)
            z.writestr("_rels/.rels", root_rels)
            z.writestr("word/document.xml", document)
            z.writestr("word/styles.xml", styles)
            z.writestr("word/numbering.xml", numbering)
            z.writestr("word/_rels/document.xml.rels", doc_rels)
            for rid, arc, fp in self.media:
                with open(fp, "rb") as f:
                    z.writestr("word/" + arc, f.read())
        return path
