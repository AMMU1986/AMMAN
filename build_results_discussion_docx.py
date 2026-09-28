#!/usr/bin/env python3
"""
Build a Word .docx for the revised Results and Discussion section.
Uses raw OOXML (ZIP + XML) since python-docx is unavailable in this sandbox.
Parses the markdown, rendering:
  - #, ##, ### headings
  - *italic* runs
  - --- horizontal rule (rendered as a bottom-bordered spacer paragraph)
  - paragraphs
"""

import zipfile
import re

MD_PATH = "Results_and_Discussion_Revised.md"
DOCX_PATH = "Results_and_Discussion_Revised.docx"

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

DOC_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr></w:rPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:pPr><w:spacing w:after="160" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="36"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="30"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:pPr><w:spacing w:before="200" w:after="100"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/></w:rPr></w:style>
</w:styles>'''


def xml_escape(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def make_runs(text):
    """Split text on *italic* markers into <w:r> runs."""
    runs = []
    parts = re.split(r'(\*[^*]+\*)', text)
    for p in parts:
        if not p:
            continue
        if p.startswith('*') and p.endswith('*') and len(p) > 2:
            inner = xml_escape(p[1:-1])
            runs.append(f'<w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">{inner}</w:t></w:r>')
        else:
            runs.append(f'<w:r><w:t xml:space="preserve">{xml_escape(p)}</w:t></w:r>')
    return "".join(runs)


def para(text, style=None, italic_para=False):
    ppr = ""
    if style:
        ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
    if italic_para:
        return f'<w:p>{ppr}<w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">{xml_escape(text)}</w:t></w:r></w:p>'
    return f'<w:p>{ppr}{make_runs(text)}</w:p>'


def hr():
    return ('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" '
            'w:color="999999"/></w:pBdr></w:pPr></w:p>')


def build_body(md):
    out = []
    lines = md.split("\n")
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.strip() == "---":
            out.append(hr())
        elif line.startswith("### "):
            out.append(para(line[4:].strip(), style="Heading2"))
        elif line.startswith("## "):
            out.append(para(line[3:].strip(), style="Heading1"))
        elif line.startswith("# "):
            out.append(para(line[2:].strip(), style="Title"))
        else:
            txt = line.strip()
            # A fully-italic line like "*(note...)*"
            if txt.startswith("*(") and txt.endswith(")*"):
                out.append(para(txt[1:-1], italic_para=True))
            else:
                out.append(para(txt))
    return "".join(out)


def main():
    with open(MD_PATH, encoding="utf-8") as f:
        md = f.read()
    body = build_body(md)
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'<w:body>{body}'
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
        '</w:body></w:document>'
    )
    with zipfile.ZipFile(DOCX_PATH, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/document.xml", document)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/styles.xml", STYLES)
    print("Wrote", DOCX_PATH)


if __name__ == "__main__":
    main()
