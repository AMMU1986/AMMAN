#!/usr/bin/env python3
"""
Create a Word document (.docx) from the Response to Reviewers markdown file.
Uses only the Python standard library (zipfile for docx). No third-party deps.
Modeled on create_manuscript_docx.py (escape_xml / create_paragraph_xml /
markdown_to_docx_xml / styles.xml).
"""

import zipfile
import re

INPUT_MD = '/projects/sandbox/AMMAN/Response_to_Reviewers.md'
OUTPUT_DOCX = '/projects/sandbox/AMMAN/Response_to_Reviewers.docx'


def read_response():
    """Read the markdown response letter."""
    with open(INPUT_MD, 'r') as f:
        return f.read()


def escape_xml(text):
    """Escape XML special characters."""
    return (text.replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def create_paragraph_xml(text, style='Normal', bold=False, size=24):
    """Create a Word XML paragraph."""
    text = escape_xml(text)

    rpr = ''
    if bold:
        rpr = '<w:rPr><w:b/></w:rPr>'
    if size != 24:
        if bold:
            rpr = f'<w:rPr><w:b/><w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'
        else:
            rpr = f'<w:rPr><w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'

    ppr = ''
    if style == 'Heading1':
        ppr = '<w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
    elif style == 'Heading2':
        ppr = '<w:pPr><w:pStyle w:val="Heading2"/></w:pPr>'
    elif style == 'Heading3':
        ppr = '<w:pPr><w:pStyle w:val="Heading3"/></w:pPr>'
    elif style == 'Title':
        ppr = '<w:pPr><w:pStyle w:val="Title"/><w:jc w:val="center"/></w:pPr>'

    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r></w:p>'


def create_runs_xml(text):
    """Create a Normal paragraph supporting inline **bold** runs."""
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    runs = ''
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            inner = escape_xml(part[2:-2])
            runs += (f'<w:r><w:rPr><w:b/></w:rPr>'
                     f'<w:t xml:space="preserve">{inner}</w:t></w:r>')
        else:
            runs += (f'<w:r><w:t xml:space="preserve">'
                     f'{escape_xml(part)}</w:t></w:r>')
    return f'<w:p>{runs}</w:p>'


def markdown_to_docx_xml(md_text):
    """Convert markdown text to Word XML paragraphs."""
    paragraphs = []
    lines = md_text.split('\n')

    for line in lines:
        line = line.rstrip()

        if not line:
            paragraphs.append('<w:p/>')
            continue

        # Title (# heading)
        if line.startswith('# ') and not line.startswith('## '):
            text = line[2:].strip()
            paragraphs.append(create_paragraph_xml(text, style='Title', bold=True, size=32))
        # Section heading (##)
        elif line.startswith('## ') and not line.startswith('### '):
            text = line[3:].strip()
            paragraphs.append(create_paragraph_xml(text, style='Heading1', bold=True, size=28))
        # Subsection (###) - also handles #### (comment 6a-6d)
        elif line.startswith('#### '):
            text = line[5:].strip()
            paragraphs.append(create_paragraph_xml(text, style='Heading3', bold=True, size=24))
        elif line.startswith('### '):
            text = line[4:].strip()
            paragraphs.append(create_paragraph_xml(text, style='Heading2', bold=True, size=24))
        # Horizontal rule
        elif line.startswith('---'):
            paragraphs.append('<w:p/>')
        # Bold-only line (e.g. **Manuscript title...**)
        elif line.startswith('**') and line.endswith('**') and line.count('**') == 2:
            text = line.strip('*').strip()
            paragraphs.append(create_paragraph_xml(text, bold=True))
        # Lines with inline bold (e.g. **Comment:** ..., **Response:** ...,
        # list items with a bold label) -> preserve bold runs
        elif '**' in line:
            # keep list bullet/number prefix as plain text
            paragraphs.append(create_runs_xml(line))
        # Regular text
        else:
            paragraphs.append(create_paragraph_xml(line))

    return '\n'.join(paragraphs)


def create_docx(output_path):
    """Create a .docx file from the response markdown."""

    md_text = read_response()
    body_content = markdown_to_docx_xml(md_text)

    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

    word_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="360" w:after="120"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="120" w:after="60"/></w:pPr>
  </w:style>
</w:styles>'''

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

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', styles)

    print(f"  Created {output_path}")


if __name__ == '__main__':
    print("Creating Response to Reviewers Word document...")
    create_docx(OUTPUT_DOCX)
    print("\nDone! File created:")
    print("  - Response_to_Reviewers.docx")
