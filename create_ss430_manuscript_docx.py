#!/usr/bin/env python3
"""
Create a Word .docx file for the manuscript
"Effect of austenitic ER309L, martensitic ER410, and super-duplex ER2594 filler
wires on the weldability of AISI 430 ferritic stainless steel".

Follows the raw-OOXML approach of create_intersectionality_docx.py, because
python-docx is not available in this sandbox. Supported Markdown subset:

  # / ## / ###                 title, section and subsection headings
  **bold**, *italic*           inline emphasis
  <sub>, <sup>, <i>, <b>       inline HTML used for chemistry and units
  <p align="center">...</p>    display equation; trailing "(n)" becomes a
                               right-aligned equation number
  | a | b |                    pipe table -> native three-line Word table
  **Table N.** / **Fig. N.**   table and figure captions
  <sup>a</sup> ... / Note: ... table notes (paragraph after a table)
  [Insert Figure N here]       figure placeholder
  1. item                      numbered conclusion
  [n] ...                      reference entry (in the References section)

Usage:
    python3 create_ss430_manuscript_docx.py
"""

import os
import re
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(HERE, 'Manuscript_SS430_Filler_Wire_Weldability.md')
DOCX_FILE = os.path.join(HERE, 'Manuscript_SS430_Filler_Wire_Weldability.docx')

TEXT_WIDTH = 9360  # twips: 6.5 in between 1 in margins on a Letter page

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>'''

PACKAGE_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>'''

DOCUMENT_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

CORE_PROPS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/">
  <dc:title>{title}</dc:title>
</cp:coreProperties>'''

STYLES = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{W_NS}">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="24"/><w:szCs w:val="24"/>
        <w:lang w:val="en-US"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
    <w:pPr><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:after="360"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
    <w:pPr><w:keepNext/><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/><w:outlineLvl w:val="0"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
    <w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/><w:outlineLvl w:val="1"/></w:pPr>
    <w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Equation">
    <w:name w:val="Equation"/><w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:tabs><w:tab w:val="center" w:pos="{TEXT_WIDTH // 2}"/><w:tab w:val="right" w:pos="{TEXT_WIDTH}"/></w:tabs>
      <w:spacing w:before="120" w:after="120"/><w:jc w:val="left"/>
    </w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigurePlaceholder">
    <w:name w:val="Figure Placeholder"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:keepNext/><w:spacing w:before="240" w:after="60"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:i/><w:color w:val="7F7F7F"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:after="240" w:line="276" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:keepNext/><w:spacing w:before="240" w:after="80" w:line="276" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableText">
    <w:name w:val="Table Text"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="40" w:after="40" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableNote">
    <w:name w:val="Table Note"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="60" w:after="240" w:line="240" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ListNumbered">
    <w:name w:val="List Numbered"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:tabs><w:tab w:val="left" w:pos="360"/></w:tabs><w:ind w:left="360" w:hanging="360"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Reference">
    <w:name w:val="Reference"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:after="80" w:line="276" w:lineRule="auto"/><w:ind w:left="540" w:hanging="540"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
</w:styles>'''

INLINE_TOKEN = re.compile(r'(\*\*|\*|</?sub>|</?sup>|</?i>|</?b>|\t)')
TAG_STRIP = re.compile(r'</?(?:sub|sup|i|b)>|\*')


def escape_xml(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


def make_run(text, bold=False, italic=False, vert=None):
    props = ''
    if bold:
        props += '<w:b/>'
    if italic:
        props += '<w:i/>'
    if vert:
        props += f'<w:vertAlign w:val="{vert}"/>'
    rpr = f'<w:rPr>{props}</w:rPr>' if props else ''
    if text == '\t':
        return f'<w:r>{rpr}<w:tab/></w:r>'
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'


def parse_inline(text, bold=False):
    """Convert the supported inline markup into a sequence of w:r runs."""
    runs = []
    italic = False
    vert = None
    for tok in INLINE_TOKEN.split(text):
        if not tok:
            continue
        if tok in ('**', '<b>', '</b>'):
            bold = (tok == '<b>') if tok != '**' else not bold
        elif tok in ('*', '<i>', '</i>'):
            italic = (tok == '<i>') if tok != '*' else not italic
        elif tok == '<sub>':
            vert = 'subscript'
        elif tok == '<sup>':
            vert = 'superscript'
        elif tok in ('</sub>', '</sup>'):
            vert = None
        else:
            runs.append(make_run(tok, bold, italic, vert))
    return ''.join(runs)


def paragraph(text, style='Normal', bold=False):
    return (f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
            f'{parse_inline(text, bold=bold)}</w:p>')


def equation_paragraph(inner):
    """Center the equation with a tab and right-align its '(n)' number."""
    m = re.match(r'^(.*?)\s{2,}(\(\d+\))\s*$', inner)
    body, number = (m.group(1), m.group(2)) if m else (inner, '')
    text = '\t' + body.strip() + ('\t' + number if number else '')
    return paragraph(text, 'Equation')


def visible_length(cell):
    return len(TAG_STRIP.sub('', cell))


def table_xml(header, rows):
    n_cols = len(header)
    weights = []
    for c in range(n_cols):
        cells = [header[c]] + [r[c] for r in rows if c < len(r)]
        weights.append(max(6, max(visible_length(x) for x in cells)))
    total = sum(weights)
    widths = [int(TEXT_WIDTH * w / total) for w in weights]
    widths[-1] = TEXT_WIDTH - sum(widths[:-1])

    rule = '<w:{side} w:val="single" w:sz="{sz}" w:space="0" w:color="000000"/>'
    xml = ['<w:tbl><w:tblPr>',
           f'<w:tblW w:w="{TEXT_WIDTH}" w:type="dxa"/><w:jc w:val="center"/>',
           '<w:tblBorders>',
           rule.format(side='top', sz=8), rule.format(side='bottom', sz=8),
           '</w:tblBorders><w:tblLayout w:type="fixed"/>',
           '<w:tblCellMar><w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar>',
           '</w:tblPr><w:tblGrid>']
    xml += [f'<w:gridCol w:w="{w}"/>' for w in widths]
    xml.append('</w:tblGrid>')

    def cell(content, width, col, is_header):
        borders = ('<w:tcBorders>' + rule.format(side='bottom', sz=4) +
                   '</w:tcBorders>') if is_header else ''
        jc = '<w:jc w:val="left"/>' if col == 0 else ''
        return (f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{borders}'
                '<w:vAlign w:val="center"/></w:tcPr>'
                f'<w:p><w:pPr><w:pStyle w:val="TableText"/>{jc}</w:pPr>'
                f'{parse_inline(content, bold=is_header)}</w:p></w:tc>')

    xml.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
    xml += [cell(h, widths[i], i, True) for i, h in enumerate(header)]
    xml.append('</w:tr>')
    for r in rows:
        r = r + [''] * (n_cols - len(r))
        xml.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>')
        xml += [cell(v, widths[i], i, False) for i, v in enumerate(r)]
        xml.append('</w:tr>')
    xml.append('</w:tbl>')
    return ''.join(xml)


def split_row(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def md_to_body(md_text):
    elements = []
    lines = md_text.split('\n')
    i = 0
    in_refs = False
    after_table = False
    while i < len(lines):
        line = lines[i].strip()
        if not line or line == '---':
            i += 1
            continue

        if line.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|$', lines[i + 1].strip()):
            header = split_row(line)
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append(split_row(lines[i]))
                i += 1
            elements.append(table_xml(header, rows))
            after_table = True
            continue

        is_note = after_table and (line.startswith('<sup>') or line.startswith('Note:'))
        after_table = False

        if line.startswith('# '):
            elements.append(paragraph(line[2:], 'Title'))
        elif line.startswith('## '):
            heading = line[3:]
            in_refs = heading.lower() == 'references'
            elements.append(paragraph(heading, 'Heading1'))
        elif line.startswith('### '):
            elements.append(paragraph(line[4:], 'Heading2'))
        elif line.startswith('<p align="center">') and line.endswith('</p>'):
            elements.append(equation_paragraph(line[len('<p align="center">'):-len('</p>')]))
        elif re.match(r'^\[Insert Figure \d+ here\]$', line):
            elements.append(paragraph(line, 'FigurePlaceholder'))
        elif line.startswith('**Fig.'):
            elements.append(paragraph(line, 'FigureCaption'))
        elif line.startswith('**Table'):
            elements.append(paragraph(line, 'TableCaption'))
        elif is_note:
            elements.append(paragraph(line, 'TableNote'))
        elif in_refs and re.match(r'^\[\d+\]', line):
            elements.append(paragraph(line, 'Reference'))
        elif re.match(r'^\d+\.\s', line):
            num, rest = line.split(' ', 1)
            elements.append(paragraph(f'{num}\t{rest}', 'ListNumbered'))
        else:
            elements.append(paragraph(line))
        i += 1
    return '\n'.join(elements)


def create_docx(md_path, docx_path):
    with open(md_path, encoding='utf-8') as f:
        md_text = f.read()
    title_match = re.search(r'^# (.+)$', md_text, re.M)
    title = title_match.group(1).strip() if title_match else ''

    body = md_to_body(md_text)
    document = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                f'<w:document xmlns:w="{W_NS}" xmlns:r="{R_NS}"><w:body>\n{body}\n'
                '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
                '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
                'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
                '</w:body></w:document>')

    with zipfile.ZipFile(docx_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', PACKAGE_RELS)
        zf.writestr('docProps/core.xml', CORE_PROPS.format(title=escape_xml(title)))
        zf.writestr('word/_rels/document.xml.rels', DOCUMENT_RELS)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)

    print(f'Created {docx_path} ({os.path.getsize(docx_path) / 1024:.1f} KB)')


if __name__ == '__main__':
    create_docx(MD_FILE, DOCX_FILE)
