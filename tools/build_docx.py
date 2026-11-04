#!/usr/bin/env python3
"""
Build Word (.docx) files from the Markdown sources of this repository, with the PNG
figures embedded in place.  Pure standard library (zipfile + raw OOXML).

    python3 tools/build_docx.py            # build every document listed in DOCS
    python3 tools/build_docx.py SRC.md OUT.docx

Supported Markdown subset (everything used by the sources):
  # .. ####  headings (the first level-1 heading becomes the document title)
  paragraphs, **bold**, *italic*, ***bold italic***, `code`, <sub>..</sub>, <sup>..</sup>
  - / * bulleted lists and 1. numbered lists (numbering restarts for every list)
  pipe tables (header row shaded; a preceding **Table N.** paragraph is its caption)
  ![alt](path.png) images on their own line (a following **Figure N.** / **Fig. N.**
  paragraph is formatted as the caption), --- rules (ignored), equation lines that end
  in a number such as (4.1) are centred.
"""
import os
import re
import struct
import sys
import zipfile
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOCS = [
    ('Chapter_Agentic_AI_Autonomous_Systems.md', 'Chapter_Agentic_AI_Autonomous_Systems.docx'),
    ('Chapter_Design_Thinking_Business_Functions.md', 'Chapter_Design_Thinking_Business_Functions.docx'),
    ('Chapter_Economic_Analysis_HRES.md', 'HRES_Economic_Analysis_Chapter.docx'),
    ('Chapter_Intersectionality_Climate_Resilience.md', 'Chapter_Intersectionality_Climate_Resilience.docx'),
    ('Manuscript_Ionic_Liquids_MQL_Machining.md', 'Manuscript_Ionic_Liquids_MQL_Machining.docx'),
    ('Chapter_16_AI_Assisted_Design_of_Nanomaterials.md', 'Chapter_16_AI_Assisted_Design_of_Nanomaterials.docx'),
    ('Chapter_4_Experimentation.md', 'Chapter_4_Experimentation.docx'),
    ('manuscript_with_references.md', 'AI_Medication_Safety_Education_with_references.docx'),
]

EMU_PER_INCH = 914400
MAX_W_IN = 6.3          # text width on Letter with 1" margins is 6.5"
MAX_H_IN = 8.0
FONT = 'Times New Roman'

W_NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')


# ------------------------------------------------------------------ inline formatting
TOKEN = re.compile(r'(\*\*\*|\*\*|\*|`|<sub>|</sub>|<sup>|</sup>|<br\s*/?>)')


def runs(text, base_bold=False, base_italic=False, size=None):
    """Convert inline Markdown to a sequence of <w:r> elements."""
    out = []
    bold, italic, code, vert = base_bold, base_italic, False, None
    for part in TOKEN.split(text):
        if not part:
            continue
        if part == '***':
            bold, italic = not bold, not italic
            continue
        if part == '**':
            bold = not bold
            continue
        if part == '*' and not code:
            italic = not italic
            continue
        if part == '`':
            code = not code
            continue
        if part in ('<sub>', '<sup>'):
            vert = 'subscript' if part == '<sub>' else 'superscript'
            continue
        if part in ('</sub>', '</sup>'):
            vert = None
            continue
        if part.startswith('<br'):
            out.append('<w:r><w:br/></w:r>')
            continue
        rpr = ''
        if code:
            rpr += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'
        if bold:
            rpr += '<w:b/><w:bCs/>'
        if italic:
            rpr += '<w:i/><w:iCs/>'
        if vert:
            rpr += '<w:vertAlign w:val="%s"/>' % vert
        if size:
            rpr += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size)
        out.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (
            '<w:rPr>%s</w:rPr>' % rpr if rpr else '', escape(part)))
    return ''.join(out)


def para(text, style=None, jc=None, keep_next=False, numpr=None, size=None, bold=False, italic=False,
         spacing=None):
    ppr = ''
    if style:
        ppr += '<w:pStyle w:val="%s"/>' % style
    if keep_next:
        ppr += '<w:keepNext/>'
    if numpr:
        ppr += '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="%d"/></w:numPr>' % numpr
    if spacing:
        ppr += spacing
    if jc:
        ppr += '<w:jc w:val="%s"/>' % jc
    return '<w:p>%s%s</w:p>' % ('<w:pPr>%s</w:pPr>' % ppr if ppr else '',
                                runs(text, bold, italic, size))


# ------------------------------------------------------------------ images
def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(32)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('not a PNG: %s' % path)
    w, h = struct.unpack('>II', head[16:24])
    return w, h


class Doc:
    def __init__(self, md_path):
        self.md_path = md_path
        self.base = os.path.dirname(os.path.abspath(md_path))
        self.media = []            # (zip name, file path)
        self.rels = []             # (rId, type, target)
        self.num_lists = 0         # number of numbered-list instances
        self.body = []
        self.title_done = False
        self.missing = []

    # -------------------------------------------------------------- pieces
    def image(self, alt, rel_path):
        path = os.path.join(self.base, rel_path)
        if not os.path.exists(path):
            self.missing.append(rel_path)
            self.body.append(para('[Missing figure: %s]' % rel_path, jc='center'))
            return
        idx = len(self.media) + 1
        name = 'image%d.png' % idx
        self.media.append((name, path))
        rid = 'rIdImg%d' % idx
        self.rels.append((rid, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image',
                          'media/' + name))
        pw, ph = png_size(path)
        w_in = MAX_W_IN
        h_in = w_in * ph / pw
        if h_in > MAX_H_IN:
            h_in = MAX_H_IN
            w_in = h_in * pw / ph
        cx, cy = int(w_in * EMU_PER_INCH), int(h_in * EMU_PER_INCH)
        descr = escape(alt, {'"': '&quot;'})
        drawing = (
            '<w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
            '<wp:extent cx="%d" cy="%d"/><wp:docPr id="%d" name="Picture %d" descr="%s"/>'
            '<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic><pic:nvPicPr><pic:cNvPr id="%d" name="%s"/><pic:cNvPicPr/></pic:nvPicPr>'
            '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
            '</a:graphicData></a:graphic></wp:inline></w:drawing>'
            % (cx, cy, idx, idx, descr, idx, name, rid, cx, cy))
        self.body.append('<w:p><w:pPr><w:pStyle w:val="Figure"/><w:keepNext/><w:jc w:val="center"/></w:pPr>'
                         '<w:r>%s</w:r></w:p>' % drawing)

    def table(self, rows):
        def cells(line):
            line = line.strip()
            if line.startswith('|'):
                line = line[1:]
            if line.endswith('|'):
                line = line[:-1]
            return [c.strip() for c in line.split('|')]
        parsed = [cells(r) for r in rows]
        header = parsed[0]
        body = [r for r in parsed[1:] if not all(re.fullmatch(r':?-{2,}:?', c or '---') for c in r)]
        ncol = len(header)
        width = 9360  # twips, 6.5"
        colw = width // max(ncol, 1)
        border = ''.join('<w:%s w:val="single" w:sz="4" w:space="0" w:color="A6A6A6"/>' % b
                         for b in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
        x = ['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="5000" w:type="pct"/>'
             '<w:tblBorders>%s</w:tblBorders><w:tblLayout w:type="autofit"/>'
             '<w:tblCellMar><w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar>'
             '</w:tblPr><w:tblGrid>%s</w:tblGrid>' % (border, '<w:gridCol w:w="%d"/>' % colw * ncol)]

        def row(cs, head):
            out = ['<w:tr>%s' % ('<w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>' if head else
                                 '<w:trPr><w:cantSplit/></w:trPr>')]
            cs = (cs + [''] * ncol)[:ncol]
            for c in cs:
                shade = '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>' if head else ''
                out.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s</w:tcPr>'
                           '<w:p><w:pPr><w:pStyle w:val="TableText"/></w:pPr>%s</w:p></w:tc>'
                           % (colw, shade, runs(c, base_bold=head)))
            out.append('</w:tr>')
            return ''.join(out)
        x.append(row(header, True))
        for r in body:
            x.append(row(r, False))
        x.append('</w:tbl>')
        self.body.append(''.join(x))
        self.body.append('<w:p><w:pPr><w:spacing w:after="0"/></w:pPr></w:p>')

    # -------------------------------------------------------------- parser
    def build(self):
        with open(self.md_path, encoding='utf8') as f:
            lines = f.read().split('\n')
        i, n = 0, len(lines)
        pending_caption = False
        while i < n:
            line = lines[i]
            s = line.strip()
            if not s:
                i += 1
                continue
            m = re.match(r'^(#{1,6})\s+(.*)$', s)
            if m:
                level, text = len(m.group(1)), m.group(2).strip()
                if level == 1 and not self.title_done:
                    self.body.append(para(text, style='Title'))
                    self.title_done = True
                else:
                    self.body.append(para(text, style='Heading%d' % min(level, 4)))
                i += 1
                continue
            if re.fullmatch(r'(-{3,}|\*{3,}|_{3,})', s):
                i += 1
                continue
            m = re.fullmatch(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)', s)
            if m:
                self.image(m.group(1), m.group(2))
                pending_caption = True
                i += 1
                continue
            if s.startswith('|'):
                rows = []
                while i < n and lines[i].strip().startswith('|'):
                    rows.append(lines[i])
                    i += 1
                self.table(rows)
                continue
            if re.match(r'^([-*+])\s+', s):
                while i < n and re.match(r'^\s*([-*+])\s+', lines[i]):
                    item = re.sub(r'^\s*[-*+]\s+', '', lines[i]).strip()
                    i += 1
                    while i < n and lines[i].strip() and lines[i].startswith('  ') and \
                            not re.match(r'^\s*([-*+]|\d+\.)\s+', lines[i]):
                        item += ' ' + lines[i].strip()
                        i += 1
                    self.body.append(para(item, style='ListParagraph', numpr=1))
                continue
            if re.match(r'^\d+\.\s+', s):
                self.num_lists += 1
                num_id = 100 + self.num_lists
                while i < n and re.match(r'^\s*\d+\.\s+', lines[i]):
                    item = re.sub(r'^\s*\d+\.\s+', '', lines[i]).strip()
                    i += 1
                    while i < n and lines[i].strip() and lines[i].startswith('  ') and \
                            not re.match(r'^\s*([-*+]|\d+\.)\s+', lines[i]):
                        item += ' ' + lines[i].strip()
                        i += 1
                    self.body.append(para(item, style='ListParagraph', numpr=num_id))
                    # allow blank lines between items of the same list
                    j = i
                    while j < n and not lines[j].strip():
                        j += 1
                    if j < n and j > i and re.match(r'^\d+\.\s+', lines[j].strip()) and \
                            not re.match(r'^1\.\s+', lines[j].strip()):
                        i = j
                continue
            # ordinary paragraph: gather until blank / block start
            buf = [s]
            i += 1
            while i < n:
                t = lines[i].strip()
                if not t or t.startswith(('#', '|', '![')) or re.match(r'^([-*+]|\d+\.)\s+', t) \
                        or re.fullmatch(r'-{3,}', t):
                    break
                buf.append(t)
                i += 1
            text = ' '.join(buf)
            if re.match(r'^\*\*(Figure|Fig\.)\s*\d+[\w.]*\.\*\*', text) and pending_caption:
                self.body.append(para(text, style='Caption'))
            elif re.match(r'^\*\*Table\s+[\dA-Z][\w.]*\.\*\*', text):
                self.body.append(para(text, style='TableCaption', keep_next=True))
            elif len(buf) == 1 and len(text) < 240 and \
                    re.search(r'\S\s{2,}\(\d+(\.\d+)?[a-z]?\)\s*$', buf[0]):
                self.body.append(para(text, style='Equation', jc='center'))
            else:
                self.body.append(para(text))
            pending_caption = False
        return self

    # -------------------------------------------------------------- package
    def save(self, out_path):
        num_instances = ''.join(
            '<w:num w:numId="%d"><w:abstractNumId w:val="1"/><w:lvlOverride w:ilvl="0">'
            '<w:startOverride w:val="1"/></w:lvlOverride></w:num>' % (100 + k)
            for k in range(1, self.num_lists + 1))
        numbering = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:numbering %s>'
            '<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="singleLevel"/>'
            '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="\u2022"/>'
            '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>'
            '</w:lvl></w:abstractNum>'
            '<w:abstractNum w:abstractNumId="1"><w:multiLevelType w:val="singleLevel"/>'
            '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%%1."/>'
            '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum>'
            '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>%s</w:numbering>' % (W_NS, num_instances))
        def st(sid, name, ppr='', rpr='', based='Normal', typ='paragraph', nxt=None):
            return ('<w:style w:type="%s" w:styleId="%s"><w:name w:val="%s"/>%s%s<w:qFormat/>'
                    '<w:pPr>%s</w:pPr><w:rPr>%s</w:rPr></w:style>' % (
                        typ, sid, name, '<w:basedOn w:val="%s"/>' % based if based else '',
                        '<w:next w:val="%s"/>' % nxt if nxt else '', ppr, rpr))
        styles = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles %s>'
            '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="%s" w:hAnsi="%s" w:eastAsia="%s" w:cs="%s"/>'
            '<w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="en-GB"/></w:rPr></w:rPrDefault>'
            '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="312" w:lineRule="auto"/></w:pPr>'
            '</w:pPrDefault></w:docDefaults>' % ((W_NS,) + (FONT,) * 4)
            + '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/>'
              '<w:pPr><w:jc w:val="both"/></w:pPr></w:style>'
            + st('Title', 'Title', '<w:keepNext/><w:spacing w:before="240" w:after="360"/><w:jc w:val="center"/>',
                 '<w:b/><w:bCs/><w:color w:val="1F3864"/><w:sz w:val="36"/><w:szCs w:val="36"/>', nxt='Normal')
            + st('Heading1', 'heading 1', '<w:keepNext/><w:keepLines/><w:spacing w:before="360" w:after="120"/>'
                 '<w:jc w:val="left"/><w:outlineLvl w:val="0"/>',
                 '<w:b/><w:bCs/><w:color w:val="1F3864"/><w:sz w:val="30"/><w:szCs w:val="30"/>', nxt='Normal')
            + st('Heading2', 'heading 2', '<w:keepNext/><w:keepLines/><w:spacing w:before="300" w:after="100"/>'
                 '<w:jc w:val="left"/><w:outlineLvl w:val="1"/>',
                 '<w:b/><w:bCs/><w:color w:val="2F5496"/><w:sz w:val="27"/><w:szCs w:val="27"/>', nxt='Normal')
            + st('Heading3', 'heading 3', '<w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="80"/>'
                 '<w:jc w:val="left"/><w:outlineLvl w:val="2"/>',
                 '<w:b/><w:bCs/><w:color w:val="2F5496"/><w:sz w:val="25"/><w:szCs w:val="25"/>', nxt='Normal')
            + st('Heading4', 'heading 4', '<w:keepNext/><w:keepLines/><w:spacing w:before="200" w:after="60"/>'
                 '<w:jc w:val="left"/><w:outlineLvl w:val="3"/>',
                 '<w:b/><w:bCs/><w:i/><w:iCs/><w:color w:val="2F5496"/>', nxt='Normal')
            + st('ListParagraph', 'List Paragraph', '<w:spacing w:after="60"/><w:ind w:left="720"/>'
                 '<w:contextualSpacing/>')
            + st('Figure', 'Figure', '<w:keepNext/><w:spacing w:before="200" w:after="60"/><w:jc w:val="center"/>')
            + st('Caption', 'caption', '<w:spacing w:after="240"/><w:jc w:val="both"/>',
                 '<w:color w:val="262626"/><w:sz w:val="21"/><w:szCs w:val="21"/>')
            + st('TableCaption', 'Table Caption', '<w:keepNext/><w:spacing w:before="200" w:after="80"/>'
                 '<w:jc w:val="left"/>', '<w:sz w:val="21"/><w:szCs w:val="21"/>')
            + st('TableText', 'Table Text', '<w:spacing w:before="20" w:after="20" w:line="240" '
                 'w:lineRule="auto"/><w:jc w:val="left"/>', '<w:sz w:val="19"/><w:szCs w:val="19"/>')
            + st('Equation', 'Equation', '<w:spacing w:before="120" w:after="120"/><w:jc w:val="center"/>')
            + '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/>'
              '<w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
              '</w:tblBorders></w:tblPr></w:style>'
            + '</w:styles>')

        document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document %s><w:body>%s'
                    '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
                    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" '
                    'w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>'
                    % (W_NS, ''.join(self.body)))
        content_types = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Default Extension="png" ContentType="image/png"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-'
            'officedocument.wordprocessingml.document.main+xml"/>'
            '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-'
            'officedocument.wordprocessingml.styles+xml"/>'
            '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-'
            'officedocument.wordprocessingml.numbering+xml"/>'
            '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-'
            'package.core-properties+xml"/>'
            '</Types>')
        root_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
            'relationships/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/'
            'metadata/core-properties" Target="docProps/core.xml"/>'
            '</Relationships>')
        rels = [('rIdStyles', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles',
                 'styles.xml'),
                ('rIdNum', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering',
                 'numbering.xml')] + self.rels
        doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">%s'
                    '</Relationships>' % ''.join('<Relationship Id="%s" Type="%s" Target="%s"/>' % r
                                                 for r in rels))
        title = ''
        for b in self.body:
            if 'w:val="Title"' in b:
                title = re.sub(r'<[^>]+>', '', b)
                break
        core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/'
                'core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">'
                '<dc:title>%s</dc:title></cp:coreProperties>' % escape(title))
        with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
            z.writestr('[Content_Types].xml', content_types)
            z.writestr('_rels/.rels', root_rels)
            z.writestr('docProps/core.xml', core)
            z.writestr('word/document.xml', document)
            z.writestr('word/styles.xml', styles)
            z.writestr('word/numbering.xml', numbering)
            z.writestr('word/_rels/document.xml.rels', doc_rels)
            for name, path in self.media:
                z.write(path, 'word/media/' + name)
        return out_path


def build(src, out):
    d = Doc(src).build()
    d.save(out)
    print('  %-55s %3d figures, %4d blocks%s' % (os.path.relpath(out, ROOT), len(d.media), len(d.body),
                                                 ('  MISSING: %s' % d.missing) if d.missing else ''))
    return d


if __name__ == '__main__':
    if len(sys.argv) == 3:
        build(sys.argv[1], sys.argv[2])
    else:
        for src, out in DOCS:
            build(os.path.join(ROOT, src), os.path.join(ROOT, out))
