#!/usr/bin/env python3
"""
Generate a .docx file from the chapter markdown without external dependencies.
A .docx is a ZIP archive containing XML files following the OOXML standard.
"""

import zipfile
import os
import re
from xml.sax.saxutils import escape

INPUT_FILE = "Chapter_Accreditation_Accountability_Learning_Renewal.md"
OUTPUT_FILE = "Chapter_Accreditation_Accountability_Learning_Renewal.docx"

def read_markdown():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def md_to_paragraphs(md_text):
    """Convert markdown text to a list of (style, text) tuples."""
    paragraphs = []
    lines = md_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('# ') and not line.startswith('## '):
            paragraphs.append(('Title', line[2:].strip()))
        elif line.startswith('## '):
            paragraphs.append(('Heading1', line[3:].strip()))
        elif line.startswith('### '):
            paragraphs.append(('Heading2', line[4:].strip()))
        elif line.startswith('**Keywords:'):
            paragraphs.append(('Normal', line.strip()))
        elif line.startswith('---'):
            pass  # skip horizontal rules
        elif line.strip() == '':
            pass  # skip empty lines
        else:
            # Collect paragraph (consecutive non-empty, non-heading lines)
            para_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip() != '' and not lines[i].startswith('#') and not lines[i].startswith('---'):
                para_lines.append(lines[i])
                i += 1
            full_para = ' '.join(l.strip() for l in para_lines)
            paragraphs.append(('Normal', full_para))
            continue
        i += 1
    return paragraphs

def make_run_xml(text):
    """Create run XML, handling bold (**text**) markers."""
    runs = []
    # Split by bold markers
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            inner = escape(part[2:-2])
            runs.append(f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{inner}</w:t></w:r>')
        else:
            escaped = escape(part)
            runs.append(f'<w:r><w:t xml:space="preserve">{escaped}</w:t></w:r>')
    return ''.join(runs)

def make_paragraph_xml(style, text):
    """Create a paragraph XML element."""
    style_map = {
        'Title': 'Title',
        'Heading1': 'Heading1',
        'Heading2': 'Heading2',
        'Normal': 'Normal',
    }
    s = style_map.get(style, 'Normal')
    runs = make_run_xml(text)
    return f'<w:p><w:pPr><w:pStyle w:val="{s}"/></w:pPr>{runs}</w:p>'

def create_docx(paragraphs):
    """Create a .docx file from paragraphs."""
    
    # Content Types
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

    # Relationships
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

    # Word relationships
    word_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

    # Styles
    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="200" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="300"/><w:jc w:val="center"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="400" w:after="200"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="300" w:after="150"/></w:pPr>
  </w:style>
</w:styles>'''

    # Document body
    body_paras = '\n'.join(make_paragraph_xml(s, t) for s, t in paragraphs)
    
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {body_paras}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    # Write the ZIP/docx file
    with zipfile.ZipFile(OUTPUT_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', styles)

    print(f"Created: {OUTPUT_FILE}")
    print(f"Size: {os.path.getsize(OUTPUT_FILE)} bytes")

if __name__ == '__main__':
    md_text = read_markdown()
    paragraphs = md_to_paragraphs(md_text)
    print(f"Parsed {len(paragraphs)} paragraphs")
    create_docx(paragraphs)
