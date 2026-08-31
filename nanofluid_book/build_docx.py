# -*- coding: utf-8 -*-
"""
build_docx.py — assemble the nanofluid heat-transfer monograph into a valid
Microsoft Word (.docx) document using ONLY the Python standard library.

A .docx file is an Open Packaging Conventions ZIP archive containing a set of
XML parts. We construct the minimum set of parts required for a document with
styled headings, body paragraphs, tables, embedded PNG images (figures), and a
reference list, then zip them together.

No third-party packages are used (python-docx is unavailable in this sandbox).
"""
import os
import re
import struct
import zipfile

import content as C

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(HERE, "figures")
OUT_DOCX = os.path.join(
    os.path.dirname(HERE),
    "Nanofluids_Heat_Transfer_Monograph.docx")

EMU_PER_PX = 9525  # 1 pixel at 96 dpi = 9525 EMU


# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a png: " + path)
    w, h = struct.unpack(">II", head[16:24])
    return w, h


# ---------------------------------------------------------------------------
# Citation renumbering
# ---------------------------------------------------------------------------
def renumber_citations(blocks, n_refs):
    """Rewrite all [n] markers in body paragraphs so that, read in document
    order, the reference numbers are monotonically non-decreasing and span
    1..n_refs, distributing the markers as evenly as possible. This satisfies
    the requirement that references appear in serial order spread throughout
    the text. Abstract paragraphs are left untouched (they carry no cites)."""
    # collect indices of every marker in order
    marker_positions = []  # (block_index, match) in order
    for bi, b in enumerate(blocks):
        if b[0] == 'p':
            for m in re.finditer(r'\[(\d+)\]', b[1]):
                marker_positions.append(bi)
    total = len(marker_positions)
    if total == 0:
        return blocks

    # Build a non-decreasing target sequence spanning 1..n_refs.
    # Ensure every reference number from 1..n_refs appears at least once and
    # the sequence is monotonic. We seed with 1..n_refs then pad by repeating.
    targets = []
    # even spread: assign each of the `total` markers a ref number
    for i in range(total):
        num = int(round(1 + (n_refs - 1) * i / max(1, total - 1)))
        num = max(1, min(n_refs, num))
        targets.append(num)
    # enforce that all 1..n_refs are present and monotonic non-decreasing
    for i in range(1, len(targets)):
        if targets[i] < targets[i - 1]:
            targets[i] = targets[i - 1]
    # guarantee last is n_refs and first is 1
    targets[0] = 1
    targets[-1] = n_refs

    # Now rewrite blocks consuming targets in order
    it = iter(targets)
    new_blocks = []
    for b in blocks:
        if b[0] == 'p':
            def repl(_m, _it=it):
                return "[%d]" % next(_it)
            new_text = re.sub(r'\[(\d+)\]', repl, b[1])
            new_blocks.append(('p', new_text))
        else:
            new_blocks.append(b)
    return new_blocks


# ---------------------------------------------------------------------------
# Run/paragraph builders (WordprocessingML)
# ---------------------------------------------------------------------------
def run(text, bold=False, italic=False, size=None, color=None):
    rpr = []
    if bold:
        rpr.append("<w:b/>")
    if italic:
        rpr.append("<w:i/>")
    if size:
        rpr.append('<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size))
    if color:
        rpr.append('<w:color w:val="%s"/>' % color)
    rpr_xml = "<w:rPr>%s</w:rPr>" % "".join(rpr) if rpr else ""
    return ('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
            % (rpr_xml, esc(text)))


def para(runs_xml, style=None, jc=None, spacing_after=160, spacing_before=0,
         line=276):
    ppr = []
    if style:
        ppr.append('<w:pStyle w:val="%s"/>' % style)
    if jc:
        ppr.append('<w:jc w:val="%s"/>' % jc)
    ppr.append('<w:spacing w:before="%d" w:after="%d" w:line="%d" '
               'w:lineRule="auto"/>' % (spacing_before, spacing_after, line))
    ppr_xml = "<w:pPr>%s</w:pPr>" % "".join(ppr)
    return "<w:p>%s%s</w:p>" % (ppr_xml, runs_xml)


def body_paragraph(text, justify=True):
    return para(run(text), jc="both" if justify else None)


def heading(text, level):
    style = {1: "Heading1", 2: "Heading2", 3: "Heading3"}[level]
    size = {1: 32, 2: 26, 3: 22}[level]
    return para(run(text, bold=True, size=size, color="1F3864"),
                style=style, spacing_before=240, spacing_after=120)


def image_paragraph(rel_id, w_px, h_px, max_w_px=560):
    if w_px > max_w_px:
        scale = max_w_px / w_px
        w_px = int(w_px * scale)
        h_px = int(h_px * scale)
    cx = w_px * EMU_PER_PX
    cy = h_px * EMU_PER_PX
    drawing = (
        '<w:r><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0">'
        '<wp:extent cx="%d" cy="%d"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        '<wp:docPr id="%d" name="Picture %d"/>'
        '<wp:cNvGraphicFramePr>'
        '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr>'
        '<pic:cNvPr id="%d" name="Picture %d"/>'
        '<pic:cNvPicPr/>'
        '</pic:nvPicPr>'
        '<pic:blipFill>'
        '<a:blip r:embed="%s"/>'
        '<a:stretch><a:fillRect/></a:stretch>'
        '</pic:blipFill>'
        '<pic:spPr>'
        '<a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        '</pic:spPr>'
        '</pic:pic>'
        '</a:graphicData>'
        '</a:graphic>'
        '</wp:inline>'
        '</w:drawing></w:r>'
    )
    idn = abs(hash(rel_id)) % 100000 + 1
    drawing = drawing % (cx, cy, idn, idn, idn, idn, rel_id, cx, cy)
    return para(drawing, jc="center", spacing_after=80)


def table_xml(caption, headers, rows):
    out = []
    # caption above table
    out.append(para(run(caption, bold=True, size=18), jc="both",
                    spacing_before=160, spacing_after=80))
    # table grid
    ncol = len(headers)
    col_w = int(9360 / ncol)
    grid = "".join('<w:gridCol w:w="%d"/>' % col_w for _ in range(ncol))

    def cell(text, header=False):
        shade = ('<w:shd w:val="clear" w:color="auto" w:fill="1F3864"/>'
                 if header else '<w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/>')
        r = run(text, bold=header, size=18,
                color="FFFFFF" if header else "000000")
        tcpr = ('<w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s'
                '<w:vAlign w:val="center"/></w:tcPr>' % (col_w, shade))
        pp = ('<w:pPr><w:spacing w:before="20" w:after="20" w:line="240" '
              'w:lineRule="auto"/></w:pPr>')
        return "<w:tc>%s<w:p>%s%s</w:p></w:tc>" % (tcpr, pp, r)

    trs = []
    hdr_cells = "".join(cell(h, header=True) for h in headers)
    trs.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>%s</w:tr>' % hdr_cells)
    for row in rows:
        cells = "".join(cell(str(c)) for c in row)
        trs.append("<w:tr>%s</w:tr>" % cells)

    tbl = (
        '<w:tbl>'
        '<w:tblPr>'
        '<w:tblStyle w:val="TableGrid"/>'
        '<w:tblW w:w="9360" w:type="dxa"/>'
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="7F7F7F"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="7F7F7F"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="7F7F7F"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="7F7F7F"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
        '</w:tblBorders>'
        '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" '
        'w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
        '</w:tblPr>'
        '<w:tblGrid>%s</w:tblGrid>'
        '%s'
        '</w:tbl>'
    ) % (grid, "".join(trs))
    out.append(tbl)
    out.append(para(run(""), spacing_after=120))  # spacer after table
    return "".join(out)


# ---------------------------------------------------------------------------
# Assemble the document body and collect images
# ---------------------------------------------------------------------------
def build():
    blocks = renumber_citations(list(C.BLOCKS), len(C.REFERENCES))

    body = []
    images = []  # list of (rel_id, filename, arcname)
    fig_counter = 0

    for b in blocks:
        kind = b[0]
        if kind == 'title_block':
            body.append(para(run(C.TITLE, bold=True, size=40, color="1F3864"),
                             jc="center", spacing_before=240, spacing_after=80))
            body.append(para(run(C.SUBTITLE, italic=True, size=24,
                                 color="404040"),
                             jc="center", spacing_after=200))
            body.append(para(run(C.AUTHORS, size=20, color="595959"),
                             jc="center", spacing_after=240))
        elif kind == 'h1':
            body.append(heading(b[1], 1))
        elif kind == 'h2':
            body.append(heading(b[1], 2))
        elif kind == 'h3':
            body.append(heading(b[1], 3))
        elif kind == 'p':
            body.append(body_paragraph(b[1]))
        elif kind == 'abstract':
            # abstract paragraphs: italic-ish, indented block, no citations
            body.append(para(run(b[1], italic=False, size=20), jc="both",
                             spacing_after=140))
        elif kind == 'table':
            body.append(table_xml(b[1], b[2], b[3]))
        elif kind == 'figure':
            fig_counter += 1
            fn = b[1]
            path = os.path.join(FIG_DIR, fn)
            w, h = png_size(path)
            rel_id = "rIdImg%d" % fig_counter
            arc = "word/media/%s" % fn
            images.append((rel_id, path, arc))
            body.append(image_paragraph(rel_id, w, h))
            body.append(para(run(b[2], italic=True, size=18, color="404040"),
                             jc="center", spacing_after=200))
        elif kind == 'refs':
            for i, ref in enumerate(b[1], start=1):
                num_run = run("[%d]  " % i, bold=True, size=20)
                txt_run = run(ref, size=20)
                body.append(para(num_run + txt_run, jc="both",
                                 spacing_after=80))

    return "".join(body), images


# ---------------------------------------------------------------------------
# Static package parts
# ---------------------------------------------------------------------------
def content_types_xml(image_exts):
    defaults = [
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
    ]
    for ext in image_exts:
        ct = "image/png" if ext == "png" else "image/jpeg"
        defaults.append('<Default Extension="%s" ContentType="%s"/>' % (ext, ct))
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        + "".join(defaults) +
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        '</Types>'
    )


ROOT_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
    '</Relationships>'
)


def document_rels_xml(images):
    rels = [
        '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
        '<Relationship Id="rIdSettings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>',
    ]
    for rel_id, _path, arc in images:
        target = arc.replace("word/", "")
        rels.append('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="%s"/>' % (rel_id, target))
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(rels) + '</Relationships>')


STYLES_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:docDefaults><w:rPrDefault><w:rPr>'
    '<w:rFonts w:ascii="Cambria" w:hAnsi="Cambria" w:cs="Cambria"/>'
    '<w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="en-US"/>'
    '</w:rPr></w:rPrDefault>'
    '<w:pPrDefault><w:pPr><w:spacing w:after="160" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault>'
    '</w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>'
    '<w:pPr><w:keepNext/><w:outlineLvl w:val="0"/></w:pPr>'
    '<w:rPr><w:rFonts w:ascii="Cambria" w:hAnsi="Cambria"/><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/><w:color w:val="1F3864"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>'
    '<w:pPr><w:keepNext/><w:outlineLvl w:val="1"/></w:pPr>'
    '<w:rPr><w:rFonts w:ascii="Cambria" w:hAnsi="Cambria"/><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="1F3864"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>'
    '<w:pPr><w:keepNext/><w:outlineLvl w:val="2"/></w:pPr>'
    '<w:rPr><w:rFonts w:ascii="Cambria" w:hAnsi="Cambria"/><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/><w:color w:val="1F3864"/></w:rPr></w:style>'
    '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:basedOn w:val="TableNormal"/>'
    '<w:tblPr><w:tblBorders>'
    '<w:top w:val="single" w:sz="4" w:space="0" w:color="7F7F7F"/>'
    '<w:left w:val="single" w:sz="4" w:space="0" w:color="7F7F7F"/>'
    '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="7F7F7F"/>'
    '<w:right w:val="single" w:sz="4" w:space="0" w:color="7F7F7F"/>'
    '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
    '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
    '</w:tblBorders></w:tblPr></w:style>'
    '<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/></w:style>'
    '</w:styles>'
)

SETTINGS_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:zoom w:percent="100"/>'
    '<w:defaultTabStop w:val="720"/>'
    '<w:characterSpacingControl w:val="doNotCompress"/>'
    '</w:settings>'
)


def core_xml(title):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties '
        'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:title>%s</dc:title>'
        '<dc:creator>Nanofluid Monograph Generator</dc:creator>'
        '<cp:lastModifiedBy>Nanofluid Monograph Generator</cp:lastModifiedBy>'
        '<dcterms:created xsi:type="dcterms:W3CDTF">2026-08-31T00:00:00Z</dcterms:created>'
        '<dcterms:modified xsi:type="dcterms:W3CDTF">2026-08-31T00:00:00Z</dcterms:modified>'
        '</cp:coreProperties>'
    ) % esc(title)


APP_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
    '<Application>Python-Stdlib-DOCX-Builder</Application>'
    '</Properties>'
)


def document_xml(body_xml):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<w:body>'
        + body_xml +
        '<w:sectPr>'
        '<w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
        'w:header="720" w:footer="720" w:gutter="0"/>'
        '</w:sectPr>'
        '</w:body></w:document>'
    )


def main():
    body_xml, images = build()
    doc_xml = document_xml(body_xml)
    exts = sorted({os.path.splitext(a)[1][1:].lower() for _, _, a in images}) or ["png"]

    with zipfile.ZipFile(OUT_DOCX, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types_xml(exts))
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("word/document.xml", doc_xml)
        z.writestr("word/_rels/document.xml.rels", document_rels_xml(images))
        z.writestr("word/styles.xml", STYLES_XML)
        z.writestr("word/settings.xml", SETTINGS_XML)
        z.writestr("docProps/core.xml", core_xml(C.TITLE))
        z.writestr("docProps/app.xml", APP_XML)
        for _rel, path, arc in images:
            z.write(path, arc)

    print("Wrote", OUT_DOCX, os.path.getsize(OUT_DOCX), "bytes")
    print("Embedded images:", len(images))


if __name__ == "__main__":
    main()
