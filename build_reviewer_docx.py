#!/usr/bin/env python3
"""Convert the reviewer Markdown files to .docx using only the Python standard
library (no python-docx / pandoc needed). Produces valid Office Open XML.

Supports: # / ## / ### headings, **bold** inline, bullet lists (-),
blockquotes (>), markdown pipe tables, horizontal rules (---).
"""
import os
import re
import zipfile
from xml.sax.saxutils import escape

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr><w:rPr><w:b/><w:sz w:val="36"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:pPr><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="30"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:pPr><w:spacing w:before="200" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:pPr><w:spacing w:before="160" w:after="80"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:i/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Quote"><w:name w:val="Quote"/><w:pPr><w:ind w:left="360"/></w:pPr><w:rPr><w:i/><w:color w:val="555555"/></w:rPr></w:style>
</w:styles>"""


def runs_from_inline(text):
    """Split **bold** segments into runs."""
    out = []
    parts = re.split(r"(\*\*.+?\*\*)", text)
    for p in parts:
        if not p:
            continue
        if p.startswith("**") and p.endswith("**"):
            inner = escape(p[2:-2])
            out.append('<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % inner)
        else:
            out.append('<w:r><w:t xml:space="preserve">%s</w:t></w:r>' % escape(p))
    return "".join(out)


def para(text, style=None, bullet=False):
    ppr = ""
    props = []
    if style:
        props.append('<w:pStyle w:val="%s"/>' % style)
    if bullet:
        props.append('<w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>')
        props.append('<w:ind w:left="360" w:hanging="180"/>')
    if props:
        ppr = "<w:pPr>%s</w:pPr>" % "".join(props)
    prefix = "\u2022  " if bullet else ""
    inline = runs_from_inline(prefix + text) if prefix else runs_from_inline(text)
    return "<w:p>%s%s</w:p>" % (ppr, inline)


def table_xml(rows):
    borders = ('<w:tblBorders>'
               + ''.join('<w:%s w:val="single" w:sz="4" w:space="0" w:color="999999"/>' % b
                         for b in ["top", "left", "bottom", "right", "insideH", "insideV"])
               + '</w:tblBorders>')
    tbl = ['<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/>%s</w:tblPr>' % borders]
    for ri, row in enumerate(rows):
        tbl.append("<w:tr>")
        for cell in row:
            shade = '<w:shd w:val="clear" w:fill="E7E6E6"/>' if ri == 0 else ''
            cell_runs = runs_from_inline(cell.strip())
            if ri == 0:
                # bold header
                cell_runs = '<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % escape(cell.strip())
            tbl.append('<w:tc><w:tcPr><w:tcW w:w="0" w:type="auto"/>%s</w:tcPr><w:p>%s</w:p></w:tc>' % (shade, cell_runs))
        tbl.append("</w:tr>")
    tbl.append("</w:tbl>")
    # empty paragraph after table (required by Word)
    tbl.append("<w:p/>")
    return "".join(tbl)


def md_to_body(md):
    lines = md.split("\n")
    body = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip("\n")
        stripped = line.strip()

        # table block
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\|[\s:|-]+\|?$", lines[i + 1].strip()):
            rows = []
            header = [c for c in stripped.strip("|").split("|")]
            rows.append(header)
            i += 2  # skip header + separator
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c for c in lines[i].strip().strip("|").split("|")])
                i += 1
            body.append(table_xml(rows))
            continue

        if not stripped:
            i += 1
            continue

        if stripped.startswith("### "):
            body.append(para(stripped[4:], style="Heading3"))
        elif stripped.startswith("## "):
            body.append(para(stripped[3:], style="Heading2"))
        elif stripped.startswith("# "):
            # first H1 becomes Title, rest Heading1
            style = "Title" if not any('w:pStyle w:val="Title"' in b for b in body) else "Heading1"
            body.append(para(stripped[2:], style=style))
        elif stripped.startswith("> "):
            body.append(para(stripped[2:], style="Quote"))
        elif re.match(r"^[-*]{3,}$", stripped):
            body.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="AAAAAA"/></w:pBdr></w:pPr></w:p>')
        elif stripped.startswith("- ") or stripped.startswith("* "):
            body.append(para(stripped[2:], bullet=True))
        elif re.match(r"^\d+\.\s", stripped):
            body.append(para(stripped, bullet=True))
        else:
            body.append(para(stripped))
        i += 1
    return "".join(body)


def build_docx(md_path, docx_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md = f.read()
    body = md_to_body(md)
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                '<w:body>%s'
                '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
                '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
                '</w:body></w:document>') % body
    with zipfile.ZipFile(docx_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/document.xml", document)
    print("Wrote", docx_path)


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    build_docx(os.path.join(base, "Revised_Manuscript_Dissimilar_Weld.md"),
               os.path.join(base, "Revised_Manuscript_Dissimilar_Weld.docx"))
    build_docx(os.path.join(base, "Response_to_Reviewers_Dissimilar_Weld.md"),
               os.path.join(base, "Response_to_Reviewers_Dissimilar_Weld.docx"))
