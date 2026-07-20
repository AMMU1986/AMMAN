#!/usr/bin/env python3
"""
Generate a Word .docx file for APA-style references with DOIs.
Uses only Python standard library (zipfile + xml).
"""

import zipfile
import os
from xml.sax.saxutils import escape

INPUT_FILE = "/projects/sandbox/AMMAN/References_APA_with_DOI.md"
OUTPUT_FILE = "/projects/sandbox/AMMAN/References_APA_with_DOI.docx"

# Read the markdown file
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Parse into elements
elements = []
for line in lines:
    stripped = line.rstrip("\n")
    if stripped.startswith("# "):
        elements.append(("heading1", stripped[2:].strip()))
    elif stripped == "":
        elements.append(("empty", ""))
    else:
        elements.append(("paragraph", stripped))

# Build document.xml paragraphs
def make_paragraph_with_italic(text, style=None, bold=False, font_size=24):
    """Create paragraph with italic support for text between * markers."""
    pPr = ""
    if style:
        pPr_inner = f'<w:pStyle w:val="{style}"/>'
        if style == "Heading1":
            pPr_inner += '<w:jc w:val="center"/>'
        pPr = f'<w:pPr>{pPr_inner}</w:pPr>'
    else:
        pPr = '<w:pPr><w:spacing w:after="240" w:line="480" w:lineRule="auto"/><w:ind w:left="720" w:hanging="720"/></w:pPr>'
    
    # Split text by italic markers
    import re
    parts = re.split(r'(\*[^*]+\*)', text)
    
    runs = ""
    for part in parts:
        if part.startswith('*') and part.endswith('*') and len(part) > 2:
            # Italic text
            inner = part[1:-1]
            escaped = escape(inner)
            rPr = "<w:rPr>"
            rPr += '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
            rPr += "<w:i/>"
            if bold:
                rPr += "<w:b/>"
            rPr += f'<w:sz w:val="{font_size}"/>'
            rPr += "</w:rPr>"
            runs += f'<w:r>{rPr}<w:t xml:space="preserve">{escaped}</w:t></w:r>'
        else:
            if part:
                escaped = escape(part)
                rPr = "<w:rPr>"
                rPr += '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
                if bold:
                    rPr += "<w:b/>"
                rPr += f'<w:sz w:val="{font_size}"/>'
                rPr += "</w:rPr>"
                runs += f'<w:r>{rPr}<w:t xml:space="preserve">{escaped}</w:t></w:r>'
    
    return f'<w:p>{pPr}{runs}</w:p>'

def make_empty_paragraph():
    return '<w:p><w:pPr><w:spacing w:after="0"/></w:pPr></w:p>'

# Build body content
body_content = []
for elem_type, text in elements:
    if elem_type == "heading1":
        body_content.append(make_paragraph_with_italic(text, style="Heading1", bold=True, font_size=28))
    elif elem_type == "empty":
        body_content.append(make_empty_paragraph())
    elif elem_type == "paragraph":
        body_content.append(make_paragraph_with_italic(text, font_size=24))

body_xml = "\n".join(body_content)

# XML templates
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

DOCUMENT_XML = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
            xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
            xmlns:o="urn:schemas-microsoft-com:office:office"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
            xmlns:v="urn:schemas-microsoft-com:vml"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:w10="urn:schemas-microsoft-com:office:word"
            xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
            mc:Ignorable="w14 wp14">
  <w:body>
{body_xml}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

STYLES_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="24"/>
    </w:rPr>
    <w:pPr>
      <w:spacing w:after="240" w:line="480" w:lineRule="auto"/>
    </w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="480" w:after="240"/>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="28"/>
    </w:rPr>
  </w:style>
</w:styles>'''

# Create the .docx file
with zipfile.ZipFile(OUTPUT_FILE, 'w', zipfile.ZIP_DEFLATED) as docx:
    docx.writestr('[Content_Types].xml', CONTENT_TYPES)
    docx.writestr('_rels/.rels', RELS)
    docx.writestr('word/_rels/document.xml.rels', WORD_RELS)
    docx.writestr('word/document.xml', DOCUMENT_XML)
    docx.writestr('word/styles.xml', STYLES_XML)

file_size = os.path.getsize(OUTPUT_FILE)
print(f"Successfully created: {OUTPUT_FILE}")
print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
