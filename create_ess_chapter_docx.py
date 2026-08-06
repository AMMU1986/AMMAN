#!/usr/bin/env python3
"""
Create a Word document (.docx) for the ESS chapter.
Uses only Python standard library (zipfile for docx format).
"""
import zipfile
import re
import os


def escape_xml(text):
    """Escape XML special characters."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def create_paragraph_xml(text, style='Normal', bold=False, italic=False, size=24):
    """Create a Word XML paragraph."""
    text = escape_xml(text)
    rpr_parts = []
    if bold:
        rpr_parts.append('<w:b/>')
    if italic:
        rpr_parts.append('<w:i/>')
    if size != 24:
        rpr_parts.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    rpr = f'<w:rPr>{"".join(rpr_parts)}</w:rPr>' if rpr_parts else ''

    ppr = ''
    if style == 'Heading1':
        ppr = '<w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
    elif style == 'Heading2':
        ppr = '<w:pPr><w:pStyle w:val="Heading2"/></w:pPr>'
    elif style == 'Heading3':
        ppr = '<w:pPr><w:pStyle w:val="Heading3"/></w:pPr>'
    elif style == 'Title':
        ppr = '<w:pPr><w:pStyle w:val="Title"/><w:jc w:val="center"/></w:pPr>'
    elif style == 'Subtitle':
        ppr = '<w:pPr><w:jc w:val="center"/></w:pPr>'

    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r></w:p>'



def markdown_to_docx_xml(md_text):
    """Convert markdown text to Word XML paragraphs."""
    paragraphs = []
    lines = md_text.split('\n')

    in_table = False
    table_rows = []

    for line in lines:
        line = line.rstrip()

        # Skip empty lines
        if not line:
            if in_table and table_rows:
                for row in table_rows:
                    paragraphs.append(create_paragraph_xml(row, size=20))
                table_rows = []
                in_table = False
            paragraphs.append('<w:p/>')
            continue

        # Table detection
        if '|' in line and line.strip().startswith('|'):
            in_table = True
            if re.match(r'^\|[\s\-:|]+\|$', line):
                continue
            table_rows.append(line)
            continue
        elif in_table:
            for row in table_rows:
                paragraphs.append(create_paragraph_xml(row, size=20))
            table_rows = []
            in_table = False

        # Title (# heading)
        if line.startswith('# ') and not line.startswith('## '):
            text = line[2:].strip()
            paragraphs.append(create_paragraph_xml(text, style='Title', bold=True, size=32))
        # Section heading (##)
        elif line.startswith('## ') and not line.startswith('### '):
            text = line[3:].strip()
            paragraphs.append(create_paragraph_xml(text, style='Heading1', bold=True, size=28))
        # Subsection (###)
        elif line.startswith('### '):
            text = line[4:].strip()
            paragraphs.append(create_paragraph_xml(text, style='Heading2', bold=True, size=24))
        # Horizontal rule
        elif line.startswith('---'):
            paragraphs.append('<w:p/>')
        # Math equations ($$...$$)
        elif line.startswith('$$'):
            text = line.strip('$').strip()
            paragraphs.append(create_paragraph_xml(text, italic=True, size=22))
        # Bold text lines
        elif line.startswith('**') and line.endswith('**'):
            text = line.strip('*').strip()
            paragraphs.append(create_paragraph_xml(text, bold=True))
        # Bullet points
        elif line.startswith('- ') or line.startswith('* '):
            text = line[2:].strip()
            clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
            clean = re.sub(r'\*([^*]+)\*', r'\1', clean)
            paragraphs.append(create_paragraph_xml(f"  \u2022  {clean}"))
        # Numbered items
        elif re.match(r'^\d+\.', line):
            clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
            clean = re.sub(r'\*([^*]+)\*', r'\1', clean)
            paragraphs.append(create_paragraph_xml(clean))
        # Regular text
        else:
            clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
            clean = re.sub(r'\*([^*]+)\*', r'\1', clean)
            clean = re.sub(r'\$([^$]+)\$', r'\1', clean)
            paragraphs.append(create_paragraph_xml(clean))

    if table_rows:
        for row in table_rows:
            paragraphs.append(create_paragraph_xml(row, size=20))

    return '\n'.join(paragraphs)



def create_docx(input_md, output_path):
    """Create a .docx file from the chapter markdown."""

    with open(input_md, 'r') as f:
        md_text = f.read()

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

    file_size = os.path.getsize(output_path)
    print(f"Created: {output_path} ({file_size / 1024:.1f} KB)")


if __name__ == '__main__':
    input_file = '/projects/sandbox/AMMAN/Chapter_Optimal_Sizing_Placement_ESS_HRES.md'
    output_file = '/projects/sandbox/AMMAN/Chapter_Optimal_Sizing_Placement_ESS_HRES.docx'
    create_docx(input_file, output_file)
