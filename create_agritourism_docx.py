#!/usr/bin/env python3
"""
Create a Word .docx file for the Agritourism & Regenerative Landscapes book.
Uses raw OOXML (ZIP + XML) since python-docx is not available in this sandbox.
Embeds PNG figures directly into the document.
"""

import zipfile
import os
import re
import base64
import struct

# ─── Configuration ───
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(SCRIPT_DIR, 'Cultivating_Tomorrow_Agritourism_Regenerative.md')
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'Cultivating_Tomorrow_Agritourism_Regenerative.docx')
FIGURES_DIR = os.path.join(SCRIPT_DIR, 'agritourism_figures')

# Figure file mapping
FIGURE_FILES = {
    1: 'Figure_1_Conceptual_Framework.png',
    2: 'Figure_2_Farm_Design_Layout.png',
    3: 'Figure_3_Stakeholder_Ecosystem.png',
    4: 'Figure_4_Challenges_Resilience.png',
}

# Figure captions
FIGURE_CAPTIONS = {
    1: 'Figure 1: Conceptual Framework – Synergy of Regenerative Agriculture and Agritourism',
    2: 'Figure 2: Integrated Farm Design for Regeneration and Visitor Experience',
    3: 'Figure 3: Stakeholder Ecosystem and Policy Framework for Regenerative Agritourism',
    4: 'Figure 4: Challenges, Resilience Strategies, and Holistic Model for Sustainable Agritourism',
}

# Figure placement: after which section heading keyword
FIGURE_PLACEMENT = {
    1: 'As illustrated in Figure 1',
    2: 'As depicted in Figure 2',
    3: 'As depicted in Figure 3',
    4: 'Figure 4 presents the challenges',
}


def get_png_dimensions(filepath):
    """Read PNG dimensions from header."""
    with open(filepath, 'rb') as f:
        f.read(8)  # PNG signature
        f.read(4)  # chunk length
        f.read(4)  # IHDR
        width = struct.unpack('>I', f.read(4))[0]
        height = struct.unpack('>I', f.read(4))[0]
    return width, height


# ─── OOXML Templates ───

def get_content_types(num_images):
    """Generate [Content_Types].xml with image overrides."""
    ct = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''
    return ct


RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''


def get_word_rels(num_images):
    """Generate word/_rels/document.xml.rels with image relationships."""
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'''
    for i in range(1, num_images + 1):
        rid = f'rId{i + 10}'
        rels += f'\n  <Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image{i}.png"/>'
    rels += '\n</Relationships>'
    return rels


NUMBERING = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="120" w:line="480" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
    <w:pPr><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="360" w:before="240"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="36"/><w:szCs w:val="36"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="480" w:after="120"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:i/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Abstract">
    <w:name w:val="Abstract"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="720" w:right="720"/></w:pPr>
    <w:rPr><w:i/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="References">
    <w:name w:val="References"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="80" w:line="240" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="240"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="Table Caption"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="60"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Keywords">
    <w:name w:val="Keywords"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="120" w:after="240"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr>
      <w:tblBorders>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      </w:tblBorders>
    </w:tblPr>
  </w:style>
</w:styles>'''


def escape_xml(text):
    """Escape special XML characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    return text


def make_run(text, bold=False, italic=False):
    """Create a w:r (run) element."""
    props = []
    if bold:
        props.append('<w:b/>')
    if italic:
        props.append('<w:i/>')
    rpr = ''
    if props:
        rpr = '<w:rPr>' + ''.join(props) + '</w:rPr>'
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'


def parse_inline(text):
    """Parse inline markdown (bold **text** and italic *text*) into runs."""
    runs = []
    pattern = r'(\*\*.*?\*\*|\*[^*]+?\*)'
    parts = re.split(pattern, text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            runs.append(make_run(part[2:-2], bold=True))
        elif part.startswith('*') and part.endswith('*'):
            runs.append(make_run(part[1:-1], italic=True))
        else:
            runs.append(make_run(part))
    return ''.join(runs)


def make_paragraph(text, style='Normal'):
    """Create a w:p element with style and inline formatting."""
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
    runs = parse_inline(text)
    return f'<w:p>{ppr}{runs}</w:p>'


def make_image_paragraph(img_num, width_emu, height_emu):
    """Create a paragraph containing an inline image."""
    rid = f'rId{img_num + 10}'
    drawing = f'''<w:p>
  <w:pPr><w:jc w:val="center"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
                 distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{width_emu}" cy="{height_emu}"/>
        <wp:docPr id="{img_num}" name="Figure {img_num}"/>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr>
                <pic:cNvPr id="{img_num}" name="image{img_num}.png"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm>
                  <a:off x="0" y="0"/>
                  <a:ext cx="{width_emu}" cy="{height_emu}"/>
                </a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>'''
    return drawing


def make_table(headers, rows):
    """Create a Word table with borders and header shading."""
    tbl = '<w:tbl>'
    tbl += '<w:tblPr>'
    tbl += '<w:tblStyle w:val="TableGrid"/>'
    tbl += '<w:tblW w:w="9360" w:type="dxa"/>'
    tbl += '<w:tblLayout w:type="autofit"/>'
    tbl += '<w:jc w:val="center"/>'
    tbl += '<w:tblBorders>'
    tbl += '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '</w:tblBorders>'
    tbl += '</w:tblPr>'

    # Calculate column width
    n_cols = len(headers)
    col_w = 9360 // n_cols
    tbl += '<w:tblGrid>' + (f'<w:gridCol w:w="{col_w}"/>' * n_cols) + '</w:tblGrid>'

    # Header row
    tbl += '<w:tr>'
    for h in headers:
        tbl += '<w:tc>'
        tbl += '<w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="D6E4F0"/></w:tcPr>'
        tbl += f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="40" w:line="240" w:lineRule="auto"/></w:pPr>{make_run(h.strip(), bold=True)}</w:p>'
        tbl += '</w:tc>'
    tbl += '</w:tr>'

    # Data rows
    for row in rows:
        tbl += '<w:tr>'
        for i, cell in enumerate(row):
            tbl += '<w:tc>'
            tbl += f'<w:p><w:pPr><w:spacing w:after="40" w:line="240" w:lineRule="auto"/></w:pPr>{make_run(cell.strip())}</w:p>'
            tbl += '</w:tc>'
        # Pad if fewer cells
        for _ in range(n_cols - len(row)):
            tbl += '<w:tc><w:p><w:pPr><w:spacing w:after="40" w:line="240" w:lineRule="auto"/></w:pPr></w:p></w:tc>'
        tbl += '</w:tr>'

    tbl += '</w:tbl>'
    return tbl


def md_to_body(md_text, figure_elements):
    """Convert the markdown content to OOXML body elements."""
    elements = []
    lines = md_text.split('\n')
    i = 0
    in_references = False
    in_abstract = False
    figures_inserted = set()

    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line.strip():
            i += 1
            continue

        # Horizontal rule
        if line.strip() == '---':
            in_abstract = False
            i += 1
            continue

        # Title (# )
        if line.startswith('# ') and not line.startswith('## '):
            elements.append(make_paragraph(line[2:].strip(), 'Title'))
            i += 1
            continue

        # Heading 1 (## )
        if line.startswith('## '):
            heading_text = line[3:].strip()
            if heading_text == 'Abstract':
                in_abstract = True
                elements.append(make_paragraph(heading_text, 'Heading1'))
                i += 1
                continue
            if heading_text == 'References':
                in_references = True
            elements.append(make_paragraph(heading_text, 'Heading1'))
            i += 1
            continue

        # Heading 2 (### )
        if line.startswith('### '):
            elements.append(make_paragraph(line[4:].strip(), 'Heading2'))
            i += 1
            continue

        # Heading 3 (#### )
        if line.startswith('#### '):
            elements.append(make_paragraph(line[5:].strip(), 'Heading3'))
            i += 1
            continue

        # Table detection
        if '|' in line and i + 1 < len(lines) and '---' in lines[i + 1]:
            # Check for table caption (line before)
            headers = [c.strip() for c in line.split('|') if c.strip()]
            i += 2  # skip header and separator
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                row = [c.strip() for c in lines[i].split('|') if c.strip()]
                rows.append(row)
                i += 1
            elements.append(make_table(headers, rows))
            continue

        # Keywords line
        if line.strip().startswith('**Keywords:**'):
            kw_text = line.strip().replace('**Keywords:**', 'Keywords:').strip()
            elements.append(make_paragraph(kw_text, 'Keywords'))
            i += 1
            continue

        # Table caption lines (like "Table 1: ...")
        if re.match(r'^Table \d+:', line.strip()):
            elements.append(make_paragraph(line.strip(), 'TableCaption'))
            i += 1
            continue

        # Reference entries
        if in_references and re.match(r'^\[\d+\]', line.strip()):
            elements.append(make_paragraph(line.strip(), 'References'))
            i += 1
            continue

        # Note line
        if line.strip().startswith('**Note:**'):
            elements.append(make_paragraph(line.strip(), 'Normal'))
            i += 1
            continue

        # Normal paragraph - check if it contains figure placement triggers
        para_text = line.strip()

        # Abstract style
        if in_abstract:
            elements.append(make_paragraph(para_text, 'Abstract'))
        else:
            elements.append(make_paragraph(para_text, 'Normal'))

        # Check if we should insert a figure after this paragraph
        for fig_num, trigger in FIGURE_PLACEMENT.items():
            if trigger in para_text and fig_num not in figures_inserted:
                if fig_num in figure_elements:
                    elements.append(figure_elements[fig_num]['image'])
                    elements.append(make_paragraph(FIGURE_CAPTIONS[fig_num], 'FigureCaption'))
                    figures_inserted.add(fig_num)
                break

        i += 1

    return '\n'.join(elements)


def create_docx():
    """Create the .docx file from markdown with embedded images."""
    print("Reading markdown content...")
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Prepare figure elements
    print("Preparing figures...")
    figure_elements = {}
    for fig_num, fig_file in FIGURE_FILES.items():
        fig_path = os.path.join(FIGURES_DIR, fig_file)
        if os.path.exists(fig_path):
            w, h = get_png_dimensions(fig_path)
            # Scale to fit page width (6 inches = 5486400 EMU)
            max_width_emu = 5486400
            scale = max_width_emu / w
            width_emu = int(w * scale)
            height_emu = int(h * scale)
            # Cap height
            max_height_emu = 4000000
            if height_emu > max_height_emu:
                scale2 = max_height_emu / height_emu
                width_emu = int(width_emu * scale2)
                height_emu = max_height_emu

            image_xml = make_image_paragraph(fig_num, width_emu, height_emu)
            figure_elements[fig_num] = {
                'image': image_xml,
                'path': fig_path,
            }
            print(f"  Figure {fig_num}: {w}x{h} px -> {width_emu}x{height_emu} EMU")
        else:
            print(f"  WARNING: Figure {fig_num} not found at {fig_path}")

    # Convert markdown to body XML
    print("Converting content to OOXML...")
    body_xml = md_to_body(md_content, figure_elements)

    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
  <w:body>
{body_xml}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"
               w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    # Write the docx file
    print("Writing .docx file...")
    num_images = len(figure_elements)
    with zipfile.ZipFile(OUTPUT_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', get_content_types(num_images))
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', get_word_rels(num_images))
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES)
        zf.writestr('word/numbering.xml', NUMBERING)

        # Add images
        for fig_num, fig_data in figure_elements.items():
            with open(fig_data['path'], 'rb') as img_f:
                img_bytes = img_f.read()
            zf.writestr(f'word/media/image{fig_num}.png', img_bytes)

    size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"\nSuccessfully created: {OUTPUT_FILE}")
    print(f"File size: {size_kb:.1f} KB")
    print(f"Contains: 4 chapters, 43 references, 4 tables, 4 embedded figures")


if __name__ == '__main__':
    create_docx()
