#!/usr/bin/env python3
"""
Create an editable Word .docx for the diagram:
"Challenges in Machining Biomaterials".

Produces a title + a 4-column table (one column per biomaterial class).
Uses raw OOXML (ZIP + XML) so it works without python-docx.
The resulting table is fully editable in Microsoft Word.
"""

import zipfile
from xml.sax.saxutils import escape

OUT = "Challenges_in_Machining_Biomaterials.docx"

COLUMNS = [
    ("Metallic Biomaterials", [
        "Low thermal conductivity",
        "High strength and work hardening",
        "High cutting forces",
        "Tool wear: diffusion and adhesion",
        "Built-up edge formation",
        "Poor surface finish",
        "Heat concentration in cutting zone",
    ]),
    ("Ceramic Biomaterials", [
        "High hardness",
        "Low fracture toughness",
        "Brittle nature",
        "Prone to cracking and chipping",
        "Surface and subsurface damage",
        "Low machining efficiency",
        "Requires non-traditional machining methods",
    ]),
    ("Polymeric Biomaterials", [
        "Low melting point",
        "Low thermal conductivity",
        "Heat accumulation in cutting zone",
        "Thermal softening and melting",
        "Burr formation",
        "Viscoelastic behavior",
        "Dimensional inaccuracy",
        "Poor surface finish",
    ]),
    ("Composite Biomaterials", [
        "Heterogeneous structure",
        "Non-uniform cutting forces",
        "Fiber pull-out",
        "Matrix cracking",
        "Delamination",
        "Surface damage",
        "Difficult to predict machining behavior",
        "Requires optimized cutting parameters",
    ]),
]

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

WORD_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>
        <w:sz w:val="22"/><w:szCs w:val="22"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
  </w:style>
</w:styles>'''


def run(text, bold=False, size=None):
    rpr = ""
    props = ""
    if bold:
        props += "<w:b/>"
    if size:
        props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    if props:
        rpr = f"<w:rPr>{props}</w:rPr>"
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def para(text, bold=False, size=None, align=None, bullet=False):
    ppr_items = ""
    if align:
        ppr_items += f'<w:jc w:val="{align}"/>'
    if bullet:
        ppr_items += ('<w:pPr></w:pPr>')  # placeholder, replaced below
    ppr = f"<w:pPr>{ppr_items}</w:pPr>" if ppr_items else ""
    prefix = "\u2022  " if bullet else ""
    return f'<w:p>{ppr}{run(prefix + text, bold=bold, size=size)}</w:p>'


def cell(paras_xml, width, shade=None, header=False):
    shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>' if shade else ""
    tcpr = (
        f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>'
        f'{shd}<w:vAlign w:val="top"/></w:tcPr>'
    )
    return f'<w:tc>{tcpr}{paras_xml}</w:tc>'


def build_document():
    col_w = 2340  # twips per column (4 cols ~ 9360 total, fits landscape/portrait)

    # borders for the whole table
    borders = (
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:left w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:right w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:insideH w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:insideV w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '</w:tblBorders>'
    )
    tblpr = (
        f'<w:tblPr><w:tblW w:w="{col_w*4}" w:type="dxa"/>'
        f'{borders}'
        '<w:tblLayout w:type="fixed"/></w:tblPr>'
    )
    grid = "<w:tblGrid>" + ("".join(
        f'<w:gridCol w:w="{col_w}"/>' for _ in COLUMNS)) + "</w:tblGrid>"

    # header row
    header_cells = ""
    for title, _ in COLUMNS:
        p = para(title, bold=True, align="center")
        header_cells += cell(p, col_w, shade="D9D9D9")
    header_row = f'<w:tr>{header_cells}</w:tr>'

    # body row (one cell per column with bulleted list)
    body_cells = ""
    for _, items in COLUMNS:
        paras = "".join(para(it, bullet=True) for it in items)
        body_cells += cell(paras, col_w)
    body_row = f'<w:tr>{body_cells}</w:tr>'

    table = f'<w:tbl>{tblpr}{grid}{header_row}{body_row}</w:tbl>'

    title = para("Challenges in Machining Biomaterials",
                 bold=True, size=32, align="center")

    body = (
        '<w:body>'
        + title
        + '<w:p/>'
        + table
        + '<w:p/>'
        + '<w:sectPr>'
        '<w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" '
        'w:header="720" w:footer="720" w:gutter="0"/>'
        '</w:sectPr>'
        '</w:body>'
    )

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        + body +
        '</w:document>'
    )


def main():
    document_xml = build_document()
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", WORD_RELS)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/document.xml", document_xml)
    print(f"Created {OUT}")


if __name__ == "__main__":
    main()
