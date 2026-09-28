#!/usr/bin/env python3
"""
Pure-stdlib .docx writer with native Office Math (OMML) equation support.

A .docx is a ZIP of XML parts. Equations authored as <m:oMath> render in
Microsoft Word's equation editor as fully editable equations (not images).

This module provides:
  * OMML builders (run/r, sup/sSup, sub/sSub, subsup, frac, rad, delim, nary,
    func, group) that emit well-formed m:* XML.
  * A Document class that accumulates paragraphs (headings, body, equations,
    figures, tables) and serialises a valid .docx package.

Only the Python standard library is used.
"""

import os
import zipfile
from xml.sax.saxutils import escape


# ---------------------------------------------------------------------------
# OMML expression builders. Each returns an XML string in the m: namespace.
# ---------------------------------------------------------------------------
def _mr(text, sty=None, italic=None):
    """A math run. sty: 'p'(plain/upright) 'i'(italic) 'b'(bold) 'bi'."""
    rpr = ""
    if sty:
        rpr = '<m:rPr><m:sty m:val="%s"/></m:rPr>' % sty
    # normal text run properties (font)
    return '<m:r>%s<m:t xml:space="preserve">%s</m:t></m:r>' % (rpr, escape(text))


def run(text, upright=False):
    """Ordinary italic (variable) run, or upright for operators/words."""
    return _mr(text, sty='p' if upright else None)


def op(text):
    """Upright operator/word run (e.g. sin, Pr, d, =, +)."""
    return _mr(text, sty='p')


def sup(base, exponent):
    return ('<m:sSup><m:e>%s</m:e><m:sup>%s</m:sup></m:sSup>' % (base, exponent))


def sub(base, subscript):
    return ('<m:sSub><m:e>%s</m:e><m:sub>%s</m:sub></m:sSub>' % (base, subscript))


def subsup(base, subscript, superscript):
    return ('<m:sSubSup><m:e>%s</m:e><m:sub>%s</m:sub><m:sup>%s</m:sup></m:sSubSup>'
            % (base, subscript, superscript))


def frac(num, den):
    return ('<m:f><m:num>%s</m:num><m:den>%s</m:den></m:f>' % (num, den))


def rad(radicand, degree=None):
    if degree is None:
        return ('<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr>'
                '<m:deg/><m:e>%s</m:e></m:rad>' % radicand)
    return '<m:rad><m:deg>%s</m:deg><m:e>%s</m:e></m:rad>' % (degree, radicand)


def delim(inner, left="(", right=")"):
    return ('<m:d><m:dPr><m:begChr m:val="%s"/><m:endChr m:val="%s"/></m:dPr>'
            '<m:e>%s</m:e></m:d>' % (escape(left), escape(right), inner))


def brack(inner):
    return delim(inner, "[", "]")


def nary(chartype, sub_, sup_, e):
    """N-ary operator (e.g. integral)."""
    return ('<m:nary><m:naryPr><m:chr m:val="%s"/><m:limLoc m:val="subSup"/>'
            '<m:supHide m:val="0"/><m:subHide m:val="0"/></m:naryPr>'
            '<m:sub>%s</m:sub><m:sup>%s</m:sup><m:e>%s</m:e></m:nary>'
            % (escape(chartype), sub_, sup_, e))


def group(*parts):
    return "".join(parts)


# Greek / symbol convenience (Unicode) -------------------------------------
G = {
    'eta': '\u03b7', 'theta': '\u03b8', 'phi': '\u03c6', 'psi': '\u03c8',
    'mu': '\u03bc', 'nu': '\u03bd', 'rho': '\u03c1', 'sigma': '\u03c3',
    'kappa': '\u03ba', 'gamma': '\u03b3', 'Gamma': '\u0393', 'tau': '\u03c4',
    'Omega': '\u03a9', 'omega': '\u03c9', 'Lambda': '\u039b', 'zeta': '\u03b6',
    'partial': '\u2202', 'nabla': '\u2207', 'infty': '\u221e', 'times': '\u00d7',
    'cdot': '\u22c5', 'minus': '\u2212', 'prime': '\u2032', 'Delta': '\u0394',
    'to': '\u2192', 'leq': '\u2264', 'geq': '\u2265', 'approx': '\u2248',
    'chi': '\u03c7', 'Phi': '\u03a6', 'xi': '\u039e',
}


# ---------------------------------------------------------------------------
# Document assembly
# ---------------------------------------------------------------------------
class Document:
    def __init__(self):
        self.body = []           # list of paragraph/table XML strings
        self.images = []         # list of (rId, arcname, filepath)
        self._img_counter = 0
        self._eq_counter = 0

    # -- paragraphs ----------------------------------------------------------
    def heading(self, text, level=1):
        style = {1: "Heading1", 2: "Heading2", 3: "Heading3"}.get(level, "Heading2")
        self.body.append(
            '<w:p><w:pPr><w:pStyle w:val="%s"/></w:pPr>'
            '<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r></w:p>'
            % (style, escape(text)))

    def title(self, text):
        self.body.append(
            '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr>'
            '<w:r><w:rPr><w:b/><w:sz w:val="30"/></w:rPr>'
            '<w:t xml:space="preserve">%s</w:t></w:r></w:p>' % escape(text))

    def para(self, text, bold=False, italic=False, justify=True):
        runs = self._runs_from_text(text, bold, italic)
        jc = '<w:jc w:val="both"/>' if justify else ''
        self.body.append('<w:p><w:pPr>%s<w:spacing w:after="120"/></w:pPr>%s</w:p>' % (jc, runs))

    def _runs_from_text(self, text, bold=False, italic=False):
        rpr = ""
        if bold or italic:
            rpr = "<w:rPr>%s%s</w:rPr>" % ("<w:b/>" if bold else "", "<w:i/>" if italic else "")
        return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, escape(text))

    # -- equations -----------------------------------------------------------
    def equation(self, omml, number=None):
        """Insert a display equation (centered) with an optional right-aligned
        equation number in parentheses, using a tab-stop layout."""
        self._eq_counter += 1
        math_block = '<m:oMathPara><m:oMathParaPr><m:jc m:val="center"/></m:oMathParaPr>' \
                     '<m:oMath>%s</m:oMath></m:oMathPara>' % omml
        if number is None:
            self.body.append('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="120"/></w:pPr>%s</w:p>'
                             % math_block)
        else:
            # equation with number: use a right tab stop at ~9360 twips
            self.body.append(
                '<w:p><w:pPr><w:tabs><w:tab w:val="center" w:pos="4680"/>'
                '<w:tab w:val="right" w:pos="9360"/></w:tabs><w:spacing w:after="120"/></w:pPr>'
                '<w:r><w:tab/></w:r>'
                '<m:oMath>%s</m:oMath>'
                '<w:r><w:tab/><w:t xml:space="preserve">(%s)</w:t></w:r></w:p>'
                % (omml, escape(str(number))))

    def inline_math(self, text_before, omml, text_after=""):
        parts = []
        if text_before:
            parts.append(self._runs_from_text(text_before))
        parts.append('<m:oMath>%s</m:oMath>' % omml)
        if text_after:
            parts.append(self._runs_from_text(text_after))
        self.body.append('<w:p><w:pPr><w:jc w:val="both"/><w:spacing w:after="120"/></w:pPr>%s</w:p>'
                         % "".join(parts))

    # -- figures -------------------------------------------------------------
    def figure(self, filepath, caption, width_emu=5486400):
        self._img_counter += 1
        rId = "rIdImg%d" % self._img_counter
        arc = "media/image%d.png" % self._img_counter
        self.images.append((rId, arc, filepath))
        # get image dims to preserve aspect ratio
        w_px, h_px = _png_size(filepath)
        aspect = h_px / w_px if w_px else 0.66
        cx = width_emu
        cy = int(cx * aspect)
        drawing = _drawing_xml(rId, self._img_counter, cx, cy)
        self.body.append('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/></w:pPr>'
                         '<w:r>%s</w:r></w:p>' % drawing)
        self.body.append('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="160"/></w:pPr>'
                         '<w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr>'
                         '<w:t xml:space="preserve">%s</w:t></w:r></w:p>' % escape(caption))

    # -- tables --------------------------------------------------------------
    def table(self, caption, headers, rows):
        if caption:
            self.body.append('<w:p><w:pPr><w:spacing w:before="120" w:after="60"/></w:pPr>'
                             '<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r></w:p>'
                             % escape(caption))
        ncol = len(headers)
        gridw = int(9360 / ncol)
        grid = "".join('<w:gridCol w:w="%d"/>' % gridw for _ in range(ncol))
        def cell(txt, bold=False):
            rpr = "<w:rPr><w:b/></w:rPr>" if bold else ""
            return ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/></w:tcPr>'
                    '<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>'
                    '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p></w:tc>'
                    % (gridw, rpr, escape(str(txt))))
        hdr = '<w:tr>%s</w:tr>' % "".join(cell(h, True) for h in headers)
        body_rows = ""
        for r in rows:
            body_rows += '<w:tr>%s</w:tr>' % "".join(cell(c) for c in r)
        tblpr = ('<w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="9360" w:type="dxa"/>'
                 '<w:tblBorders>'
                 '<w:top w:val="single" w:sz="4" w:space="0" w:color="666666"/>'
                 '<w:left w:val="single" w:sz="4" w:space="0" w:color="666666"/>'
                 '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="666666"/>'
                 '<w:right w:val="single" w:sz="4" w:space="0" w:color="666666"/>'
                 '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
                 '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
                 '</w:tblBorders></w:tblPr>')
        self.body.append('<w:tbl>%s<w:tblGrid>%s</w:tblGrid>%s%s</w:tbl>'
                         % (tblpr, grid, hdr, body_rows))
        self.body.append('<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>')

    # -- serialise -----------------------------------------------------------
    def save(self, path):
        body_xml = "".join(self.body)
        document = _DOC_TMPL % body_xml
        content_types = _CONTENT_TYPES
        rels = _ROOT_RELS
        doc_rels = _document_rels(self.images)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", content_types)
            z.writestr("_rels/.rels", rels)
            z.writestr("word/document.xml", document)
            z.writestr("word/_rels/document.xml.rels", doc_rels)
            z.writestr("word/styles.xml", _STYLES)
            for rId, arc, fp in self.images:
                with open(fp, "rb") as fh:
                    z.writestr("word/" + arc, fh.read())
        return path


# ---------------------------------------------------------------------------
# PNG size reader (IHDR) — stdlib only
# ---------------------------------------------------------------------------
def _png_size(path):
    import struct
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return (800, 500)
    w, h = struct.unpack(">II", head[16:24])
    return (w, h)


def _drawing_xml(rId, docpr_id, cx, cy):
    return (
        '<w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
        '<wp:extent cx="%d" cy="%d"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        '<wp:docPr id="%d" name="Picture %d"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr><pic:cNvPr id="%d" name="Picture %d"/><pic:cNvPicPr/></pic:nvPicPr>'
        '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing>'
        % (cx, cy, docpr_id, docpr_id, docpr_id, docpr_id, rId, cx, cy))


def _document_rels(images):
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rIdStyles" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
            'Target="styles.xml"/>']
    for rId, arc, _ in images:
        rels.append('<Relationship Id="%s" '
                    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                    'Target="%s"/>' % (rId, arc))
    rels.append('</Relationships>')
    return "".join(rels)


_CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Default Extension="png" ContentType="image/png"/>'
    '<Override PartName="/word/document.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    '</Types>')

_ROOT_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
    'Target="word/document.xml"/></Relationships>')

_STYLES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:docDefaults><w:rPrDefault><w:rPr>'
    '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
    '<w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
    '<w:pPr><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr>'
    '<w:rPr><w:b/><w:sz w:val="26"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
    '<w:pPr><w:spacing w:before="200" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr>'
    '<w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/>'
    '<w:pPr><w:spacing w:before="160" w:after="80"/><w:outlineLvl w:val="2"/></w:pPr>'
    '<w:rPr><w:b/><w:i/><w:sz w:val="22"/></w:rPr></w:style>'
    '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/></w:style>'
    '</w:styles>')

_DOC_TMPL = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document '
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
    '<w:body>%s'
    '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
    'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
    '</w:body></w:document>')


if __name__ == "__main__":
    d = Document()
    d.title("OMML self-test")
    d.para("Quadratic formula:")
    eq = group(run("x"), op("="),
               frac(group(op(G['minus']), run("b"), op("\u00b1"),
                          rad(group(sup(run("b"), run("2")), op(G['minus']),
                                    run("4"), run("a"), run("c")))),
                    group(run("2"), run("a"))))
    d.equation(eq, number=1)
    d.save("/tmp/_omml_selftest.docx")
    print("wrote /tmp/_omml_selftest.docx")
