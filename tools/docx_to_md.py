#!/usr/bin/env python3
"""
One-off extractor: convert a simple raw-OOXML .docx (as produced by the
legacy build scripts in this repo) into an editable Markdown source.

Handles: headings (Title/Heading1-3 styles), bold/italic runs, sub/superscript
(kept as Unicode where already Unicode), tables (-> pipe tables), and drops
images / empty paragraphs.

Usage:  python3 tools/docx_to_md.py input.docx output.md
"""
import re
import sys
import zipfile
import html


def run_text(r):
    t = ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', r, re.S))
    t = html.unescape(t)
    if not t.strip():
        return t
    bold = re.search(r'<w:b/>|<w:b w:val="(1|true)"/>', r) is not None
    ital = re.search(r'<w:i/>|<w:i w:val="(1|true)"/>', r) is not None
    va = re.search(r'<w:vertAlign w:val="(superscript|subscript)"/>', r)
    if va:
        t = ('<sup>%s</sup>' if va.group(1) == 'superscript' else '<sub>%s</sub>') % t
    lead = len(t) - len(t.lstrip())
    trail = len(t) - len(t.rstrip())
    core = t.strip()
    if bold and ital:
        core = '***%s***' % core
    elif bold:
        core = '**%s**' % core
    elif ital:
        core = '*%s*' % core
    return t[:lead] + core + (t[len(t) - trail:] if trail else '')


def para_text(p):
    runs = re.findall(r'<w:r[ >].*?</w:r>', p, re.S)
    s = ''.join(run_text(r) for r in runs)
    s = s.replace('****', '').replace('** **', ' ')
    return s.strip()


def para_style(p):
    m = re.search(r'<w:pStyle w:val="([^"]+)"', p)
    return m.group(1) if m else ''


def convert(xml):
    body = re.search(r'<w:body>(.*)</w:body>', xml, re.S).group(1)
    out = []
    pos = 0
    for m in re.finditer(r'<w:tbl>.*?</w:tbl>|<w:p[ >].*?</w:p>|<w:p/>', body, re.S):
        blk = m.group(0)
        if blk.startswith('<w:tbl>'):
            rows = re.findall(r'<w:tr[ >].*?</w:tr>', blk, re.S)
            md_rows = []
            for row in rows:
                cells = re.findall(r'<w:tc>.*?</w:tc>', row, re.S)
                vals = []
                for c in cells:
                    ps = re.findall(r'<w:p[ >].*?</w:p>', c, re.S)
                    v = ' '.join(para_text(p) for p in ps).replace('|', '/')
                    v = re.sub(r'^\*\*(.*)\*\*$', r'\1', v)
                    vals.append(v)
                md_rows.append('| ' + ' | '.join(vals) + ' |')
            if md_rows:
                ncol = md_rows[0].count('|') - 1
                md_rows.insert(1, '|' + '---|' * ncol)
                out.append('\n'.join(md_rows))
            continue
        if '<w:drawing' in blk or '<w:pict' in blk:
            continue
        t = para_text(blk)
        if not t:
            continue
        st = para_style(blk)
        plain = re.sub(r'\*+', '', t)
        if st == 'Title':
            out.append('# ' + plain)
        elif st == 'Heading1':
            out.append('# ' + plain)
        elif st == 'Heading2':
            out.append('## ' + plain)
        elif st == 'Heading3':
            out.append('### ' + plain)
        else:
            out.append(t)
    return '\n\n'.join(out) + '\n'


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    with zipfile.ZipFile(src) as z:
        xml = z.read('word/document.xml').decode('utf8')
    with open(dst, 'w', encoding='utf8') as f:
        f.write(convert(xml))
    print('wrote', dst)
