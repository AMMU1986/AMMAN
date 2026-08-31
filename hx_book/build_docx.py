#!/usr/bin/env python3
"""
Build the full book Word (.docx) document from the chapter markdown files,
embedding the PNG figures as inline images. Pure stdlib (zipfile, struct, re).

Marker syntax understood in the markdown:
  # Title line                       -> Title style
  ## Section heading                 -> Heading1
  ## X.Y Subsection                  -> Heading2 (detected by leading number)
  **Table X.Y** caption              -> Table caption, followed by a md table
  | a | b |  /  |---|---|             -> table rows
  [[FIG:file.png|Figure X.Y caption]] -> embedded image + caption
  [n] inline                          -> left as text (already serial)
  ## References  + [n] entries        -> References style
"""
import zipfile
import os
import re
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(HERE, 'figures')

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

NUMBERING = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults><w:rPrDefault><w:rPr>
    <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
    <w:sz w:val="24"/><w:szCs w:val="24"/>
  </w:rPr></w:rPrDefault>
  <w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1"><w:name w:val="Normal"/><w:pPr><w:jc w:val="both"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="240" w:after="240"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="140"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="260" w:after="120"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Abstract"><w:name w:val="Abstract"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="720" w:right="720"/></w:pPr><w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="References"><w:name w:val="References"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption"><w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="240"/><w:keepLines/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="FigureImage"><w:name w:val="Figure Image"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="200" w:after="40"/><w:keepNext/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption"><w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="80"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
</w:styles>'''


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;'))


def png_size(path):
    with open(path, 'rb') as f:
        f.read(16)
        w, h = struct.unpack('>II', f.read(8))
    return w, h


def run(text, bold=False, italic=False):
    props = ''
    if bold or italic:
        props = '<w:rPr>' + ('<w:b/>' if bold else '') + ('<w:i/>' if italic else '') + '</w:rPr>'
    return f'<w:r>{props}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'


def inline(text):
    out = []
    for part in re.split(r'(\*\*.*?\*\*|\*[^*]+?\*)', text):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            out.append(run(part[2:-2], bold=True))
        elif part.startswith('*') and part.endswith('*'):
            out.append(run(part[1:-1], italic=True))
        else:
            out.append(run(part))
    return ''.join(out)


def para(text, style='Normal'):
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{inline(text)}</w:p>'


def table(headers, rows):
    n = len(headers)
    colw = 9360 // n
    x = '<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
    x += '<w:tblBorders>'
    for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        x += f'<w:{e} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    x += '</w:tblBorders></w:tblPr>'
    x += '<w:tblGrid>' + f'<w:gridCol w:w="{colw}"/>' * n + '</w:tblGrid>'
    x += '<w:tr>'
    for h in headers:
        x += ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>'
              '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>'
              '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="20"/></w:pPr>%s</w:p></w:tc>'
              % (colw, run(h.strip(), bold=True)))
    x += '</w:tr>'
    for r in rows:
        x += '<w:tr>'
        for i in range(n):
            cell = r[i].strip() if i < len(r) else ''
            x += ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/></w:tcPr>'
                  '<w:p><w:pPr><w:spacing w:after="20"/><w:jc w:val="left"/></w:pPr>%s</w:p></w:tc>'
                  % (colw, run(cell)))
        x += '</w:tr>'
    x += '</w:tbl><w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>'
    return x


def image_para(rid, w, h, cx_max=5486400):
    # cx_max ~ 6.0 inch in EMU (914400 EMU per inch). Scale to fit width.
    emu_w = w * 9525
    emu_h = h * 9525
    if emu_w > cx_max:
        s = cx_max / emu_w
        emu_w = int(emu_w * s)
        emu_h = int(emu_h * s)
    return f'''<w:p><w:pPr><w:pStyle w:val="FigureImage"/></w:pPr><w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
<wp:extent cx="{emu_w}" cy="{emu_h}"/>
<wp:docPr id="{rid}" name="Picture{rid}"/>
<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:nvPicPr><pic:cNvPr id="{rid}" name="Picture{rid}"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed="rId{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>
<a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{emu_w}" cy="{emu_h}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''


def parse_markdown(md, state):
    """Return list of body-XML chunks; state carries image rels + rid counter."""
    out = []
    lines = md.split('\n')
    i = 0
    in_refs = False
    in_abstract = False
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        # leaving abstract when a new heading appears
        if in_abstract and s.startswith('## ') and s != '## Abstract':
            in_abstract = False
        # figure embed
        m = re.match(r'\[\[FIG:([^|]+)\|(.+)\]\]$', s)
        if m:
            fn = m.group(1).strip()
            cap = m.group(2).strip()
            path = os.path.join(FIG_DIR, fn)
            rid = state['rid']
            state['rid'] += 1
            state['images'].append((rid, fn, path))
            w, h = png_size(path)
            out.append(image_para(rid, w, h))
            out.append(para(cap, 'FigureCaption'))
            i += 1
            continue
        # title (single #)
        if s.startswith('# ') and not s.startswith('## '):
            out.append(para(s[2:].strip(), 'Title'))
            i += 1
            continue
        # heading level 2 (##)
        if s.startswith('## '):
            htext = s[3:].strip()
            if htext.lower() == 'references':
                in_refs = True
                out.append(para(htext, 'Heading1'))
                i += 1
                continue
            # subsection if starts with number like 1.1
            if re.match(r'^\d+\.\d+', htext):
                out.append(para(htext, 'Heading2'))
            else:
                out.append(para(htext, 'Heading1'))
            i += 1
            continue
        # table caption
        if s.startswith('**Table '):
            out.append(para(s, 'TableCaption'))
            i += 1
            continue
        # markdown table
        if '|' in line and i + 1 < len(lines) and re.search(r'\|?\s*-{2,}', lines[i + 1]):
            headers = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            out.append(table(headers, rows))
            continue
        # abstract heading
        if s == '## Abstract':
            out.append(para('Abstract', 'Heading1'))
            in_abstract = True
            i += 1
            continue
        # reference entry
        if in_refs and re.match(r'^\[\d+\]', s):
            out.append(para(s, 'References'))
            i += 1
            continue
        # abstract body paragraph uses Abstract style
        style = 'Abstract' if in_abstract else 'Normal'
        out.append(para(s, style))
        i += 1
    return out


def build(chapter_files, ref_file, out_path, page_break_between=True):
    state = {'rid': 1000, 'images': []}
    body = []
    # Cover
    body.append(para('Artificial Intelligence and Machine Learning for the '
                     'Design of Nanofluid Heat Exchangers', 'Title'))
    body.append(para('An Integrated Treatment of Heat Transfer, Nanofluids, '
                     'Computational Fluid Dynamics and Data-Driven Modelling', 'Heading2'))
    body.append('<w:p/>')
    for idx, cf in enumerate(chapter_files):
        md = open(cf, encoding='utf-8').read()
        # mark abstract body as Abstract style: post-process
        body.extend(parse_markdown(md, state))
        if page_break_between:
            body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
    # references
    md = open(ref_file, encoding='utf-8').read()
    body.extend(parse_markdown(md, state))

    body_xml = '\n'.join(body)
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<w:body>
{body_xml}
<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>
<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
</w:sectPr>
</w:body></w:document>'''

    # doc rels: styles, numbering, + each image
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '<Relationship Id="rIdNum" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>']
    for rid, fn, path in state['images']:
        rels.append(f'<Relationship Id="rId{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{fn}"/>')
    rels.append('</Relationships>')
    word_rels = '\n'.join(rels)

    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CONTENT_TYPES)
        z.writestr('_rels/.rels', RELS)
        z.writestr('word/_rels/document.xml.rels', word_rels)
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', STYLES)
        z.writestr('word/numbering.xml', NUMBERING)
        seen = set()
        for rid, fn, path in state['images']:
            if fn in seen:
                continue
            seen.add(fn)
            z.write(path, f'word/media/{fn}')
    kb = os.path.getsize(out_path) / 1024
    print(f"Wrote {out_path} ({kb:.0f} KB), {len(state['images'])} images embedded")


if __name__ == '__main__':
    chapters = [os.path.join(HERE, f'ch{i}.md') for i in range(1, 10)]
    refs = os.path.join(HERE, 'references.md')
    out = os.path.join(os.path.dirname(HERE),
                       'AI_ML_Nanofluid_Heat_Exchangers_Book.docx')
    build(chapters, refs, out)
