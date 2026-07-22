#!/usr/bin/env python3
"""
Create a Word document (.docx) for the chapter:
"Differential Equations and Dynamical Systems in Biology"
Uses only Python standard library (zipfile-based DOCX creation).
"""

import zipfile
import os
import re
from xml.sax.saxutils import escape


def create_docx_from_markdown(md_path, output_path):
    """Create a DOCX file from markdown content using raw XML."""
    
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Parse markdown into structured elements
    elements = parse_markdown(md_content)
    
    # Generate document.xml body content
    body_xml = generate_body_xml(elements)
    
    # Create the DOCX zip file
    write_docx(output_path, body_xml)
    print(f"Successfully created: {output_path}")


def parse_markdown(content):
    """Parse markdown into a list of elements (headings, paragraphs)."""
    elements = []
    lines = content.split('\n')
    i = 0
    paragraph_buffer = []
    
    while i < len(lines):
        line = lines[i]
        
        # Flush paragraph buffer if we hit a special line
        if line.strip() == '' or line.startswith('#') or line.strip() == '---':
            if paragraph_buffer:
                text = ' '.join(paragraph_buffer)
                elements.append(('paragraph', text))
                paragraph_buffer = []
        
        if line.strip() == '---':
            i += 1
            continue
        elif line.strip() == '':
            i += 1
            continue
        elif line.startswith('####'):
            elements.append(('heading4', line.lstrip('#').strip()))
        elif line.startswith('###'):
            elements.append(('heading3', line.lstrip('#').strip()))
        elif line.startswith('##'):
            elements.append(('heading2', line.lstrip('#').strip()))
        elif line.startswith('#'):
            elements.append(('heading1', line.lstrip('#').strip()))
        elif line.startswith('*') and line.endswith('*') and not line.startswith('**'):
            elements.append(('italic', line.strip('*').strip()))
        else:
            paragraph_buffer.append(line.strip())
        
        i += 1
    
    # Flush remaining buffer
    if paragraph_buffer:
        text = ' '.join(paragraph_buffer)
        elements.append(('paragraph', text))
    
    return elements


def generate_body_xml(elements):
    """Generate the XML body content for the document."""
    body_parts = []
    
    for elem_type, text in elements:
        escaped_text = escape(text)
        
        if elem_type == 'heading1':
            body_parts.append(f'''<w:p>
  <w:pPr><w:pStyle w:val="Heading1"/><w:spacing w:before="240" w:after="120"/></w:pPr>
  <w:r><w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr><w:t>{escaped_text}</w:t></w:r>
</w:p>''')
        elif elem_type == 'heading2':
            body_parts.append(f'''<w:p>
  <w:pPr><w:pStyle w:val="Heading2"/><w:spacing w:before="200" w:after="100"/></w:pPr>
  <w:r><w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr><w:t>{escaped_text}</w:t></w:r>
</w:p>''')
        elif elem_type == 'heading3':
            body_parts.append(f'''<w:p>
  <w:pPr><w:pStyle w:val="Heading3"/><w:spacing w:before="160" w:after="80"/></w:pPr>
  <w:r><w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr><w:t>{escaped_text}</w:t></w:r>
</w:p>''')
        elif elem_type == 'heading4':
            body_parts.append(f'''<w:p>
  <w:pPr><w:pStyle w:val="Heading4"/><w:spacing w:before="120" w:after="60"/></w:pPr>
  <w:r><w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:t>{escaped_text}</w:t></w:r>
</w:p>''')
        elif elem_type == 'italic':
            body_parts.append(f'''<w:p>
  <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="120"/></w:pPr>
  <w:r><w:rPr><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:t>{escaped_text}</w:t></w:r>
</w:p>''')
        elif elem_type == 'paragraph':
            body_parts.append(f'''<w:p>
  <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:ind w:firstLine="720"/><w:jc w:val="both"/></w:pPr>
  <w:r><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:t xml:space="preserve">{escaped_text}</w:t></w:r>
</w:p>''')
    
    return '\n'.join(body_parts)


def write_docx(output_path, body_xml):
    """Write a complete DOCX file."""
    
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
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:pPr><w:spacing w:before="160" w:after="80"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading4">
    <w:name w:val="heading 4"/>
    <w:pPr><w:spacing w:before="120" w:after="60"/></w:pPr>
    <w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
</w:styles>'''
    
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{body_xml}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800"/>
    </w:sectPr>
  </w:body>
</w:document>'''
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', styles)


if __name__ == '__main__':
    md_path = 'Chapter_Differential_Equations_Dynamical_Systems_Biology.md'
    output_path = 'Chapter_Differential_Equations_Dynamical_Systems_Biology.docx'
    create_docx_from_markdown(md_path, output_path)
