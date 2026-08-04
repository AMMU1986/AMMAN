#!/usr/bin/env python3
"""
Generate a properly formatted .docx file for the book chapter:
'AI for Electric Vehicles and Charging Infrastructure'

Requirements:
- 11pt Times New Roman font
- Proper heading hierarchy
- Embedded figures at 300 DPI
- Tables with borders
- References section
- No external dependencies (pure Python using zipfile + XML)

A .docx file is a ZIP archive with Office Open XML content.
"""

import zipfile
import os
import struct
import base64
import re
from xml.sax.saxutils import escape

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(SCRIPT_DIR, "Chapter_AI_Electric_Vehicles_Charging.md")
FIG_DIR = os.path.join(SCRIPT_DIR, "ev_chapter_figures")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "Chapter_AI_Electric_Vehicles_Charging.docx")


# ============================================================
# OOXML Document Structure Templates
# ============================================================

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

def make_word_rels(image_ids):
    """Generate word/_rels/document.xml.rels with image relationships."""
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>']
    for img_id, img_path in image_ids:
        rels.append(f'  <Relationship Id="{img_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{os.path.basename(img_path)}"/>')
    rels.append('</Relationships>')
    return '\n'.join(rels)


STYLES_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="22"/>
        <w:szCs w:val="22"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="120" w:line="276" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="22"/>
      <w:szCs w:val="22"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="360" w:after="120"/>
      <w:keepNext/>
      <w:outlineLvl w:val="0"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="28"/>
      <w:szCs w:val="28"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="240" w:after="120"/>
      <w:keepNext/>
      <w:outlineLvl w:val="1"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="26"/>
      <w:szCs w:val="26"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="200" w:after="80"/>
      <w:keepNext/>
      <w:outlineLvl w:val="2"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="0" w:after="200"/>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="32"/>
      <w:szCs w:val="32"/>
    </w:rPr>
  </w:style>
</w:styles>'''


NUMBERING_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:abstractNum w:abstractNumId="0">
    <w:lvl w:ilvl="0">
      <w:start w:val="1"/>
      <w:numFmt w:val="decimal"/>
      <w:lvlText w:val="%1."/>
      <w:lvlJc w:val="left"/>
      <w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>
    </w:lvl>
  </w:abstractNum>
  <w:num w:numId="1">
    <w:abstractNumId w:val="0"/>
  </w:num>
</w:numbering>'''


# ============================================================
# XML Paragraph/Run Builders
# ============================================================

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
WP_NS = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
PIC_NS = 'http://schemas.openxmlformats.org/drawingml/2006/picture'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def make_run(text_content, bold=False, italic=False, size=22):
    """Create a w:r element with optional formatting."""
    rpr = ''
    parts = []
    if bold:
        parts.append('<w:b/>')
    if italic:
        parts.append('<w:i/>')
    if size != 22:
        parts.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    if parts:
        rpr = '<w:rPr>' + ''.join(parts) + '</w:rPr>'
    t_attr = ' xml:space="preserve"' if text_content.startswith(' ') or text_content.endswith(' ') else ''
    return f'<w:r>{rpr}<w:t{t_attr}>{escape(text_content)}</w:t></w:r>'


def make_paragraph(runs, style=None, alignment=None, numbering=None, spacing_before=None):
    """Create a w:p element."""
    ppr_parts = []
    if style:
        ppr_parts.append(f'<w:pStyle w:val="{style}"/>')
    if alignment:
        ppr_parts.append(f'<w:jc w:val="{alignment}"/>')
    if numbering:
        ppr_parts.append(f'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="{numbering}"/></w:numPr>')
    if spacing_before:
        ppr_parts.append(f'<w:spacing w:before="{spacing_before}"/>')
    ppr = ''
    if ppr_parts:
        ppr = '<w:pPr>' + ''.join(ppr_parts) + '</w:pPr>'
    return f'<w:p>{ppr}{"".join(runs)}</w:p>'


def make_image_paragraph(rel_id, width_px, height_px, caption=""):
    """Create a paragraph with an inline image."""
    # Convert pixels to EMU (English Metric Units): 1 inch = 914400 EMU, at 300 DPI
    emu_per_px = 914400 // 300  # 3048
    # Scale image to fit page width (max ~6 inches = 5486400 EMU)
    max_width_emu = 5486400
    img_width_emu = width_px * emu_per_px
    img_height_emu = height_px * emu_per_px

    if img_width_emu > max_width_emu:
        scale = max_width_emu / img_width_emu
        img_width_emu = int(img_width_emu * scale)
        img_height_emu = int(img_height_emu * scale)

    drawing = f'''<w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0"
        xmlns:wp="{WP_NS}">
        <wp:extent cx="{img_width_emu}" cy="{img_height_emu}"/>
        <wp:docPr id="1" name="Picture"/>
        <a:graphic xmlns:a="{A_NS}">
          <a:graphicData uri="{PIC_NS}">
            <pic:pic xmlns:pic="{PIC_NS}">
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="Picture"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{rel_id}" xmlns:r="{R_NS}"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm>
                  <a:off x="0" y="0"/>
                  <a:ext cx="{img_width_emu}" cy="{img_height_emu}"/>
                </a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>'''

    img_para = f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r>{drawing}</w:r></w:p>'

    if caption:
        cap_para = make_paragraph([make_run(caption, italic=True)], alignment='center')
        return img_para + '\n' + cap_para
    return img_para


def make_table(headers, rows):
    """Create a simple table with borders."""
    border = '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>' \
             '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>' \
             '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>' \
             '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>' \
             '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>' \
             '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'

    tbl_pr = f'<w:tblPr><w:tblBorders>{border}</w:tblBorders><w:tblW w:w="5000" w:type="pct"/></w:tblPr>'

    xml_rows = []
    # Header row
    cells = []
    for h in headers:
        cell = f'<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>{make_paragraph([make_run(h, bold=True, size=20)])}</w:tc>'
        cells.append(cell)
    xml_rows.append('<w:tr>' + ''.join(cells) + '</w:tr>')

    # Data rows
    for row in rows:
        cells = []
        for cell_text in row:
            cell = f'<w:tc>{make_paragraph([make_run(cell_text, size=20)])}</w:tc>'
            cells.append(cell)
        xml_rows.append('<w:tr>' + ''.join(cells) + '</w:tr>')

    return f'<w:tbl>{tbl_pr}{"".join(xml_rows)}</w:tbl>'


# ============================================================
# Parse Markdown and Convert to OOXML
# ============================================================

def get_image_dimensions(filepath):
    """Read PNG width/height from IHDR chunk."""
    with open(filepath, 'rb') as f:
        f.read(8)  # signature
        f.read(4)  # length
        f.read(4)  # IHDR type
        w, h = struct.unpack('>II', f.read(8))
    return w, h


def parse_inline_formatting(text_content):
    """Parse bold (**text**) and italic (*text*) in a line, return list of runs."""
    runs = []
    # Pattern: **bold** or *italic*
    pattern = re.compile(r'(\*\*(.+?)\*\*|\*(.+?)\*)')
    pos = 0
    for m in pattern.finditer(text_content):
        # Add text before match
        if m.start() > pos:
            runs.append(make_run(text_content[pos:m.start()]))
        if m.group(2):  # bold
            runs.append(make_run(m.group(2), bold=True))
        elif m.group(3):  # italic
            runs.append(make_run(m.group(3), italic=True))
        pos = m.end()
    if pos < len(text_content):
        runs.append(make_run(text_content[pos:]))
    if not runs:
        runs.append(make_run(text_content))
    return runs


def convert_md_to_docx_body(md_content, fig_dir):
    """Convert markdown content to OOXML body paragraphs."""
    paragraphs = []
    image_refs = []  # (rel_id, filepath)
    img_counter = [0]
    lines = md_content.split('\n')

    # Figure mapping
    figures = {
        1: os.path.join(fig_dir, "Figure_1_BMS_Architecture.png"),
        2: os.path.join(fig_dir, "Figure_2_SOC_Estimation_Comparison.png"),
        3: os.path.join(fig_dir, "Figure_3_Charging_Network_Architecture.png"),
        4: os.path.join(fig_dir, "Figure_4_V2G_Framework.png"),
        5: os.path.join(fig_dir, "Figure_5_Digital_Twin_Framework.png"),
    }

    # Figure insertion points (after which heading to insert)
    figure_insertions = {
        "2.1 Intelligent Battery Management Systems (BMS)": 1,
        "2.2 AI for Energy Consumption and Range Prediction": 2,
        "3.1 Intelligent Charging Station Management": 3,
        "3.2 AI for Vehicle-to-Grid (V2G) and Grid Integration": 4,
        "4.1 Digital Twins and AI-Based Simulation": 5,
    }

    figure_captions = {
        1: "Figure 1. Hierarchical AI architecture for intelligent battery management systems showing multi-level integration from physical sensing to cloud analytics.",
        2: "Figure 2. Comparative accuracy (RMSE %) of SOC estimation methods across traditional, Kalman filter, machine learning, and deep learning approaches.",
        3: "Figure 3. AI-enabled smart charging network architecture with cloud, edge, and device layers showing hierarchical control and communication structure.",
        4: "Figure 4. V2G energy flow optimization framework illustrating bidirectional energy exchanges coordinated by AI optimization engine.",
        5: "Figure 5. Digital twin framework for EV battery systems showing bidirectional data flow between physical and virtual domains with continuous learning loop.",
    }

    i = 0
    in_table = False
    table_headers = []
    table_rows = []
    current_heading_text = ""
    numbered_list_counter = 0

    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line.strip():
            i += 1
            continue

        # Table detection
        if '|' in line and not in_table:
            # Check if next line is separator
            if i + 1 < len(lines) and re.match(r'\|[\s\-|]+\|', lines[i+1]):
                in_table = True
                # Parse header
                table_headers = [c.strip() for c in line.split('|')[1:-1]]
                i += 2  # skip header and separator
                table_rows = []
                continue

        if in_table:
            if '|' in line:
                row = [c.strip() for c in line.split('|')[1:-1]]
                table_rows.append(row)
                i += 1
                continue
            else:
                # End of table
                paragraphs.append(make_table(table_headers, table_rows))
                paragraphs.append(make_paragraph([make_run('')]))  # spacing
                in_table = False
                table_headers = []
                table_rows = []
                continue

        # Headings
        if line.startswith('# '):
            heading_text = line[2:].strip()
            paragraphs.append(make_paragraph([make_run(heading_text, bold=True, size=32)], style='Title'))
            i += 1
            continue

        if line.startswith('## '):
            heading_text = line[3:].strip()
            paragraphs.append(make_paragraph([make_run(heading_text, bold=True)], style='Heading1'))
            current_heading_text = heading_text
            i += 1
            continue

        if line.startswith('### '):
            heading_text = line[4:].strip()
            paragraphs.append(make_paragraph([make_run(heading_text, bold=True)], style='Heading2'))
            current_heading_text = heading_text

            # Check if we should insert a figure after this heading
            for key, fig_num in figure_insertions.items():
                if key in heading_text:
                    img_counter[0] += 1
                    rel_id = f"rId{img_counter[0] + 10}"
                    fig_path = figures[fig_num]
                    if os.path.exists(fig_path):
                        w, h = get_image_dimensions(fig_path)
                        image_refs.append((rel_id, fig_path))
                        # Add some spacing, then image
                        paragraphs.append(make_paragraph([make_run('')]))
                        paragraphs.append(make_image_paragraph(rel_id, w, h, figure_captions[fig_num]))
                        paragraphs.append(make_paragraph([make_run('')]))
            i += 1
            continue

        # Numbered list items (1. 2. etc)
        num_match = re.match(r'^(\d+)\.\s+\*\*(.+?)\*\*\s*(.*)', line)
        if num_match:
            num = num_match.group(1)
            bold_text = num_match.group(2)
            rest = num_match.group(3)
            runs = [make_run(f"{num}. ", bold=False), make_run(bold_text, bold=True)]
            if rest:
                runs.extend(parse_inline_formatting(' ' + rest))
            paragraphs.append(make_paragraph(runs, numbering=None, spacing_before="60"))
            i += 1
            continue

        # Regular numbered list
        num_match2 = re.match(r'^(\d+)\.\s+(.*)', line)
        if num_match2:
            num = num_match2.group(1)
            content = num_match2.group(2)
            runs = [make_run(f"{num}. ")] + parse_inline_formatting(content)
            paragraphs.append(make_paragraph(runs, spacing_before="60"))
            i += 1
            continue

        # Bold paragraph start: **Text:** content
        bold_start = re.match(r'^\*\*(.+?)\*\*\s*(.*)', line)
        if bold_start:
            bold_text = bold_start.group(1)
            rest = bold_start.group(2)
            runs = [make_run(bold_text, bold=True)]
            if rest:
                runs.append(make_run(' ' + rest))
            paragraphs.append(make_paragraph(runs))
            i += 1
            continue

        # Regular paragraph
        runs = parse_inline_formatting(line)
        paragraphs.append(make_paragraph(runs, alignment='both'))
        i += 1

    # Close any open table
    if in_table and table_headers:
        paragraphs.append(make_table(table_headers, table_rows))

    return '\n'.join(paragraphs), image_refs


def build_document_xml(body_content):
    """Wrap body content in document XML structure."""
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
  <w:body>
    {body_content}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>'''


# ============================================================
# Main: Build the .docx ZIP archive
# ============================================================

def main():
    print("=" * 60)
    print("Building DOCX: AI for Electric Vehicles and Charging Infrastructure")
    print("=" * 60)

    # Read markdown
    print("Reading markdown content...")
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert to OOXML body
    print("Converting to OOXML format...")
    body_content, image_refs = convert_md_to_docx_body(md_content, FIG_DIR)

    # Build document.xml
    document_xml = build_document_xml(body_content)

    # Build relationships
    word_rels = make_word_rels(image_refs)

    # Create ZIP (docx)
    print(f"Creating DOCX archive: {OUTPUT_FILE}")
    with zipfile.ZipFile(OUTPUT_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES_XML)
        zf.writestr('word/numbering.xml', NUMBERING_XML)
        zf.writestr('word/_rels/document.xml.rels', word_rels)

        # Add images
        for rel_id, img_path in image_refs:
            img_name = os.path.basename(img_path)
            zf.write(img_path, f'word/media/{img_name}')
            print(f"  Added image: {img_name}")

    # Verify
    file_size = os.path.getsize(OUTPUT_FILE)
    print()
    print(f"SUCCESS: {OUTPUT_FILE}")
    print(f"  File size: {file_size / 1024:.1f} KB")
    print(f"  Images embedded: {len(image_refs)}")
    print(f"  Format: 11pt Times New Roman, 1-inch margins")
    print(f"  DPI: 300 (figures)")
    print("=" * 60)


if __name__ == "__main__":
    main()
