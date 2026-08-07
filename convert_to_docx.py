#!/usr/bin/env python3
"""
Convert Chapter_4_Experimentation.md to a proper .docx file
using only Python standard library (zipfile + XML).
Fonts: Candara 13pt for headings, Book Antiqua 12pt for body.
"""

import zipfile
import os
import re

# --- OOXML boilerplate ---

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
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr>
      <w:rFonts w:ascii="Book Antiqua" w:hAnsi="Book Antiqua"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
    <w:pPr>
      <w:spacing w:after="120" w:line="360" w:lineRule="auto"/>
    </w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="360" w:after="120"/>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Candara" w:hAnsi="Candara"/>
      <w:b/>
      <w:sz w:val="26"/>
      <w:szCs w:val="26"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="240" w:after="120"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Candara" w:hAnsi="Candara"/>
      <w:b/>
      <w:sz w:val="26"/>
      <w:szCs w:val="26"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="200" w:after="100"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Candara" w:hAnsi="Candara"/>
      <w:b/>
      <w:sz w:val="26"/>
      <w:szCs w:val="26"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading4">
    <w:name w:val="heading 4"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="200" w:after="100"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Candara" w:hAnsi="Candara"/>
      <w:b/>
      <w:sz w:val="26"/>
      <w:szCs w:val="26"/>
    </w:rPr>
  </w:style>
</w:styles>'''


def escape_xml(text):
    """Escape XML special characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text


def make_paragraph(text, style=None, bold=False):
    """Create a Word XML paragraph."""
    style_xml = ''
    if style:
        style_xml = f'<w:pStyle w:val="{style}"/>'
    
    ppr = ''
    if style_xml:
        ppr = f'<w:pPr>{style_xml}</w:pPr>'
    
    # Handle bold text markers
    runs = []
    # Split by **bold** markers
    parts = re.split(r'\*\*(.*?)\*\*', text)
    for i, part in enumerate(parts):
        if not part:
            continue
        escaped = escape_xml(part)
        if i % 2 == 1:  # Bold part
            runs.append(f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{escaped}</w:t></w:r>')
        else:
            runs.append(f'<w:r><w:t xml:space="preserve">{escaped}</w:t></w:r>')
    
    run_xml = ''.join(runs)
    return f'<w:p>{ppr}{run_xml}</w:p>'


def md_to_docx_paragraphs(md_text):
    """Convert markdown text to list of Word XML paragraphs."""
    paragraphs = []
    lines = md_text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip HTML comments
        if line.strip().startswith('<!--'):
            while i < len(lines) and '-->' not in lines[i]:
                i += 1
            i += 1
            continue
        
        # Headings
        if line.startswith('#### '):
            text = line[5:].strip()
            paragraphs.append(make_paragraph(text, style='Heading4'))
        elif line.startswith('### '):
            text = line[4:].strip()
            paragraphs.append(make_paragraph(text, style='Heading3'))
        elif line.startswith('## '):
            text = line[3:].strip()
            paragraphs.append(make_paragraph(text, style='Heading2'))
        elif line.startswith('# '):
            text = line[2:].strip()
            paragraphs.append(make_paragraph(text, style='Heading1'))
        elif line.strip().startswith('|') and '|' in line:
            # Table row - convert to simple text paragraph
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if cells and not all(set(c) <= set('- :') for c in cells):
                row_text = ' | '.join(cells)
                paragraphs.append(make_paragraph(row_text))
        elif line.strip() == '':
            # Empty line - skip (spacing handled by paragraph properties)
            pass
        elif line.strip().startswith('- '):
            # List item
            text = line.strip()[2:]
            paragraphs.append(make_paragraph('  • ' + text))
        elif line.strip().startswith('```'):
            # Code block - skip markers, keep content
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                paragraphs.append(make_paragraph('    ' + lines[i]))
                i += 1
        else:
            # Regular paragraph
            text = line.strip()
            if text:
                paragraphs.append(make_paragraph(text))
        
        i += 1
    
    return paragraphs


def create_docx(md_file, docx_file):
    """Create a .docx file from markdown."""
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert MD to paragraphs
    paras = md_to_docx_paragraphs(md_content)
    
    # Build document.xml
    body_content = '\n'.join(paras)
    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {body_content}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>'''
    
    # Create the .docx (ZIP) file
    with zipfile.ZipFile(docx_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', WORD_RELS)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES)
    
    print(f"Created: {docx_file}")
    print(f"Size: {os.path.getsize(docx_file) / 1024:.1f} KB")


if __name__ == '__main__':
    md_file = '/projects/sandbox/AMMAN/Chapter_4_Experimentation.md'
    docx_file = '/projects/sandbox/AMMAN/Chapter_4_Experimentation.docx'
    create_docx(md_file, docx_file)
