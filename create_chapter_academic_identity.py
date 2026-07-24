#!/usr/bin/env python3
"""
Create a Word document (.docx) for the book chapter:
"Academic Identity and Professional Development"
From: Higher Education Beyond Boundaries

Uses only Python standard library (zipfile for docx creation).
Format: Times New Roman, 12pt, double-spaced
Target: ~6,500 words including references
"""

import zipfile
import os

def escape_xml(text):
    """Escape XML special characters."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def create_paragraph_xml(text, style="Normal", bold=False, italic=False):
    """Create a Word XML paragraph with Times New Roman 12pt double-spaced."""
    text = escape_xml(text)
    rpr_parts = []
    if bold:
        rpr_parts.append("<w:b/>")
    if italic:
        rpr_parts.append("<w:i/>")
    if style == "Title":
        rpr_parts.append('<w:sz w:val="32"/><w:szCs w:val="32"/>')
    elif style == "Heading1":
        rpr_parts.append('<w:sz w:val="28"/><w:szCs w:val="28"/>')
    elif style == "Heading2":
        rpr_parts.append('<w:sz w:val="26"/><w:szCs w:val="26"/>')
    elif style == "Heading3":
        rpr_parts.append('<w:sz w:val="24"/><w:szCs w:val="24"/>')
    else:
        rpr_parts.append('<w:sz w:val="24"/><w:szCs w:val="24"/>')
    rpr = ""
    if rpr_parts:
        rpr = "<w:rPr>" + "".join(rpr_parts) + "</w:rPr>"
    ppr_parts = []
    if style == "Title":
        ppr_parts.append('<w:jc w:val="center"/>')
        ppr_parts.append('<w:spacing w:line="480" w:lineRule="auto" w:after="240"/>')
    elif style in ("Heading1", "Heading2", "Heading3"):
        ppr_parts.append('<w:spacing w:line="480" w:lineRule="auto" w:before="240" w:after="120"/>')
    else:
        ppr_parts.append('<w:spacing w:line="480" w:lineRule="auto" w:after="0"/>')
        ppr_parts.append('<w:ind w:firstLine="720"/>')
    ppr = ""
    if ppr_parts:
        ppr = "<w:pPr>" + "".join(ppr_parts) + "</w:pPr>"
    if not text:
        return f"<w:p>{ppr}</w:p>"
    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r></w:p>'


def parse_content_file(filepath):
    """Parse the chapter content text file into (style, text) tuples."""
    content = []
    with open(filepath, "r") as f:
        text = f.read()
    
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#TITLE# "):
            content.append(("Title", line[8:]))
        elif line.startswith("#SUBTITLE# "):
            content.append(("Normal", line[11:]))
        elif line.startswith("#H1# "):
            content.append(("Heading1", line[5:]))
        elif line.startswith("#H2# "):
            content.append(("Heading2", line[5:]))
        elif line.startswith("#H3# "):
            content.append(("Heading3", line[5:]))
        elif line.strip() == "":
            content.append(("Normal", ""))
        else:
            content.append(("Normal", line))
        i += 1
    return content


def build_document_xml(content):
    """Build the complete document.xml from content tuples."""
    paragraphs = []
    for style, text in content:
        bold = style in ("Title", "Heading1", "Heading2", "Heading3")
        italic = style == "Heading3"
        paragraphs.append(create_paragraph_xml(text, style=style, bold=bold, italic=italic))
    
    body_content = "\n    ".join(paragraphs)
    
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {body_content}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>'''
    return document


def create_docx(content_filepath, output_path):
    """Create the .docx file from the content file."""
    content = parse_content_file(content_filepath)
    document_xml = build_document_xml(content)
    
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
</Types>'''

    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

    word_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>'''

    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:pPr>
      <w:spacing w:line="480" w:lineRule="auto" w:after="0"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
  </w:style>
</w:styles>'''

    settings = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:defaultTabStop w:val="720"/>
  <w:compat>
    <w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>
  </w:compat>
</w:settings>'''

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("word/_rels/document.xml.rels", word_rels)
        zf.writestr("word/document.xml", document_xml)
        zf.writestr("word/styles.xml", styles)
        zf.writestr("word/settings.xml", settings)
    
    print(f"Created: {output_path}")
    return content


def count_words(content):
    """Count words in the chapter content."""
    total = 0
    for style, text in content:
        if text:
            total += len(text.split())
    return total


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    content_file = os.path.join(script_dir, "chapter_content.txt")
    output_file = os.path.join(script_dir, "Chapter_Academic_Identity_Professional_Development.docx")
    
    content = create_docx(content_file, output_file)
    word_count = count_words(content)
    print(f"Chapter word count: {word_count}")
    print("Done!")
