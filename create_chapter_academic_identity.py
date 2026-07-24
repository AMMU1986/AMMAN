#!/usr/bin/env python3
"""
Create a Word document (.docx) for the book chapter:
"Academic Identity and Professional Development"
From: Higher Education Beyond Boundaries

Supports: text, headings, tables, embedded PNG images.
Uses only Python standard library (zipfile for docx creation).
Format: Times New Roman, 12pt, double-spaced
"""

import zipfile
import os
import struct


def escape_xml(text):
    """Escape XML special characters."""
    if not text:
        return ""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def get_png_dimensions(filepath):
    """Read PNG width and height from file header."""
    with open(filepath, 'rb') as f:
        f.read(8)  # PNG signature
        f.read(4)  # chunk length
        f.read(4)  # IHDR
        w = struct.unpack('>I', f.read(4))[0]
        h = struct.unpack('>I', f.read(4))[0]
    return w, h



def create_paragraph_xml(text, style="Normal", bold=False, italic=False):
    """Create a Word XML paragraph."""
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
    elif style == "Caption":
        ppr_parts.append('<w:spacing w:line="480" w:lineRule="auto" w:after="120"/>')
        ppr_parts.append('<w:jc w:val="center"/>')
    elif style == "TableTitle":
        ppr_parts.append('<w:spacing w:line="240" w:lineRule="auto" w:before="240" w:after="120"/>')
    else:
        ppr_parts.append('<w:spacing w:line="480" w:lineRule="auto" w:after="0"/>')
        ppr_parts.append('<w:ind w:firstLine="720"/>')
    ppr = ""
    if ppr_parts:
        ppr = "<w:pPr>" + "".join(ppr_parts) + "</w:pPr>"
    if not text:
        return f"<w:p>{ppr}</w:p>"
    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r></w:p>'



def create_image_xml(rel_id, cx_emu, cy_emu, img_name):
    """Create Word XML for an inline image."""
    return f'''<w:p>
  <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="120"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
                 distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{cx_emu}" cy="{cy_emu}"/>
        <wp:docPr id="1" name="{escape_xml(img_name)}"/>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="{escape_xml(img_name)}"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{rel_id}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx_emu}" cy="{cy_emu}"/></a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>'''



def create_table_xml(title, headers, rows):
    """Create Word XML for a table with header row and data rows."""
    num_cols = len(headers)
    col_width = 9360 // num_cols  # total page width in twips divided by cols

    # Table title paragraph
    title_para = create_paragraph_xml(title, style="TableTitle", bold=True, italic=True)

    # Table XML
    tbl_parts = []
    tbl_parts.append('<w:tbl>')
    tbl_parts.append('<w:tblPr>')
    tbl_parts.append('<w:tblStyle w:val="TableGrid"/>')
    tbl_parts.append(f'<w:tblW w:w="9360" w:type="dxa"/>')
    tbl_parts.append('<w:tblBorders>')
    for border in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        tbl_parts.append(f'<w:{border} w:val="single" w:sz="4" w:space="0" w:color="000000"/>')
    tbl_parts.append('</w:tblBorders>')
    tbl_parts.append('<w:tblLayout w:type="fixed"/>')
    tbl_parts.append('</w:tblPr>')

    # Column grid
    tbl_parts.append('<w:tblGrid>')
    for _ in range(num_cols):
        tbl_parts.append(f'<w:gridCol w:w="{col_width}"/>')
    tbl_parts.append('</w:tblGrid>')

    # Header row
    tbl_parts.append('<w:tr>')
    for h in headers:
        cell_text = escape_xml(h.strip())
        tbl_parts.append(f'''<w:tc>
  <w:tcPr><w:tcW w:w="{col_width}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>
  <w:p><w:pPr><w:spacing w:line="240" w:lineRule="auto" w:after="0"/></w:pPr>
  <w:r><w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  <w:t xml:space="preserve">{cell_text}</w:t></w:r></w:p>
</w:tc>''')
    tbl_parts.append('</w:tr>')

    # Data rows
    for row in rows:
        cells = row.split('|')
        tbl_parts.append('<w:tr>')
        for j, cell in enumerate(cells):
            cell_text = escape_xml(cell.strip())
            tbl_parts.append(f'''<w:tc>
  <w:tcPr><w:tcW w:w="{col_width}" w:type="dxa"/></w:tcPr>
  <w:p><w:pPr><w:spacing w:line="240" w:lineRule="auto" w:after="0"/></w:pPr>
  <w:r><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  <w:t xml:space="preserve">{cell_text}</w:t></w:r></w:p>
</w:tc>''')
        # Pad if fewer cells than headers
        for _ in range(num_cols - len(cells)):
            tbl_parts.append(f'<w:tc><w:tcPr><w:tcW w:w="{col_width}" w:type="dxa"/></w:tcPr><w:p/></w:tc>')
        tbl_parts.append('</w:tr>')

    tbl_parts.append('</w:tbl>')

    return title_para + '\n' + '\n'.join(tbl_parts)



def parse_content_file(filepath, figure_dir):
    """Parse the chapter content text file into XML elements.
    Returns (xml_parts, image_files) where image_files is a list of (rel_id, filepath) tuples."""
    xml_parts = []
    image_files = []
    img_counter = 0

    with open(filepath, "r") as f:
        text = f.read()

    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("#TITLE# "):
            xml_parts.append(create_paragraph_xml(line[8:], "Title", bold=True))
        elif line.startswith("#SUBTITLE# "):
            xml_parts.append(create_paragraph_xml(line[11:], "Normal"))
        elif line.startswith("#H1# "):
            xml_parts.append(create_paragraph_xml(line[5:], "Heading1", bold=True))
        elif line.startswith("#H2# "):
            xml_parts.append(create_paragraph_xml(line[5:], "Heading2", bold=True))
        elif line.startswith("#H3# "):
            xml_parts.append(create_paragraph_xml(line[5:], "Heading3", bold=True, italic=True))
        elif line.startswith("#FIGURE# "):
            # Image embedding
            img_filename = line[9:].strip()
            img_path = os.path.join(figure_dir, img_filename)
            if os.path.exists(img_path):
                img_counter += 1
                rel_id = f"rId{100 + img_counter}"
                image_files.append((rel_id, img_path, img_filename))
                pw, ph = get_png_dimensions(img_path)
                # Scale to fit page width (5.5 inches = 5029200 EMU max)
                max_width_emu = 5029200
                scale = min(1.0, max_width_emu / (pw * 9525))
                cx = int(pw * 9525 * scale)
                cy = int(ph * 9525 * scale)
                xml_parts.append(create_image_xml(rel_id, cx, cy, img_filename))
        elif line.startswith("#CAPTION# "):
            caption_text = line[10:].strip()
            xml_parts.append(create_paragraph_xml(caption_text, "Caption", italic=True))
        elif line.startswith("#TABLE# "):
            # Collect table: title, headers, rows
            table_title = line[8:].strip()
            headers = []
            rows = []
            i += 1
            while i < len(lines):
                if lines[i].startswith("#THEAD# "):
                    headers = lines[i][8:].split("|")
                elif lines[i].startswith("#TROW# "):
                    rows.append(lines[i][7:])
                elif lines[i].strip() == "" or not lines[i].startswith("#T"):
                    break
                i += 1
            xml_parts.append(create_table_xml(table_title, headers, rows))
            xml_parts.append('<w:p/>')  # blank line after table
            continue  # don't increment i again
        elif line.strip() == "":
            xml_parts.append('<w:p><w:pPr><w:spacing w:line="480" w:lineRule="auto" w:after="0"/></w:pPr></w:p>')
        else:
            xml_parts.append(create_paragraph_xml(line, "Normal"))
        i += 1

    return xml_parts, image_files



def create_docx(content_filepath, figure_dir, output_path):
    """Create the .docx file with text, tables, and images."""
    xml_parts, image_files = parse_content_file(content_filepath, figure_dir)
    body_content = "\n    ".join(xml_parts)

    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
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

    # Content Types - include PNG
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
</Types>'''

    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

    # Build word/_rels/document.xml.rels with image relationships
    rel_entries = [
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>',
    ]
    for rel_id, _, img_filename in image_files:
        rel_entries.append(
            f'<Relationship Id="{rel_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{img_filename}"/>'
        )
    word_rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n  ' + '\n  '.join(rel_entries) + '\n</Relationships>'



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
    <w:pPr><w:spacing w:line="480" w:lineRule="auto" w:after="0"/></w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:sz w:val="24"/><w:szCs w:val="24"/>
    </w:rPr>
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

    settings = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:defaultTabStop w:val="720"/>
  <w:compat>
    <w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>
  </w:compat>
</w:settings>'''

    # Write the docx ZIP
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("word/_rels/document.xml.rels", word_rels)
        zf.writestr("word/document.xml", document)
        zf.writestr("word/styles.xml", styles)
        zf.writestr("word/settings.xml", settings)
        # Embed images
        for rel_id, img_path, img_filename in image_files:
            with open(img_path, 'rb') as img_f:
                zf.writestr(f"word/media/{img_filename}", img_f.read())

    print(f"Created: {output_path}")
    print(f"  Images embedded: {len(image_files)}")
    return xml_parts



def count_words_from_file(filepath):
    """Count words in the text content file (excluding markup)."""
    total = 0
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#') and '# ' in line:
                # Count words in headings/content after the tag
                tag_end = line.index('# ') + 2
                total += len(line[tag_end:].split())
            elif not line.startswith('#'):
                total += len(line.split())
    return total


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    content_file = os.path.join(script_dir, "chapter_content.txt")
    figure_dir = os.path.join(script_dir, "chapter_figures")
    output_file = os.path.join(script_dir, "Chapter_Academic_Identity_Professional_Development.docx")

    # Generate docx
    create_docx(content_file, figure_dir, output_file)

    # Word count
    wc = count_words_from_file(content_file)
    print(f"Chapter word count: ~{wc}")
    print("Done!")
