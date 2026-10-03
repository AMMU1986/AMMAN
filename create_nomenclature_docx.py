#!/usr/bin/env python3
"""
Build Nomenclature_Word.docx: a paste-ready Nomenclature section for the
manuscript, with proper Unicode symbols/units (superscripts, subscripts, Greek),
rendered as a native Word table plus Subscripts / Abbreviations paragraphs.

Pure Python standard library (zipfile). Open the file and copy the whole
Nomenclature block straight into the manuscript, or paste individual rows.
"""

import os
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "Nomenclature_Word.docx")


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def p(text, bold=False, italic=False, size=22, after=120, center=False):
    rpr = ""
    inner = ""
    if bold:
        inner += "<w:b/>"
    if italic:
        inner += "<w:i/>"
    inner += '<w:sz w:val="{0}"/><w:szCs w:val="{0}"/>'.format(size)
    rpr = "<w:rPr>{}</w:rPr>".format(inner)
    jc = '<w:jc w:val="center"/>' if center else ""
    return ('<w:p><w:pPr><w:spacing w:after="{a}"/>{jc}</w:pPr>'
            '<w:r>{rpr}<w:t xml:space="preserve">{t}</w:t></w:r></w:p>'
            .format(a=after, jc=jc, rpr=rpr, t=esc(text)))


def mixed_p(runs, after=120):
    """Paragraph from a list of (text, {b,i}) run dicts (for bold labels)."""
    out = ['<w:p><w:pPr><w:spacing w:after="{}"/></w:pPr>'.format(after)]
    for text, opt in runs:
        inner = ""
        if opt.get("b"):
            inner += "<w:b/>"
        if opt.get("i"):
            inner += "<w:i/>"
        inner += '<w:sz w:val="22"/><w:szCs w:val="22"/>'
        out.append('<w:r><w:rPr>{}</w:rPr><w:t xml:space="preserve">{}</w:t></w:r>'
                   .format(inner, esc(text)))
    out.append("</w:p>")
    return "".join(out)


def sym_runs(symbol):
    """Return run XML for a symbol cell, applying true subscripts for the
    known multi-char subscripted symbols (cp, Dh, DT_LMTD)."""
    base_rpr = '<w:i/><w:sz w:val="20"/><w:szCs w:val="20"/>'
    sub_rpr = '<w:i/><w:vertAlign w:val="subscript"/><w:sz w:val="20"/><w:szCs w:val="20"/>'

    def run(text, rpr):
        return ('<w:r><w:rPr>{}</w:rPr><w:t xml:space="preserve">{}</w:t></w:r>'
                .format(rpr, esc(text)))

    specials = {
        "cp": [("c", base_rpr), ("p", sub_rpr)],
        "Dh": [("D", base_rpr), ("h", sub_rpr)],
        "DTLMTD": [("\u0394T", base_rpr), ("LMTD", sub_rpr)],
    }
    if symbol in specials:
        return "".join(run(t, r) for t, r in specials[symbol])
    return run(symbol, base_rpr)


def table(rows, widths):
    """rows: list of [symbol, desc, unit]; first row = header.
    Symbol cells may use the keys 'cp','Dh','DTLMTD' to trigger true subscripts."""
    grid = "".join('<w:gridCol w:w="{}"/>'.format(w) for w in widths)
    out = ['<w:tbl>',
           '<w:tblPr><w:tblStyle w:val="TableGrid"/>'
           '<w:tblW w:w="9360" w:type="dxa"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
           '</w:tblBorders></w:tblPr>',
           '<w:tblGrid>' + grid + '</w:tblGrid>']
    for ri, row in enumerate(rows):
        out.append("<w:tr>")
        for ci, cell in enumerate(row):
            shade = ('<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>'
                     if ri == 0 else "")
            if ri > 0 and ci == 0:
                # symbol column body: build runs (with true subscripts)
                runs = sym_runs(cell)
            else:
                bold = "<w:b/>" if ri == 0 else ""
                runs = ('<w:r><w:rPr>{bold}<w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
                        '<w:t xml:space="preserve">{t}</w:t></w:r>'
                        .format(bold=bold, t=esc(cell)))
            out.append(
                '<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shade}</w:tcPr>'
                '<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>{runs}</w:p></w:tc>'
                .format(w=widths[ci], shade=shade, runs=runs))
        out.append("</w:tr>")
    out.append("</w:tbl>")
    out.append("<w:p/>")
    return "".join(out)


# ---- content (Unicode: superscripts/subscripts/Greek already applied) ----
SYMBOLS = [
    ["Symbol", "Description", "Unit"],
    ["A", "heat transfer surface area", "m\u00b2"],
    ["cp", "specific heat", "J kg\u207b\u00b9 K\u207b\u00b9"],
    ["Dh", "hydraulic diameter", "m"],
    ["h", "heat transfer coefficient", "W m\u207b\u00b2 K\u207b\u00b9"],
    ["k", "thermal conductivity", "W m\u207b\u00b9 K\u207b\u00b9"],
    ["\u1e45", "mass flow rate", "kg s\u207b\u00b9"],
    ["N", "number of samples", "\u2013"],
    ["Nu", "Nusselt number", "\u2013"],
    ["Pr", "Prandtl number", "\u2013"],
    ["Q", "heat transfer rate", "W"],
    ["Re", "Reynolds number", "\u2013"],
    ["T", "temperature", "K"],
    ["U", "velocity", "m s\u207b\u00b9"],
    ["\u03b5", "radiator effectiveness", "\u2013"],
    ["\u03c6", "nanoparticle volume concentration", "%"],
    ["\u03bc", "dynamic viscosity", "kg m\u207b\u00b9 s\u207b\u00b9"],
    ["\u03c1", "density", "kg m\u207b\u00b3"],
    ["DTLMTD", "log-mean temperature difference", "K"],
]

SUBSCRIPTS = ("nf = nanofluid;  p = particles;  w = base fluid (water);  "
              "in = inlet;  out = outlet;  a = air;  c = coolant;  "
              "max = maximum;  min = minimum.")

ABBREVIATIONS = ("DIW = deionized water;  NF = nanofluid;  HNF = hybrid nanofluid;  "
                 "ML = machine learning;  MLRR = Multiple Linear Ridge Regression;  "
                 "PLSR = Partial Least Squares Regression;  MLP = Multi-Layer Perceptron;  "
                 "SVR = Support Vector Regression;  AdaBoost (AB) = Adaptive Boosting;  "
                 "RFR = Random Forest Regression.")


STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
    <w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr>
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
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

ROOT_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

DOC_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''


def build():
    body = []
    body.append(p("Nomenclature", bold=True, size=28, after=160))
    body.append(table(SYMBOLS, [1600, 5600, 2160]))
    body.append(mixed_p([("Subscripts: ", {"b": True}),
                         (SUBSCRIPTS, {})]))
    body.append(mixed_p([("Abbreviations: ", {"b": True}),
                         (ABBREVIATIONS, {})]))

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:body>' + "".join(body) +
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
        '</w:sectPr></w:body></w:document>'
    )

    with zipfile.ZipFile(OUT_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", CONTENT_TYPES)
        zf.writestr("_rels/.rels", ROOT_RELS)
        zf.writestr("word/_rels/document.xml.rels", DOC_RELS)
        zf.writestr("word/document.xml", document)
        zf.writestr("word/styles.xml", STYLES)

    print("Created {}".format(OUT_PATH))


if __name__ == "__main__":
    build()
