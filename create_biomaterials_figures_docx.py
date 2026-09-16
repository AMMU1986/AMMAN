#!/usr/bin/env python3
"""Generate an editable Word (.docx) document reconstructing three biomaterials
machining flowcharts as native, editable Word objects.

The three figures are rebuilt using WordprocessingML tables styled as flowchart
boxes (bordered, shaded cells with centered bold headings and editable text)
plus downward-arrow glyph rows to indicate flow. All text and boxes remain fully
editable inside Microsoft Word - nothing is embedded as a raster image.

This script depends only on the Python standard library. A .docx file is an
Office Open XML package: a ZIP archive of XML parts. We emit those parts
directly, which avoids any dependency on python-docx / lxml (unavailable here
due to the offline environment).
"""

import zipfile
from xml.sax.saxutils import escape

OUTPUT = "Biomaterials_Editable_Figures.docx"

# ---------------------------------------------------------------------------
# Low-level WordprocessingML helpers
# ---------------------------------------------------------------------------

# Standard EMU / twip helpers. Page usable width (Letter, 1in margins) ~ 9360 twips.
PAGE_WIDTH_TWIPS = 9360


def run(text, bold=False, size=22, color="000000"):
    """Build a <w:r> run. size is in half-points (22 => 11pt)."""
    rpr = ["<w:rPr>"]
    if bold:
        rpr.append("<w:b/>")
    rpr.append('<w:sz w:val="%d"/>' % size)
    rpr.append('<w:szCs w:val="%d"/>' % size)
    rpr.append('<w:color w:val="%s"/>' % color)
    rpr.append("</w:rPr>")
    return (
        "<w:r>"
        + "".join(rpr)
        + '<w:t xml:space="preserve">%s</w:t>' % escape(text)
        + "</w:r>"
    )


def paragraph(runs, align="center", spacing_after=40, spacing_before=40):
    """Build a <w:p> from a list of run XML strings (or (text, opts) segments)."""
    ppr = ["<w:pPr>"]
    ppr.append('<w:spacing w:before="%d" w:after="%d"/>' % (spacing_before, spacing_after))
    ppr.append('<w:jc w:val="%s"/>' % align)
    ppr.append("</w:pPr>")
    return "<w:p>" + "".join(ppr) + "".join(runs) + "</w:p>"


def empty_paragraph():
    return "<w:p><w:pPr><w:spacing w:before=\"0\" w:after=\"0\"/></w:pPr></w:p>"


def cell(paragraphs, width, shade=None, borders=True, valign="center"):
    """Build a <w:tc> table cell (a flowchart box)."""
    tcpr = ["<w:tcPr>"]
    tcpr.append('<w:tcW w:w="%d" w:type="dxa"/>' % width)
    if borders:
        b = (
            '<w:tcBorders>'
            '<w:top w:val="single" w:sz="12" w:space="0" w:color="2F5496"/>'
            '<w:left w:val="single" w:sz="12" w:space="0" w:color="2F5496"/>'
            '<w:bottom w:val="single" w:sz="12" w:space="0" w:color="2F5496"/>'
            '<w:right w:val="single" w:sz="12" w:space="0" w:color="2F5496"/>'
            '</w:tcBorders>'
        )
        tcpr.append(b)
    else:
        tcpr.append(
            '<w:tcBorders>'
            '<w:top w:val="nil"/><w:left w:val="nil"/>'
            '<w:bottom w:val="nil"/><w:right w:val="nil"/>'
            '</w:tcBorders>'
        )
    if shade:
        tcpr.append('<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % shade)
    tcpr.append('<w:vAlign w:val="%s"/>' % valign)
    tcpr.append(
        '<w:tcMar>'
        '<w:top w:w="80" w:type="dxa"/><w:left w:w="120" w:type="dxa"/>'
        '<w:bottom w:w="80" w:type="dxa"/><w:right w:w="120" w:type="dxa"/>'
        '</w:tcMar>'
    )
    tcpr.append("</w:tcPr>")
    body = "".join(paragraphs) if paragraphs else empty_paragraph()
    return "<w:tc>" + "".join(tcpr) + body + "</w:tc>"


def table(rows_xml, total_width=PAGE_WIDTH_TWIPS):
    """Wrap rows (<w:tr> strings) into a <w:tbl> with no default borders."""
    tblpr = (
        "<w:tblPr>"
        + ('<w:tblW w:w="%d" w:type="dxa"/>' % total_width)
        + '<w:jc w:val="center"/>'
        '<w:tblBorders>'
        '<w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/>'
        '<w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/>'
        '</w:tblBorders>'
        '<w:tblCellMar>'
        '<w:left w:w="60" w:type="dxa"/><w:right w:w="60" w:type="dxa"/>'
        '</w:tblCellMar>'
        "</w:tblPr>"
    )
    return "<w:tbl>" + tblpr + "".join(rows_xml) + "</w:tbl>"


def row(cells_xml, height=None):
    trpr = ""
    if height:
        trpr = '<w:trPr><w:trHeight w:val="%d"/></w:trPr>' % height
    return "<w:tr>" + trpr + "".join(cells_xml) + "</w:tr>"


def box_cell(width, heading, subtitle=None, bullets=None, shade="DEEBF7",
             heading_bold=True, heading_size=24, prefix_bold_word=None):
    """A flowchart box: bold heading, optional subtitle, optional bullet lines."""
    paras = []
    if prefix_bold_word:
        # Render a heading where a leading word is bold and the rest is normal.
        segs = [run(prefix_bold_word + " ", bold=True, size=heading_size)]
        segs.append(run(heading, bold=False, size=heading_size))
        paras.append(paragraph(segs, align="center"))
    else:
        paras.append(
            paragraph([run(heading, bold=heading_bold, size=heading_size)], align="center")
        )
    if subtitle:
        paras.append(paragraph([run(subtitle, bold=False, size=20)], align="center"))
    if bullets:
        for bt in bullets:
            paras.append(
                paragraph(
                    [run("\u2022 ", bold=False, size=20), run(bt, bold=False, size=20)],
                    align="left",
                    spacing_after=20,
                    spacing_before=20,
                )
            )
    return cell(paras, width, shade=shade, borders=True, valign="center")


def arrow_row(n_cols, total_width=PAGE_WIDTH_TWIPS):
    """A borderless row of downward arrow glyphs, one per column."""
    w = total_width // n_cols
    cells = []
    for _ in range(n_cols):
        p = paragraph([run("\u2193", bold=True, size=32, color="2F5496")],
                      align="center", spacing_after=20, spacing_before=20)
        cells.append(cell([p], w, shade=None, borders=False, valign="center"))
    return row(cells)


def spacer_row(text, total_width=PAGE_WIDTH_TWIPS):
    """A single borderless cell used for converging arrows / flow arrows."""
    p = paragraph([run(text, bold=True, size=32, color="2F5496")],
                  align="center", spacing_after=20, spacing_before=20)
    return row([cell([p], total_width, shade=None, borders=False, valign="center")])


def caption(text):
    return paragraph(
        [run(text, bold=True, size=22, color="000000")],
        align="center", spacing_before=120, spacing_after=200,
    )


def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def heading_line(text):
    return paragraph([run(text, bold=True, size=28, color="1F3864")],
                     align="center", spacing_before=120, spacing_after=160)


# ---------------------------------------------------------------------------
# Figure builders
# ---------------------------------------------------------------------------

def figure1():
    parts = []
    parts.append(heading_line("Figure 1"))

    # Top title box (full width), white heading on dark fill for contrast.
    top = row([cell(
        [paragraph([run("Machining of Biomaterials", bold=True, size=28, color="FFFFFF")],
                   align="center")],
        PAGE_WIDTH_TWIPS, shade="2F5496", borders=True, valign="center")])
    parts.append(table([top]))

    # arrows down to three columns
    parts.append(table([arrow_row(3)]))

    col_w = PAGE_WIDTH_TWIPS // 3
    mid = row([
        box_cell(col_w, "Titanium Alloy Machining", subtitle="Ti-6Al-4V implants"),
        box_cell(col_w, "Parametric Optimization", subtitle="Best Ra = 0.34 \u00b5m"),
        box_cell(col_w, "Hybrid Manufacturing", subtitle="AM + CNC, EBM parts"),
    ])
    parts.append(table([mid]))

    # converging arrows into bottom box
    parts.append(table([spacer_row("\u2193")]))

    bottom = row([cell(
        [paragraph(
            [run("Outcome: ", bold=True, size=24),
             run("Better Surface Quality, Reduced Tool Wear, Optimized Performance",
                 bold=False, size=24)],
            align="center")],
        PAGE_WIDTH_TWIPS, shade="E2EFDA", borders=True, valign="center")])
    parts.append(table([bottom]))

    parts.append(caption("Figure 1. Machining of biomaterials: pathways to improved "
                         "surface quality and performance."))
    return parts


def figure2():
    parts = []
    parts.append(heading_line("Figure 2"))

    top = row([cell(
        [paragraph([run("Computational Optimization and Performance Evaluation",
                        bold=True, size=28, color="FFFFFF")], align="center")],
        PAGE_WIDTH_TWIPS, shade="2F5496", borders=True, valign="center")])
    parts.append(table([top]))

    parts.append(table([arrow_row(3)]))

    col_w = PAGE_WIDTH_TWIPS // 3
    cols = row([
        box_cell(col_w, "Multi-Objective Optimization Using GA, PSO and GRA",
                 bullets=["Optimizes MRR, roughness, tool wear together",
                          "Finds Pareto-optimal solutions"],
                 shade="DEEBF7", heading_size=22),
        box_cell(col_w, "Genetic Algorithms (GA)",
                 bullets=["Based on natural selection",
                          "Selection, crossover, mutation",
                          "Optimizes turning parameters"],
                 shade="FCE4D6", heading_size=22),
        box_cell(col_w, "Particle Swarm (PSO)",
                 bullets=["Inspired by bird flocking",
                          "Searches for best solution",
                          "Fast convergence, simple use"],
                 shade="E2EFDA", heading_size=22),
    ])
    parts.append(table([cols]))

    parts.append(caption("Figure 2. Computational optimization methods for machining "
                         "parameter evaluation."))
    return parts


def figure3():
    parts = []
    parts.append(heading_line("Figure 3"))

    top = row([cell(
        [paragraph([run("Industrial Case Studies on Patient-Specific Implants and "
                        "Medical Device Manufacturing",
                        bold=True, size=26, color="FFFFFF")], align="center")],
        PAGE_WIDTH_TWIPS, shade="2F5496", borders=True, valign="center")])
    parts.append(table([top]))

    parts.append(table([arrow_row(2)]))

    col_w = PAGE_WIDTH_TWIPS // 2
    cols = row([
        box_cell(col_w, "Case Study: Hip Prosthesis Manufacturing",
                 bullets=[
                     "CNC turning of hip prosthesis components using titanium alloys",
                     "Alloys studied: Ti-6Al-4V, Ti-6Al-7Nb, Ti-13Nb-13Zr",
                     "Minimum roughness Ra = 0.44 \u00b5m at feed rate 0.1 mm/rev for Ti-6Al-4V",
                     "Ti-13Nb-13Zr showed lower cutting forces at all feed rates",
                     "Surface quality affects osseointegration and implant life",
                 ],
                 shade="DEEBF7", heading_size=22),
        box_cell(col_w, "Case Study: Additively Manufactured Femoral Cones",
                 bullets=[
                     "Post-processing of femoral cones made by electron beam melting (EBM)",
                     "~30% reduction in cutting forces vs. wrought Ti-6Al-4V",
                     "'Shell' effect of EBM specimens had no significant impact on "
                     "cutting forces or roughness",
                     "Part orientation significantly affects machined surface quality",
                 ],
                 shade="FCE4D6", heading_size=22),
    ])
    parts.append(table([cols]))

    parts.append(table([spacer_row("\u2193")]))

    bottom = row([cell(
        [paragraph(
            [run("Optimized Machining Parameters \u2192 Improved Surface Quality and "
                 "Precision \u2192 Better Osseointegration and Implant Life \u2192 "
                 "Enhanced Production Efficiency", bold=True, size=22)],
            align="center")],
        PAGE_WIDTH_TWIPS, shade="E2EFDA", borders=True, valign="center")])
    parts.append(table([bottom]))

    parts.append(caption("Figure 3. Industrial case studies linking optimized machining "
                         "to implant performance."))
    return parts


# ---------------------------------------------------------------------------
# Document assembly
# ---------------------------------------------------------------------------

def build_document_xml():
    body = []
    body.append(paragraph(
        [run("Editable Reconstructed Figures: Machining of Biomaterials",
             bold=True, size=32, color="1F3864")],
        align="center", spacing_before=0, spacing_after=240))
    body.append(paragraph(
        [run("The three flowcharts below are reconstructed as native, editable Word "
             "objects. Every box is a table cell and every label is selectable, "
             "editable text - no diagram is embedded as an image.", size=20)],
        align="center", spacing_after=240))

    body += figure1()
    body.append(page_break())
    body += figure2()
    body.append(page_break())
    body += figure3()

    sect = (
        '<w:sectPr>'
        '<w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
        'w:header="720" w:footer="720" w:gutter="0"/>'
        '</w:sectPr>'
    )

    doc = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<w:body>' + "".join(body) + sect + '</w:body></w:document>'
    )
    return doc


CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/docProps/core.xml" '
    'ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
    '<Override PartName="/docProps/app.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
    '</Types>'
)

ROOT_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
    'Target="word/document.xml"/>'
    '<Relationship Id="rId2" '
    'Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" '
    'Target="docProps/core.xml"/>'
    '<Relationship Id="rId3" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" '
    'Target="docProps/app.xml"/>'
    '</Relationships>'
)

DOCUMENT_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '</Relationships>'
)

CORE_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<cp:coreProperties '
    'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
    'xmlns:dc="http://purl.org/dc/elements/1.1/" '
    'xmlns:dcterms="http://purl.org/dc/terms/" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    '<dc:title>Editable Reconstructed Figures: Machining of Biomaterials</dc:title>'
    '<dc:creator>AMMAN</dc:creator>'
    '</cp:coreProperties>'
)

APP_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Properties '
    'xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
    '<Application>create_biomaterials_figures_docx.py</Application>'
    '</Properties>'
)


def main():
    document_xml = build_document_xml()
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("word/document.xml", document_xml)
        z.writestr("word/_rels/document.xml.rels", DOCUMENT_RELS)
        z.writestr("docProps/core.xml", CORE_XML)
        z.writestr("docProps/app.xml", APP_XML)
    print("Wrote %s" % OUTPUT)


if __name__ == "__main__":
    main()
