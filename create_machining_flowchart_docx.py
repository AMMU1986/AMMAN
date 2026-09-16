#!/usr/bin/env python3
"""
Create an editable Word .docx recreation of the flowchart:
"Machining of Biomaterials".

Layout (a bordered table mimicking the flowchart):
    [ Machining of Biomaterials ]            (full-width box)
                 v  v  v
  [Titanium Alloy] [Parametric Opt.] [Hybrid Mfg.]   (three boxes)
                 \  |  /
    [ Outcome: ... ]                         (full-width box)

Everything is real Word text in table cells -> fully editable.
Uses raw OOXML (ZIP + XML) so no python-docx dependency is needed.
"""

import zipfile
from xml.sax.saxutils import escape

OUT = "Machining_of_Biomaterials_Flowchart.docx"

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

COL_W = 3120  # twips per column; 3 columns => 9360 total (fits letter w/ 1080 margins)


def r(text, bold=False, size=None):
    props = ""
    if bold:
        props += "<w:b/>"
    if size:
        props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    rpr = f"<w:rPr>{props}</w:rPr>" if props else ""
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def p(runs, align="center", space_before=40, space_after=40):
    if isinstance(runs, str):
        runs = [runs]
    runs_xml = "".join(runs)
    ppr = (
        f'<w:pPr><w:jc w:val="{align}"/>'
        f'<w:spacing w:before="{space_before}" w:after="{space_after}"/></w:pPr>'
    )
    return f'<w:p>{ppr}{runs_xml}</w:p>'


def cell(paras, span=1, box=True, width=COL_W):
    """A table cell. box=True draws a full border (a flowchart box);
    box=False draws no borders (used for arrow / spacer rows)."""
    if box:
        borders = (
            '<w:tcBorders>'
            '<w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
            '<w:left w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
            '<w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
            '<w:right w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
            '</w:tcBorders>'
        )
    else:
        borders = (
            '<w:tcBorders>'
            '<w:top w:val="nil"/><w:left w:val="nil"/>'
            '<w:bottom w:val="nil"/><w:right w:val="nil"/>'
            '</w:tcBorders>'
        )
    gridspan = f'<w:gridSpan w:val="{span}"/>' if span > 1 else ""
    tcpr = (
        f'<w:tcPr><w:tcW w:w="{width*span}" w:type="dxa"/>'
        f'{gridspan}{borders}<w:vAlign w:val="center"/></w:tcPr>'
    )
    return f'<w:tc>{tcpr}{"".join(paras)}</w:tc>'


def row(cells, height=None):
    trpr = ""
    if height:
        trpr = f'<w:trPr><w:trHeight w:val="{height}"/></w:trPr>'
    return f'<w:tr>{trpr}{"".join(cells)}</w:tr>'


def build_document():
    borders_none_tbl = (
        '<w:tblBorders>'
        '<w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/>'
        '<w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/>'
        '</w:tblBorders>'
    )
    tblpr = (
        f'<w:tblPr><w:tblW w:w="{COL_W*3}" w:type="dxa"/>'
        f'<w:jc w:val="center"/>{borders_none_tbl}'
        '<w:tblCellMar>'
        '<w:top w:w="80" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
        '<w:bottom w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/>'
        '</w:tblCellMar>'
        '<w:tblLayout w:type="fixed"/></w:tblPr>'
    )
    grid = "<w:tblGrid>" + "".join(
        f'<w:gridCol w:w="{COL_W}"/>' for _ in range(3)) + "</w:tblGrid>"

    rows = []

    # Row 1 — title box (spans 3)
    rows.append(row([
        cell([p([r("Machining of Biomaterials", bold=True, size=32)])],
             span=3, box=True)
    ], height=700))

    # Row 2 — three down arrows (no borders)
    rows.append(row([
        cell([p([r("\u2193", size=32)])], box=False),
        cell([p([r("\u2193", size=32)])], box=False),
        cell([p([r("\u2193", size=32)])], box=False),
    ], height=350))

    # Row 3 — three boxes
    rows.append(row([
        cell([
            p([r("Titanium Alloy Machining", bold=True)]),
            p([r("Ti-6Al-4V implants")]),
        ], box=True),
        cell([
            p([r("Parametric Optimization", bold=True)]),
            p([r("Best Ra = 0.34 \u00b5m")]),
        ], box=True),
        cell([
            p([r("Hybrid Manufacturing", bold=True)]),
            p([r("AM + CNC, EBM parts")]),
        ], box=True),
    ], height=900))

    # Row 4 — converging arrows toward the outcome (no borders)
    rows.append(row([
        cell([p([r("\u2198", size=32)])], box=False),
        cell([p([r("\u2193", size=32)])], box=False),
        cell([p([r("\u2199", size=32)])], box=False),
    ], height=350))

    # Row 5 — outcome box (spans 3)
    rows.append(row([
        cell([
            p([r("Outcome: ", bold=True),
               r("Better Surface Quality, Reduced Tool Wear,")]),
            p([r("Optimized Performance")]),
        ], span=3, box=True)
    ], height=750))

    table = f'<w:tbl>{tblpr}{grid}{"".join(rows)}</w:tbl>'

    heading = p([r("Machining of Biomaterials \u2014 Process Flow",
                   bold=True, size=28)], align="center")

    body = (
        '<w:body>'
        + heading
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
    doc = build_document()
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", WORD_RELS)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/document.xml", doc)
    print(f"Created {OUT}")


if __name__ == "__main__":
    main()
