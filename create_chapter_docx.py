#!/usr/bin/env python3
"""
Create Word document (.docx) for the DRL-HVAC Optimization chapter.
Uses pure Python standard library (zipfile, xml) - no external packages.
DOCX is a ZIP archive containing XML files following the Office Open XML standard.
Formats: 11pt Times New Roman, proper heading styles, embedded SVG figures.
"""

import zipfile
import os
import base64
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "Chapter_DRL_HVAC_Digital_Twin.docx")
FIGURES_DIR = os.path.join(SCRIPT_DIR, "chapter_figures")
CHAPTER_MD = os.path.join(SCRIPT_DIR, "Chapter_DRL_HVAC_Optimization.md")


# ============================================================
# OOXML Templates
# ============================================================

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="svg" ContentType="image/svg+xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''


STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
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
        <w:spacing w:after="120" w:line="360" w:lineRule="auto"/>
        <w:jc w:val="both"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="22"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:pPr>
      <w:keepNext/>
      <w:spacing w:before="360" w:after="120"/>
      <w:jc w:val="center"/>
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
    <w:next w:val="Normal"/>
    <w:pPr>
      <w:keepNext/>
      <w:spacing w:before="240" w:after="120"/>
      <w:outlineLvl w:val="1"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:pPr>
      <w:keepNext/>
      <w:spacing w:before="200" w:after="80"/>
      <w:outlineLvl w:val="2"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:i/>
      <w:sz w:val="22"/>
      <w:szCs w:val="22"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Abstract">
    <w:name w:val="Abstract"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="120" w:after="120"/>
      <w:ind w:left="720" w:right="720"/>
    </w:pPr>
    <w:rPr>
      <w:i/>
      <w:sz w:val="20"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="60" w:after="200"/>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:rPr>
      <w:i/>
      <w:sz w:val="20"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableHeader">
    <w:name w:val="Table Header"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:jc w:val="center"/>
      <w:spacing w:before="60" w:after="60"/>
    </w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="20"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCell">
    <w:name w:val="Table Cell"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:jc w:val="center"/>
      <w:spacing w:before="40" w:after="40" w:line="240" w:lineRule="auto"/>
    </w:pPr>
    <w:rPr>
      <w:sz w:val="20"/>
    </w:rPr>
  </w:style>
</w:styles>'''


SETTINGS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:defaultTabStop w:val="720"/>
  <w:compat>
    <w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>
  </w:compat>
</w:settings>'''

NUMBERING = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
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


def word_rels_xml(image_rels):
    """Generate word/_rels/document.xml.rels with image relationships."""
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>',
            '  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>']
    for rid, target in image_rels:
        rels.append(f'  <Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{target}"/>')
    rels.append('</Relationships>')
    return '\n'.join(rels)


# ============================================================
# Document Body XML Generators
# ============================================================

def make_paragraph(text, style="Normal", bold=False, italic=False, size=None):
    """Create a paragraph XML element."""
    ppr = ''
    if style != "Normal":
        ppr = f'<w:pStyle w:val="{style}"/>'

    rpr_parts = []
    if bold:
        rpr_parts.append('<w:b/>')
    if italic:
        rpr_parts.append('<w:i/>')
    if size:
        rpr_parts.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    rpr = f'<w:rPr>{"".join(rpr_parts)}</w:rPr>' if rpr_parts else ''

    # Handle special characters
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = text.replace('°', '&#176;')

    return f'<w:p><w:pPr>{ppr}</w:pPr><w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r></w:p>'


def make_heading(text, level):
    """Create a heading paragraph."""
    style = f"Heading{level}"
    return make_paragraph(text, style, bold=True)


def make_image_paragraph(rid, width_emu, height_emu, caption=""):
    """Create a paragraph with an embedded image."""
    # EMU = English Metric Units (1 inch = 914400 EMU)
    img_xml = f'''<w:p>
  <w:pPr><w:jc w:val="center"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
                 distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{width_emu}" cy="{height_emu}"/>
        <wp:docPr id="1" name="Figure"/>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="Figure"/>
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

    if caption:
        cap_text = caption.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        img_xml += f'\n<w:p><w:pPr><w:pStyle w:val="FigureCaption"/></w:pPr><w:r><w:rPr><w:i/><w:sz w:val="20"/></w:rPr><w:t>{cap_text}</w:t></w:r></w:p>'

    return img_xml



def make_table(headers, rows):
    """Create a table XML element."""
    n_cols = len(headers)
    col_width = 9000 // n_cols  # Total width ~9000 twips (6.25 inches)

    table_xml = ['<w:tbl>']
    table_xml.append('<w:tblPr>')
    table_xml.append(f'<w:tblW w:w="9000" w:type="dxa"/>')
    table_xml.append('<w:tblBorders>')
    for border in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        table_xml.append(f'<w:{border} w:val="single" w:sz="4" w:space="0" w:color="000000"/>')
    table_xml.append('</w:tblBorders>')
    table_xml.append('<w:jc w:val="center"/>')
    table_xml.append('</w:tblPr>')

    # Column grid
    table_xml.append('<w:tblGrid>')
    for _ in range(n_cols):
        table_xml.append(f'<w:gridCol w:w="{col_width}"/>')
    table_xml.append('</w:tblGrid>')

    # Header row
    table_xml.append('<w:tr>')
    for h in headers:
        h_escaped = h.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        table_xml.append(f'<w:tc><w:tcPr><w:shd w:val="clear" w:fill="E8E8E8"/></w:tcPr>')
        table_xml.append(f'<w:p><w:pPr><w:pStyle w:val="TableHeader"/></w:pPr>')
        table_xml.append(f'<w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>{h_escaped}</w:t></w:r></w:p></w:tc>')
    table_xml.append('</w:tr>')

    # Data rows
    for row in rows:
        table_xml.append('<w:tr>')
        for cell in row:
            c_escaped = str(cell).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            table_xml.append(f'<w:tc>')
            table_xml.append(f'<w:p><w:pPr><w:pStyle w:val="TableCell"/></w:pPr>')
            table_xml.append(f'<w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>{c_escaped}</w:t></w:r></w:p></w:tc>')
        table_xml.append('</w:tr>')

    table_xml.append('</w:tbl>')
    # Add spacing after table
    table_xml.append('<w:p><w:pPr><w:spacing w:before="120"/></w:pPr></w:p>')
    return '\n'.join(table_xml)


def make_list_item(text, num_id=1, level=0):
    """Create a numbered list item."""
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return f'''<w:p>
  <w:pPr>
    <w:numPr><w:ilvl w:val="{level}"/><w:numId w:val="{num_id}"/></w:numPr>
    <w:ind w:left="720" w:hanging="360"/>
  </w:pPr>
  <w:r><w:t xml:space="preserve">{text}</w:t></w:r>
</w:p>'''


def make_bold_paragraph(parts):
    """Create a paragraph with mixed bold/normal text.
    parts: list of (text, is_bold) tuples."""
    runs = []
    for text, is_bold in parts:
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        rpr = '<w:rPr><w:b/></w:rPr>' if is_bold else ''
        runs.append(f'<w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r>')
    return f'<w:p>{"".join(runs)}</w:p>'



# ============================================================
# Parse Markdown and Convert to DOCX Body
# ============================================================

def parse_markdown_to_docx_body(md_content, image_rels_collector):
    """Parse the markdown chapter content and convert to OOXML body elements."""
    body_parts = []
    lines = md_content.split('\n')
    i = 0
    figure_counter = 0
    image_rel_id = 10  # Start rel IDs at rId10 for images

    # Figure mapping
    figure_files = {
        1: "Figure_1_System_Architecture.svg",
        2: "Figure_2_TD3_Architecture.svg",
        3: "Figure_3_Calibration_Results.svg",
        4: "Figure_4_Training_Convergence.svg",
        5: "Figure_5_Energy_Comparison.svg",
        6: "Figure_6_Load_Profiles.svg",
    }

    # Figure captions
    figure_captions = {
        1: "Figure 1. System Architecture of the DRL-Digital Twin HVAC Optimization Framework",
        2: "Figure 2. Enhanced TD3 Algorithm Architecture with Domain-Specific Modifications",
        3: "Figure 3. Digital Twin Calibration Results: Measured vs. Predicted Zone Temperatures over 7-day period",
        4: "Figure 4. Training Convergence Curves showing Episode Reward and Energy Savings over 2M training steps",
        5: "Figure 5. Monthly Energy Consumption Comparison between DRL Agent and Baseline Controller",
        6: "Figure 6. Daily Electrical Load Profiles showing peak demand reduction through DRL optimization",
    }

    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line.strip():
            i += 1
            continue

        # Chapter title (# heading)
        if line.startswith('# ') and not line.startswith('## '):
            title = line[2:].strip()
            body_parts.append(make_heading(title, 1))
            i += 1
            continue

        # Section heading (## heading)
        if line.startswith('## '):
            heading = line[3:].strip()
            body_parts.append(make_heading(heading, 2))
            i += 1
            continue

        # Subsection heading (### heading)
        if line.startswith('### '):
            heading = line[4:].strip()
            body_parts.append(make_heading(heading, 3))
            i += 1
            continue

        # Figure placeholder
        if line.strip().startswith('**[Figure'):
            figure_counter += 1
            if figure_counter in figure_files:
                rid = f"rId{image_rel_id}"
                target = f"media/{figure_files[figure_counter]}"
                image_rels_collector.append((rid, target))
                # 6.5 inches wide, aspect ratio ~0.625 for most figures
                w_emu = int(6.0 * 914400)  # 6 inches wide
                h_emu = int(3.75 * 914400)  # ~3.75 inches tall
                caption = figure_captions.get(figure_counter, f"Figure {figure_counter}")
                body_parts.append(make_image_paragraph(rid, w_emu, h_emu, caption))
                image_rel_id += 1
            i += 1
            continue

        # Table detection
        if '|' in line and i + 1 < len(lines) and '---' in lines[i + 1]:
            # Parse markdown table
            headers = [h.strip() for h in line.split('|') if h.strip()]
            i += 2  # Skip header and separator
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                cells = [c.strip() for c in lines[i].split('|') if c.strip()]
                rows.append(cells)
                i += 1
            # Add table title if previous line was bold
            body_parts.append(make_table(headers, rows))
            continue

        # Numbered list
        if re.match(r'^\d+\.', line.strip()):
            text = re.sub(r'^\d+\.\s*', '', line.strip())
            # Remove markdown bold markers
            text = text.replace('**', '')
            body_parts.append(make_list_item(text))
            i += 1
            continue

        # Bullet list
        if line.strip().startswith('- '):
            text = line.strip()[2:]
            text = text.replace('**', '')
            body_parts.append(make_list_item(text))
            i += 1
            continue

        # Keywords line
        if line.strip().startswith('**Keywords:**'):
            kw_text = line.strip().replace('**Keywords:**', '').strip()
            body_parts.append(make_bold_paragraph([
                ("Keywords: ", True), (kw_text, False)
            ]))
            i += 1
            continue

        # Bold paragraph (table titles, etc.)
        if line.strip().startswith('**') and line.strip().endswith('**'):
            text = line.strip()[2:-2]
            body_parts.append(make_paragraph(text, bold=True))
            i += 1
            continue

        # Regular paragraph - collect consecutive lines
        paragraph_lines = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith('#') \
                and not lines[i].startswith('**[Figure') \
                and not (re.match(r'^\d+\.', lines[i].strip())) \
                and not lines[i].strip().startswith('- ') \
                and not ('|' in lines[i] and i + 1 < len(lines) and '---' in lines[i + 1]):
            paragraph_lines.append(lines[i].strip())
            i += 1
            # Check next line for table separator
            if i < len(lines) and '|' in lines[i]:
                break

        if paragraph_lines:
            full_text = ' '.join(paragraph_lines)
            # Remove markdown formatting
            full_text = full_text.replace('**', '')
            full_text = full_text.replace('*', '')

            # Check if this is abstract
            if 'account for approximately 40-60%' in full_text and 'Heating' in full_text:
                body_parts.append(make_paragraph(full_text, "Abstract", italic=True, size=20))
            else:
                body_parts.append(make_paragraph(full_text))

    return body_parts



def build_document_xml(body_parts):
    """Assemble the complete document.xml."""
    header = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
  <w:body>
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
      <w:cols w:space="720"/>
    </w:sectPr>
'''
    footer = '''  </w:body>
</w:document>'''

    return header + '\n'.join(body_parts) + '\n' + footer


def create_docx():
    """Main function to create the .docx file."""
    print("Reading chapter content...")
    with open(CHAPTER_MD, 'r') as f:
        md_content = f.read()

    print("Parsing markdown and generating XML...")
    image_rels = []
    body_parts = parse_markdown_to_docx_body(md_content, image_rels)

    print(f"  Generated {len(body_parts)} document elements")
    print(f"  Found {len(image_rels)} figure references")

    # Build document XML
    document_xml = build_document_xml(body_parts)
    word_rels = word_rels_xml(image_rels)

    print("Creating .docx archive...")
    with zipfile.ZipFile(OUTPUT_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Root files
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)

        # Word directory
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES)
        zf.writestr('word/settings.xml', SETTINGS)
        zf.writestr('word/numbering.xml', NUMBERING)
        zf.writestr('word/_rels/document.xml.rels', word_rels)

        # Embed figures
        for rid, target in image_rels:
            fig_filename = os.path.basename(target)
            fig_path = os.path.join(FIGURES_DIR, fig_filename)
            if os.path.exists(fig_path):
                zf.write(fig_path, f'word/{target}')
                print(f"  Embedded: {fig_filename}")
            else:
                print(f"  WARNING: Figure not found: {fig_path}")

    file_size = os.path.getsize(OUTPUT_FILE)
    print()
    print("=" * 60)
    print(f"Document created: {OUTPUT_FILE}")
    print(f"File size: {file_size / 1024:.1f} KB")
    print(f"Format: Microsoft Word (.docx)")
    print(f"Font: 11pt Times New Roman (body), with heading styles")
    print(f"Figures: {len(image_rels)} SVG figures embedded")
    print(f"Margins: 1 inch all sides")
    print(f"Line spacing: 1.5")
    print("=" * 60)


if __name__ == "__main__":
    create_docx()
