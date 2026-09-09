#!/usr/bin/env python3
"""Convert a Markdown document to a Word (.docx) file using ONLY the Python
standard library.

A .docx file is an Office Open XML (OOXML) package: a ZIP archive that contains
``[Content_Types].xml``, ``_rels/.rels``, ``word/document.xml`` and the
relationship/media parts. This module builds a valid, well-formed package that
Microsoft Word opens without a repair prompt, using nothing beyond ``zipfile``,
``struct``, ``re``, ``html`` and ``os`` -- no ``python-docx``, ``pandoc`` or any
external dependency, so it runs in a network-isolated environment.

Supported Markdown constructs:
  * ATX headings (``#`` .. ``######``) -> Word heading paragraphs
  * paragraphs -> normal paragraphs
  * bold (``**text**``), italic (``*text*`` / ``_text_``) -> runs
  * inline code (`` `code` ``) -> monospaced runs
  * GitHub pipe tables -> native Word tables (``w:tbl``)
  * bullet (``-`` / ``*``) and ordered (``1.``) lists -> list paragraphs
  * images (``![alt](path)``) -> embedded inline drawings (PNG parts)
  * block quotes (``>``) -> indented paragraphs
  * horizontal rules (``---``) -> bottom-bordered paragraph
  * inline HTML ``<sub>``/``<sup>`` -> subscript/superscript runs

Usage:
    python3 md_to_docx.py INPUT.md OUTPUT.docx
    python3 md_to_docx.py            # convert the two Tesla-valve documents
"""

import html
import os
import re
import struct
import sys
import zipfile

# English Metric Units: 914400 EMU per inch. Word content area is ~6.0 in wide.
EMU_PER_INCH = 914400
MAX_IMAGE_WIDTH_EMU = int(6.0 * EMU_PER_INCH)


def xml_escape(text):
    """Escape the five XML special characters for use in element text."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def png_dimensions(path):
    """Return (width_px, height_px) for a PNG by reading its IHDR header."""
    with open(path, "rb") as fh:
        header = fh.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file: %s" % path)
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def emu_size_for_png(path):
    """Compute an inline image size in EMU, capped to the content width."""
    width_px, height_px = png_dimensions(path)
    dpi = 96.0
    width_emu = int(width_px / dpi * EMU_PER_INCH)
    height_emu = int(height_px / dpi * EMU_PER_INCH)
    if width_emu > MAX_IMAGE_WIDTH_EMU:
        scale = MAX_IMAGE_WIDTH_EMU / width_emu
        width_emu = MAX_IMAGE_WIDTH_EMU
        height_emu = int(height_emu * scale)
    return width_emu, height_emu


# --------------------------------------------------------------------------
# Inline formatting: bold / italic / code / <sub> / <sup> -> list of runs.
# --------------------------------------------------------------------------

# Token regex, evaluated in priority order.
_INLINE_TOKEN = re.compile(
    r"(?P<code>`[^`]+`)"
    r"|(?P<bold>\*\*.+?\*\*)"
    r"|(?P<bolditalic>___.+?___)"
    r"|(?P<italicstar>\*[^*]+?\*)"
    r"|(?P<italicunder>(?<![A-Za-z0-9_])_[^_]+?_(?![A-Za-z0-9_]))"
    r"|(?P<subopen><sub>)"
    r"|(?P<subclose></sub>)"
    r"|(?P<supopen><sup>)"
    r"|(?P<supclose></sup>)"
)


def _run_xml(text, bold=False, italic=False, code=False, vert=None):
    """Build a single ``w:r`` run element from text and formatting flags."""
    if text == "":
        return ""
    props = []
    if bold:
        props.append("<w:b/>")
    if italic:
        props.append("<w:i/>")
    if code:
        props.append('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>')
    if vert == "sub":
        props.append('<w:vertAlign w:val="subscript"/>')
    elif vert == "sup":
        props.append('<w:vertAlign w:val="superscript"/>')
    rpr = "<w:rPr>%s</w:rPr>" % "".join(props) if props else ""
    # xml:space=preserve keeps leading/trailing spaces between runs.
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (
        rpr,
        xml_escape(text),
    )


def inline_runs(text):
    """Parse inline Markdown/HTML into a concatenated string of ``w:r`` XML.

    Strips Markdown/HTML markers and emits runs carrying the appropriate
    bold/italic/code/vertical-align formatting. Unmatched markers degrade to
    literal text so nothing is lost.
    """
    runs = []
    vert = None  # current subscript/superscript context
    pos = 0
    for match in _INLINE_TOKEN.finditer(text):
        if match.start() > pos:
            runs.append(_run_xml(text[pos:match.start()], vert=vert))
        kind = match.lastgroup
        token = match.group()
        if kind == "code":
            runs.append(_run_xml(token[1:-1], code=True, vert=vert))
        elif kind == "bold":
            runs.append(_run_xml(token[2:-2], bold=True, vert=vert))
        elif kind == "bolditalic":
            runs.append(_run_xml(token[3:-3], bold=True, italic=True, vert=vert))
        elif kind in ("italicstar", "italicunder"):
            runs.append(_run_xml(token[1:-1], italic=True, vert=vert))
        elif kind == "subopen":
            vert = "sub"
        elif kind == "subclose":
            vert = None
        elif kind == "supopen":
            vert = "sup"
        elif kind == "supclose":
            vert = None
        pos = match.end()
    if pos < len(text):
        runs.append(_run_xml(text[pos:], vert=vert))
    return "".join(r for r in runs if r)


# --------------------------------------------------------------------------
# Block-level paragraph builders.
# --------------------------------------------------------------------------

def paragraph(text, style=None, extra_ppr=""):
    """Build a ``w:p`` paragraph from inline Markdown text."""
    ppr_parts = []
    if style:
        ppr_parts.append('<w:pStyle w:val="%s"/>' % style)
    if extra_ppr:
        ppr_parts.append(extra_ppr)
    ppr = "<w:pPr>%s</w:pPr>" % "".join(ppr_parts) if ppr_parts else ""
    return "<w:p>%s%s</w:p>" % (ppr, inline_runs(text))


def heading_paragraph(text, level):
    """Build a heading paragraph (Heading1..Heading6)."""
    return paragraph(text, style="Heading%d" % level)


def list_paragraph(text, ordered, number):
    """Render a list item as an indented paragraph with a text bullet/number.

    Native numbering (numbering.xml) is intentionally avoided to keep the
    package minimal and robust; a prefixed marker is an accepted rendering.
    """
    marker = ("%d." % number) if ordered else "\u2022"
    indent = '<w:ind w:left="720" w:hanging="360"/>'
    body = _run_xml(marker + " ") + inline_runs(text)
    return "<w:p><w:pPr>%s</w:pPr>%s</w:p>" % (indent, body)


def hr_paragraph():
    """Horizontal rule rendered as a paragraph with a bottom border."""
    ppr = (
        "<w:pPr><w:pBdr>"
        '<w:bottom w:val="single" w:sz="6" w:space="1" w:color="auto"/>'
        "</w:pBdr></w:pPr>"
    )
    return "<w:p>%s</w:p>" % ppr


def blockquote_paragraph(text):
    """Block quote rendered as an indented italic-friendly paragraph."""
    return paragraph(text, extra_ppr='<w:ind w:left="720"/>')


def image_paragraph(rel_id, width_emu, height_emu, doc_pr_id, alt="image"):
    """Build a centred paragraph containing an inline PNG drawing."""
    alt = xml_escape(alt) or "image"
    drawing = (
        "<w:drawing>"
        '<wp:inline distT="0" distB="0" distL="0" distR="0">'
        '<wp:extent cx="%d" cy="%d"/>' % (width_emu, height_emu)
        + '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        '<wp:docPr id="%d" name="%s"/>' % (doc_pr_id, alt)
        + "<wp:cNvGraphicFramePr>"
        '<a:graphicFrameLocks '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'noChangeAspect="1"/>'
        "</wp:cNvGraphicFramePr>"
        '<a:graphic '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData '
        'uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        "<pic:nvPicPr>"
        '<pic:cNvPr id="%d" name="%s"/>' % (doc_pr_id, alt)
        + "<pic:cNvPicPr/>"
        "</pic:nvPicPr>"
        "<pic:blipFill>"
        '<a:blip r:embed="%s"/>' % rel_id
        + "<a:stretch><a:fillRect/></a:stretch>"
        "</pic:blipFill>"
        "<pic:spPr>"
        '<a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
        % (width_emu, height_emu)
        + '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        "</pic:spPr>"
        "</pic:pic>"
        "</a:graphicData>"
        "</a:graphic>"
        "</wp:inline>"
        "</w:drawing>"
    )
    ppr = '<w:pPr><w:jc w:val="center"/></w:pPr>'
    return "<w:p>%s<w:r>%s</w:r></w:p>" % (ppr, drawing)


# --------------------------------------------------------------------------
# Table builder.
# --------------------------------------------------------------------------

def _split_table_row(line):
    """Split a Markdown pipe-table row into cell strings."""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def _is_table_separator(line):
    """True if the line is a pipe-table header/body separator (---|:--:)."""
    stripped = line.strip().strip("|")
    if not stripped:
        return False
    return bool(re.fullmatch(r"[\s:\-|]+", stripped)) and "-" in stripped


def table_xml(rows):
    """Build a ``w:tbl`` element from a list of cell-string lists.

    The first row is rendered bold (header). Columns are evenly distributed
    across the ~9026 twip content width.
    """
    ncols = max(len(r) for r in rows)
    col_width = 9026 // ncols
    grid = "".join('<w:gridCol w:w="%d"/>' % col_width for _ in range(ncols))

    borders = (
        "<w:tblBorders>"
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        "</w:tblBorders>"
    )
    tbl_pr = (
        "<w:tblPr>"
        '<w:tblStyle w:val="TableGrid"/>'
        '<w:tblW w:w="9026" w:type="dxa"/>'
        + borders
        + "<w:tblLook w:val=\"04A0\" w:firstRow=\"1\" w:lastRow=\"0\" "
        "w:firstColumn=\"1\" w:lastColumn=\"0\" w:noHBand=\"0\" "
        "w:noVBand=\"1\"/>"
        "</w:tblPr>"
    )

    body_rows = []
    for r_index, row in enumerate(rows):
        cells = list(row) + [""] * (ncols - len(row))
        is_header = r_index == 0
        cell_xml_parts = []
        for cell in cells:
            cell_ppr = ""
            # Emit bold header text by wrapping cell content.
            content = cell
            if is_header and content and "**" not in content:
                content = "**%s**" % content
            runs = inline_runs(content) or _run_xml("")
            tc_pr = '<w:tcPr><w:tcW w:w="%d" w:type="dxa"/></w:tcPr>' % col_width
            cell_xml_parts.append(
                "<w:tc>%s<w:p>%s%s</w:p></w:tc>" % (tc_pr, cell_ppr, runs)
            )
        row_pr = "<w:trPr><w:tblHeader/></w:trPr>" if is_header else ""
        body_rows.append("<w:tr>%s%s</w:tr>" % (row_pr, "".join(cell_xml_parts)))

    return "<w:tbl>%s<w:tblGrid>%s</w:tblGrid>%s</w:tbl>" % (
        tbl_pr,
        grid,
        "".join(body_rows),
    )


# --------------------------------------------------------------------------
# Markdown parser -> ordered list of block dicts.
# --------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_IMAGE_RE = re.compile(r"^!\[(?P<alt>[^\]]*)\]\((?P<path>[^)]+)\)\s*$")
_ORDERED_RE = re.compile(r"^(\d+)\.\s+(.*)$")
_BULLET_RE = re.compile(r"^[-*]\s+(.*)$")


def parse_markdown(text):
    """Parse Markdown text into an ordered list of block descriptors."""
    lines = text.split("\n")
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Blank line.
        if stripped == "":
            i += 1
            continue

        # Horizontal rule.
        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", stripped):
            blocks.append({"type": "hr"})
            i += 1
            continue

        # Heading.
        m = _HEADING_RE.match(line)
        if m:
            blocks.append(
                {"type": "heading", "level": len(m.group(1)), "text": m.group(2).strip()}
            )
            i += 1
            continue

        # Image.
        m = _IMAGE_RE.match(stripped)
        if m:
            blocks.append(
                {"type": "image", "alt": m.group("alt"), "path": m.group("path").strip()}
            )
            i += 1
            continue

        # Table: current line has a pipe and the next line is a separator.
        if "|" in line and i + 1 < n and _is_table_separator(lines[i + 1]):
            rows = [_split_table_row(line)]
            i += 2  # skip header + separator
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(_split_table_row(lines[i]))
                i += 1
            blocks.append({"type": "table", "rows": rows})
            continue

        # Block quote.
        if stripped.startswith(">"):
            quote_lines = []
            while i < n and lines[i].strip().startswith(">"):
                quote_lines.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            blocks.append({"type": "quote", "text": " ".join(l.strip() for l in quote_lines)})
            continue

        # Ordered list.
        m = _ORDERED_RE.match(stripped)
        if m:
            while i < n and _ORDERED_RE.match(lines[i].strip()):
                mm = _ORDERED_RE.match(lines[i].strip())
                blocks.append(
                    {"type": "list", "ordered": True, "number": int(mm.group(1)), "text": mm.group(2).strip()}
                )
                i += 1
            continue

        # Bullet list.
        m = _BULLET_RE.match(stripped)
        if m:
            while i < n and _BULLET_RE.match(lines[i].strip()):
                mm = _BULLET_RE.match(lines[i].strip())
                blocks.append(
                    {"type": "list", "ordered": False, "number": 0, "text": mm.group(1).strip()}
                )
                i += 1
            continue

        # Paragraph: gather consecutive non-blank, non-structural lines.
        para_lines = [line]
        i += 1
        while i < n:
            nxt = lines[i]
            nxt_stripped = nxt.strip()
            if nxt_stripped == "":
                break
            if _HEADING_RE.match(nxt) or _IMAGE_RE.match(nxt_stripped):
                break
            if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", nxt_stripped):
                break
            if nxt_stripped.startswith(">"):
                break
            if _ORDERED_RE.match(nxt_stripped) or _BULLET_RE.match(nxt_stripped):
                break
            if "|" in nxt and i + 1 < n and _is_table_separator(lines[i + 1]):
                break
            para_lines.append(nxt)
            i += 1
        blocks.append({"type": "paragraph", "text": " ".join(l.strip() for l in para_lines)})
    return blocks


# --------------------------------------------------------------------------
# Package assembly.
# --------------------------------------------------------------------------

CONTENT_TYPES_TMPL = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType='
    '"application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    "%(png_default)s"
    '<Override PartName="/word/document.xml" ContentType='
    '"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType='
    '"application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    "</Types>"
)

RELS_ROOT = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type='
    '"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
    'Target="word/document.xml"/>'
    "</Relationships>"
)

STYLES_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:docDefaults><w:rPrDefault><w:rPr>'
    '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>'
    '<w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
    '<w:name w:val="Normal"/></w:style>'
    + "".join(
        '<w:style w:type="paragraph" w:styleId="Heading%d">'
        '<w:name w:val="heading %d"/><w:basedOn w:val="Normal"/>'
        '<w:pPr><w:keepNext/><w:spacing w:before="%d" w:after="120"/>'
        '<w:outlineLvl w:val="%d"/></w:pPr>'
        '<w:rPr><w:b/><w:sz w:val="%d"/></w:rPr></w:style>'
        % (lvl, lvl, 280 - (lvl - 1) * 20, lvl - 1, 36 - (lvl - 1) * 3)
        for lvl in range(1, 7)
    )
    + '<w:style w:type="table" w:styleId="TableGrid">'
    '<w:name w:val="Table Grid"/><w:tblPr>'
    '<w:tblBorders>'
    '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    "</w:tblBorders></w:tblPr></w:style>"
    "</w:styles>"
)

DOC_OPEN = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    "<w:document "
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
    "<w:body>"
)

SECTION_PR = (
    '<w:sectPr>'
    '<w:pgSz w:w="12240" w:h="15840"/>'
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
    'w:header="720" w:footer="720" w:gutter="0"/>'
    "</w:sectPr>"
)

DOC_CLOSE = "%s</w:body></w:document>" % SECTION_PR


def build_docx(md_path, out_path):
    """Convert ``md_path`` (Markdown) into ``out_path`` (a .docx package)."""
    with open(md_path, "r", encoding="utf-8") as fh:
        text = fh.read()

    base_dir = os.path.dirname(os.path.abspath(md_path))
    blocks = parse_markdown(text)

    body_parts = []
    # image relationships: rel_id -> (media member name, source path)
    images = []
    rel_counter = 1  # rId1 reserved for styles.xml
    doc_pr_counter = 1

    # First relationship is styles.xml.
    rels = [
        '<Relationship Id="rId1" Type='
        '"http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
        'Target="styles.xml"/>'
    ]

    for block in blocks:
        btype = block["type"]
        if btype == "heading":
            body_parts.append(heading_paragraph(block["text"], block["level"]))
        elif btype == "paragraph":
            body_parts.append(paragraph(block["text"]))
        elif btype == "hr":
            body_parts.append(hr_paragraph())
        elif btype == "quote":
            body_parts.append(blockquote_paragraph(block["text"]))
        elif btype == "list":
            body_parts.append(
                list_paragraph(block["text"], block["ordered"], block["number"])
            )
        elif btype == "table":
            body_parts.append(table_xml(block["rows"]))
        elif btype == "image":
            src = os.path.normpath(os.path.join(base_dir, block["path"]))
            if os.path.isfile(src) and block["path"].lower().endswith(".png"):
                rel_counter += 1
                rel_id = "rId%d" % rel_counter
                media_name = "image%d.png" % len(images)
                images.append((media_name, src))
                rels.append(
                    '<Relationship Id="%s" Type='
                    '"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                    'Target="media/%s"/>' % (rel_id, media_name)
                )
                w_emu, h_emu = emu_size_for_png(src)
                doc_pr_counter += 1
                body_parts.append(
                    image_paragraph(
                        rel_id, w_emu, h_emu, doc_pr_counter, alt=block["alt"] or media_name
                    )
                )
            else:
                # Image missing or non-PNG: preserve a reference so nothing is lost.
                body_parts.append(
                    paragraph("[Figure: %s (%s)]" % (block["alt"], block["path"]))
                )

    document_xml = DOC_OPEN + "".join(body_parts) + DOC_CLOSE

    png_default = (
        '<Default Extension="png" ContentType="image/png"/>' if images else ""
    )
    content_types = CONTENT_TYPES_TMPL % {"png_default": png_default}

    doc_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(rels)
        + "</Relationships>"
    )

    # Assemble the ZIP with correct member names (no leading "./").
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", RELS_ROOT)
        zf.writestr("word/document.xml", document_xml)
        zf.writestr("word/styles.xml", STYLES_XML)
        zf.writestr("word/_rels/document.xml.rels", doc_rels)
        for media_name, src in images:
            with open(src, "rb") as img:
                zf.writestr("word/media/%s" % media_name, img.read())

    return out_path


def main(argv):
    if len(argv) == 3:
        pairs = [(argv[1], argv[2])]
    elif len(argv) == 1:
        pairs = [
            ("Response_to_Reviewers.md", "Response_to_Reviewers.docx"),
            (
                "Revised_Tesla_Valve_CFD_Manuscript.md",
                "Revised_Tesla_Valve_CFD_Manuscript.docx",
            ),
        ]
    else:
        sys.stderr.write("usage: python3 md_to_docx.py [INPUT.md OUTPUT.docx]\n")
        return 2

    for md_path, out_path in pairs:
        build_docx(md_path, out_path)
        size = os.path.getsize(out_path)
        print("wrote %s (%d bytes) from %s" % (out_path, size, md_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
